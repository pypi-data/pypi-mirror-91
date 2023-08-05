# autogenerated module
from dataclasses import dataclass, field
from typing import List

from ..core.dataclasses_dict import DataclassDictMixIn

from . import meta_v1


@dataclass
class Lease(DataclassDictMixIn):
    """Lease defines a lease concept.

      **parameters**

      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
      * **spec** ``LeaseSpec`` - *(optional)* Specification of the Lease. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
    """
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    spec: 'LeaseSpec' = None


@dataclass
class LeaseList(DataclassDictMixIn):
    """LeaseList is a list of Lease objects.

      **parameters**

      * **items** ``List[Lease]`` - Items is a list of schema objects.
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ListMeta`` - *(optional)* Standard list metadata. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
    """
    items: 'List[Lease]'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ListMeta' = None


@dataclass
class LeaseSpec(DataclassDictMixIn):
    """LeaseSpec is a specification of a Lease.

      **parameters**

      * **acquireTime** ``meta_v1.MicroTime`` - *(optional)* acquireTime is a time when the current lease was acquired.
      * **holderIdentity** ``str`` - *(optional)* holderIdentity contains the identity of the holder of a current lease.
      * **leaseDurationSeconds** ``int`` - *(optional)* leaseDurationSeconds is a duration that candidates for a lease need to wait to
        force acquire it. This is measure against time of last observed RenewTime.
      * **leaseTransitions** ``int`` - *(optional)* leaseTransitions is the number of transitions of a lease between holders.
      * **renewTime** ``meta_v1.MicroTime`` - *(optional)* renewTime is a time when the current holder of a lease has last updated the
        lease.
    """
    acquireTime: 'meta_v1.MicroTime' = None
    holderIdentity: 'str' = None
    leaseDurationSeconds: 'int' = None
    leaseTransitions: 'int' = None
    renewTime: 'meta_v1.MicroTime' = None


