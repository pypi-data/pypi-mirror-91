# autogenerated module
from typing import ClassVar

from ..core import resource as res
from ..models import apps_v1beta2 as m_apps_v1beta2


class ControllerRevision(res.NamespacedResourceG, m_apps_v1beta2.ControllerRevision):
    """* **Extends**: ``models.apps_v1beta2.ControllerRevision``
       * **Type**: Namespaced Resource
       * **Accepted client methods**: `delete`, `deletecollection`, `get`, `list` all, `watch` all, `list`, `patch`, `create`, `replace`, `watch`
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('apps', 'v1beta2', 'ControllerRevision'),
        plural='controllerrevisions',
        verbs=['delete', 'deletecollection', 'get', 'global_list', 'global_watch', 'list', 'patch', 'post', 'put', 'watch'],
    )


class DaemonSetStatus(res.NamespacedSubResource, m_apps_v1beta2.DaemonSet):
    """* **Extends**: ``models.apps_v1beta2.DaemonSet``
       * **Type**: Namespaced Resource
       * **Accepted client methods**: `get`, `patch`, `replace`
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('apps', 'v1beta2', 'DaemonSet'),
        parent=res.ResourceDef('apps', 'v1beta2', 'DaemonSet'),
        plural='daemonsets',
        verbs=['get', 'patch', 'put'],
        action='status',
    )


class DaemonSet(res.NamespacedResourceG, m_apps_v1beta2.DaemonSet):
    """* **Extends**: ``models.apps_v1beta2.DaemonSet``
       * **Type**: Namespaced Resource
       * **Accepted client methods**: `delete`, `deletecollection`, `get`, `list` all, `watch` all, `list`, `patch`, `create`, `replace`, `watch`

       **Subresources**:

       * **Status**: ``DaemonSetStatus``
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('apps', 'v1beta2', 'DaemonSet'),
        plural='daemonsets',
        verbs=['delete', 'deletecollection', 'get', 'global_list', 'global_watch', 'list', 'patch', 'post', 'put', 'watch'],
    )

    Status: ClassVar = DaemonSetStatus


class DeploymentScale(res.NamespacedSubResource, m_apps_v1beta2.Scale):
    """* **Extends**: ``models.apps_v1beta2.Scale``
       * **Type**: Namespaced Resource
       * **Accepted client methods**: `get`, `patch`, `replace`
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('apps', 'v1beta2', 'Scale'),
        parent=res.ResourceDef('apps', 'v1beta2', 'Deployment'),
        plural='deployments',
        verbs=['get', 'patch', 'put'],
        action='scale',
    )


class DeploymentStatus(res.NamespacedSubResource, m_apps_v1beta2.Deployment):
    """* **Extends**: ``models.apps_v1beta2.Deployment``
       * **Type**: Namespaced Resource
       * **Accepted client methods**: `get`, `patch`, `replace`
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('apps', 'v1beta2', 'Deployment'),
        parent=res.ResourceDef('apps', 'v1beta2', 'Deployment'),
        plural='deployments',
        verbs=['get', 'patch', 'put'],
        action='status',
    )


class Deployment(res.NamespacedResourceG, m_apps_v1beta2.Deployment):
    """* **Extends**: ``models.apps_v1beta2.Deployment``
       * **Type**: Namespaced Resource
       * **Accepted client methods**: `delete`, `deletecollection`, `get`, `list` all, `watch` all, `list`, `patch`, `create`, `replace`, `watch`

       **Subresources**:

       * **Scale**: ``DeploymentScale``
       * **Status**: ``DeploymentStatus``
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('apps', 'v1beta2', 'Deployment'),
        plural='deployments',
        verbs=['delete', 'deletecollection', 'get', 'global_list', 'global_watch', 'list', 'patch', 'post', 'put', 'watch'],
    )

    Scale: ClassVar = DeploymentScale
    Status: ClassVar = DeploymentStatus


class ReplicaSetScale(res.NamespacedSubResource, m_apps_v1beta2.Scale):
    """* **Extends**: ``models.apps_v1beta2.Scale``
       * **Type**: Namespaced Resource
       * **Accepted client methods**: `get`, `patch`, `replace`
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('apps', 'v1beta2', 'Scale'),
        parent=res.ResourceDef('apps', 'v1beta2', 'ReplicaSet'),
        plural='replicasets',
        verbs=['get', 'patch', 'put'],
        action='scale',
    )


class ReplicaSetStatus(res.NamespacedSubResource, m_apps_v1beta2.ReplicaSet):
    """* **Extends**: ``models.apps_v1beta2.ReplicaSet``
       * **Type**: Namespaced Resource
       * **Accepted client methods**: `get`, `patch`, `replace`
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('apps', 'v1beta2', 'ReplicaSet'),
        parent=res.ResourceDef('apps', 'v1beta2', 'ReplicaSet'),
        plural='replicasets',
        verbs=['get', 'patch', 'put'],
        action='status',
    )


class ReplicaSet(res.NamespacedResourceG, m_apps_v1beta2.ReplicaSet):
    """* **Extends**: ``models.apps_v1beta2.ReplicaSet``
       * **Type**: Namespaced Resource
       * **Accepted client methods**: `delete`, `deletecollection`, `get`, `list` all, `watch` all, `list`, `patch`, `create`, `replace`, `watch`

       **Subresources**:

       * **Scale**: ``ReplicaSetScale``
       * **Status**: ``ReplicaSetStatus``
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('apps', 'v1beta2', 'ReplicaSet'),
        plural='replicasets',
        verbs=['delete', 'deletecollection', 'get', 'global_list', 'global_watch', 'list', 'patch', 'post', 'put', 'watch'],
    )

    Scale: ClassVar = ReplicaSetScale
    Status: ClassVar = ReplicaSetStatus


class StatefulSetScale(res.NamespacedSubResource, m_apps_v1beta2.Scale):
    """* **Extends**: ``models.apps_v1beta2.Scale``
       * **Type**: Namespaced Resource
       * **Accepted client methods**: `get`, `patch`, `replace`
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('apps', 'v1beta2', 'Scale'),
        parent=res.ResourceDef('apps', 'v1beta2', 'StatefulSet'),
        plural='statefulsets',
        verbs=['get', 'patch', 'put'],
        action='scale',
    )


class StatefulSetStatus(res.NamespacedSubResource, m_apps_v1beta2.StatefulSet):
    """* **Extends**: ``models.apps_v1beta2.StatefulSet``
       * **Type**: Namespaced Resource
       * **Accepted client methods**: `get`, `patch`, `replace`
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('apps', 'v1beta2', 'StatefulSet'),
        parent=res.ResourceDef('apps', 'v1beta2', 'StatefulSet'),
        plural='statefulsets',
        verbs=['get', 'patch', 'put'],
        action='status',
    )


class StatefulSet(res.NamespacedResourceG, m_apps_v1beta2.StatefulSet):
    """* **Extends**: ``models.apps_v1beta2.StatefulSet``
       * **Type**: Namespaced Resource
       * **Accepted client methods**: `delete`, `deletecollection`, `get`, `list` all, `watch` all, `list`, `patch`, `create`, `replace`, `watch`

       **Subresources**:

       * **Scale**: ``StatefulSetScale``
       * **Status**: ``StatefulSetStatus``
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('apps', 'v1beta2', 'StatefulSet'),
        plural='statefulsets',
        verbs=['delete', 'deletecollection', 'get', 'global_list', 'global_watch', 'list', 'patch', 'post', 'put', 'watch'],
    )

    Scale: ClassVar = StatefulSetScale
    Status: ClassVar = StatefulSetStatus

