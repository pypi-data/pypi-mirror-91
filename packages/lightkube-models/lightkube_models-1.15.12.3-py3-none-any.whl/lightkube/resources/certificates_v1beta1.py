# autogenerated module
from typing import ClassVar

from ..core import resource as res
from ..models import certificates_v1beta1 as m_certificates_v1beta1


class CertificateSigningRequestApproval(res.GlobalSubResource, m_certificates_v1beta1.CertificateSigningRequest):
    """* **Extends**: ``models.certificates_v1beta1.CertificateSigningRequest``
       * **Type**: Global Resource
       * **Accepted client methods**: `replace`
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('certificates.k8s.io', 'v1beta1', 'CertificateSigningRequest'),
        parent=res.ResourceDef('certificates.k8s.io', 'v1beta1', 'CertificateSigningRequest'),
        plural='certificatesigningrequests',
        verbs=['put'],
        action='approval',
    )


class CertificateSigningRequestStatus(res.GlobalSubResource, m_certificates_v1beta1.CertificateSigningRequest):
    """* **Extends**: ``models.certificates_v1beta1.CertificateSigningRequest``
       * **Type**: Global Resource
       * **Accepted client methods**: `get`, `patch`, `replace`
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('certificates.k8s.io', 'v1beta1', 'CertificateSigningRequest'),
        parent=res.ResourceDef('certificates.k8s.io', 'v1beta1', 'CertificateSigningRequest'),
        plural='certificatesigningrequests',
        verbs=['get', 'patch', 'put'],
        action='status',
    )


class CertificateSigningRequest(res.GlobalResource, m_certificates_v1beta1.CertificateSigningRequest):
    """* **Extends**: ``models.certificates_v1beta1.CertificateSigningRequest``
       * **Type**: Global Resource
       * **Accepted client methods**: `delete`, `deletecollection`, `get`, `list`, `patch`, `create`, `replace`, `watch`

       **Subresources**:

       * **Approval**: ``CertificateSigningRequestApproval``
       * **Status**: ``CertificateSigningRequestStatus``
    """
    _api_info = res.ApiInfo(
        resource=res.ResourceDef('certificates.k8s.io', 'v1beta1', 'CertificateSigningRequest'),
        plural='certificatesigningrequests',
        verbs=['delete', 'deletecollection', 'get', 'list', 'patch', 'post', 'put', 'watch'],
    )

    Approval: ClassVar = CertificateSigningRequestApproval
    Status: ClassVar = CertificateSigningRequestStatus

