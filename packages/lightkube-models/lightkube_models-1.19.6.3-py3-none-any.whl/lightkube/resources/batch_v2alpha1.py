# autogenerated module
from typing import ClassVar

from ..core import resource as res
from ..models import batch_v2alpha1 as m_batch_v2alpha1


class CronJobStatus(res.NamespacedSubResource, m_batch_v2alpha1.CronJob):
    """* **Extends**: ``models.batch_v2alpha1.CronJob``
       * **Type**: Namespaced Resource
       * **Accepted client methods**: `get`, `patch`, `replace`
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('batch', 'v2alpha1', 'CronJob'),
        parent=res.ResourceDef('batch', 'v2alpha1', 'CronJob'),
        plural='cronjobs',
        verbs=['get', 'patch', 'put'],
        action='status',
    )


class CronJob(res.NamespacedResourceG, m_batch_v2alpha1.CronJob):
    """* **Extends**: ``models.batch_v2alpha1.CronJob``
       * **Type**: Namespaced Resource
       * **Accepted client methods**: `delete`, `deletecollection`, `get`, `list` all, `watch` all, `list`, `patch`, `create`, `replace`, `watch`

       **Subresources**:

       * **Status**: ``CronJobStatus``
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('batch', 'v2alpha1', 'CronJob'),
        plural='cronjobs',
        verbs=['delete', 'deletecollection', 'get', 'global_list', 'global_watch', 'list', 'patch', 'post', 'put', 'watch'],
    )

    Status: ClassVar = CronJobStatus

