# autogenerated module
from dataclasses import dataclass, field
from typing import List

from ..core.dataclasses_dict import DataclassDictMixIn

from . import meta_v1
from . import core_v1


@dataclass
class Endpoint(DataclassDictMixIn):
    """Endpoint represents a single logical "backend" implementing a service.

      **parameters**

      * **addresses** ``List[str]`` - addresses of this endpoint. The contents of this field are interpreted
        according to the corresponding EndpointSlice addressType field. Consumers must
        handle different types of addresses in the context of their own capabilities.
        This must contain at least one address but no more than 100.
      * **conditions** ``EndpointConditions`` - *(optional)* conditions contains information about the current status of the endpoint.
      * **hostname** ``str`` - *(optional)* hostname of this endpoint. This field may be used by consumers of endpoints to
        distinguish endpoints from each other (e.g. in DNS names). Multiple endpoints
        which use the same hostname should be considered fungible (e.g. multiple A
        values in DNS). Must be lowercase and pass DNS Label (RFC 1123) validation.
      * **nodeName** ``str`` - *(optional)* nodeName represents the name of the Node hosting this endpoint. This can be
        used to determine endpoints local to a Node. This field can be enabled with
        the EndpointSliceNodeName feature gate.
      * **targetRef** ``core_v1.ObjectReference`` - *(optional)* targetRef is a reference to a Kubernetes object that represents this endpoint.
      * **topology** ``dict`` - *(optional)* topology contains arbitrary topology information associated with the endpoint.
        These key/value pairs must conform with the label format.
        https://kubernetes.io/docs/concepts/overview/working-with-objects/labels
        Topology may include a maximum of 16 key/value pairs. This includes, but is
        not limited to the following well known keys: * kubernetes.io/hostname: the
        value indicates the hostname of the node
          where the endpoint is located. This should match the corresponding
          node label.
        * topology.kubernetes.io/zone: the value indicates the zone where the
          endpoint is located. This should match the corresponding node label.
        * topology.kubernetes.io/region: the value indicates the region where the
          endpoint is located. This should match the corresponding node label.
        This field is deprecated and will be removed in future api versions.
    """
    addresses: 'List[str]'
    conditions: 'EndpointConditions' = None
    hostname: 'str' = None
    nodeName: 'str' = None
    targetRef: 'core_v1.ObjectReference' = None
    topology: 'dict' = None


@dataclass
class EndpointConditions(DataclassDictMixIn):
    """EndpointConditions represents the current condition of an endpoint.

      **parameters**

      * **ready** ``bool`` - *(optional)* ready indicates that this endpoint is prepared to receive traffic, according
        to whatever system is managing the endpoint. A nil value indicates an unknown
        state. In most cases consumers should interpret this unknown state as ready.
        For compatibility reasons, ready should never be "true" for terminating
        endpoints.
      * **serving** ``bool`` - *(optional)* serving is identical to ready except that it is set regardless of the
        terminating state of endpoints. This condition should be set to true for a
        ready endpoint that is terminating. If nil, consumers should defer to the
        ready condition. This field can be enabled with the
        EndpointSliceTerminatingCondition feature gate.
      * **terminating** ``bool`` - *(optional)* terminating indicates that this endpoint is terminating. A nil value indicates
        an unknown state. Consumers should interpret this unknown state to mean that
        the endpoint is not terminating. This field can be enabled with the
        EndpointSliceTerminatingCondition feature gate.
    """
    ready: 'bool' = None
    serving: 'bool' = None
    terminating: 'bool' = None


@dataclass
class EndpointPort(DataclassDictMixIn):
    """EndpointPort represents a Port used by an EndpointSlice

      **parameters**

      * **appProtocol** ``str`` - *(optional)* The application protocol for this port. This field follows standard Kubernetes
        label syntax. Un-prefixed names are reserved for IANA standard service names
        (as per RFC-6335 and http://www.iana.org/assignments/service-names).
        Non-standard protocols should use prefixed names such as
        mycompany.com/my-custom-protocol.
      * **name** ``str`` - *(optional)* The name of this port. All ports in an EndpointSlice must have a unique name.
        If the EndpointSlice is dervied from a Kubernetes service, this corresponds to
        the Service.ports[].name. Name must either be an empty string or pass
        DNS_LABEL validation: * must be no more than 63 characters long. * must
        consist of lower case alphanumeric characters or '-'. * must start and end
        with an alphanumeric character. Default is empty string.
      * **port** ``int`` - *(optional)* The port number of the endpoint. If this is not specified, ports are not
        restricted and must be interpreted in the context of the specific consumer.
      * **protocol** ``str`` - *(optional)* The IP protocol for this port. Must be UDP, TCP, or SCTP. Default is TCP.
    """
    appProtocol: 'str' = None
    name: 'str' = None
    port: 'int' = None
    protocol: 'str' = None


@dataclass
class EndpointSlice(DataclassDictMixIn):
    """EndpointSlice represents a subset of the endpoints that implement a service.
      For a given service there may be multiple EndpointSlice objects, selected by
      labels, which must be joined to produce the full set of endpoints.

      **parameters**

      * **addressType** ``str`` - addressType specifies the type of address carried by this EndpointSlice. All
        addresses in this slice must be the same type. This field is immutable after
        creation. The following address types are currently supported: * IPv4:
        Represents an IPv4 Address. * IPv6: Represents an IPv6 Address. * FQDN:
        Represents a Fully Qualified Domain Name.
      * **endpoints** ``List[Endpoint]`` - endpoints is a list of unique endpoints in this slice. Each slice may include
        a maximum of 1000 endpoints.
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* Standard object's metadata.
      * **ports** ``List[EndpointPort]`` - *(optional)* ports specifies the list of network ports exposed by each endpoint in this
        slice. Each port must have a unique name. When ports is empty, it indicates
        that there are no defined ports. When a port is defined with a nil port value,
        it indicates "all ports". Each slice may include a maximum of 100 ports.
    """
    addressType: 'str'
    endpoints: 'List[Endpoint]'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    ports: 'List[EndpointPort]' = None


@dataclass
class EndpointSliceList(DataclassDictMixIn):
    """EndpointSliceList represents a list of endpoint slices

      **parameters**

      * **items** ``List[EndpointSlice]`` - List of endpoint slices
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ListMeta`` - *(optional)* Standard list metadata.
    """
    items: 'List[EndpointSlice]'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ListMeta' = None


