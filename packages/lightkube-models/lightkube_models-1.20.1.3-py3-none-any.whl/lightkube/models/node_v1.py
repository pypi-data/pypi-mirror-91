# autogenerated module
from dataclasses import dataclass, field
from typing import List

from ..core.dataclasses_dict import DataclassDictMixIn

from . import core_v1
from . import meta_v1


@dataclass
class Overhead(DataclassDictMixIn):
    """Overhead structure represents the resource overhead associated with running a
      pod.

      **parameters**

      * **podFixed** ``dict`` - *(optional)* PodFixed represents the fixed resource overhead associated with running a pod.
    """
    podFixed: 'dict' = None


@dataclass
class RuntimeClass(DataclassDictMixIn):
    """RuntimeClass defines a class of container runtime supported in the cluster.
      The RuntimeClass is used to determine which container runtime is used to run
      all containers in a pod. RuntimeClasses are manually defined by a user or
      cluster provisioner, and referenced in the PodSpec. The Kubelet is responsible
      for resolving the RuntimeClassName reference before running the pod.  For more
      details, see https://kubernetes.io/docs/concepts/containers/runtime-class/

      **parameters**

      * **handler** ``str`` - Handler specifies the underlying runtime and configuration that the CRI
        implementation will use to handle pods of this class. The possible values are
        specific to the node & CRI configuration.  It is assumed that all handlers are
        available on every node, and handlers of the same name are equivalent on every
        node. For example, a handler called "runc" might specify that the runc OCI
        runtime (using native Linux containers) will be used to run the containers in
        a pod. The Handler must be lowercase, conform to the DNS Label (RFC 1123)
        requirements, and is immutable.
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
      * **overhead** ``Overhead`` - *(optional)* Overhead represents the resource overhead associated with running a pod for a
        given RuntimeClass. For more details, see
         https://kubernetes.io/docs/concepts/scheduling-eviction/pod-overhead/
        This field is in beta starting v1.18 and is only honored by servers that
        enable the PodOverhead feature.
      * **scheduling** ``Scheduling`` - *(optional)* Scheduling holds the scheduling constraints to ensure that pods running with
        this RuntimeClass are scheduled to nodes that support it. If scheduling is
        nil, this RuntimeClass is assumed to be supported by all nodes.
    """
    handler: 'str'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    overhead: 'Overhead' = None
    scheduling: 'Scheduling' = None


@dataclass
class RuntimeClassList(DataclassDictMixIn):
    """RuntimeClassList is a list of RuntimeClass objects.

      **parameters**

      * **items** ``List[RuntimeClass]`` - Items is a list of schema objects.
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
    items: 'List[RuntimeClass]'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ListMeta' = None


@dataclass
class Scheduling(DataclassDictMixIn):
    """Scheduling specifies the scheduling constraints for nodes supporting a
      RuntimeClass.

      **parameters**

      * **nodeSelector** ``dict`` - *(optional)* nodeSelector lists labels that must be present on nodes that support this
        RuntimeClass. Pods using this RuntimeClass can only be scheduled to a node
        matched by this selector. The RuntimeClass nodeSelector is merged with a pod's
        existing nodeSelector. Any conflicts will cause the pod to be rejected in
        admission.
      * **tolerations** ``List[core_v1.Toleration]`` - *(optional)* tolerations are appended (excluding duplicates) to pods running with this
        RuntimeClass during admission, effectively unioning the set of nodes tolerated
        by the pod and the RuntimeClass.
    """
    nodeSelector: 'dict' = None
    tolerations: 'List[core_v1.Toleration]' = None


