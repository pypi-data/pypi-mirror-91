"""Main cloudwanderer module."""
from typing import List
import logging
from typing import TYPE_CHECKING, Iterator
import concurrent.futures
from boto3.resources.base import ServiceResource
from botocore import xform_name
import boto3
from .utils import exception_logging_wrapper
from .boto3_interface import CloudWandererBoto3Interface
from .aws_urn import AwsUrn
from .service_mappings import ServiceMappingCollection, GlobalServiceResourceMappingNotFound
from boto3.resources.model import ResourceModel

logger = logging.getLogger('cloudwanderer')

if TYPE_CHECKING:
    from .storage_connectors import BaseStorageConnector  # noqa


class CloudWanderer():
    """CloudWanderer.

    Args:
        storage_connectors: CloudWanderer storage connector objects.
        boto3_session (boto3.session.Session): A boto3 :class:`~boto3.session.Session` object.
    """

    def __init__(
            self, storage_connectors: List['BaseStorageConnector'],
            boto3_session: boto3.session.Session = None) -> None:
        """Initialise CloudWanderer."""
        self.storage_connectors = storage_connectors
        self.boto3_session = boto3_session or boto3.session.Session()
        self.boto3_interface = CloudWandererBoto3Interface(boto3_session=self.boto3_session)
        self.service_maps = ServiceMappingCollection(boto3_session=self.boto3_session)
        self._account_id = None
        self._enabled_regions = None

    def write_resources(
            self, exclude_resources: List[str] = None, client_args: dict = None) -> None:
        """Write all AWS resources in this account from all regions and all services to storage.

        Arguments:
            exclude_resources (list): A list of resource names to exclude (e.g. ``['instance']``)
            client_args (dict): Arguments to pass into the boto3 client.
                See: :meth:`boto3.session.Session.client`
        """
        logger.info('Writing resources in all regions')
        for region_name in self.enabled_regions:
            self.write_resources_in_region(
                exclude_resources=exclude_resources,
                region_name=region_name,
                client_args=client_args
            )

    def write_resources_concurrently(
            self, session_generator: callable, exclude_resources: List[str] = None, client_args: dict = None,
            concurrency: int = 10) -> None:
        """Write all AWS resources in this account from all regions and all services to storage.

        Arguments:
            exclude_resources (list): A list of resource names to exclude (e.g. ``['instance']``)
            client_args (dict): Arguments to pass into the boto3 client.
                See: :meth:`boto3.session.Session.client`
            concurrency (int): Number of query threads to invoke concurrently.
                If the number of threads exceeds the number of regions by at least two times
                multiple services to be queried concurrently in each region.
                **WARNING:** Experimental. Complete data capture depends heavily on the thread safeness of the
                storage connector and has not been thoroughly tested!
            session_generator (callable): A method which returns a new boto3 session when called.
                You're usually safe to pass in ``boto3.session.Session``
        """
        logger.info('Writing resources in all regions')
        logger.warning('Using concurrency of: %s - CONCURRENCY IS EXPERIMENTAL', concurrency)
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
            for region_name in self.enabled_regions:
                boto3_session = session_generator() if session_generator else self.boto3_session
                cw = CloudWanderer(
                    storage_connectors=self.storage_connectors,
                    boto3_session=boto3_session
                )

                executor.submit(
                    exception_logging_wrapper,
                    method=cw.write_resources_in_region,
                    exclude_resources=exclude_resources,
                    region_name=region_name,
                    client_args=client_args
                )

    def write_resources_in_region(
            self, exclude_resources: List[str] = None, region_name: str = None,
            client_args: dict = None) -> None:
        """Write all AWS resources in this account region from all services to storage.

        Arguments:
            exclude_resources (list): A list of resource names to exclude (e.g. ``['instance']``)
            region_name (str): The name of the region to get resources from
                (defaults to session default if not specified)
            client_args (dict): Arguments to pass into the boto3 client.
                See: :meth:`boto3.session.Session.client`
        """
        exclude_resources = exclude_resources or []
        for boto3_service in self.boto3_interface.get_all_resource_services():
            self.write_resources_of_service_in_region(
                service_name=boto3_service.meta.service_name,
                exclude_resources=exclude_resources,
                region_name=region_name,
                client_args=client_args
            )

    def write_resources_of_service_in_region(
            self, service_name: str, exclude_resources: List[str] = None,
            region_name: str = None, client_args: dict = None) -> None:
        """Write all AWS resources in this region in this service to storage.

        Cleans up any resources in the StorageConnector that no longer exist.

        Arguments:
            service_name (str): The name of the service to write resources for (e.g. ``'ec2'``)
            exclude_resources (list): A list of resource names to exclude (e.g. ``['instance']``)
            region_name (str): The name of the region to get resources from
                (defaults to session default if not specified)
            client_args (dict): Arguments to pass into the boto3 client.
                See: :meth:`boto3.session.Session.client`
        """
        client_args = client_args.copy() if client_args else {}
        if region_name:
            client_args['region_name'] = region_name
        if 'region_name' not in client_args:
            client_args['region_name'] = self.boto3_session.region_name

        logger.info("Writing all %s resources in %s", service_name, client_args['region_name'])
        exclude_resources = exclude_resources or []

        for resource_type in self.boto3_interface.get_service_resource_types(service_name=service_name):
            if resource_type in exclude_resources:
                logger.info('Skipping %s as per exclude_resources', resource_type)
                continue
            self.write_resources_of_type_in_region(
                service_name=service_name,
                resource_type=resource_type,
                client_args=client_args
            )

    def write_resources_of_type_in_region(
            self, service_name: str, resource_type: str = None,
            region_name: str = None, client_args: dict = None) -> None:
        """Write all AWS resources in this region in this service to storage.

        Cleans up any resources in the StorageConnector that no longer exist.

        Arguments:
            service_name (str): The name of the service to write resources for (e.g. ``'ec2'``)
            resource_type (str): The name of the type of the resource to write (e.g. ``'instance'``)
            region_name (str): The name of the region to get resources from
                (defaults to session default if not specified)
            client_args (dict): Arguments to pass into the boto3 client.
                See: :meth:`boto3.session.Session.client`
        """
        client_args = client_args or {
            'region_name': region_name or self.boto3_session.region_name
        }
        service_map = self.service_maps.get_service_mapping(service_name=service_name)
        if service_map.is_global_service and service_map.global_service_region != client_args['region_name']:
            logger.info("Skipping %s as it does not have resources in %s",
                        service_name, client_args['region_name'])
            return
        logger.info('--> Fetching %s %s from %s', service_name, resource_type, client_args['region_name'])
        resources = self.boto3_interface.get_resources_of_type(service_name, resource_type, client_args)
        urns = []
        for boto3_resource in resources:
            urns.extend(list(self._write_resource(boto3_resource, client_args['region_name'])))
        self._clean_resources_in_region(service_name, resource_type, client_args['region_name'], urns)

    def _write_resource(self, boto3_resource: ServiceResource, region_name: str) -> Iterator[AwsUrn]:
        urn = self._get_resource_urn(boto3_resource, region_name)
        for storage_connector in self.storage_connectors:
            storage_connector.write_resource(urn, boto3_resource)
        yield urn

        for subresource in self.boto3_interface.get_subresources(boto3_resource=boto3_resource):
            subresource.load()
            urn = self._get_resource_urn(subresource, region_name)
            yield urn
            for storage_connector in self.storage_connectors:
                storage_connector.write_resource(urn, subresource)

    def _clean_resources_in_region(
            self, service_name: str, resource_type: str, region_name: str, current_urns: List[AwsUrn]) -> None:
        """Remove all resources of this type in this region which no longer exist."""
        for storage_connector in self.storage_connectors:
            storage_connector.delete_resource_of_type_in_account_region(
                service=service_name,
                resource_type=resource_type,
                account_id=self.account_id,
                region=region_name,
                urns_to_keep=current_urns
            )

    def write_secondary_attributes(
            self, exclude_resources: List[str] = None, client_args: dict = None) -> None:
        """Write all secondary attributes in this account from all regions and all services to storage.

        Arguments:
            exclude_resources (list): A list of resource names to exclude (e.g. ``['instance']``)
            client_args (dict): Arguments to pass into the boto3 client.
                See: :meth:`boto3.session.Session.client`
        """
        logger.info('Writing secondary attributes in all enabled regions')
        for region_name in self.enabled_regions:
            self.write_secondary_attributes_in_region(
                region_name=region_name,
                exclude_resources=exclude_resources,
                client_args=client_args
            )

    def write_secondary_attributes_in_region(
            self, exclude_resources: List[str] = None, region_name: str = None, client_args: dict = None) -> None:
        """Write all secondary attributes in this account in this region to storage.

        These custom resource attribute definitions allow us to fetch secondary attributes that are not returned by the
        resource's default describe calls.
        Unlike :meth:`~CloudWanderer.write_resources` and :meth:`~CloudWanderer.write_resources_of_type_in_region`
        this method does not clean up stale secondary attributes from storage.

        Arguments:
            exclude_resources (list): A list of resources not to write attributes for (e.g. ``['vpc']``)
            region_name (str): The name of the region to get resources from
                (defaults to session default if not specified)
            client_args (dict): Arguments to pass into the boto3 client.
                See: :meth:`boto3.session.Session.client`
        """
        for boto3_service in self.boto3_interface.get_all_resource_services():
            self.write_secondary_attributes_of_service_in_region(
                service_name=boto3_service.meta.service_name,
                exclude_resources=exclude_resources,
                client_args=client_args,
                region_name=region_name,
            )

    def write_secondary_attributes_of_service_in_region(
            self, service_name: str, exclude_resources: List[str] = None,
            region_name: str = None, client_args: dict = None) -> None:
        """Write all secondary attributes in this account in this service to storage.

        These custom resource attribute definitions allow us to fetch secondary attributes that are not returned by the
        resource's default describe calls.
        Unlike :meth:`~CloudWanderer.write_resources` and :meth:`~CloudWanderer.write_resources_of_type_in_region`
        this method does not clean up stale secondary attributes from storage.

        Arguments:
            service_name (str): The name of the service to write the attributes of (e.g. ``'ec2'``)
            exclude_resources (list): A list of resources not to write attributes for (e.g. ``['vpc']``)
            region_name (str): The name of the region to get resources from
                (defaults to session default if not specified)
            client_args (dict): Arguments to pass into the boto3 client.
                See: :meth:`boto3.session.Session.client`
        """
        client_args = client_args or {
            'region_name': region_name or self.boto3_session.region_name
        }
        exclude_resources = exclude_resources or []
        service_map = self.service_maps.get_service_mapping(service_name=service_name)
        if service_map.is_global_service and service_map.global_service_region != client_args['region_name']:
            logger.info("Skipping %s as it does not have resources in %s",
                        service_name, client_args['region_name'])
            return
        exclude_resources = exclude_resources or []
        collections = self.boto3_interface.get_resource_collections(
            boto3_service=self.boto3_interface.get_resource_service_by_name(
                service_name=service_name,
                client_args=client_args
            )
        )
        for resource_type in self.boto3_interface.get_service_resource_types_from_collections(collections):
            try:
                resource_map = service_map.get_resource_mapping(resource_type=resource_type)
            except GlobalServiceResourceMappingNotFound:
                continue
            if not resource_map.has_secondary_attributes:
                continue
            logger.info("Writing all %s %s secondary attributes in %s",
                        service_name, resource_type, client_args['region_name'])
            if resource_type in exclude_resources:
                logger.info('Skipping %s as per exclude_resources', resource_type)
                continue
            self.write_secondary_attributes_of_type_in_region(
                service_name=service_name,
                resource_type=resource_type,
                client_args=client_args
            )

    def write_secondary_attributes_of_type_in_region(
            self, service_name: str, resource_type: str, region_name: str = None, client_args: dict = None) -> None:
        """Write all secondary attributes in this account of this resource type to storage.

        These custom resource attribute definitions allow us to fetch secondary attributes that are not returned by the
        resource's default describe calls.

        Arguments:
            service_name (str): The name of the service to write the attributes of (e.g. ``ec2``)
            resource_type (str): The type of resource to write the attributes of (e.g. ``instance``)
            region_name (str): The name of the region to get resources from
                (defaults to session default if not specified)
            client_args (dict): Arguments to pass into the boto3 client.
                See: :meth:`boto3.session.Session.client`
        """
        client_args = client_args or {
            'region_name': region_name or self.boto3_session.region_name
        }
        resources = self.boto3_interface.get_resources_of_type(
            service_name=service_name,
            resource_type=resource_type,
            client_args=client_args
        )
        service_map = self.service_maps.get_service_mapping(service_name=service_name)
        try:
            resource_map = service_map.get_resource_mapping(resource_type=resource_type)
        except GlobalServiceResourceMappingNotFound:
            logger.warning('Skipping %s %s as it does not have secondary attributes', service_name, resource_type)
            return
        if not resource_map.has_secondary_attributes:
            logger.warning('Skipping %s %s as it does not have secondary attributes', service_name, resource_type)
            return
        for resource in resources:
            secondary_attributes = self.boto3_interface.get_secondary_attributes(
                boto3_resource=resource)
            for secondary_attribute in secondary_attributes:
                attribute_type = xform_name(secondary_attribute.meta.resource_model.name)
                logger.info('--> Fetching %s %s %s in %s', service_name,
                            resource_type, attribute_type, client_args['region_name'])
                urn = self._get_resource_urn(resource, client_args['region_name'])
                for storage_connector in self.storage_connectors:
                    storage_connector.write_secondary_attribute(
                        urn=urn,
                        secondary_attribute=secondary_attribute,
                        attribute_type=attribute_type
                    )

    @property
    def account_id(self) -> str:
        """Return the AWS Account ID our boto3 session is authenticated against."""
        if self._account_id is None:
            sts = self.boto3_session.client('sts')
            self._account_id = sts.get_caller_identity()['Account']
        return self._account_id

    @property
    def enabled_regions(self) -> List[str]:
        """Return a list of enabled regions in this account."""
        if not self._enabled_regions:
            regions = self.boto3_session.client('ec2').describe_regions()['Regions']
            self._enabled_regions = [
                region['RegionName']
                for region in regions
                if region['OptInStatus'] != 'not-opted-in'
            ]
        return self._enabled_regions

    def _get_resource_urn(self, resource: ResourceModel, region_name: str) -> 'AwsUrn':
        id_members = [x.name for x in resource.meta.resource_model.identifiers]
        resource_ids = []
        for id_member in id_members:
            id_part = getattr(resource, id_member)
            if id_part.startswith('arn:'):
                id_part = ''.join(id_part.split(':')[5:])
            resource_ids.append(id_part)
        compound_resource_id = ':'.join(resource_ids)
        service_map = self.service_maps.get_service_mapping(resource.meta.service_name)
        return AwsUrn(
            account_id=self.account_id,
            region=service_map.get_resource_region(resource, region_name),
            service=resource.meta.service_name,
            resource_type=xform_name(resource.meta.resource_model.name),
            resource_id=compound_resource_id
        )
