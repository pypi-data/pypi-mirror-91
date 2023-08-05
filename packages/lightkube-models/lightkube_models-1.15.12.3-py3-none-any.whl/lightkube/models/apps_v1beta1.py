# autogenerated module
from dataclasses import dataclass, field
from typing import List

from ..core.dataclasses_dict import DataclassDictMixIn

from . import core_v1
from . import runtime
from . import util_intstr
from . import meta_v1


@dataclass
class ControllerRevision(DataclassDictMixIn):
    """DEPRECATED - This group version of ControllerRevision is deprecated by
      apps/v1beta2/ControllerRevision. See the release notes for more information.
      ControllerRevision implements an immutable snapshot of state data. Clients are
      responsible for serializing and deserializing the objects that contain their
      internal state. Once a ControllerRevision has been successfully created, it
      can not be updated. The API Server will fail validation of all requests that
      attempt to mutate the Data field. ControllerRevisions may, however, be
      deleted. Note that, due to its use by both the DaemonSet and StatefulSet
      controllers for update and rollback, this object is beta. However, it may be
      subject to name and representation changes in future releases, and clients
      should not depend on its stability. It is primarily for internal use by
      controllers.

      **parameters**

      * **revision** ``int`` - Revision indicates the revision of the state represented by Data.
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#resources
      * **data** ``runtime.RawExtension`` - *(optional)* Data is the serialized representation of the state.
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* Standard object's metadata. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#metadata
    """
    revision: 'int'
    apiVersion: 'str' = None
    data: 'runtime.RawExtension' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None


@dataclass
class ControllerRevisionList(DataclassDictMixIn):
    """ControllerRevisionList is a resource containing a list of ControllerRevision
      objects.

      **parameters**

      * **items** ``List[ControllerRevision]`` - Items is the list of ControllerRevisions
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ListMeta`` - *(optional)* More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#metadata
    """
    items: 'List[ControllerRevision]'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ListMeta' = None


@dataclass
class Deployment(DataclassDictMixIn):
    """DEPRECATED - This group version of Deployment is deprecated by
      apps/v1beta2/Deployment. See the release notes for more information.
      Deployment enables declarative updates for Pods and ReplicaSets.

      **parameters**

      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* Standard object metadata.
      * **spec** ``DeploymentSpec`` - *(optional)* Specification of the desired behavior of the Deployment.
      * **status** ``DeploymentStatus`` - *(optional)* Most recently observed status of the Deployment.
    """
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    spec: 'DeploymentSpec' = None
    status: 'DeploymentStatus' = None


@dataclass
class DeploymentCondition(DataclassDictMixIn):
    """DeploymentCondition describes the state of a deployment at a certain point.

      **parameters**

      * **status** ``str`` - Status of the condition, one of True, False, Unknown.
      * **type** ``str`` - Type of deployment condition.
      * **lastTransitionTime** ``meta_v1.Time`` - *(optional)* Last time the condition transitioned from one status to another.
      * **lastUpdateTime** ``meta_v1.Time`` - *(optional)* The last time this condition was updated.
      * **message** ``str`` - *(optional)* A human readable message indicating details about the transition.
      * **reason** ``str`` - *(optional)* The reason for the condition's last transition.
    """
    status: 'str'
    type: 'str'
    lastTransitionTime: 'meta_v1.Time' = None
    lastUpdateTime: 'meta_v1.Time' = None
    message: 'str' = None
    reason: 'str' = None


@dataclass
class DeploymentList(DataclassDictMixIn):
    """DeploymentList is a list of Deployments.

      **parameters**

      * **items** ``List[Deployment]`` - Items is the list of Deployments.
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ListMeta`` - *(optional)* Standard list metadata.
    """
    items: 'List[Deployment]'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ListMeta' = None


@dataclass
class DeploymentRollback(DataclassDictMixIn):
    """DEPRECATED. DeploymentRollback stores the information required to rollback a
      deployment.

      **parameters**

      * **name** ``str`` - Required: This must match the Name of a deployment.
      * **rollbackTo** ``RollbackConfig`` - The config of this deployment rollback.
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds
      * **updatedAnnotations** ``dict`` - *(optional)* The annotations to be updated to a deployment
    """
    name: 'str'
    rollbackTo: 'RollbackConfig'
    apiVersion: 'str' = None
    kind: 'str' = None
    updatedAnnotations: 'dict' = None


@dataclass
class DeploymentSpec(DataclassDictMixIn):
    """DeploymentSpec is the specification of the desired behavior of the Deployment.

      **parameters**

      * **template** ``core_v1.PodTemplateSpec`` - Template describes the pods that will be created.
      * **minReadySeconds** ``int`` - *(optional)* Minimum number of seconds for which a newly created pod should be ready
        without any of its container crashing, for it to be considered available.
        Defaults to 0 (pod will be considered available as soon as it is ready)
      * **paused** ``bool`` - *(optional)* Indicates that the deployment is paused.
      * **progressDeadlineSeconds** ``int`` - *(optional)* The maximum time in seconds for a deployment to make progress before it is
        considered to be failed. The deployment controller will continue to process
        failed deployments and a condition with a ProgressDeadlineExceeded reason will
        be surfaced in the deployment status. Note that progress will not be estimated
        during the time a deployment is paused. Defaults to 600s.
      * **replicas** ``int`` - *(optional)* Number of desired pods. This is a pointer to distinguish between explicit zero
        and not specified. Defaults to 1.
      * **revisionHistoryLimit** ``int`` - *(optional)* The number of old ReplicaSets to retain to allow rollback. This is a pointer
        to distinguish between explicit zero and not specified. Defaults to 2.
      * **rollbackTo** ``RollbackConfig`` - *(optional)* DEPRECATED. The config this deployment is rolling back to. Will be cleared
        after rollback is done.
      * **selector** ``meta_v1.LabelSelector`` - *(optional)* Label selector for pods. Existing ReplicaSets whose pods are selected by this
        will be the ones affected by this deployment.
      * **strategy** ``DeploymentStrategy`` - *(optional)* The deployment strategy to use to replace existing pods with new ones.
    """
    template: 'core_v1.PodTemplateSpec'
    minReadySeconds: 'int' = None
    paused: 'bool' = None
    progressDeadlineSeconds: 'int' = None
    replicas: 'int' = None
    revisionHistoryLimit: 'int' = None
    rollbackTo: 'RollbackConfig' = None
    selector: 'meta_v1.LabelSelector' = None
    strategy: 'DeploymentStrategy' = None


@dataclass
class DeploymentStatus(DataclassDictMixIn):
    """DeploymentStatus is the most recently observed status of the Deployment.

      **parameters**

      * **availableReplicas** ``int`` - *(optional)* Total number of available pods (ready for at least minReadySeconds) targeted
        by this deployment.
      * **collisionCount** ``int`` - *(optional)* Count of hash collisions for the Deployment. The Deployment controller uses
        this field as a collision avoidance mechanism when it needs to create the name
        for the newest ReplicaSet.
      * **conditions** ``List[DeploymentCondition]`` - *(optional)* Represents the latest available observations of a deployment's current state.
      * **observedGeneration** ``int`` - *(optional)* The generation observed by the deployment controller.
      * **readyReplicas** ``int`` - *(optional)* Total number of ready pods targeted by this deployment.
      * **replicas** ``int`` - *(optional)* Total number of non-terminated pods targeted by this deployment (their labels
        match the selector).
      * **unavailableReplicas** ``int`` - *(optional)* Total number of unavailable pods targeted by this deployment. This is the
        total number of pods that are still required for the deployment to have 100%
        available capacity. They may either be pods that are running but not yet
        available or pods that still have not been created.
      * **updatedReplicas** ``int`` - *(optional)* Total number of non-terminated pods targeted by this deployment that have the
        desired template spec.
    """
    availableReplicas: 'int' = None
    collisionCount: 'int' = None
    conditions: 'List[DeploymentCondition]' = None
    observedGeneration: 'int' = None
    readyReplicas: 'int' = None
    replicas: 'int' = None
    unavailableReplicas: 'int' = None
    updatedReplicas: 'int' = None


@dataclass
class DeploymentStrategy(DataclassDictMixIn):
    """DeploymentStrategy describes how to replace existing pods with new ones.

      **parameters**

      * **rollingUpdate** ``RollingUpdateDeployment`` - *(optional)* Rolling update config params. Present only if DeploymentStrategyType =
        RollingUpdate.
      * **type** ``str`` - *(optional)* Type of deployment. Can be "Recreate" or "RollingUpdate". Default is
        RollingUpdate.
    """
    rollingUpdate: 'RollingUpdateDeployment' = None
    type: 'str' = None


@dataclass
class RollbackConfig(DataclassDictMixIn):
    """DEPRECATED.

      **parameters**

      * **revision** ``int`` - *(optional)* The revision to rollback to. If set to 0, rollback to the last revision.
    """
    revision: 'int' = None


@dataclass
class RollingUpdateDeployment(DataclassDictMixIn):
    """Spec to control the desired behavior of rolling update.

      **parameters**

      * **maxSurge** ``util_intstr.IntOrString`` - *(optional)* The maximum number of pods that can be scheduled above the desired number of
        pods. Value can be an absolute number (ex: 5) or a percentage of desired pods
        (ex: 10%). This can not be 0 if MaxUnavailable is 0. Absolute number is
        calculated from percentage by rounding up. Defaults to 25%. Example: when this
        is set to 30%, the new ReplicaSet can be scaled up immediately when the
        rolling update starts, such that the total number of old and new pods do not
        exceed 130% of desired pods. Once old pods have been killed, new ReplicaSet
        can be scaled up further, ensuring that total number of pods running at any
        time during the update is at most 130% of desired pods.
      * **maxUnavailable** ``util_intstr.IntOrString`` - *(optional)* The maximum number of pods that can be unavailable during the update. Value
        can be an absolute number (ex: 5) or a percentage of desired pods (ex: 10%).
        Absolute number is calculated from percentage by rounding down. This can not
        be 0 if MaxSurge is 0. Defaults to 25%. Example: when this is set to 30%, the
        old ReplicaSet can be scaled down to 70% of desired pods immediately when the
        rolling update starts. Once new pods are ready, old ReplicaSet can be scaled
        down further, followed by scaling up the new ReplicaSet, ensuring that the
        total number of pods available at all times during the update is at least 70%
        of desired pods.
    """
    maxSurge: 'util_intstr.IntOrString' = None
    maxUnavailable: 'util_intstr.IntOrString' = None


@dataclass
class RollingUpdateStatefulSetStrategy(DataclassDictMixIn):
    """RollingUpdateStatefulSetStrategy is used to communicate parameter for
      RollingUpdateStatefulSetStrategyType.

      **parameters**

      * **partition** ``int`` - *(optional)* Partition indicates the ordinal at which the StatefulSet should be
        partitioned.
    """
    partition: 'int' = None


@dataclass
class Scale(DataclassDictMixIn):
    """Scale represents a scaling request for a resource.

      **parameters**

      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* Standard object metadata; More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#metadata.
      * **spec** ``ScaleSpec`` - *(optional)* defines the behavior of the scale. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#spec-and-status.
      * **status** ``ScaleStatus`` - *(optional)* current status of the scale. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#spec-and-status.
        Read-only.
    """
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    spec: 'ScaleSpec' = None
    status: 'ScaleStatus' = None


@dataclass
class ScaleSpec(DataclassDictMixIn):
    """ScaleSpec describes the attributes of a scale subresource

      **parameters**

      * **replicas** ``int`` - *(optional)* desired number of instances for the scaled object.
    """
    replicas: 'int' = None


@dataclass
class ScaleStatus(DataclassDictMixIn):
    """ScaleStatus represents the current status of a scale subresource.

      **parameters**

      * **replicas** ``int`` - actual number of observed instances of the scaled object.
      * **selector** ``dict`` - *(optional)* label query over pods that should match the replicas count. More info:
        http://kubernetes.io/docs/user-guide/labels#label-selectors
      * **targetSelector** ``str`` - *(optional)* label selector for pods that should match the replicas count. This is a
        serializated version of both map-based and more expressive set-based
        selectors. This is done to avoid introspection in the clients. The string will
        be in the same format as the query-param syntax. If the target type only
        supports map-based selectors, both this field and map-based selector field are
        populated. More info:
        https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors
    """
    replicas: 'int'
    selector: 'dict' = None
    targetSelector: 'str' = None


@dataclass
class StatefulSet(DataclassDictMixIn):
    """DEPRECATED - This group version of StatefulSet is deprecated by
      apps/v1beta2/StatefulSet. See the release notes for more information.
      StatefulSet represents a set of pods with consistent identities. Identities
      are defined as:
       - Network: A single stable DNS and hostname.
       - Storage: As many VolumeClaims as requested.
      The StatefulSet guarantees that a given network identity will always map to
      the same storage identity.

      **parameters**

      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* 
      * **spec** ``StatefulSetSpec`` - *(optional)* Spec defines the desired identities of pods in this set.
      * **status** ``StatefulSetStatus`` - *(optional)* Status is the current status of Pods in this StatefulSet. This data may be out
        of date by some window of time.
    """
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    spec: 'StatefulSetSpec' = None
    status: 'StatefulSetStatus' = None


@dataclass
class StatefulSetCondition(DataclassDictMixIn):
    """StatefulSetCondition describes the state of a statefulset at a certain point.

      **parameters**

      * **status** ``str`` - Status of the condition, one of True, False, Unknown.
      * **type** ``str`` - Type of statefulset condition.
      * **lastTransitionTime** ``meta_v1.Time`` - *(optional)* Last time the condition transitioned from one status to another.
      * **message** ``str`` - *(optional)* A human readable message indicating details about the transition.
      * **reason** ``str`` - *(optional)* The reason for the condition's last transition.
    """
    status: 'str'
    type: 'str'
    lastTransitionTime: 'meta_v1.Time' = None
    message: 'str' = None
    reason: 'str' = None


@dataclass
class StatefulSetList(DataclassDictMixIn):
    """StatefulSetList is a collection of StatefulSets.

      **parameters**

      * **items** ``List[StatefulSet]`` - 
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ListMeta`` - *(optional)* 
    """
    items: 'List[StatefulSet]'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ListMeta' = None


@dataclass
class StatefulSetSpec(DataclassDictMixIn):
    """A StatefulSetSpec is the specification of a StatefulSet.

      **parameters**

      * **serviceName** ``str`` - serviceName is the name of the service that governs this StatefulSet. This
        service must exist before the StatefulSet, and is responsible for the network
        identity of the set. Pods get DNS/hostnames that follow the pattern:
        pod-specific-string.serviceName.default.svc.cluster.local where
        "pod-specific-string" is managed by the StatefulSet controller.
      * **template** ``core_v1.PodTemplateSpec`` - template is the object that describes the pod that will be created if
        insufficient replicas are detected. Each pod stamped out by the StatefulSet
        will fulfill this Template, but have a unique identity from the rest of the
        StatefulSet.
      * **podManagementPolicy** ``str`` - *(optional)* podManagementPolicy controls how pods are created during initial scale up,
        when replacing pods on nodes, or when scaling down. The default policy is
        `OrderedReady`, where pods are created in increasing order (pod-0, then pod-1,
        etc) and the controller will wait until each pod is ready before continuing.
        When scaling down, the pods are removed in the opposite order. The alternative
        policy is `Parallel` which will create pods in parallel to match the desired
        scale without waiting, and on scale down will delete all pods at once.
      * **replicas** ``int`` - *(optional)* replicas is the desired number of replicas of the given Template. These are
        replicas in the sense that they are instantiations of the same Template, but
        individual replicas also have a consistent identity. If unspecified, defaults
        to 1.
      * **revisionHistoryLimit** ``int`` - *(optional)* revisionHistoryLimit is the maximum number of revisions that will be
        maintained in the StatefulSet's revision history. The revision history
        consists of all revisions not represented by a currently applied
        StatefulSetSpec version. The default value is 10.
      * **selector** ``meta_v1.LabelSelector`` - *(optional)* selector is a label query over pods that should match the replica count. If
        empty, defaulted to labels on the pod template. More info:
        https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/#label-selectors
      * **updateStrategy** ``StatefulSetUpdateStrategy`` - *(optional)* updateStrategy indicates the StatefulSetUpdateStrategy that will be employed
        to update Pods in the StatefulSet when a revision is made to Template.
      * **volumeClaimTemplates** ``List[core_v1.PersistentVolumeClaim]`` - *(optional)* volumeClaimTemplates is a list of claims that pods are allowed to reference.
        The StatefulSet controller is responsible for mapping network identities to
        claims in a way that maintains the identity of a pod. Every claim in this list
        must have at least one matching (by name) volumeMount in one container in the
        template. A claim in this list takes precedence over any volumes in the
        template, with the same name.
    """
    serviceName: 'str'
    template: 'core_v1.PodTemplateSpec'
    podManagementPolicy: 'str' = None
    replicas: 'int' = None
    revisionHistoryLimit: 'int' = None
    selector: 'meta_v1.LabelSelector' = None
    updateStrategy: 'StatefulSetUpdateStrategy' = None
    volumeClaimTemplates: 'List[core_v1.PersistentVolumeClaim]' = None


@dataclass
class StatefulSetStatus(DataclassDictMixIn):
    """StatefulSetStatus represents the current state of a StatefulSet.

      **parameters**

      * **replicas** ``int`` - replicas is the number of Pods created by the StatefulSet controller.
      * **collisionCount** ``int`` - *(optional)* collisionCount is the count of hash collisions for the StatefulSet. The
        StatefulSet controller uses this field as a collision avoidance mechanism when
        it needs to create the name for the newest ControllerRevision.
      * **conditions** ``List[StatefulSetCondition]`` - *(optional)* Represents the latest available observations of a statefulset's current state.
      * **currentReplicas** ``int`` - *(optional)* currentReplicas is the number of Pods created by the StatefulSet controller
        from the StatefulSet version indicated by currentRevision.
      * **currentRevision** ``str`` - *(optional)* currentRevision, if not empty, indicates the version of the StatefulSet used
        to generate Pods in the sequence [0,currentReplicas).
      * **observedGeneration** ``int`` - *(optional)* observedGeneration is the most recent generation observed for this
        StatefulSet. It corresponds to the StatefulSet's generation, which is updated
        on mutation by the API Server.
      * **readyReplicas** ``int`` - *(optional)* readyReplicas is the number of Pods created by the StatefulSet controller that
        have a Ready Condition.
      * **updateRevision** ``str`` - *(optional)* updateRevision, if not empty, indicates the version of the StatefulSet used to
        generate Pods in the sequence [replicas-updatedReplicas,replicas)
      * **updatedReplicas** ``int`` - *(optional)* updatedReplicas is the number of Pods created by the StatefulSet controller
        from the StatefulSet version indicated by updateRevision.
    """
    replicas: 'int'
    collisionCount: 'int' = None
    conditions: 'List[StatefulSetCondition]' = None
    currentReplicas: 'int' = None
    currentRevision: 'str' = None
    observedGeneration: 'int' = None
    readyReplicas: 'int' = None
    updateRevision: 'str' = None
    updatedReplicas: 'int' = None


@dataclass
class StatefulSetUpdateStrategy(DataclassDictMixIn):
    """StatefulSetUpdateStrategy indicates the strategy that the StatefulSet
      controller will use to perform updates. It includes any additional parameters
      necessary to perform the update for the indicated strategy.

      **parameters**

      * **rollingUpdate** ``RollingUpdateStatefulSetStrategy`` - *(optional)* RollingUpdate is used to communicate parameters when Type is
        RollingUpdateStatefulSetStrategyType.
      * **type** ``str`` - *(optional)* Type indicates the type of the StatefulSetUpdateStrategy.
    """
    rollingUpdate: 'RollingUpdateStatefulSetStrategy' = None
    type: 'str' = None


