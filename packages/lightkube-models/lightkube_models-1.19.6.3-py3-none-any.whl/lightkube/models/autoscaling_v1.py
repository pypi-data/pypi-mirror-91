# autogenerated module
from dataclasses import dataclass, field
from typing import List

from ..core.dataclasses_dict import DataclassDictMixIn

from . import meta_v1


@dataclass
class CrossVersionObjectReference(DataclassDictMixIn):
    """CrossVersionObjectReference contains enough information to let you identify
      the referred resource.

      **parameters**

      * **kind** ``str`` - Kind of the referent; More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds"
      * **name** ``str`` - Name of the referent; More info:
        http://kubernetes.io/docs/user-guide/identifiers#names
      * **apiVersion** ``str`` - *(optional)* API version of the referent
    """
    kind: 'str'
    name: 'str'
    apiVersion: 'str' = None


@dataclass
class HorizontalPodAutoscaler(DataclassDictMixIn):
    """configuration of a horizontal pod autoscaler.

      **parameters**

      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* Standard object metadata. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
      * **spec** ``HorizontalPodAutoscalerSpec`` - *(optional)* behaviour of autoscaler. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status.
      * **status** ``HorizontalPodAutoscalerStatus`` - *(optional)* current information about the autoscaler.
    """
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    spec: 'HorizontalPodAutoscalerSpec' = None
    status: 'HorizontalPodAutoscalerStatus' = None


@dataclass
class HorizontalPodAutoscalerList(DataclassDictMixIn):
    """list of horizontal pod autoscaler objects.

      **parameters**

      * **items** ``List[HorizontalPodAutoscaler]`` - list of horizontal pod autoscaler objects.
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
    items: 'List[HorizontalPodAutoscaler]'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ListMeta' = None


@dataclass
class HorizontalPodAutoscalerSpec(DataclassDictMixIn):
    """specification of a horizontal pod autoscaler.

      **parameters**

      * **maxReplicas** ``int`` - upper limit for the number of pods that can be set by the autoscaler; cannot
        be smaller than MinReplicas.
      * **scaleTargetRef** ``CrossVersionObjectReference`` - reference to scaled resource; horizontal pod autoscaler will learn the current
        resource consumption and will set the desired number of pods by using its
        Scale subresource.
      * **minReplicas** ``int`` - *(optional)* minReplicas is the lower limit for the number of replicas to which the
        autoscaler can scale down.  It defaults to 1 pod.  minReplicas is allowed to
        be 0 if the alpha feature gate HPAScaleToZero is enabled and at least one
        Object or External metric is configured.  Scaling is active as long as at
        least one metric value is available.
      * **targetCPUUtilizationPercentage** ``int`` - *(optional)* target average CPU utilization (represented as a percentage of requested CPU)
        over all the pods; if not specified the default autoscaling policy will be
        used.
    """
    maxReplicas: 'int'
    scaleTargetRef: 'CrossVersionObjectReference'
    minReplicas: 'int' = None
    targetCPUUtilizationPercentage: 'int' = None


@dataclass
class HorizontalPodAutoscalerStatus(DataclassDictMixIn):
    """current status of a horizontal pod autoscaler

      **parameters**

      * **currentReplicas** ``int`` - current number of replicas of pods managed by this autoscaler.
      * **desiredReplicas** ``int`` - desired number of replicas of pods managed by this autoscaler.
      * **currentCPUUtilizationPercentage** ``int`` - *(optional)* current average CPU utilization over all pods, represented as a percentage of
        requested CPU, e.g. 70 means that an average pod is using now 70% of its
        requested CPU.
      * **lastScaleTime** ``meta_v1.Time`` - *(optional)* last time the HorizontalPodAutoscaler scaled the number of pods; used by the
        autoscaler to control how often the number of pods is changed.
      * **observedGeneration** ``int`` - *(optional)* most recent generation observed by this autoscaler.
    """
    currentReplicas: 'int'
    desiredReplicas: 'int'
    currentCPUUtilizationPercentage: 'int' = None
    lastScaleTime: 'meta_v1.Time' = None
    observedGeneration: 'int' = None


@dataclass
class Scale(DataclassDictMixIn):
    """Scale represents a scaling request for a resource.

      **parameters**

      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* Standard object metadata; More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.
      * **spec** ``ScaleSpec`` - *(optional)* defines the behavior of the scale. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status.
      * **status** ``ScaleStatus`` - *(optional)* current status of the scale. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status.
        Read-only.
    """
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    spec: 'ScaleSpec' = None
    status: 'ScaleStatus' = None


@dataclass
class ScaleSpec(DataclassDictMixIn):
    """ScaleSpec describes the attributes of a scale subresource.

      **parameters**

      * **replicas** ``int`` - *(optional)* desired number of instances for the scaled object.
    """
    replicas: 'int' = None


@dataclass
class ScaleStatus(DataclassDictMixIn):
    """ScaleStatus represents the current status of a scale subresource.

      **parameters**

      * **replicas** ``int`` - actual number of observed instances of the scaled object.
      * **selector** ``str`` - *(optional)* label query over pods that should match the replicas count. This is same as
        the label selector but in the string format to avoid introspection by clients.
        The string will be in the same format as the query-param syntax. More info
        about label selectors:
        http://kubernetes.io/docs/user-guide/labels#label-selectors
    """
    replicas: 'int'
    selector: 'str' = None


