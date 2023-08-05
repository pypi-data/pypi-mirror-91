# autogenerated module
from dataclasses import dataclass, field
from typing import List

from ..core.dataclasses_dict import DataclassDictMixIn

from typing import Dict
from . import meta_v1


@dataclass
class ServerStorageVersion(DataclassDictMixIn):
    """An API server instance reports the version it can decode and the version it
      encodes objects to when persisting objects in the backend.

      **parameters**

      * **apiServerID** ``str`` - *(optional)* The ID of the reporting API server.
      * **decodableVersions** ``List[str]`` - *(optional)* The API server can decode objects encoded in these versions. The
        encodingVersion must be included in the decodableVersions.
      * **encodingVersion** ``str`` - *(optional)* The API server encodes the object to this version when persisting it in the
        backend (e.g., etcd).
    """
    apiServerID: 'str' = None
    decodableVersions: 'List[str]' = None
    encodingVersion: 'str' = None


@dataclass
class StorageVersion(DataclassDictMixIn):
    """
       Storage version of a specific resource.

      **parameters**

      * **spec** ``StorageVersionSpec`` - Spec is an empty spec. It is here to comply with Kubernetes API style.
      * **status** ``StorageVersionStatus`` - API server instances report the version they can decode and the version they
        encode objects to when persisting objects in the backend.
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* The name is <group>.<resource>.
    """
    spec: 'StorageVersionSpec'
    status: 'StorageVersionStatus'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None


@dataclass
class StorageVersionCondition(DataclassDictMixIn):
    """Describes the state of the storageVersion at a certain point.

      **parameters**

      * **reason** ``str`` - The reason for the condition's last transition.
      * **status** ``str`` - Status of the condition, one of True, False, Unknown.
      * **type** ``str`` - Type of the condition.
      * **lastTransitionTime** ``meta_v1.Time`` - *(optional)* Last time the condition transitioned from one status to another.
      * **message** ``str`` - *(optional)* A human readable message indicating details about the transition.
      * **observedGeneration** ``int`` - *(optional)* If set, this represents the .metadata.generation that the condition was set
        based upon.
    """
    reason: 'str'
    status: 'str'
    type: 'str'
    lastTransitionTime: 'meta_v1.Time' = None
    message: 'str' = None
    observedGeneration: 'int' = None


@dataclass
class StorageVersionList(DataclassDictMixIn):
    """A list of StorageVersions.

      **parameters**

      * **items** ``List[StorageVersion]`` - 
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ListMeta`` - *(optional)* 
    """
    items: 'List[StorageVersion]'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ListMeta' = None


StorageVersionSpec = Dict


@dataclass
class StorageVersionStatus(DataclassDictMixIn):
    """API server instances report the versions they can decode and the version they
      encode objects to when persisting objects in the backend.

      **parameters**

      * **commonEncodingVersion** ``str`` - *(optional)* If all API server instances agree on the same encoding storage version, then
        this field is set to that version. Otherwise this field is left empty. API
        servers should finish updating its storageVersionStatus entry before serving
        write operations, so that this field will be in sync with the reality.
      * **conditions** ``List[StorageVersionCondition]`` - *(optional)* The latest available observations of the storageVersion's state.
      * **storageVersions** ``List[ServerStorageVersion]`` - *(optional)* The reported versions per API server instance.
    """
    commonEncodingVersion: 'str' = None
    conditions: 'List[StorageVersionCondition]' = None
    storageVersions: 'List[ServerStorageVersion]' = None


