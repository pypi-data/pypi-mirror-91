# autogenerated module
from typing import ClassVar

from ..core import resource as res
from ..models import networking_v1beta1 as m_networking_v1beta1


class IngressStatus(res.NamespacedSubResource, m_networking_v1beta1.Ingress):
    """* **Extends**: ``models.networking_v1beta1.Ingress``
       * **Type**: Namespaced Resource
       * **Accepted client methods**: `get`, `patch`, `replace`
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('networking.k8s.io', 'v1beta1', 'Ingress'),
        parent=res.ResourceDef('networking.k8s.io', 'v1beta1', 'Ingress'),
        plural='ingresses',
        verbs=['get', 'patch', 'put'],
        action='status',
    )


class Ingress(res.NamespacedResourceG, m_networking_v1beta1.Ingress):
    """* **Extends**: ``models.networking_v1beta1.Ingress``
       * **Type**: Namespaced Resource
       * **Accepted client methods**: `delete`, `deletecollection`, `get`, `list` all, `watch` all, `list`, `patch`, `create`, `replace`, `watch`

       **Subresources**:

       * **Status**: ``IngressStatus``
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('networking.k8s.io', 'v1beta1', 'Ingress'),
        plural='ingresses',
        verbs=['delete', 'deletecollection', 'get', 'global_list', 'global_watch', 'list', 'patch', 'post', 'put', 'watch'],
    )

    Status: ClassVar = IngressStatus

