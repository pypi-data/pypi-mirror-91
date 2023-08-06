# Copyright 2020 Cognite AS
"""Cognite Geospatial API store and query spatial data.

 Spatial objects represent a revision of an object present in a geographic position at a point
 in time (or for all time if no time is specified). The object has a position according to a
 specific coordinate reference system and can be a point, linestring, polygon, or surface
 defined by a position in 3-dimensional space. Within the defined area, the object can have
 attributes or values associated with more specific points or areas.

"""
import asyncio
import base64
import concurrent
import json
import os
import sys
import tempfile
import threading
from functools import lru_cache, partial
from json.decoder import JSONDecodeError
from typing import Any, Callable, Dict, List, Optional, Union

import numpy as np
import pyarrow as pa
from cognite import geospatial as geospatial
from cognite.geospatial._client import (
    AttributeTypeDTO,
    Configuration,
    CoreGeometrySpatialItemDTO,
    CreateSpatialItemsDTO,
    DataExtractorDTO,
    EitherIdDTO,
    ExternalIdDTO,
    FeatureLayersFilterDTO,
    GeometryDTO,
    GeometryItemsDTO,
    GridCoverageRequestDTO,
    InternalIdDTO,
    IntersectionQueryDTO,
    ItemAttributeDTO,
    ItemAttributesDTO,
    SpatialApi,
    SpatialCoverageRequestDTO,
    SpatialDataRequestDTO,
    SpatialIdsDTO,
    SpatialItemCoverageDTO,
    SpatialRelationshipDTO,
    SpatialSearchRequestDTO,
    TextBasedGeometryDTO,
    UpdateSpatialItemDTO,
    UpdateSpatialItemsDTO,
    UpdateSpatialItemWithIdDTO,
)
from cognite.geospatial._client.rest import ApiException
from cognite.geospatial._layer import Layer
from cognite.geospatial._retry_client import RetryApiClient
from cognite.geospatial._spatial_filter_object import SpatialFilterObject
from cognite.geospatial._spatial_item import SpatialItem, SpatialList, UpdateSpatialItem
from cognite.geospatial.types import DataExtractor, Geometry, GridCoverage, SpatialRelationship, TextBasedGeometry
from pyarrow import parquet as pq
from shapely import wkt
from shapely.geometry import shape
from shapely.geometry.base import BaseGeometry
from tornado import ioloop
from tornado.concurrent import Future, future_set_exc_info, is_future

from ._console import in_interactive_session

TORNADO_TIMEOUT_ERROR = 599
TORNADO_MESSAGE = "Could not get a response from the server. The server is down or timeout happens."


class GeospatialError(Exception):
    """Geospatial reised for internal errors.
    Attributes:
        message: explanation of the error
    """

    def __init__(self, message):
        super().__init__(message)


def _check_id(id: int):
    if id is not None and id > 9007199254740991:
        raise ValueError("Invalid value for `id`, must be a value less than or equal to `9007199254740991`")
    if id is not None and id < 1:
        raise ValueError("Invalid value for `id`, must be a value greater than or equal to `1`")


def _check_external_id(external_id: str):
    if external_id is None:
        raise ValueError("Invalid value for `external_id`, must not be `None`")
    if external_id is not None and len(external_id) > 255:
        raise ValueError("Invalid value for `external_id`, length must be less than or equal to `255`")


def _throw_exception(ex: ApiException):
    # check for tornado timout exception code
    if ex.status == TORNADO_TIMEOUT_ERROR:
        raise GeospatialError(message=TORNADO_MESSAGE)

    if ex.body:
        try:
            error_json = json.loads(ex.body)
        except JSONDecodeError:
            # not a json
            raise ex
        if "error" in error_json:
            error = error_json["error"]
            raise GeospatialError(message=error["message"])
    raise ex


def _check_either_external_id(id: int = None, external_id: str = None):
    if id is None and external_id is None:
        raise ValueError("Either id or external_id must be provided")


def _first_item(response):
    if response is None or response.items is None or len(response.items) == 0:
        return None
    return response.items[0]


def _create_spatial_ids(id: int = None, external_id: str = None) -> SpatialIdsDTO:
    _check_either_external_id(id, external_id)
    if id is not None:
        item = InternalIdDTO(id=id)
    else:
        item = ExternalIdDTO(external_id=external_id)
    return SpatialIdsDTO(items=[item])


def _create_spatial_id(id: int = None, external_id: str = None):
    _check_either_external_id(id, external_id)
    if id is not None:
        return InternalIdDTO(id=id)
    else:
        return ExternalIdDTO(external_id=external_id)
    raise GeospatialError(message="Id or external id is not provided")


def _is_primitive(obj: object):
    return isinstance(obj, str) or isinstance(obj, int) or isinstance(obj, float)


def _write_parquet(file, field_name: str, values, data_type):
    schema = pa.schema([pa.field(field_name, pa.list_(data_type))])
    records = list()
    records.append({field_name: values})
    columns = list()

    for column in schema.names:
        filed_type = schema.types[schema.get_field_index(column)]
        field_data = pa.array([v[column] for v in records], type=filed_type)
        columns.append(field_data)

    table = pa.Table.from_arrays(columns, schema=schema)
    with pq.ParquetWriter(file, schema, compression="zstd", use_byte_stream_split=True) as writer:
        writer.write_table(table)


def _decode_attribute(value, type: AttributeTypeDTO):
    if isinstance(value, str) and type in [AttributeTypeDTO.DOUBLE, AttributeTypeDTO.INT, AttributeTypeDTO.BOOLEAN]:
        byte_buffer = base64.urlsafe_b64decode(value)
        if type == AttributeTypeDTO.DOUBLE:
            return np.frombuffer(byte_buffer, dtype=">d")
        elif type == AttributeTypeDTO.INT:
            return np.frombuffer(byte_buffer, dtype=">i")
        elif type == AttributeTypeDTO.BOOLEAN:
            vector = np.frombuffer(byte_buffer, dtype=np.uint8)
            bit_array = np.unpackbits(vector, bitorder="little")
            bool_data = np.array(bit_array, dtype=bool)
            if len(bool_data) == 0:
                return bool_data
            true_index = np.argwhere(bool_data == True).flatten()  # noqa: E712
            if len(true_index) == 0:
                return bool_data
            return bool_data[: true_index[-1]]

    return value


def api_exception_handler(func):
    if asyncio.iscoroutinefunction(func):

        async def inner_function(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except ApiException as e:
                _throw_exception(e)

        return inner_function
    else:

        def inner_function(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except ApiException as e:
                _throw_exception(e)

        return inner_function


def _is_simple(value) -> bool:
    if isinstance(value, dict):
        return True
    return not isinstance(value, list) and not isinstance(value, np.ndarray) and not isinstance(value, np.generic)


def _filter_simple_attributes(attributes: Optional[dict]) -> dict:
    if attributes is None:
        return {}
    return {k: v for k, v in attributes.items() if _is_simple(v)}


def _filter_list_attributes(attributes: Optional[dict]) -> dict:
    if attributes is None:
        return {}
    return {k: v for k, v in attributes.items() if not _is_simple(v)}


def _to_update_spatial_item(item: SpatialItem) -> UpdateSpatialItemDTO:
    update = UpdateSpatialItemDTO(
        name=item.name,
        description=item.description,
        metadata=item.metadata,
        asset_ids=item.asset_ids,
        attributes=_filter_simple_attributes(item.attributes),
        source=item.source,
    )
    return UpdateSpatialItemWithIdDTO(item_id={"id": item.id, "external_id": item.external_id}, update=update)


class CogniteGeospatialClient:
    """
    Main class for the seismic client
    """

    def __init__(
        self,
        api_key: str = None,
        base_url: str = None,
        port: int = None,
        api_token: str = None,
        project: str = None,
        timeout: int = 600,  # seconds
    ):
        # configure env
        api_key = api_key or os.getenv("COGNITE_API_KEY")
        if (api_key is None or not api_key.strip()) and api_token is None:
            raise ValueError(
                "You have either not passed an api key or not set the COGNITE_API_KEY environment variable."
            )
        self.configuration = Configuration()
        self.configuration.client_side_validation = False
        if api_token is None and api_key is not None:
            self.configuration.api_key["api-key"] = api_key.strip()
        self.configuration.access_token = api_token

        base_url = base_url or "api.cognitedata.com"
        base_url = base_url.strip("/")
        port = port or 443

        if not base_url.startswith("http://") and not base_url.startswith("https://"):
            if port == 443:
                base_url = "https://" + base_url
            else:
                base_url = "http://" + base_url

        self.configuration.host = base_url + ":" + str(port)

        self.project = project or os.getenv("COGNITE_PROJECT")
        if self.project is None:
            raise ValueError("Project must be provided")

        api_client = RetryApiClient(self.configuration)
        api_client.user_agent = "Cognite-Geospatial-SDK_" + geospatial.__version__ + "/python"
        self.api = SpatialApi(api_client)
        self.timeout = timeout
        self.ingestion_timeout = 21600

        self._interactive_session = in_interactive_session()

        if self._interactive_session:
            self._make_new_loop()

    def _make_new_loop(self):
        alt_ioloop_fut = concurrent.futures.Future()

        def run_alt_loop():
            asyncio.set_event_loop(asyncio.SelectorEventLoop())
            loop = ioloop.IOLoop()
            alt_ioloop_fut.set_result(loop)
            loop.start()

        alt_thread = threading.Thread(target=run_alt_loop)
        alt_thread.daemon = True
        alt_thread.start()
        self.loop = alt_ioloop_fut.result()

    def _run_sync(self, func: Callable, timeout: Optional[float] = None) -> Any:
        if not self._interactive_session:
            return ioloop.IOLoop.current().run_sync(func, timeout)

        loop = self.loop
        future_cell = [None]
        await_future = concurrent.futures.Future()

        async def run():
            try:
                result = await func()
                # if result is not None:
                #     from tornado.gen import convert_yielded

                #     result = convert_yielded(result)
                await_future.set_result(result)
            except Exception as e:
                fut = Future()  # type: Future[Any]
                future_cell[0] = fut
                future_set_exc_info(fut, sys.exc_info())
                await_future.set_exception(e)
            else:
                if is_future(result):
                    future_cell[0] = result
                else:
                    fut = Future()
                    future_cell[0] = fut
                    fut.set_result(result)
            assert future_cell[0] is not None
            loop.add_future(future_cell[0], lambda future: await_future.cancel())

        self.loop.add_callback(run)
        if timeout is not None:

            def timeout_callback() -> None:
                # If we can cancel the future, do so and wait on it. If not,
                # Just stop the loop and return with the task still pending.
                # (If we neither cancel nor wait for the task, a warning
                # will be logged).
                assert future_cell[0] is not None
                future_cell[0].cancel()

            timeout_handle = self.loop.add_timeout(self.loop.time() + timeout, timeout_callback)

        await_future.result()

        if timeout is not None:
            self.loop.remove_timeout(timeout_handle)
        assert future_cell[0] is not None
        if future_cell[0].cancelled() or not future_cell[0].done():
            raise TimeoutError("Operation timed out after %s seconds" % timeout)
        return future_cell[0].result()

    def _to_spatial_item(self, response) -> SpatialItem:
        spatial_item = SpatialItem(
            layer=response.layer,
            crs=response.crs,
            id=response.id,
            external_id=response.external_id,
            name=response.name,
            description=response.description,
            metadata=response.metadata,
            asset_ids=response.asset_ids,
            source=response.source,
            attributes=response.attributes,
            created_time=response.created_time,
            last_updated_time=response.last_updated_time,
        )
        spatial_item.client = self
        return spatial_item

    def _to_spatial_items(self, response, single: bool, layer_name: str = None) -> Union[SpatialItem, SpatialList]:
        if response is None or response.items is None:
            raise GeospatialError("No items in response")

        if single:
            if len(response.items) == 0:
                return None
            return self._to_spatial_item(response.items[0])

        spatial_list = SpatialList(client=self, layer_name=layer_name)
        if len(response.items) == 0:
            return spatial_list

        spatial_list.extend(list(map(lambda x: self._to_spatial_item(x), response.items)))
        return spatial_list

    @api_exception_handler
    async def parquet_file_save_async(self, file, id: int = -1, external_id: str = ""):
        return await self.api.file_save(
            self.project,
            file_type="parquet",
            file=file,
            id=id,
            external_id=external_id,
            _request_timeout=self.ingestion_timeout,
        )

    async def add_spatial_item_data_async(self, id: int, name: str, value, attribute_type: str):
        value_buff = None
        if not _is_primitive(value):
            if attribute_type == "int":
                value_buff = value.astype(">i4").tobytes()
            elif attribute_type == "long":
                value_buff = value.astype(">i8").tobytes()
            elif attribute_type == "float":
                value_buff = value.astype(">f4").tobytes()
            elif attribute_type == "double":
                value_buff = value.astype(">f8").tobytes()
            elif attribute_type == "string":
                value_buff = bytearray(value, encoding="utf-8")
            elif attribute_type == "boolean":
                end_value = np.append(value.astype(np.uint8), 1)
                pack_int = np.packbits(end_value, bitorder="little")  # uint8
                value_buff = pack_int.tobytes()

        if value_buff is not None:
            value_data = str(base64.urlsafe_b64encode(value_buff), "utf-8")
        else:
            value_data = value
        spatial_data = ItemAttributesDTO(
            items=[
                ItemAttributeDTO(
                    item_id=EitherIdDTO(id=id, local_vars_configuration=self.configuration), name=name, value=value_data
                )
            ]
        )

        response = await api_exception_handler(self.api.add_spatial_item_attributes)(
            self.project, spatial_data, _request_timeout=self.timeout
        )
        if response is not None:
            return response.items
        return None

    async def store_spatial_item_data_async(self, id: int, name: str, value, attribute_type: str):
        if (
            type(value) is dict
            or np.isscalar(value)
            or value.size <= 100
            or attribute_type == "string"
            or attribute_type == "boolean"
        ):
            await self.add_spatial_item_data_async(id, name, value, attribute_type)
        else:
            pa_type = None
            if attribute_type == "int":
                pa_type = pa.int32()
            elif attribute_type == "long":
                pa_type = pa.int64()
            elif attribute_type == "float":
                pa_type = pa.float32()
            elif attribute_type == "double":
                pa_type = pa.float64()
            with tempfile.NamedTemporaryFile() as fp:
                _write_parquet(fp.name, name, value, pa_type)
                await self.parquet_file_save_async(file=fp.name, id=id)

    @api_exception_handler
    async def get_spatial_info_async(self, id: int = None, external_id: str = None) -> Optional[SpatialItem]:
        """Retrieves spatial item information by internal ids or external ids.
        """
        spatial_by_ids = _create_spatial_ids(id, external_id)
        response = await self.api.by_ids_spatial_items(self.project, spatial_by_ids, _request_timeout=self.timeout)
        return self._to_spatial_items(response, True)

    def _to_core_geometry_spatial_item(self, item: SpatialItem) -> CoreGeometrySpatialItemDTO:
        if item.id is not None:
            raise GeospatialError("Spatial item id must benot defined")
        spatial_item = CoreGeometrySpatialItemDTO(
            name=item.name,
            external_id=item.external_id,
            description=item.description,
            metadata=item.metadata,
            asset_ids=item.asset_ids,
            layer=item.layer,
            source=item.source,
            attributes=_filter_simple_attributes(item.attributes),
            crs=item.crs,
        )
        return spatial_item

    def create_spatial(self, items: Union[SpatialItem, List[SpatialItem]]) -> Union[SpatialItem, List[SpatialItem]]:
        """`Create one or more spatial items with additional attributes.`

        Args:
            item (Union[SpatialItem, List[SpatialItem]]): SpatialItem or list of spatial items.
        Returns:
            Union[SpatialItem, List[SpatialItem]]: The created spatial items(s).
        """
        run_func = partial(self.create_spatial_async, items)
        result = self._run_sync(run_func, self.ingestion_timeout)
        return result

    @api_exception_handler
    async def create_spatial_async(
        self, items: Union[SpatialItem, List[SpatialItem]]
    ) -> Union[SpatialItem, List[SpatialItem]]:
        single_item = not isinstance(items, list)
        if single_item:
            items = [items]
        if len(items) == 0:
            return []
        spatial_items = [self._to_core_geometry_spatial_item(item) for item in items]

        create_spatial_items = CreateSpatialItemsDTO(items=spatial_items)
        response = await self.api.create_spatial(self.project, create_spatial_items, _request_timeout=self.timeout)

        stored_items = self._to_spatial_items(response, False)
        layer_map = {}

        for spatial_item, create_item in zip(stored_items, items):
            attributes = _filter_list_attributes(create_item.attributes)
            if len(attributes) > 0:
                spatial_item._layer_info = await self._load_layer(spatial_item.layer, layer_map)
                for name, value in attributes.items():
                    await self._store_attribute(spatial_item, name, value)

        if single_item:
            return stored_items[0]

        return stored_items

    async def _load_layer(self, layer_name: str, layer_cache: dict):
        layer = layer_cache.get(layer_name)
        if layer is None:
            layer = await self.get_layer_async(name=layer_name)
            layer_cache[layer_name] = layer
        return layer

    async def _store_attribute(self, spatial_item: SpatialItem, attribute_name: str, value: list):
        layer = spatial_item._layer_info
        attribute = None
        for attr in layer.attributes:
            if attr.name == attribute_name:
                attribute = attr
                break
        if attribute is None:
            raise GeospatialError("Attribute not found")
        elif not attribute.is_array:
            raise GeospatialError("Only array attributes can be stored")

        await self.store_spatial_item_data_async(spatial_item.id, attribute_name, value, attribute.type)

        if attribute.type == AttributeTypeDTO.DOUBLE:
            spatial_item._add_double(attribute_name, value)
        elif attribute.type == AttributeTypeDTO.INT:
            spatial_item._add_integer(attribute_name, value)
        elif attribute.type == AttributeTypeDTO.LONG:
            spatial_item._add_long(attribute_name, value)
        elif attribute.type == AttributeTypeDTO.BOOLEAN:
            spatial_item._add_boolean(attribute_name, value)

    def create_update_spatial(
        self, items: Union[SpatialItem, List[SpatialItem]]
    ) -> Union[SpatialItem, List[SpatialItem]]:
        """`Create or update one or more spatial items with additional attributes.`

        Args:
            item (Union[SpatialItem, List[SpatialItem]]): SpatialItem or list of spatial items.
        Returns:
            Union[SpatialItem, List[SpatialItem]]: The created or updated spatial items(s).
        """
        run_func = partial(self.create_update_spatial_async, items)
        result = self._run_sync(run_func, self.ingestion_timeout)
        return result

    @api_exception_handler
    async def create_update_spatial_async(self, items: Union[SpatialItem, List[SpatialItem]]) -> Optional[SpatialItem]:
        single_item = not isinstance(items, list)
        if single_item:
            items = [items]
        if len(items) == 0:
            return []

        items_ids = [
            _create_spatial_id(item.id, item.external_id)
            for item in items
            if item.id is not None or item.external_id is not None
        ]

        response = await self.api.by_ids_spatial_items(
            self.project, SpatialIdsDTO(items=[items_ids]), _request_timeout=self.timeout
        )
        existing_items = self._to_spatial_items(response)

        existing_items_ids = set()
        existing_items_external_ids = set()
        for item in existing_items:
            existing_items_ids.add(item.id)
            if item.external_id is not None:
                existing_items_external_ids.add(item.external_id)

        items_to_create = []
        items_to_update = []
        for item in items:
            if item.id in existing_items_ids or (item.external_id in existing_items_external_ids):
                items_to_update.append(item)
            else:
                items_to_create.append(item)

        created_items = await self.create_spatial_async(items_to_create)
        updated_items = await self.update_spatial_async(items_to_update)

        # return in the same order
        created_updated_items = created_items + updated_items
        created_updated_id_map = {item.id: item for item in created_updated_items}
        created_updated_external_map = {
            item.external_id: item for item in created_updated_items if item.external_id is not None
        }

        result_items = []
        for item in items:
            if item.id in created_updated_id_map:
                result_items.append(created_updated_id_map[item.id])
            elif item.external_id in created_updated_external_map:
                result_items.append(created_updated_external_map[item.external_id])

        if single_item:
            return result_items[0]

        return result_items

    @api_exception_handler
    async def delete_spatial_async(self, id: int = None, external_id: str = None) -> Optional[SpatialItem]:
        """Delete spatial item by internal ids or external ids.
        """
        spatial_delete_ids = _create_spatial_ids(id, external_id)
        response = await self.api.delete_spatial(self.project, spatial_delete_ids, _request_timeout=self.timeout)
        return self._to_spatial_items(response, True)

    def delete_spatial(self, id: int = None, external_id: str = None) -> Optional[SpatialItem]:
        """Delete spatial item by internal ids or external ids.

        Args:
            id (int): the id of the spatial object
            external_id (str): the external_id reference of the spatial object

        Returns:
            SpatialItem: spatial object
        """
        run_func = partial(self.delete_spatial_async, id, external_id)
        item = self._run_sync(run_func, self.timeout)
        return item

    async def get_coverage_async(
        self,
        output_crs: str,
        id: int = None,
        external_id: str = None,
        dimensional_space: str = "2d",
        geometry_format: str = None,
    ):
        """Retrieves the coverage of the spatial object by internal ids or external ids.
        """
        dimensional_space = dimensional_space.lower()
        if dimensional_space not in ["2d", "3d"]:
            raise GeospatialError("dimensional_space - must be 2d or 3d only")

        item_id = EitherIdDTO(id, external_id, local_vars_configuration=self.configuration)
        spatial_coverage_request = SpatialCoverageRequestDTO(
            items=[item_id],
            dimensional_space=dimensional_space,
            output_crs=output_crs,
            local_vars_configuration=self.configuration,
        )
        response = await api_exception_handler(self.api.get_spatial_coverage)(
            self.project, spatial_coverage_request, geometry=geometry_format, _request_timeout=self.timeout
        )
        return _first_item(response)

    @api_exception_handler
    async def interpret_async(self, id: int = None, external_id: str = None):
        """Interpret attributes from spatial item by internal ids or external ids.
        """
        spatial_by_ids = _create_spatial_ids(id, external_id)
        return await self.api.interpret(self.project, spatial_by_ids, _request_timeout=self.ingestion_timeout)

    async def get_spatial_async(
        self, id: int = None, external_id: str = None, extractors: List[DataExtractor] = None
    ) -> Optional[SpatialItem]:
        """Retrieves spatial item data by internal ids or external ids.
        """
        _check_either_external_id(id, external_id)
        spatial_id = EitherIdDTO(id=id, external_id=external_id, local_vars_configuration=self.configuration)

        spatial_item = await self.get_spatial_info_async(id=id, external_id=external_id)
        if spatial_item is None:
            return None

        layer = await self.get_layer_async(name=spatial_item.layer)
        if layer is not None:
            spatial_item._set_layer_info(layer)
            attribute_types = {attribute.name: attribute for attribute in layer.attributes}
            attribute_data = await self.get_attributes_async(
                item_id=spatial_id, attributes=list(attribute_types.keys()), extractors=extractors
            )
            for name, data in attribute_data.items():
                if not attribute_types[name].is_array:
                    spatial_item._add_text(name, data)
                elif attribute_types[name].type == AttributeTypeDTO.DOUBLE:
                    spatial_item._add_double(name, data)
                elif attribute_types[name].type == AttributeTypeDTO.INT:
                    spatial_item._add_integer(name, data)
                elif attribute_types[name].type == AttributeTypeDTO.BOOLEAN:
                    spatial_item._add_boolean(name, data)

        return spatial_item

    @api_exception_handler
    async def get_attributes_async(
        self, item_id: EitherIdDTO, attributes: List[str], extractors: List[DataExtractor] = None
    ):
        spatial_item = await self.get_spatial_info_async(item_id.id, item_id.external_id)
        layer_name = spatial_item.layer
        layer = await self.get_layer_async(name=layer_name)
        if layer is None:
            raise ValueError("layer does not exist")

        extractors_dto = (
            [DataExtractorDTO(e.attribute, e.min_val, e.max_val) for e in extractors]
            if extractors is not None
            else None
        )
        data_request = SpatialDataRequestDTO(spatial_id=item_id, attributes=attributes, extractors=extractors_dto)
        response = await self.api.get_spatial_item_attributes(self.project, spatial_data_request_dto=data_request)
        layer_types = {la.name: la.type for la in layer.attributes}
        result = {}
        for attribute, value in response.items():
            val = _decode_attribute(value, layer_types[attribute])
            result[attribute] = val
        return result

    @api_exception_handler
    async def list_layers_async(self, names: List[str] = None):
        layer_filter = FeatureLayersFilterDTO(names=[] if names is None else names)
        response = await self.api.find_feature_layer(self.project, layer_filter, _request_timeout=self.timeout)
        if response is None or response.items is None:
            return None
        return [Layer(client=self, layer=layer) for layer in response.items]

    async def find_spatial_async(
        self,
        layer: str,
        spatial_relationship: SpatialRelationship = None,
        geometry: Geometry = None,
        distance: float = None,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
        geometry_format: str = None,
    ) -> List[SpatialItem]:
        """Searches and returns the spatial items based on resource type content or coordinates.
        """

        def _create_geometry(geometry: Geometry):
            wkt = None
            geojson = None
            if geometry.id is not None:
                _check_id(geometry.id)
            elif geometry.external_id is not None:
                _check_external_id(geometry.external_id)
            elif geometry.wkt is not None:
                wkt = geometry.wkt
                if geometry.crs is None:
                    raise ValueError("crs must be provided")
            elif geometry.geojson is not None:
                geojson = geometry.geojson
                if geometry.crs is None:
                    raise ValueError("crs must be provided")
            else:
                raise ValueError("geometry is not defined")

            return GeometryDTO(
                id=geometry.id,
                external_id=geometry.external_id,
                wkt=wkt,
                geojson=geojson,
                crs=geometry.crs,
                local_vars_configuration=self.configuration,
            )

        spatial_filter = None
        if spatial_relationship is not None:
            geometry = _create_geometry(geometry)
            spatial_relationship = SpatialRelationshipDTO(
                name=spatial_relationship.value, distance=distance, local_vars_configuration=self.configuration
            )
            spatial_filter = SpatialFilterObject(
                spatial_relationship, geometry, local_vars_configuration=self.configuration
            )
        spatial_search_request = SpatialSearchRequestDTO(
            name=name,
            asset_ids=asset_ids,
            metadata=metadata,
            source=source,
            external_id_prefix=external_id_prefix,
            spatial_filter=spatial_filter,
            layer=layer,
            attributes=attributes,
            output_crs=output_crs,
            limit=limit,
            offset=offset,
        )

        response = await api_exception_handler(self.api.search_spatial)(
            self.project,
            spatial_search_request_dto=spatial_search_request,
            _request_timeout=self.timeout,
            geometry=geometry_format,
        )

        return self._to_spatial_items(response, False, layer_name=layer)

    @api_exception_handler
    async def shape_file_save_async(self, file, layer: str, create_layer: bool = False, attributes: List[str] = None):
        """Shapefile save as spatial items.
        """
        params = {
            "file_type": "shp",
            "file": file,
            "layer": layer,
            "create_layer": create_layer,
            "_request_timeout": self.ingestion_timeout,
        }
        if attributes is not None:
            params["attributes"] = ",".join(attributes)
        return await self.api.file_save(self.project, **params)

    @api_exception_handler
    async def get_grid_coverage_async(
        self, geometry: TextBasedGeometry, id: int = None, external_id: str = None, distance: float = None
    ) -> GridCoverage:
        spatial_id = EitherIdDTO(id=id, external_id=external_id, local_vars_configuration=self.configuration)
        geom = TextBasedGeometryDTO(
            geojson=geometry.geojson, crs=geometry.crs, wkt=geometry.wkt, local_vars_configuration=self.configuration
        )
        grid_coverage_request = GridCoverageRequestDTO(spatial_id=spatial_id, geometry=geom, distance=distance)
        response = await self.api.grid_coverage(self.project, grid_coverage_request, _request_timeout=self.timeout)
        return GridCoverage({item.linenumber: item.list for item in response.rows})

    def update_spatial(
        self, items: Union[UpdateSpatialItem, List[UpdateSpatialItem]]
    ) -> Union[SpatialItem, List[SpatialItem]]:
        """ Update spatial object(s) with given id or external_id

        Args:
            item (Union[UpdateSpatialItem, List[UpdateSpatialItem]]): SpatialItem or list of spatial items.
        Returns:
            Union[SpatialItem, List[SpatialItem]]: The updated spatial object
        """
        run_func = partial(self.update_spatial_async, items)
        return self._run_sync(run_func, self.ingestion_timeout)

    @api_exception_handler
    async def update_spatial_async(
        self, items: Union[UpdateSpatialItem, List[UpdateSpatialItem]]
    ) -> Union[SpatialItem, List[SpatialItem]]:
        single_item = not isinstance(items, list)
        if single_item:
            items = [items]

        if len(items) == 0:
            return []

        update_items = [_to_update_spatial_item(item) for item in items]
        update_spatial_items = UpdateSpatialItemsDTO(items=update_items)

        response = await self.api.update_spatial(self.project, update_spatial_items, _request_timeout=self.timeout)
        updated_items = self._to_spatial_items(response, False)

        layer_map = {}
        for spatial_item, create_item in zip(updated_items, items):
            attributes = _filter_list_attributes(create_item.attributes)
            if len(attributes) > 0:
                spatial_item._layer_info = await self._load_layer(spatial_item.layer, layer_map)
                for name, value in attributes.items():
                    await self._store_attribute(spatial_item, name, value)

        if single_item:
            return updated_items[0]

        return updated_items

    @api_exception_handler
    def get_coverage(
        self,
        output_crs: str,
        id: int = None,
        external_id: str = None,
        dimensional_space: str = "2d",
        geometry_format: str = None,
    ) -> SpatialItemCoverageDTO:
        """Retrieve the coverage of the spatial object by internal ids or external ids.

        Args:
            id (int): the id of the spatial object
            external_id (str): the external_id reference of the spatial object
            dimensional_space (str): The spatial dimension of the coverage. Valid values are "2d", "3d"
            output_crs (str): the crs of the output coverage
            geometry_format (str): Geometry format wkt or geojson

        Returns:
            SpatialItemCoverageDTO: spatial object's data
        """
        run_func = partial(self.get_coverage_async, output_crs, id, external_id, dimensional_space, geometry_format)
        item = self._run_sync(run_func, self.timeout)
        return item

    def interpret(self, id: int = None, external_id: str = None):
        """Interpret attributes from spatial item by internal id or external id.

        Args:
            id (int): the id of the spatial object
            external_id (str): the external_id reference of the spatial object

        """
        run_func = partial(self.interpret_async, id, external_id)
        result = self._run_sync(run_func, self.timeout)
        return result

    def get_spatial_info(self, id: int = None, external_id: str = None) -> Optional[SpatialItem]:
        """Retrieves spatial item information by internal ids or external ids.

        Args:
            id (int): the id of the spatial object
            external_id (str): the external_id reference of the spatial object

        Returns:
            SpatialItem: A spatial object
        """
        run_func = partial(self.get_spatial_info_async, id, external_id)
        item = self._run_sync(run_func, self.timeout)
        return item

    def get_spatial(
        self, id: int = None, external_id: str = None, extractors: List[DataExtractor] = None
    ) -> Optional[SpatialItem]:
        """Retrieves spatial item data by internal ids or external ids.

        Args:
            id (int): the id of the spatial object
            external_id (str): the external_id reference of the spatial object
            extractors (List[DataExtractor]): a list of extractors. Each extractor will be applied to a specific
                attribute so that we don't get entire data for that attribute, but only the part we are interested in

        Returns:
            SpatialItem: spatial object's data
        """
        run_func = partial(self.get_spatial_async, id, external_id, extractors)
        result = self._run_sync(run_func, self.timeout)
        return result

    def get_intersections(
        self, geometry: Geometry, geometries: List[Geometry], output_crs, geometry_format: str = None
    ) -> List[BaseGeometry]:
        """ Find intersection between an array of geometries and another geometry

        Args:
            geometry (Geometry): a single geometry
            geometries (List[Geometry]): an array of geometries
            output_crs (str): the crs of intersection geometries
            geometry_format (str): the output format of the geometry if any. Valid values: wkt, geojson. Default to wkt
        Returns:
            List[BaseGeometry]: a list of intersections, each is a shapely geometry

        Example:
                >>> intersections = client.get_intersections(
                ...         output_crs="epsg:4326",
                ...         geometry=Geometry(external_id="external_id_1"),
                ...         geometries=[
                ...             Geometry(external_id="external_id_2"),
                ...             Geometry(external_id="external_id_3"),
                ...             Geometry(external_id="external_id_4"),
                ...         ],
                ...     )

        """

        @api_exception_handler
        async def get_intersections_async(
            geometry: Geometry, geometries: List[Geometry], output_crs, geometry_format: str = None
        ):
            geometry_dto = EitherIdDTO(
                id=geometry.id, external_id=geometry.external_id, local_vars_configuration=self.configuration
            )
            geometries_dto = [
                EitherIdDTO(id=geom.id, external_id=geom.external_id, local_vars_configuration=self.configuration)
                for geom in geometries
            ]
            intersection_query_dto = IntersectionQueryDTO(
                geometry=geometry_dto, geometries=geometries_dto, output_crs=output_crs
            )
            response = await self.api.find_intersection(
                self.project, intersection_query_dto, geometry=geometry_format, _request_timeout=self.timeout
            )
            if response is None:
                return None
            return [
                shape(geometry.intersection) if geometry_format == "geojson" else wkt.loads(geometry.intersection)
                for geometry in response.geometries
            ]

        run_func = partial(get_intersections_async, geometry, geometries, output_crs, geometry_format)
        result = self._run_sync(run_func, self.timeout)
        return result

    def persist_spatial_attribute(self, id: int, external_id: str, name: str, value) -> None:
        """Persist spatial attribute of the specified item into data store. The data must follow the  format specified
        in the layer of the item

        Args:
            id (int): the id of the spatial object
            external_id (str): the external_id reference of the spatial object
            name (str): the name of the attribute
            value: the value of the attribute
        """

        async def _persis_data(id: int, external_id: str, name: str, value):
            spatial_item = await self.get_spatial_info_async(id, external_id)
            layer_name = spatial_item.layer
            layer = await self.get_layer_async(name=layer_name)
            attributes = layer.attributes
            attribute = next((attribute for attribute in attributes if attribute.name == name), None)
            if attribute is None:
                raise GeospatialError("Attribute is not defined in the layer")
            await self.store_spatial_item_data_async(spatial_item.id, name, value, attribute.type)

        run_func = partial(_persis_data, id, external_id, name, value)
        self._run_sync(run_func, self.timeout)

    def get_attributes(
        self, attributes: List[str], id: int = None, external_id: str = None, extractors: List[DataExtractor] = None
    ) -> Dict[str, object]:
        """ Get spatial object's attributes

        Args:
            id (int): the id of the spatial object
            external_id (str): the external_id reference of the spatial object
            attributes (List[str]): a list of attribute names to get
            extractors (List[DataExtractor]): a list of extractors. Each extractor will be applied to a specific
                attribute so that we don't get entire data for that attribute, but only the part we are interested in

        Returns:
            Dict[str, object]: a dict of attribute's name and its value
        """

        item_id = EitherIdDTO(id, external_id, local_vars_configuration=self.configuration)
        run_func = partial(self.get_attributes_async, item_id, attributes, extractors)
        return self._run_sync(run_func, self.timeout)

    def list_layers(self, names: List[str] = None):
        """List all available layers.

        Args:
            names (List[str]): list of layer's names to retrieve. Use None to list all available layers.

        Returns:
            list[Layer]: list of layers
        """
        run_func = partial(self.list_layers_async, names)
        items = self._run_sync(run_func, self.timeout)
        return items

    @api_exception_handler
    async def get_layer_async(self, name: str):
        if name is None:
            raise GeospatialError(message="Layer name required")

        layer_filter = FeatureLayersFilterDTO(names=[name])
        response = await self.api.find_feature_layer(self.project, layer_filter, _request_timeout=self.timeout)
        layer = _first_item(response)
        if layer is None:
            return None

        return Layer(client=self, layer=layer)

    @lru_cache(maxsize=128)
    def get_layer(self, name: str):
        """Get layer by name.

        Args:
            name (str): name of the layer

        Returns:
            Layer: layer information
        """
        run_func = partial(self.get_layer_async, name)
        layer = self._run_sync(run_func, self.timeout)
        if layer is None:
            return None
        return Layer(client=self, layer=layer)

    def within(
        self,
        layer: str,
        geometry: Geometry,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
        geometry_format: str = None,
    ) -> SpatialList:
        """Search the spatial objects within 2D geometry.

        Args:
            layer (str): the layer to which objects belong
            geometry (Geometry): the input geometry
            name (str): the name of returned objects
            asset_ids (List[int]): the list of asset ids which spatial objects must link to
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            metadata (dict): a set of metadata pairs which spatial objects must have
            source (str): the source of spatial objects
            external_id_prefix (str): the prefix of external_id reference which spatial objects must have
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            limit (int): number of objects to be returned
            offset (int): the starting offset of objects in the results
            geometry_format (str): the output format of the geometry if any. Valid values: wkt, geojson. Default to wkt
        Returns:
            SpatialList: spatial object's data

        Example:
                >>> # search within the geometry of another spatial item
                >>> client.within(layer="polygon",
                ...        geometry=Geometry(external_id="external_id"),
                ...    )
                >>> # search within a specific area defined by user
                >>> items = client.within(
                ...     layer="polygon",
                ...     geometry=Geometry(
                ...         wkt="POLYGON ((289999 5999999, 290006 5999999, 290006 6000006, 289999 6000006, 289999 5999999))",
                ...         crs="epsg:23031",
                ...         ),
                ...     )

        """
        return self.find_spatial(
            layer,
            SpatialRelationship.within,
            geometry,
            None,
            name,
            asset_ids,
            attributes,
            metadata,
            source,
            external_id_prefix,
            output_crs,
            limit,
            offset,
            geometry_format,
        )

    def within_distance(
        self,
        layer: str,
        geometry: Geometry,
        distance: float,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
        geometry_format: str = None,
    ) -> SpatialList:
        """Search the spatial objects within distance 2D geometry.

        Args:
            layer (str): the layer to which objects belong
            geometry (Geometry): the input geometry
            distance (float): the distance to the input geometry when spatial_relationship is within distance
            name (str): the name of returned objects
            asset_ids (List[int]): the list of asset ids which spatial objects must link to
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            metadata (dict): a set of metadata pairs which spatial objects must have
            source (str): the source of spatial objects
            external_id_prefix (str): the prefix of external_id reference which spatial objects must have
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            limit (int): number of objects to be returned
            offset (int): the starting offset of objects in the results
            geometry_format (str): the output format of the geometry if any. Valid values: wkt, geojson. Default to wkt
        Returns:
            SpatialList: spatial object's data

        Example:
                >>> # search within the geometry of another spatial item
                >>> client.within_distance(layer="polygon",
                ...        geometry=Geometry(external_id="external_id"),
                ...        distance=10,
                ...    )
                >>> # search within a specific area defined by user
                >>> items = client.within_distance(
                ...     layer="polygon",
                ...     geometry=Geometry(
                ...         wkt="POLYGON ((289999 5999999, 290006 5999999, 290006 6000006, 289999 6000006, 289999 5999999))",
                ...         crs="epsg:23031",
                ...         ),
                ...     distance=10,
                ...     )

        """
        return self.find_spatial(
            layer,
            SpatialRelationship.within_distance,
            geometry,
            distance,
            name,
            asset_ids,
            attributes,
            metadata,
            source,
            external_id_prefix,
            output_crs,
            limit,
            offset,
            geometry_format,
        )

    def within_completely(
        self,
        layer: str,
        geometry: Geometry,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
        geometry_format: str = None,
    ) -> SpatialList:
        """Search the spatial objects within distance 2D geometry.

        Args:
            layer (str): the layer to which objects belong
            geometry (Geometry): the input geometry
            name (str): the name of returned objects
            asset_ids (List[int]): the list of asset ids which spatial objects must link to
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            metadata (dict): a set of metadata pairs which spatial objects must have
            source (str): the source of spatial objects
            external_id_prefix (str): the prefix of external_id reference which spatial objects must have
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            limit (int): number of objects to be returned
            offset (int): the starting offset of objects in the results
            geometry_format (str): the output format of the geometry if any. Valid values: wkt, geojson. Default to wkt
        Returns:
            SpatialList: spatial object's data

        Example:
                >>> # search within the geometry of another spatial item
                >>> client.within_completely(layer="polygon",
                ...        geometry=Geometry(external_id="external_id"),
                ...    )
                >>> # search within a specific area defined by user
                >>> items = client.within_completely(
                ...     layer="polygon",
                ...     geometry=Geometry(
                ...         wkt="POLYGON ((289999 5999999, 290006 5999999, 290006 6000006, 289999 6000006, 289999 5999999))",
                ...         crs="epsg:23031",
                ...         ),
                ...     )

        """
        return self.find_spatial(
            layer,
            SpatialRelationship.within_completely,
            geometry,
            None,
            name,
            asset_ids,
            attributes,
            metadata,
            source,
            external_id_prefix,
            output_crs,
            limit,
            offset,
            geometry_format,
        )

    def intersect(
        self,
        layer: str,
        geometry: Geometry,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
        geometry_format: str = None,
    ) -> SpatialList:
        """Search the spatial objects intersect 2D geometry.

        Args:
            layer (str): the layer to which objects belong
            geometry (Geometry): the input geometry
            name (str): the name of returned objects
            asset_ids (List[int]): the list of asset ids which spatial objects must link to
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            metadata (dict): a set of metadata pairs which spatial objects must have
            source (str): the source of spatial objects
            external_id_prefix (str): the prefix of external_id reference which spatial objects must have
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            limit (int): number of objects to be returned
            offset (int): the starting offset of objects in the results
            geometry_format (str): the output format of the geometry if any. Valid values: wkt, geojson. Default to wkt
        Returns:
            SpatialList: spatial object's data

        Example:
                >>> # search within the geometry of another spatial item
                >>> client.intersect(layer="polygon",
                ...        geometry=Geometry(external_id="external_id"),
                ...    )
                >>> # search within a specific area defined by user
                >>> items = client.intersect(
                ...     layer="polygon",
                ...     geometry=Geometry(
                ...         wkt="POLYGON ((289999 5999999, 290006 5999999, 290006 6000006, 289999 6000006, 289999 5999999))",
                ...         crs="epsg:23031",
                ...         ),
                ...     )

        """
        return self.find_spatial(
            layer,
            SpatialRelationship.intersect,
            geometry,
            None,
            name,
            asset_ids,
            attributes,
            metadata,
            source,
            external_id_prefix,
            output_crs,
            limit,
            offset,
            geometry_format,
        )

    def within_3d(
        self,
        layer: str,
        geometry: Geometry,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
        geometry_format: str = None,
    ) -> SpatialList:
        """Search the spatial objects within 3D geometry.

        Args:
            layer (str): the layer to which objects belong
            geometry (Geometry): the input geometry
            name (str): the name of returned objects
            asset_ids (List[int]): the list of asset ids which spatial objects must link to
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            metadata (dict): a set of metadata pairs which spatial objects must have
            source (str): the source of spatial objects
            external_id_prefix (str): the prefix of external_id reference which spatial objects must have
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            limit (int): number of objects to be returned
            offset (int): the starting offset of objects in the results
            geometry_format (str): the output format of the geometry if any. Valid values: wkt, geojson. Default to wkt
        Returns:
            SpatialList: spatial object's data

        Example:
                >>> # search within the geometry of another spatial item
                >>> client.within_3d(layer="polygon",
                ...        geometry=Geometry(external_id="external_id"),
                ...    )
                >>> # search within a specific area defined by user
                >>> items = client.within_3d(
                ...     layer="polygon",
                ...     geometry=Geometry(
                ...         wkt="POLYGON ((289999 5999999, 290006 5999999, 290006 6000006, 289999 6000006, 289999 5999999))",
                ...         crs="epsg:23031",
                ...         ),
                ...     )

        """
        return self.find_spatial(
            layer,
            SpatialRelationship.within_3d,
            geometry,
            None,
            name,
            asset_ids,
            attributes,
            metadata,
            source,
            external_id_prefix,
            output_crs,
            limit,
            offset,
            geometry_format,
        )

    def within_distance_3d(
        self,
        layer: str,
        geometry: Geometry,
        distance: float,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
        geometry_format: str = None,
    ) -> SpatialList:
        """Search the spatial objects within distance 3D geometry.

        Args:
            layer (str): the layer to which objects belong
            geometry (Geometry): the input geometry
            distance (float): the distance to the input geometry when spatial_relationship is within distance.
            name (str): the name of returned objects
            asset_ids (List[int]): the list of asset ids which spatial objects must link to
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            metadata (dict): a set of metadata pairs which spatial objects must have
            source (str): the source of spatial objects
            external_id_prefix (str): the prefix of external_id reference which spatial objects must have
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            limit (int): number of objects to be returned
            offset (int): the starting offset of objects in the results
            geometry_format (str): the output format of the geometry if any. Valid values: wkt, geojson. Default to wkt
        Returns:
            SpatialList: spatial object's data

        Example:
                >>> # search within the geometry of another spatial item
                >>> client.within_distance_3d(layer="polygon",
                ...        geometry=Geometry(external_id="external_id"),
                ...    )
                >>> # search within a specific area defined by user
                >>> items = client.within_distance_3d(
                ...     layer="polygon",
                ...     geometry=Geometry(
                ...         wkt="POLYGON ((289999 5999999, 290006 5999999, 290006 6000006, 289999 6000006, 289999 5999999))",
                ...         crs="epsg:23031",
                ...         ),
                ...     )

        """
        return self.find_spatial(
            layer,
            SpatialRelationship.within_distance_3d,
            geometry,
            distance,
            name,
            asset_ids,
            attributes,
            metadata,
            source,
            external_id_prefix,
            output_crs,
            limit,
            offset,
            geometry_format,
        )

    def within_completely_3d(
        self,
        layer: str,
        geometry: Geometry,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
        geometry_format: str = None,
    ) -> SpatialList:
        """Search the spatial objects completely 3D geometry.

        Args:
            layer (str): the layer to which objects belong
            geometry (Geometry): the input geometry
            name (str): the name of returned objects
            asset_ids (List[int]): the list of asset ids which spatial objects must link to
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            metadata (dict): a set of metadata pairs which spatial objects must have
            source (str): the source of spatial objects
            external_id_prefix (str): the prefix of external_id reference which spatial objects must have
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            limit (int): number of objects to be returned
            offset (int): the starting offset of objects in the results
            geometry_format (str): the output format of the geometry if any. Valid values: wkt, geojson. Default to wkt
        Returns:
            SpatialList: spatial object's data

        Example:
                >>> # search within the geometry of another spatial item
                >>> client.within_completely_3d(layer="polygon",
                ...        geometry=Geometry(external_id="external_id"),
                ...    )
                >>> # search within a specific area defined by user
                >>> items = client.within_completely_3d(
                ...     layer="polygon",
                ...     geometry=Geometry(
                ...         wkt="POLYGON ((289999 5999999, 290006 5999999, 290006 6000006, 289999 6000006, 289999 5999999))",
                ...         crs="epsg:23031",
                ...         ),
                ...     )

        """
        return self.find_spatial(
            layer,
            SpatialRelationship.within_completely_3d,
            geometry,
            None,
            name,
            asset_ids,
            attributes,
            metadata,
            source,
            external_id_prefix,
            output_crs,
            limit,
            offset,
            geometry_format,
        )

    def intersect_3d(
        self,
        layer: str,
        geometry: Geometry,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
        geometry_format: str = None,
    ) -> SpatialList:
        """Search the spatial objects inersect 3D geometry.

        Args:
            layer (str): the layer to which objects belong
            geometry (Geometry): the input geometry
            name (str): the name of returned objects
            asset_ids (List[int]): the list of asset ids which spatial objects must link to
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            metadata (dict): a set of metadata pairs which spatial objects must have
            source (str): the source of spatial objects
            external_id_prefix (str): the prefix of external_id reference which spatial objects must have
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            limit (int): number of objects to be returned
            offset (int): the starting offset of objects in the results
            geometry_format (str): the output format of the geometry if any. Valid values: wkt, geojson. Default to wkt
        Returns:
            SpatialList: spatial object's data

        Example:
                >>> # search within the geometry of another spatial item
                >>> client.intersect_3d(layer="polygon",
                ...        geometry=Geometry(external_id="external_id"),
                ...    )
                >>> # search within a specific area defined by user
                >>> items = client.intersect_3d(
                ...     layer="polygon",
                ...     geometry=Geometry(
                ...         wkt="POLYGON ((289999 5999999, 290006 5999999, 290006 6000006, 289999 6000006, 289999 5999999))",
                ...         crs="epsg:23031",
                ...         ),
                ...     )

        """
        return self.find_spatial(
            layer,
            SpatialRelationship.intersect_3d,
            geometry,
            None,
            name,
            asset_ids,
            attributes,
            metadata,
            source,
            external_id_prefix,
            output_crs,
            limit,
            offset,
            geometry_format,
        )

    def find_spatial(
        self,
        layer: str,
        spatial_relationship: SpatialRelationship = None,
        geometry: Geometry = None,
        distance: float = None,
        name: str = None,
        asset_ids: List[int] = None,
        attributes: List[str] = None,
        metadata: Dict[str, str] = None,
        source: str = None,
        external_id_prefix: str = None,
        output_crs: str = None,
        limit: int = 10,
        offset: int = 0,
        geometry_format: str = None,
    ) -> SpatialList:
        """Search the spatial objects based on metadata or spatial relationships.

        Args:
            layer (str): the layer to which objects belong
            spatial_relationship (SpatialRelationship): the spatial relationship between looking objects and the input geometry
            geometry (Geometry): the input geometry
            distance (float): the distance to the input geometry when spatial_relationship is within distance.
            name (str): the name of returned objects
            asset_ids (List[int]): the list of asset ids which spatial objects must link to
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            metadata (dict): a set of metadata pairs which spatial objects must have
            source (str): the source of spatial objects
            external_id_prefix (str): the prefix of external_id reference which spatial objects must have
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            limit (int): number of objects to be returned
            offset (int): the starting offset of objects in the results
            geometry_format (str): the output format of the geometry if any. Valid values: wkt, geojson. Default to wkt
        Returns:
            SpatialList: spatial object's data

        Example:
                >>> # search within the geometry of another spatial item
                >>> client.find_spatial(layer="polygon", spatial_relationship=SpatialRelationship.within,
                ...        geometry=Geometry(external_id="external_id"),
                ...    )
                >>> # search within a specific area defined by user
                >>> items = client.find_spatial(
                ...     layer="polygon",
                ...     spatial_relationship=SpatialRelationship.within,
                ...     geometry=Geometry(
                ...         wkt="POLYGON ((289999 5999999, 290006 5999999, 290006 6000006, 289999 6000006, 289999 5999999))",
                ...         crs="epsg:23031",
                ...         ),
                ...     )

        """
        run_func = partial(
            self.find_spatial_async,
            layer,
            spatial_relationship,
            geometry,
            distance,
            name,
            asset_ids,
            attributes,
            metadata,
            source,
            external_id_prefix,
            output_crs,
            limit,
            offset,
            geometry_format,
        )
        result = self._run_sync(run_func, self.timeout)
        return result

    def get_layer_items(
        self, layer: str, attributes: List[str] = None, output_crs: str = None, geometry_format: str = None
    ) -> List[SpatialItem]:
        """Get all spatial items belong to layer.

        Warning:
            This method will load all spatial items into memory and has a risk to get memory overflow.

        Args:
            layer (str): the layer to which objects belong
            attributes (List[str]): the list of attribute names are returned together with spatial objects
            output_crs (str): the crs of the output geometry attribute in case `geometry` attributes are queried
            geometry_format (str): the geometry format of the output geometries. Valid values: wkt, geojson. Default to wkt

        Returns:
            SpatialList: spatial object list
        """
        spatial_list = SpatialList(client=self, layer_name=layer)
        items = []
        offset = 0
        limit = 100
        while True:
            bucket = self.find_spatial(
                layer=layer,
                attributes=attributes,
                limit=limit,
                offset=offset,
                output_crs=output_crs,
                geometry_format=geometry_format,
            )
            items.extend(bucket)
            offset += limit
            if limit != len(bucket):
                break
        spatial_list.extend(items)
        return spatial_list

    def shape_file_save(self, file, layer: str, create_layer: bool = False, attributes: Optional[List[str]] = None):
        """Extract spatial items from shapefile and save it into geospatial.

        Args:
            file (str): file location on local drive
            layer (str): the layer name to save
            create_layer (bool): create layer if not exists
            attributes (Optional[List[str]]): attributes to save (if None save all attributes)
        """
        run_func = partial(self.shape_file_save_async, file, layer, create_layer, attributes)
        result = self._run_sync(run_func, self.ingestion_timeout)
        return result

    def has_spatial_relationship(
        self, geometry: Geometry, other: Geometry, spatial_relationship: SpatialRelationship, distance: float = None
    ) -> bool:
        """ Test if a spatial relationship exists between two spatial objects

        Args:
            geometry (Geometry): the first geometry
            other (Geometry): the second geoemtry
            spatial_relationship (SpatialRelationship): the spatial relationship between objects to check.
            distance (float): the distance between spatial objects in case of checking "within distance" relationship
        Returns:
            bool: True or False

        """
        geometry_info = self.get_spatial_info(id=geometry.id, external_id=geometry.external_id)
        if geometry_info is None:
            return None

        offset = 0
        limit = 10

        while True:
            items = self.find_spatial(
                layer=geometry_info.layer,
                geometry=other,
                external_id_prefix=geometry_info.external_id,
                spatial_relationship=spatial_relationship,
                distance=distance,
                limit=limit,
                offset=offset,
            )
            for item in items:
                if item.external_id == geometry.external_id or item.id == geometry.id:
                    return True
            if len(items) < limit:
                return False

            offset = offset + limit

    def get_grid_coverage(
        self, geometry: TextBasedGeometry, id: int = None, external_id: str = None, distance: float = None
    ) -> GridCoverage:
        """Given a geometry and a seismic volume (identified by id or external_id), return a list of inlines and xlines of
        the volume covered by the geometry extent (by distance unit, default to geometry itself if distance is not specified).

        Args:
            id (int): the id of the spatial object (seismic volume)
            external_id (str): the external_id reference of the spatial object (seismic volume)
            geometry (TextBasedGeometry): the input geometry
            distance (float): the distance to extend the input geometry
        Returns:
            GridCoverage: a map from each line (inline) to a list of cross points (xlines)
        """
        run_func = partial(self.get_grid_coverage_async, geometry, id, external_id, distance)
        return self._run_sync(run_func, self.ingestion_timeout)

    def union(self, items: List[Geometry], output_crs: str, geometry_format: str = "wkt") -> BaseGeometry:
        """Compute representation of the union of the given 2D geometric objects

        Args:
            items (List[Geometry]): a list of geometries to compute the union
            output_crs (str): the desired crs of the output
            geometry_format (str): the geometry format of the output. Valid values: wkt, geojson. Default to wkt

        Returns:
            BaseGeometry: the union of input geometries
        """

        @api_exception_handler
        async def union_async(
            api: SpatialApi,
            project,
            configuration,
            timeout,
            items: List[Geometry],
            output_crs: str,
            geometry_format: str,
        ) -> BaseGeometry:
            items_dto = [
                GeometryDTO(
                    id=item.id,
                    external_id=item.external_id,
                    wkt=item.wkt,
                    crs=item.crs,
                    geojson=item.geojson,
                    local_vars_configuration=configuration,
                )
                for item in items
            ]
            geometry_items = GeometryItemsDTO(items=items_dto, output_crs=output_crs)
            response = await api.operation_union(
                project=project, geometry_items_dto=geometry_items, _request_timeout=timeout, geometry=geometry_format
            )
            geometry = shape(response.geojson) if geometry_format == "geojson" else wkt.loads(response.wkt)
            return geometry

        run_func = partial(
            union_async,
            self.api,
            self.project,
            self.configuration,
            self.timeout,
            items,
            output_crs,
            geometry_format=geometry_format,
        )
        return self._run_sync(run_func, self.timeout)
