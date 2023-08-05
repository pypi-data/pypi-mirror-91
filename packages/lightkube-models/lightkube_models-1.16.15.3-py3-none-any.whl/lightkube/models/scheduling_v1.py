# autogenerated module
from dataclasses import dataclass, field
from typing import List

from ..core.dataclasses_dict import DataclassDictMixIn

from . import meta_v1


@dataclass
class PriorityClass(DataclassDictMixIn):
    """PriorityClass defines mapping from a priority class name to the priority
      integer value. The value can be any valid integer.

      **parameters**

      * **value** ``int`` - The value of this priority class. This is the actual priority that pods
        receive when they have the name of this class in their pod spec.
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **description** ``str`` - *(optional)* description is an arbitrary string that usually provides guidelines on when
        this priority class should be used.
      * **globalDefault** ``bool`` - *(optional)* globalDefault specifies whether this PriorityClass should be considered as the
        default priority for pods that do not have any priority class. Only one
        PriorityClass can be marked as `globalDefault`. However, if more than one
        PriorityClasses exists with their `globalDefault` field set to true, the
        smallest value of such global default PriorityClasses will be used as the
        default priority.
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* Standard object's metadata. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
      * **preemptionPolicy** ``str`` - *(optional)* PreemptionPolicy is the Policy for preempting pods with lower priority. One of
        Never, PreemptLowerPriority. Defaults to PreemptLowerPriority if unset. This
        field is alpha-level and is only honored by servers that enable the
        NonPreemptingPriority feature.
    """
    value: 'int'
    apiVersion: 'str' = None
    description: 'str' = None
    globalDefault: 'bool' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    preemptionPolicy: 'str' = None


@dataclass
class PriorityClassList(DataclassDictMixIn):
    """PriorityClassList is a collection of priority classes.

      **parameters**

      * **items** ``List[PriorityClass]`` - items is the list of PriorityClasses
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ListMeta`` - *(optional)* Standard list metadata More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
    """
    items: 'List[PriorityClass]'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ListMeta' = None


