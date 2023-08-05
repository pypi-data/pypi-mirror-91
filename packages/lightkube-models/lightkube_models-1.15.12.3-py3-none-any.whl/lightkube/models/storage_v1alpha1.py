# autogenerated module
from dataclasses import dataclass, field
from typing import List

from ..core.dataclasses_dict import DataclassDictMixIn

from . import core_v1
from . import meta_v1


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
        https://git.k8s.io/community/contributors/devel/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* Standard object metadata. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#metadata
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
        https://git.k8s.io/community/contributors/devel/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ListMeta`` - *(optional)* Standard list metadata More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#metadata
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
        string maybe logged, so it should not contain sensitive information.
      * **time** ``meta_v1.Time`` - *(optional)* Time the error was encountered.
    """
    message: 'str' = None
    time: 'meta_v1.Time' = None


