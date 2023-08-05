# autogenerated module
from typing import ClassVar

from ..core import resource as res
from ..models import scheduling_v1alpha1 as m_scheduling_v1alpha1


class PriorityClass(res.GlobalResource, m_scheduling_v1alpha1.PriorityClass):
    """* **Extends**: ``models.scheduling_v1alpha1.PriorityClass``
       * **Type**: Global Resource
       * **Accepted client methods**: `delete`, `deletecollection`, `get`, `list`, `patch`, `create`, `replace`, `watch`
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('scheduling.k8s.io', 'v1alpha1', 'PriorityClass'),
        plural='priorityclasses',
        verbs=['delete', 'deletecollection', 'get', 'list', 'patch', 'post', 'put', 'watch'],
    )

