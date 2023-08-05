# autogenerated module
from dataclasses import dataclass, field
from typing import List

from ..core.dataclasses_dict import DataclassDictMixIn

from . import meta_v1
from . import core_v1
from . import util_intstr


@dataclass
class HTTPIngressPath(DataclassDictMixIn):
    """HTTPIngressPath associates a path with a backend. Incoming urls matching the
      path are forwarded to the backend.

      **parameters**

      * **backend** ``IngressBackend`` - Backend defines the referenced service endpoint to which the traffic will be
        forwarded to.
      * **path** ``str`` - *(optional)* Path is matched against the path of an incoming request. Currently it can
        contain characters disallowed from the conventional "path" part of a URL as
        defined by RFC 3986. Paths must begin with a '/'. When unspecified, all paths
        from incoming requests are matched.
      * **pathType** ``str`` - *(optional)* PathType determines the interpretation of the Path matching. PathType can be
        one of the following values: * Exact: Matches the URL path exactly. * Prefix:
        Matches based on a URL path prefix split by '/'. Matching is
          done on a path element by element basis. A path element refers is the
          list of labels in the path split by the '/' separator. A request is a
          match for path p if every p is an element-wise prefix of p of the
          request path. Note that if the last element of the path is a substring
          of the last element in request path, it is not a match (e.g. /foo/bar
          matches /foo/bar/baz, but does not match /foo/barbaz).
        * ImplementationSpecific: Interpretation of the Path matching is up to
          the IngressClass. Implementations can treat this as a separate PathType
          or treat it identically to Prefix or Exact path types.
        Implementations are required to support all path types. Defaults to
        ImplementationSpecific.
    """
    backend: 'IngressBackend'
    path: 'str' = None
    pathType: 'str' = None


@dataclass
class HTTPIngressRuleValue(DataclassDictMixIn):
    """HTTPIngressRuleValue is a list of http selectors pointing to backends. In the
      example: http://<host>/<path>?<searchpart> -> backend where where parts of the
      url correspond to RFC 3986, this resource will be used to match against
      everything after the last '/' and before the first '?' or '#'.

      **parameters**

      * **paths** ``List[HTTPIngressPath]`` - A collection of paths that map requests to backends.
    """
    paths: 'List[HTTPIngressPath]'


@dataclass
class Ingress(DataclassDictMixIn):
    """Ingress is a collection of rules that allow inbound connections to reach the
      endpoints defined by a backend. An Ingress can be configured to give services
      externally-reachable urls, load balance traffic, terminate SSL, offer name
      based virtual hosting etc. DEPRECATED - This group version of Ingress is
      deprecated by networking.k8s.io/v1beta1 Ingress. See the release notes for
      more information.

      **parameters**

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
      * **spec** ``IngressSpec`` - *(optional)* Spec is the desired state of the Ingress. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
      * **status** ``IngressStatus`` - *(optional)* Status is the current state of the Ingress. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status
    """
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    spec: 'IngressSpec' = None
    status: 'IngressStatus' = None


@dataclass
class IngressBackend(DataclassDictMixIn):
    """IngressBackend describes all endpoints for a given service and port.

      **parameters**

      * **resource** ``core_v1.TypedLocalObjectReference`` - *(optional)* Resource is an ObjectRef to another Kubernetes resource in the namespace of
        the Ingress object. If resource is specified, serviceName and servicePort must
        not be specified.
      * **serviceName** ``str`` - *(optional)* Specifies the name of the referenced service.
      * **servicePort** ``util_intstr.IntOrString`` - *(optional)* Specifies the port of the referenced service.
    """
    resource: 'core_v1.TypedLocalObjectReference' = None
    serviceName: 'str' = None
    servicePort: 'util_intstr.IntOrString' = None


@dataclass
class IngressList(DataclassDictMixIn):
    """IngressList is a collection of Ingress.

      **parameters**

      * **items** ``List[Ingress]`` - Items is the list of Ingress.
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ListMeta`` - *(optional)* Standard object's metadata. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata
    """
    items: 'List[Ingress]'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ListMeta' = None


@dataclass
class IngressRule(DataclassDictMixIn):
    """IngressRule represents the rules mapping the paths under a specified host to
      the related backend services. Incoming requests are first evaluated for a host
      match, then routed to the backend associated with the matching
      IngressRuleValue.

      **parameters**

      * **host** ``str`` - *(optional)* Host is the fully qualified domain name of a network host, as defined by RFC
        3986. Note the following deviations from the "host" part of the URI as defined
        in RFC 3986: 1. IPs are not allowed. Currently an IngressRuleValue can only
        apply to
           the IP in the Spec of the parent Ingress.
        2. The `:` delimiter is not respected because ports are not allowed.
        	  Currently the port of an Ingress is implicitly :80 for http and
        	  :443 for https.
        Both these may change in the future. Incoming requests are matched against the
        host before the IngressRuleValue. If the host is unspecified, the Ingress
        routes all traffic based on the specified IngressRuleValue.
        Host can be "precise" which is a domain name without the terminating dot of a
        network host (e.g. "foo.bar.com") or "wildcard", which is a domain name
        prefixed with a single wildcard label (e.g. "*.foo.com"). The wildcard
        character '*' must appear by itself as the first DNS label and matches only a
        single label. You cannot have a wildcard label by itself (e.g. Host == "*").
        Requests will be matched against the Host field in the following way: 1. If
        Host is precise, the request matches this rule if the http host header is
        equal to Host. 2. If Host is a wildcard, then the request matches this rule if
        the http host header is to equal to the suffix (removing the first label) of
        the wildcard rule.
      * **http** ``HTTPIngressRuleValue`` - *(optional)* 
    """
    host: 'str' = None
    http: 'HTTPIngressRuleValue' = None


@dataclass
class IngressSpec(DataclassDictMixIn):
    """IngressSpec describes the Ingress the user wishes to exist.

      **parameters**

      * **backend** ``IngressBackend`` - *(optional)* A default backend capable of servicing requests that don't match any rule. At
        least one of 'backend' or 'rules' must be specified. This field is optional to
        allow the loadbalancer controller or defaulting logic to specify a global
        default.
      * **ingressClassName** ``str`` - *(optional)* IngressClassName is the name of the IngressClass cluster resource. The
        associated IngressClass defines which controller will implement the resource.
        This replaces the deprecated `kubernetes.io/ingress.class` annotation. For
        backwards compatibility, when that annotation is set, it must be given
        precedence over this field. The controller may emit a warning if the field and
        annotation have different values. Implementations of this API should ignore
        Ingresses without a class specified. An IngressClass resource may be marked as
        default, which can be used to set a default value for this field. For more
        information, refer to the IngressClass documentation.
      * **rules** ``List[IngressRule]`` - *(optional)* A list of host rules used to configure the Ingress. If unspecified, or no rule
        matches, all traffic is sent to the default backend.
      * **tls** ``List[IngressTLS]`` - *(optional)* TLS configuration. Currently the Ingress only supports a single TLS port, 443.
        If multiple members of this list specify different hosts, they will be
        multiplexed on the same port according to the hostname specified through the
        SNI TLS extension, if the ingress controller fulfilling the ingress supports
        SNI.
    """
    backend: 'IngressBackend' = None
    ingressClassName: 'str' = None
    rules: 'List[IngressRule]' = None
    tls: 'List[IngressTLS]' = None


@dataclass
class IngressStatus(DataclassDictMixIn):
    """IngressStatus describe the current state of the Ingress.

      **parameters**

      * **loadBalancer** ``core_v1.LoadBalancerStatus`` - *(optional)* LoadBalancer contains the current status of the load-balancer.
    """
    loadBalancer: 'core_v1.LoadBalancerStatus' = None


@dataclass
class IngressTLS(DataclassDictMixIn):
    """IngressTLS describes the transport layer security associated with an Ingress.

      **parameters**

      * **hosts** ``List[str]`` - *(optional)* Hosts are a list of hosts included in the TLS certificate. The values in this
        list must match the name/s used in the tlsSecret. Defaults to the wildcard
        host setting for the loadbalancer controller fulfilling this Ingress, if left
        unspecified.
      * **secretName** ``str`` - *(optional)* SecretName is the name of the secret used to terminate SSL traffic on 443.
        Field is left optional to allow SSL routing based on SNI hostname alone. If
        the SNI host in a listener conflicts with the "Host" header field used by an
        IngressRule, the SNI host is used for termination and value of the Host header
        is used for routing.
    """
    hosts: 'List[str]' = None
    secretName: 'str' = None


