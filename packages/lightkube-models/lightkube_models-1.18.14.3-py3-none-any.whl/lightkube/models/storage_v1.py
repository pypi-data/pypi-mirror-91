# autogenerated module
from dataclasses import dataclass, field
from typing import List

from ..core.dataclasses_dict import DataclassDictMixIn

from . import core_v1
from . import meta_v1


@dataclass
class CSIDriver(DataclassDictMixIn):
    """CSIDriver captures information about a Container Storage Interface (CSI)
      volume driver deployed on the cluster. Kubernetes attach detach controller
      uses this object to determine whether attach is required. Kubelet uses this
      object to determine whether pod information needs to be passed on mount.
      CSIDriver objects are non-namespaced.

      **parameters**

      * **spec** ``CSIDriverSpec`` - Specification of the CSI Driver.
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* Standard object metadata. metadata.Name indicates the name of the CSI driver
        that this object refers to; it MUST be the same name returned by the CSI
        GetPluginName() call for that driver. The driver name must be 63 characters or
        less, beginning and ending with an alphanumeric character ([a-z0-9A-Z]) with
        dashes (-), dots (.), and alphanumerics between. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
    """
    spec: 'CSIDriverSpec'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None


@dataclass
class CSIDriverList(DataclassDictMixIn):
    """CSIDriverList is a collection of CSIDriver objects.

      **parameters**

      * **items** ``List[CSIDriver]`` - items is the list of CSIDriver
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
    items: 'List[CSIDriver]'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ListMeta' = None


@dataclass
class CSIDriverSpec(DataclassDictMixIn):
    """CSIDriverSpec is the specification of a CSIDriver.

      **parameters**

      * **attachRequired** ``bool`` - *(optional)* attachRequired indicates this CSI volume driver requires an attach operation
        (because it implements the CSI ControllerPublishVolume() method), and that the
        Kubernetes attach detach controller should call the attach volume interface
        which checks the volumeattachment status and waits until the volume is
        attached before proceeding to mounting. The CSI external-attacher coordinates
        with CSI volume driver and updates the volumeattachment status when the attach
        operation is complete. If the CSIDriverRegistry feature gate is enabled and
        the value is specified to false, the attach operation will be skipped.
        Otherwise the attach operation will be called.
      * **podInfoOnMount** ``bool`` - *(optional)* If set to true, podInfoOnMount indicates this CSI volume driver requires
        additional pod information (like podName, podUID, etc.) during mount
        operations. If set to false, pod information will not be passed on mount.
        Default is false. The CSI driver specifies podInfoOnMount as part of driver
        deployment. If true, Kubelet will pass pod information as VolumeContext in the
        CSI NodePublishVolume() calls. The CSI driver is responsible for parsing and
        validating the information passed in as VolumeContext. The following
        VolumeConext will be passed if podInfoOnMount is set to true. This list might
        grow, but the prefix will be used. "csi.storage.k8s.io/pod.name": pod.Name
        "csi.storage.k8s.io/pod.namespace": pod.Namespace
        "csi.storage.k8s.io/pod.uid": string(pod.UID) "csi.storage.k8s.io/ephemeral":
        "true" iff the volume is an ephemeral inline volume
                                        defined by a CSIVolumeSource, otherwise
        "false"
        "csi.storage.k8s.io/ephemeral" is a new feature in Kubernetes 1.16. It is only
        required for drivers which support both the "Persistent" and "Ephemeral"
        VolumeLifecycleMode. Other drivers can leave pod info disabled and/or ignore
        this field. As Kubernetes 1.15 doesn't support this field, drivers can only
        support one mode when deployed on such a cluster and the deployment determines
        which mode that is, for example via a command line parameter of the driver.
      * **volumeLifecycleModes** ``List[str]`` - *(optional)* volumeLifecycleModes defines what kind of volumes this CSI volume driver
        supports. The default if the list is empty is "Persistent", which is the usage
        defined by the CSI specification and implemented in Kubernetes via the usual
        PV/PVC mechanism. The other mode is "Ephemeral". In this mode, volumes are
        defined inline inside the pod spec with CSIVolumeSource and their lifecycle is
        tied to the lifecycle of that pod. A driver has to be aware of this because it
        is only going to get a NodePublishVolume call for such a volume. For more
        information about implementing this mode, see
        https://kubernetes-csi.github.io/docs/ephemeral-local-volumes.html A driver
        can support one or more of these modes and more modes may be added in the
        future. This field is beta.
    """
    attachRequired: 'bool' = None
    podInfoOnMount: 'bool' = None
    volumeLifecycleModes: 'List[str]' = None


@dataclass
class CSINode(DataclassDictMixIn):
    """CSINode holds information about all CSI drivers installed on a node. CSI
      drivers do not need to create the CSINode object directly. As long as they use
      the node-driver-registrar sidecar container, the kubelet will automatically
      populate the CSINode object for the CSI driver as part of kubelet plugin
      registration. CSINode has the same name as a node. If the object is missing,
      it means either there are no CSI Drivers available on the node, or the Kubelet
      version is low enough that it doesn't create this object. CSINode has an
      OwnerReference that points to the corresponding node object.

      **parameters**

      * **spec** ``CSINodeSpec`` - spec is the specification of CSINode
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* metadata.name must be the Kubernetes node name.
    """
    spec: 'CSINodeSpec'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None


@dataclass
class CSINodeDriver(DataclassDictMixIn):
    """CSINodeDriver holds information about the specification of one CSI driver
      installed on a node

      **parameters**

      * **name** ``str`` - This is the name of the CSI driver that this object refers to. This MUST be
        the same name returned by the CSI GetPluginName() call for that driver.
      * **nodeID** ``str`` - nodeID of the node from the driver point of view. This field enables
        Kubernetes to communicate with storage systems that do not share the same
        nomenclature for nodes. For example, Kubernetes may refer to a given node as
        "node1", but the storage system may refer to the same node as "nodeA". When
        Kubernetes issues a command to the storage system to attach a volume to a
        specific node, it can use this field to refer to the node name using the ID
        that the storage system will understand, e.g. "nodeA" instead of "node1". This
        field is required.
      * **allocatable** ``VolumeNodeResources`` - *(optional)* allocatable represents the volume resources of a node that are available for
        scheduling. This field is beta.
      * **topologyKeys** ``List[str]`` - *(optional)* topologyKeys is the list of keys supported by the driver. When a driver is
        initialized on a cluster, it provides a set of topology keys that it
        understands (e.g. "company.com/zone", "company.com/region"). When a driver is
        initialized on a node, it provides the same topology keys along with values.
        Kubelet will expose these topology keys as labels on its own node object. When
        Kubernetes does topology aware provisioning, it can use this list to determine
        which labels it should retrieve from the node object and pass back to the
        driver. It is possible for different nodes to use different topology keys.
        This can be empty if driver does not support topology.
    """
    name: 'str'
    nodeID: 'str'
    allocatable: 'VolumeNodeResources' = None
    topologyKeys: 'List[str]' = None


@dataclass
class CSINodeList(DataclassDictMixIn):
    """CSINodeList is a collection of CSINode objects.

      **parameters**

      * **items** ``List[CSINode]`` - items is the list of CSINode
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
    items: 'List[CSINode]'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ListMeta' = None


@dataclass
class CSINodeSpec(DataclassDictMixIn):
    """CSINodeSpec holds information about the specification of all CSI drivers
      installed on a node

      **parameters**

      * **drivers** ``List[CSINodeDriver]`` - drivers is a list of information of all CSI Drivers existing on a node. If all
        drivers in the list are uninstalled, this can become empty.
    """
    drivers: 'List[CSINodeDriver]'


@dataclass
class StorageClass(DataclassDictMixIn):
    """StorageClass describes the parameters for a class of storage for which
      PersistentVolumes can be dynamically provisioned.
      
      StorageClasses are non-namespaced; the name of the storage class according to
      etcd is in ObjectMeta.Name.

      **parameters**

      * **provisioner** ``str`` - Provisioner indicates the type of the provisioner.
      * **allowVolumeExpansion** ``bool`` - *(optional)* AllowVolumeExpansion shows whether the storage class allow volume expand
      * **allowedTopologies** ``List[core_v1.TopologySelectorTerm]`` - *(optional)* Restrict the node topologies where volumes can be dynamically provisioned.
        Each volume plugin defines its own supported topology specifications. An empty
        TopologySelectorTerm list means there is no topology restriction. This field
        is only honored by servers that enable the VolumeScheduling feature.
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* Standard object's metadata. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
      * **mountOptions** ``List[str]`` - *(optional)* Dynamically provisioned PersistentVolumes of this storage class are created
        with these mountOptions, e.g. ["ro", "soft"]. Not validated - mount of the PVs
        will simply fail if one is invalid.
      * **parameters** ``dict`` - *(optional)* Parameters holds the parameters for the provisioner that should create volumes
        of this storage class.
      * **reclaimPolicy** ``str`` - *(optional)* Dynamically provisioned PersistentVolumes of this storage class are created
        with this reclaimPolicy. Defaults to Delete.
      * **volumeBindingMode** ``str`` - *(optional)* VolumeBindingMode indicates how PersistentVolumeClaims should be provisioned
        and bound.  When unset, VolumeBindingImmediate is used. This field is only
        honored by servers that enable the VolumeScheduling feature.
    """
    provisioner: 'str'
    allowVolumeExpansion: 'bool' = None
    allowedTopologies: 'List[core_v1.TopologySelectorTerm]' = None
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    mountOptions: 'List[str]' = None
    parameters: 'dict' = None
    reclaimPolicy: 'str' = None
    volumeBindingMode: 'str' = None


@dataclass
class StorageClassList(DataclassDictMixIn):
    """StorageClassList is a collection of storage classes.

      **parameters**

      * **items** ``List[StorageClass]`` - Items is the list of StorageClasses
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
    items: 'List[StorageClass]'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ListMeta' = None


@dataclass
class VolumeAttachment(DataclassDictMixIn):
    """VolumeAttachment captures the intent to attach or detach the specified volume
      to/from the specified node.
      
      VolumeAttachment objects are non-namespaced.

      **parameters**

      * **spec** ``VolumeAttachmentSpec`` - Specification of the desired attach/detach volume behavior. Populated by the
        Kubernetes system.
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
      * **status** ``VolumeAttachmentStatus`` - *(optional)* Status of the VolumeAttachment request. Populated by the entity completing the
        attach or detach operation, i.e. the external-attacher.
    """
    spec: 'VolumeAttachmentSpec'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    status: 'VolumeAttachmentStatus' = None


@dataclass
class VolumeAttachmentList(DataclassDictMixIn):
    """VolumeAttachmentList is a collection of VolumeAttachment objects.

      **parameters**

      * **items** ``List[VolumeAttachment]`` - Items is the list of VolumeAttachments
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
    items: 'List[VolumeAttachment]'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ListMeta' = None


@dataclass
class VolumeAttachmentSource(DataclassDictMixIn):
    """VolumeAttachmentSource represents a volume that should be attached. Right now
      only PersistenVolumes can be attached via external attacher, in future we may
      allow also inline volumes in pods. Exactly one member can be set.

      **parameters**

      * **inlineVolumeSpec** ``core_v1.PersistentVolumeSpec`` - *(optional)* inlineVolumeSpec contains all the information necessary to attach a persistent
        volume defined by a pod's inline VolumeSource. This field is populated only
        for the CSIMigration feature. It contains translated fields from a pod's
        inline VolumeSource to a PersistentVolumeSpec. This field is alpha-level and
        is only honored by servers that enabled the CSIMigration feature.
      * **persistentVolumeName** ``str`` - *(optional)* Name of the persistent volume to attach.
    """
    inlineVolumeSpec: 'core_v1.PersistentVolumeSpec' = None
    persistentVolumeName: 'str' = None


@dataclass
class VolumeAttachmentSpec(DataclassDictMixIn):
    """VolumeAttachmentSpec is the specification of a VolumeAttachment request.

      **parameters**

      * **attacher** ``str`` - Attacher indicates the name of the volume driver that MUST handle this
        request. This is the name returned by GetPluginName().
      * **nodeName** ``str`` - The node that the volume should be attached to.
      * **source** ``VolumeAttachmentSource`` - Source represents the volume that should be attached.
    """
    attacher: 'str'
    nodeName: 'str'
    source: 'VolumeAttachmentSource'


@dataclass
class VolumeAttachmentStatus(DataclassDictMixIn):
    """VolumeAttachmentStatus is the status of a VolumeAttachment request.

      **parameters**

      * **attached** ``bool`` - Indicates the volume is successfully attached. This field must only be set by
        the entity completing the attach operation, i.e. the external-attacher.
      * **attachError** ``VolumeError`` - *(optional)* The last error encountered during attach operation, if any. This field must
        only be set by the entity completing the attach operation, i.e. the
        external-attacher.
      * **attachmentMetadata** ``dict`` - *(optional)* Upon successful attach, this field is populated with any information returned
        by the attach operation that must be passed into subsequent WaitForAttach or
        Mount calls. This field must only be set by the entity completing the attach
        operation, i.e. the external-attacher.
      * **detachError** ``VolumeError`` - *(optional)* The last error encountered during detach operation, if any. This field must
        only be set by the entity completing the detach operation, i.e. the
        external-attacher.
    """
    attached: 'bool'
    attachError: 'VolumeError' = None
    attachmentMetadata: 'dict' = None
    detachError: 'VolumeError' = None


@dataclass
class VolumeError(DataclassDictMixIn):
    """VolumeError captures an error encountered during a volume operation.

      **parameters**

      * **message** ``str`` - *(optional)* String detailing the error encountered during Attach or Detach operation. This
        string may be logged, so it should not contain sensitive information.
      * **time** ``meta_v1.Time`` - *(optional)* Time the error was encountered.
    """
    message: 'str' = None
    time: 'meta_v1.Time' = None


@dataclass
class VolumeNodeResources(DataclassDictMixIn):
    """VolumeNodeResources is a set of resource limits for scheduling of volumes.

      **parameters**

      * **count** ``int`` - *(optional)* Maximum number of unique volumes managed by the CSI driver that can be used on
        a node. A volume that is both attached and mounted on a node is considered to
        be used once, not twice. The same rule applies for a unique volume that is
        shared among multiple pods on the same node. If this field is not specified,
        then the supported number of volumes on this node is unbounded.
    """
    count: 'int' = None


