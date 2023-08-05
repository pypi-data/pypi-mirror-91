# autogenerated module
from typing import ClassVar

from ..core import resource as res
from ..models import auditregistration_v1alpha1 as m_auditregistration_v1alpha1


class AuditSink(res.GlobalResource, m_auditregistration_v1alpha1.AuditSink):
    """* **Extends**: ``models.auditregistration_v1alpha1.AuditSink``
       * **Type**: Global Resource
       * **Accepted client methods**: `delete`, `deletecollection`, `get`, `list`, `patch`, `create`, `replace`, `watch`
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('auditregistration.k8s.io', 'v1alpha1', 'AuditSink'),
        plural='auditsinks',
        verbs=['delete', 'deletecollection', 'get', 'list', 'patch', 'post', 'put', 'watch'],
    )

