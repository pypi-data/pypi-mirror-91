# autogenerated module
from dataclasses import dataclass, field
from typing import List

from ..core.dataclasses_dict import DataclassDictMixIn

from . import resource
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
class ExternalMetricSource(DataclassDictMixIn):
    """ExternalMetricSource indicates how to scale on a metric not associated with
      any Kubernetes object (for example length of queue in cloud messaging service,
      or QPS from loadbalancer running outside of cluster).

      **parameters**

      * **metric** ``MetricIdentifier`` - metric identifies the target metric by name and selector
      * **target** ``MetricTarget`` - target specifies the target value for the given metric
    """
    metric: 'MetricIdentifier'
    target: 'MetricTarget'


@dataclass
class ExternalMetricStatus(DataclassDictMixIn):
    """ExternalMetricStatus indicates the current value of a global metric not
      associated with any Kubernetes object.

      **parameters**

      * **current** ``MetricValueStatus`` - current contains the current value for the given metric
      * **metric** ``MetricIdentifier`` - metric identifies the target metric by name and selector
    """
    current: 'MetricValueStatus'
    metric: 'MetricIdentifier'


@dataclass
class HorizontalPodAutoscaler(DataclassDictMixIn):
    """HorizontalPodAutoscaler is the configuration for a horizontal pod autoscaler,
      which automatically manages the replica count of any resource implementing the
      scale subresource based on the metrics specified.

      **parameters**

      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* metadata is the standard object metadata. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
      * **spec** ``HorizontalPodAutoscalerSpec`` - *(optional)* spec is the specification for the behaviour of the autoscaler. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status.
      * **status** ``HorizontalPodAutoscalerStatus`` - *(optional)* status is the current information about the autoscaler.
    """
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    spec: 'HorizontalPodAutoscalerSpec' = None
    status: 'HorizontalPodAutoscalerStatus' = None


@dataclass
class HorizontalPodAutoscalerCondition(DataclassDictMixIn):
    """HorizontalPodAutoscalerCondition describes the state of a
      HorizontalPodAutoscaler at a certain point.

      **parameters**

      * **status** ``str`` - status is the status of the condition (True, False, Unknown)
      * **type** ``str`` - type describes the current condition
      * **lastTransitionTime** ``meta_v1.Time`` - *(optional)* lastTransitionTime is the last time the condition transitioned from one status
        to another
      * **message** ``str`` - *(optional)* message is a human-readable explanation containing details about the
        transition
      * **reason** ``str`` - *(optional)* reason is the reason for the condition's last transition.
    """
    status: 'str'
    type: 'str'
    lastTransitionTime: 'meta_v1.Time' = None
    message: 'str' = None
    reason: 'str' = None


@dataclass
class HorizontalPodAutoscalerList(DataclassDictMixIn):
    """HorizontalPodAutoscalerList is a list of horizontal pod autoscaler objects.

      **parameters**

      * **items** ``List[HorizontalPodAutoscaler]`` - items is the list of horizontal pod autoscaler objects.
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ListMeta`` - *(optional)* metadata is the standard list metadata.
    """
    items: 'List[HorizontalPodAutoscaler]'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ListMeta' = None


@dataclass
class HorizontalPodAutoscalerSpec(DataclassDictMixIn):
    """HorizontalPodAutoscalerSpec describes the desired functionality of the
      HorizontalPodAutoscaler.

      **parameters**

      * **maxReplicas** ``int`` - maxReplicas is the upper limit for the number of replicas to which the
        autoscaler can scale up. It cannot be less that minReplicas.
      * **scaleTargetRef** ``CrossVersionObjectReference`` - scaleTargetRef points to the target resource to scale, and is used to the pods
        for which metrics should be collected, as well as to actually change the
        replica count.
      * **metrics** ``List[MetricSpec]`` - *(optional)* metrics contains the specifications for which to use to calculate the desired
        replica count (the maximum replica count across all metrics will be used).
        The desired replica count is calculated multiplying the ratio between the
        target value and the current value by the current number of pods.  Ergo,
        metrics used must decrease as the pod count is increased, and vice-versa.  See
        the individual metric source types for more information about how each type of
        metric must respond. If not set, the default metric will be set to 80% average
        CPU utilization.
      * **minReplicas** ``int`` - *(optional)* minReplicas is the lower limit for the number of replicas to which the
        autoscaler can scale down.  It defaults to 1 pod.  minReplicas is allowed to
        be 0 if the alpha feature gate HPAScaleToZero is enabled and at least one
        Object or External metric is configured.  Scaling is active as long as at
        least one metric value is available.
    """
    maxReplicas: 'int'
    scaleTargetRef: 'CrossVersionObjectReference'
    metrics: 'List[MetricSpec]' = None
    minReplicas: 'int' = None


@dataclass
class HorizontalPodAutoscalerStatus(DataclassDictMixIn):
    """HorizontalPodAutoscalerStatus describes the current status of a horizontal pod
      autoscaler.

      **parameters**

      * **conditions** ``List[HorizontalPodAutoscalerCondition]`` - conditions is the set of conditions required for this autoscaler to scale its
        target, and indicates whether or not those conditions are met.
      * **currentReplicas** ``int`` - currentReplicas is current number of replicas of pods managed by this
        autoscaler, as last seen by the autoscaler.
      * **desiredReplicas** ``int`` - desiredReplicas is the desired number of replicas of pods managed by this
        autoscaler, as last calculated by the autoscaler.
      * **currentMetrics** ``List[MetricStatus]`` - *(optional)* currentMetrics is the last read state of the metrics used by this autoscaler.
      * **lastScaleTime** ``meta_v1.Time`` - *(optional)* lastScaleTime is the last time the HorizontalPodAutoscaler scaled the number
        of pods, used by the autoscaler to control how often the number of pods is
        changed.
      * **observedGeneration** ``int`` - *(optional)* observedGeneration is the most recent generation observed by this autoscaler.
    """
    conditions: 'List[HorizontalPodAutoscalerCondition]'
    currentReplicas: 'int'
    desiredReplicas: 'int'
    currentMetrics: 'List[MetricStatus]' = None
    lastScaleTime: 'meta_v1.Time' = None
    observedGeneration: 'int' = None


@dataclass
class MetricIdentifier(DataclassDictMixIn):
    """MetricIdentifier defines the name and optionally selector for a metric

      **parameters**

      * **name** ``str`` - name is the name of the given metric
      * **selector** ``meta_v1.LabelSelector`` - *(optional)* selector is the string-encoded form of a standard kubernetes label selector
        for the given metric When set, it is passed as an additional parameter to the
        metrics server for more specific metrics scoping. When unset, just the
        metricName will be used to gather metrics.
    """
    name: 'str'
    selector: 'meta_v1.LabelSelector' = None


@dataclass
class MetricSpec(DataclassDictMixIn):
    """MetricSpec specifies how to scale based on a single metric (only `type` and
      one other matching field should be set at once).

      **parameters**

      * **type** ``str`` - type is the type of metric source.  It should be one of "Object", "Pods" or
        "Resource", each mapping to a matching field in the object.
      * **external** ``ExternalMetricSource`` - *(optional)* external refers to a global metric that is not associated with any Kubernetes
        object. It allows autoscaling based on information coming from components
        running outside of cluster (for example length of queue in cloud messaging
        service, or QPS from loadbalancer running outside of cluster).
      * **object** ``ObjectMetricSource`` - *(optional)* object refers to a metric describing a single kubernetes object (for example,
        hits-per-second on an Ingress object).
      * **pods** ``PodsMetricSource`` - *(optional)* pods refers to a metric describing each pod in the current scale target (for
        example, transactions-processed-per-second).  The values will be averaged
        together before being compared to the target value.
      * **resource** ``ResourceMetricSource`` - *(optional)* resource refers to a resource metric (such as those specified in requests and
        limits) known to Kubernetes describing each pod in the current scale target
        (e.g. CPU or memory). Such metrics are built in to Kubernetes, and have
        special scaling options on top of those available to normal per-pod metrics
        using the "pods" source.
    """
    type: 'str'
    external: 'ExternalMetricSource' = None
    object: 'ObjectMetricSource' = None
    pods: 'PodsMetricSource' = None
    resource: 'ResourceMetricSource' = None


@dataclass
class MetricStatus(DataclassDictMixIn):
    """MetricStatus describes the last-read state of a single metric.

      **parameters**

      * **type** ``str`` - type is the type of metric source.  It will be one of "Object", "Pods" or
        "Resource", each corresponds to a matching field in the object.
      * **external** ``ExternalMetricStatus`` - *(optional)* external refers to a global metric that is not associated with any Kubernetes
        object. It allows autoscaling based on information coming from components
        running outside of cluster (for example length of queue in cloud messaging
        service, or QPS from loadbalancer running outside of cluster).
      * **object** ``ObjectMetricStatus`` - *(optional)* object refers to a metric describing a single kubernetes object (for example,
        hits-per-second on an Ingress object).
      * **pods** ``PodsMetricStatus`` - *(optional)* pods refers to a metric describing each pod in the current scale target (for
        example, transactions-processed-per-second).  The values will be averaged
        together before being compared to the target value.
      * **resource** ``ResourceMetricStatus`` - *(optional)* resource refers to a resource metric (such as those specified in requests and
        limits) known to Kubernetes describing each pod in the current scale target
        (e.g. CPU or memory). Such metrics are built in to Kubernetes, and have
        special scaling options on top of those available to normal per-pod metrics
        using the "pods" source.
    """
    type: 'str'
    external: 'ExternalMetricStatus' = None
    object: 'ObjectMetricStatus' = None
    pods: 'PodsMetricStatus' = None
    resource: 'ResourceMetricStatus' = None


@dataclass
class MetricTarget(DataclassDictMixIn):
    """MetricTarget defines the target value, average value, or average utilization
      of a specific metric

      **parameters**

      * **type** ``str`` - type represents whether the metric type is Utilization, Value, or AverageValue
      * **averageUtilization** ``int`` - *(optional)* averageUtilization is the target value of the average of the resource metric
        across all relevant pods, represented as a percentage of the requested value
        of the resource for the pods. Currently only valid for Resource metric source
        type
      * **averageValue** ``resource.Quantity`` - *(optional)* averageValue is the target value of the average of the metric across all
        relevant pods (as a quantity)
      * **value** ``resource.Quantity`` - *(optional)* value is the target value of the metric (as a quantity).
    """
    type: 'str'
    averageUtilization: 'int' = None
    averageValue: 'resource.Quantity' = None
    value: 'resource.Quantity' = None


@dataclass
class MetricValueStatus(DataclassDictMixIn):
    """MetricValueStatus holds the current value for a metric

      **parameters**

      * **averageUtilization** ``int`` - *(optional)* currentAverageUtilization is the current value of the average of the resource
        metric across all relevant pods, represented as a percentage of the requested
        value of the resource for the pods.
      * **averageValue** ``resource.Quantity`` - *(optional)* averageValue is the current value of the average of the metric across all
        relevant pods (as a quantity)
      * **value** ``resource.Quantity`` - *(optional)* value is the current value of the metric (as a quantity).
    """
    averageUtilization: 'int' = None
    averageValue: 'resource.Quantity' = None
    value: 'resource.Quantity' = None


@dataclass
class ObjectMetricSource(DataclassDictMixIn):
    """ObjectMetricSource indicates how to scale on a metric describing a kubernetes
      object (for example, hits-per-second on an Ingress object).

      **parameters**

      * **describedObject** ``CrossVersionObjectReference`` - 
      * **metric** ``MetricIdentifier`` - metric identifies the target metric by name and selector
      * **target** ``MetricTarget`` - target specifies the target value for the given metric
    """
    describedObject: 'CrossVersionObjectReference'
    metric: 'MetricIdentifier'
    target: 'MetricTarget'


@dataclass
class ObjectMetricStatus(DataclassDictMixIn):
    """ObjectMetricStatus indicates the current value of a metric describing a
      kubernetes object (for example, hits-per-second on an Ingress object).

      **parameters**

      * **current** ``MetricValueStatus`` - current contains the current value for the given metric
      * **describedObject** ``CrossVersionObjectReference`` - 
      * **metric** ``MetricIdentifier`` - metric identifies the target metric by name and selector
    """
    current: 'MetricValueStatus'
    describedObject: 'CrossVersionObjectReference'
    metric: 'MetricIdentifier'


@dataclass
class PodsMetricSource(DataclassDictMixIn):
    """PodsMetricSource indicates how to scale on a metric describing each pod in the
      current scale target (for example, transactions-processed-per-second). The
      values will be averaged together before being compared to the target value.

      **parameters**

      * **metric** ``MetricIdentifier`` - metric identifies the target metric by name and selector
      * **target** ``MetricTarget`` - target specifies the target value for the given metric
    """
    metric: 'MetricIdentifier'
    target: 'MetricTarget'


@dataclass
class PodsMetricStatus(DataclassDictMixIn):
    """PodsMetricStatus indicates the current value of a metric describing each pod
      in the current scale target (for example, transactions-processed-per-second).

      **parameters**

      * **current** ``MetricValueStatus`` - current contains the current value for the given metric
      * **metric** ``MetricIdentifier`` - metric identifies the target metric by name and selector
    """
    current: 'MetricValueStatus'
    metric: 'MetricIdentifier'


@dataclass
class ResourceMetricSource(DataclassDictMixIn):
    """ResourceMetricSource indicates how to scale on a resource metric known to
      Kubernetes, as specified in requests and limits, describing each pod in the
      current scale target (e.g. CPU or memory).  The values will be averaged
      together before being compared to the target.  Such metrics are built in to
      Kubernetes, and have special scaling options on top of those available to
      normal per-pod metrics using the "pods" source.  Only one "target" type should
      be set.

      **parameters**

      * **name** ``str`` - name is the name of the resource in question.
      * **target** ``MetricTarget`` - target specifies the target value for the given metric
    """
    name: 'str'
    target: 'MetricTarget'


@dataclass
class ResourceMetricStatus(DataclassDictMixIn):
    """ResourceMetricStatus indicates the current value of a resource metric known to
      Kubernetes, as specified in requests and limits, describing each pod in the
      current scale target (e.g. CPU or memory).  Such metrics are built in to
      Kubernetes, and have special scaling options on top of those available to
      normal per-pod metrics using the "pods" source.

      **parameters**

      * **current** ``MetricValueStatus`` - current contains the current value for the given metric
      * **name** ``str`` - Name is the name of the resource in question.
    """
    current: 'MetricValueStatus'
    name: 'str'


