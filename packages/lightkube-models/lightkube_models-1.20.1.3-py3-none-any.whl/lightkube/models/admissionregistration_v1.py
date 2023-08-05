# autogenerated module
from dataclasses import dataclass, field
from typing import List

from ..core.dataclasses_dict import DataclassDictMixIn

from . import meta_v1


@dataclass
class MutatingWebhook(DataclassDictMixIn):
    """MutatingWebhook describes an admission webhook and the resources and
      operations it applies to.

      **parameters**

      * **admissionReviewVersions** ``List[str]`` - AdmissionReviewVersions is an ordered list of preferred `AdmissionReview`
        versions the Webhook expects. API server will try to use first version in the
        list which it supports. If none of the versions specified in this list
        supported by API server, validation will fail for this object. If a persisted
        webhook configuration specifies allowed versions and does not include any
        versions known to the API Server, calls to the webhook will fail and be
        subject to the failure policy.
      * **clientConfig** ``WebhookClientConfig`` - ClientConfig defines how to communicate with the hook. Required
      * **name** ``str`` - The name of the admission webhook. Name should be fully qualified, e.g.,
        imagepolicy.kubernetes.io, where "imagepolicy" is the name of the webhook, and
        kubernetes.io is the name of the organization. Required.
      * **sideEffects** ``str`` - SideEffects states whether this webhook has side effects. Acceptable values
        are: None, NoneOnDryRun (webhooks created via v1beta1 may also specify Some or
        Unknown). Webhooks with side effects MUST implement a reconciliation system,
        since a request may be rejected by a future step in the admission change and
        the side effects therefore need to be undone. Requests with the dryRun
        attribute will be auto-rejected if they match a webhook with sideEffects ==
        Unknown or Some.
      * **failurePolicy** ``str`` - *(optional)* FailurePolicy defines how unrecognized errors from the admission endpoint are
        handled - allowed values are Ignore or Fail. Defaults to Fail.
      * **matchPolicy** ``str`` - *(optional)* matchPolicy defines how the "rules" list is used to match incoming requests.
        Allowed values are "Exact" or "Equivalent".
        - Exact: match a request only if it exactly matches a specified rule. For
        example, if deployments can be modified via apps/v1, apps/v1beta1, and
        extensions/v1beta1, but "rules" only included `apiGroups:["apps"],
        apiVersions:["v1"], resources: ["deployments"]`, a request to apps/v1beta1 or
        extensions/v1beta1 would not be sent to the webhook.
        - Equivalent: match a request if modifies a resource listed in rules, even via
        another API group or version. For example, if deployments can be modified via
        apps/v1, apps/v1beta1, and extensions/v1beta1, and "rules" only included
        `apiGroups:["apps"], apiVersions:["v1"], resources: ["deployments"]`, a
        request to apps/v1beta1 or extensions/v1beta1 would be converted to apps/v1
        and sent to the webhook.
        Defaults to "Equivalent"
      * **namespaceSelector** ``meta_v1.LabelSelector`` - *(optional)* NamespaceSelector decides whether to run the webhook on an object based on
        whether the namespace for that object matches the selector. If the object
        itself is a namespace, the matching is performed on object.metadata.labels. If
        the object is another cluster scoped resource, it never skips the webhook.
        For example, to run the webhook on any objects whose namespace is not
        associated with "runlevel" of "0" or "1";  you will set the selector as
        follows: "namespaceSelector": {
          "matchExpressions": [
            {
              "key": "runlevel",
              "operator": "NotIn",
              "values": [
                "0",
                "1"
              ]
            }
          ]
        }
        If instead you want to only run the webhook on any objects whose namespace is
        associated with the "environment" of "prod" or "staging"; you will set the
        selector as follows: "namespaceSelector": {
          "matchExpressions": [
            {
              "key": "environment",
              "operator": "In",
              "values": [
                "prod",
                "staging"
              ]
            }
          ]
        }
        See https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/
        for more examples of label selectors.
        Default to the empty LabelSelector, which matches everything.
      * **objectSelector** ``meta_v1.LabelSelector`` - *(optional)* ObjectSelector decides whether to run the webhook based on if the object has
        matching labels. objectSelector is evaluated against both the oldObject and
        newObject that would be sent to the webhook, and is considered to match if
        either object matches the selector. A null object (oldObject in the case of
        create, or newObject in the case of delete) or an object that cannot have
        labels (like a DeploymentRollback or a PodProxyOptions object) is not
        considered to match. Use the object selector only if the webhook is opt-in,
        because end users may skip the admission webhook by setting the labels.
        Default to the empty LabelSelector, which matches everything.
      * **reinvocationPolicy** ``str`` - *(optional)* reinvocationPolicy indicates whether this webhook should be called multiple
        times as part of a single admission evaluation. Allowed values are "Never" and
        "IfNeeded".
        Never: the webhook will not be called more than once in a single admission
        evaluation.
        IfNeeded: the webhook will be called at least one additional time as part of
        the admission evaluation if the object being admitted is modified by other
        admission plugins after the initial webhook call. Webhooks that specify this
        option *must* be idempotent, able to process objects they previously admitted.
        Note: * the number of additional invocations is not guaranteed to be exactly
        one. * if additional invocations result in further modifications to the
        object, webhooks are not guaranteed to be invoked again. * webhooks that use
        this option may be reordered to minimize the number of additional invocations.
        * to validate an object after all mutations are guaranteed complete, use a
        validating admission webhook instead.
        Defaults to "Never".
      * **rules** ``List[RuleWithOperations]`` - *(optional)* Rules describes what operations on what resources/subresources the webhook
        cares about. The webhook cares about an operation if it matches _any_ Rule.
        However, in order to prevent ValidatingAdmissionWebhooks and
        MutatingAdmissionWebhooks from putting the cluster in a state which cannot be
        recovered from without completely disabling the plugin,
        ValidatingAdmissionWebhooks and MutatingAdmissionWebhooks are never called on
        admission requests for ValidatingWebhookConfiguration and
        MutatingWebhookConfiguration objects.
      * **timeoutSeconds** ``int`` - *(optional)* TimeoutSeconds specifies the timeout for this webhook. After the timeout
        passes, the webhook call will be ignored or the API call will fail based on
        the failure policy. The timeout value must be between 1 and 30 seconds.
        Default to 10 seconds.
    """
    admissionReviewVersions: 'List[str]'
    clientConfig: 'WebhookClientConfig'
    name: 'str'
    sideEffects: 'str'
    failurePolicy: 'str' = None
    matchPolicy: 'str' = None
    namespaceSelector: 'meta_v1.LabelSelector' = None
    objectSelector: 'meta_v1.LabelSelector' = None
    reinvocationPolicy: 'str' = None
    rules: 'List[RuleWithOperations]' = None
    timeoutSeconds: 'int' = None


@dataclass
class MutatingWebhookConfiguration(DataclassDictMixIn):
    """MutatingWebhookConfiguration describes the configuration of and admission
      webhook that accept or reject and may change the object.

      **parameters**

      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* Standard object metadata; More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.
      * **webhooks** ``List[MutatingWebhook]`` - *(optional)* Webhooks is a list of webhooks and the affected resources and operations.
    """
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    webhooks: 'List[MutatingWebhook]' = None


@dataclass
class MutatingWebhookConfigurationList(DataclassDictMixIn):
    """MutatingWebhookConfigurationList is a list of MutatingWebhookConfiguration.

      **parameters**

      * **items** ``List[MutatingWebhookConfiguration]`` - List of MutatingWebhookConfiguration.
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ListMeta`` - *(optional)* Standard list metadata. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
    """
    items: 'List[MutatingWebhookConfiguration]'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ListMeta' = None


@dataclass
class RuleWithOperations(DataclassDictMixIn):
    """RuleWithOperations is a tuple of Operations and Resources. It is recommended
      to make sure that all the tuple expansions are valid.

      **parameters**

      * **apiGroups** ``List[str]`` - *(optional)* APIGroups is the API groups the resources belong to. '*' is all groups. If '*'
        is present, the length of the slice must be one. Required.
      * **apiVersions** ``List[str]`` - *(optional)* APIVersions is the API versions the resources belong to. '*' is all versions.
        If '*' is present, the length of the slice must be one. Required.
      * **operations** ``List[str]`` - *(optional)* Operations is the operations the admission hook cares about - CREATE, UPDATE,
        DELETE, CONNECT or * for all of those operations and any future admission
        operations that are added. If '*' is present, the length of the slice must be
        one. Required.
      * **resources** ``List[str]`` - *(optional)* Resources is a list of resources this rule applies to.
        For example: 'pods' means pods. 'pods/log' means the log subresource of pods.
        '*' means all resources, but not subresources. 'pods/*' means all subresources
        of pods. '*/scale' means all scale subresources. '*/*' means all resources and
        their subresources.
        If wildcard is present, the validation rule will ensure resources do not
        overlap with each other.
        Depending on the enclosing object, subresources might not be allowed.
        Required.
      * **scope** ``str`` - *(optional)* scope specifies the scope of this rule. Valid values are "Cluster",
        "Namespaced", and "*" "Cluster" means that only cluster-scoped resources will
        match this rule. Namespace API objects are cluster-scoped. "Namespaced" means
        that only namespaced resources will match this rule. "*" means that there are
        no scope restrictions. Subresources match the scope of their parent resource.
        Default is "*".
    """
    apiGroups: 'List[str]' = None
    apiVersions: 'List[str]' = None
    operations: 'List[str]' = None
    resources: 'List[str]' = None
    scope: 'str' = None


@dataclass
class ServiceReference(DataclassDictMixIn):
    """ServiceReference holds a reference to Service.legacy.k8s.io

      **parameters**

      * **name** ``str`` - `name` is the name of the service. Required
      * **namespace** ``str`` - `namespace` is the namespace of the service. Required
      * **path** ``str`` - *(optional)* `path` is an optional URL path which will be sent in any request to this
        service.
      * **port** ``int`` - *(optional)* If specified, the port on the service that hosting webhook. Default to 443 for
        backward compatibility. `port` should be a valid port number (1-65535,
        inclusive).
    """
    name: 'str'
    namespace: 'str'
    path: 'str' = None
    port: 'int' = None


@dataclass
class ValidatingWebhook(DataclassDictMixIn):
    """ValidatingWebhook describes an admission webhook and the resources and
      operations it applies to.

      **parameters**

      * **admissionReviewVersions** ``List[str]`` - AdmissionReviewVersions is an ordered list of preferred `AdmissionReview`
        versions the Webhook expects. API server will try to use first version in the
        list which it supports. If none of the versions specified in this list
        supported by API server, validation will fail for this object. If a persisted
        webhook configuration specifies allowed versions and does not include any
        versions known to the API Server, calls to the webhook will fail and be
        subject to the failure policy.
      * **clientConfig** ``WebhookClientConfig`` - ClientConfig defines how to communicate with the hook. Required
      * **name** ``str`` - The name of the admission webhook. Name should be fully qualified, e.g.,
        imagepolicy.kubernetes.io, where "imagepolicy" is the name of the webhook, and
        kubernetes.io is the name of the organization. Required.
      * **sideEffects** ``str`` - SideEffects states whether this webhook has side effects. Acceptable values
        are: None, NoneOnDryRun (webhooks created via v1beta1 may also specify Some or
        Unknown). Webhooks with side effects MUST implement a reconciliation system,
        since a request may be rejected by a future step in the admission change and
        the side effects therefore need to be undone. Requests with the dryRun
        attribute will be auto-rejected if they match a webhook with sideEffects ==
        Unknown or Some.
      * **failurePolicy** ``str`` - *(optional)* FailurePolicy defines how unrecognized errors from the admission endpoint are
        handled - allowed values are Ignore or Fail. Defaults to Fail.
      * **matchPolicy** ``str`` - *(optional)* matchPolicy defines how the "rules" list is used to match incoming requests.
        Allowed values are "Exact" or "Equivalent".
        - Exact: match a request only if it exactly matches a specified rule. For
        example, if deployments can be modified via apps/v1, apps/v1beta1, and
        extensions/v1beta1, but "rules" only included `apiGroups:["apps"],
        apiVersions:["v1"], resources: ["deployments"]`, a request to apps/v1beta1 or
        extensions/v1beta1 would not be sent to the webhook.
        - Equivalent: match a request if modifies a resource listed in rules, even via
        another API group or version. For example, if deployments can be modified via
        apps/v1, apps/v1beta1, and extensions/v1beta1, and "rules" only included
        `apiGroups:["apps"], apiVersions:["v1"], resources: ["deployments"]`, a
        request to apps/v1beta1 or extensions/v1beta1 would be converted to apps/v1
        and sent to the webhook.
        Defaults to "Equivalent"
      * **namespaceSelector** ``meta_v1.LabelSelector`` - *(optional)* NamespaceSelector decides whether to run the webhook on an object based on
        whether the namespace for that object matches the selector. If the object
        itself is a namespace, the matching is performed on object.metadata.labels. If
        the object is another cluster scoped resource, it never skips the webhook.
        For example, to run the webhook on any objects whose namespace is not
        associated with "runlevel" of "0" or "1";  you will set the selector as
        follows: "namespaceSelector": {
          "matchExpressions": [
            {
              "key": "runlevel",
              "operator": "NotIn",
              "values": [
                "0",
                "1"
              ]
            }
          ]
        }
        If instead you want to only run the webhook on any objects whose namespace is
        associated with the "environment" of "prod" or "staging"; you will set the
        selector as follows: "namespaceSelector": {
          "matchExpressions": [
            {
              "key": "environment",
              "operator": "In",
              "values": [
                "prod",
                "staging"
              ]
            }
          ]
        }
        See https://kubernetes.io/docs/concepts/overview/working-with-objects/labels
        for more examples of label selectors.
        Default to the empty LabelSelector, which matches everything.
      * **objectSelector** ``meta_v1.LabelSelector`` - *(optional)* ObjectSelector decides whether to run the webhook based on if the object has
        matching labels. objectSelector is evaluated against both the oldObject and
        newObject that would be sent to the webhook, and is considered to match if
        either object matches the selector. A null object (oldObject in the case of
        create, or newObject in the case of delete) or an object that cannot have
        labels (like a DeploymentRollback or a PodProxyOptions object) is not
        considered to match. Use the object selector only if the webhook is opt-in,
        because end users may skip the admission webhook by setting the labels.
        Default to the empty LabelSelector, which matches everything.
      * **rules** ``List[RuleWithOperations]`` - *(optional)* Rules describes what operations on what resources/subresources the webhook
        cares about. The webhook cares about an operation if it matches _any_ Rule.
        However, in order to prevent ValidatingAdmissionWebhooks and
        MutatingAdmissionWebhooks from putting the cluster in a state which cannot be
        recovered from without completely disabling the plugin,
        ValidatingAdmissionWebhooks and MutatingAdmissionWebhooks are never called on
        admission requests for ValidatingWebhookConfiguration and
        MutatingWebhookConfiguration objects.
      * **timeoutSeconds** ``int`` - *(optional)* TimeoutSeconds specifies the timeout for this webhook. After the timeout
        passes, the webhook call will be ignored or the API call will fail based on
        the failure policy. The timeout value must be between 1 and 30 seconds.
        Default to 10 seconds.
    """
    admissionReviewVersions: 'List[str]'
    clientConfig: 'WebhookClientConfig'
    name: 'str'
    sideEffects: 'str'
    failurePolicy: 'str' = None
    matchPolicy: 'str' = None
    namespaceSelector: 'meta_v1.LabelSelector' = None
    objectSelector: 'meta_v1.LabelSelector' = None
    rules: 'List[RuleWithOperations]' = None
    timeoutSeconds: 'int' = None


@dataclass
class ValidatingWebhookConfiguration(DataclassDictMixIn):
    """ValidatingWebhookConfiguration describes the configuration of and admission
      webhook that accept or reject and object without changing it.

      **parameters**

      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* Standard object metadata; More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#metadata.
      * **webhooks** ``List[ValidatingWebhook]`` - *(optional)* Webhooks is a list of webhooks and the affected resources and operations.
    """
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    webhooks: 'List[ValidatingWebhook]' = None


@dataclass
class ValidatingWebhookConfigurationList(DataclassDictMixIn):
    """ValidatingWebhookConfigurationList is a list of
      ValidatingWebhookConfiguration.

      **parameters**

      * **items** ``List[ValidatingWebhookConfiguration]`` - List of ValidatingWebhookConfiguration.
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ListMeta`` - *(optional)* Standard list metadata. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
    """
    items: 'List[ValidatingWebhookConfiguration]'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ListMeta' = None


@dataclass
class WebhookClientConfig(DataclassDictMixIn):
    """WebhookClientConfig contains the information to make a TLS connection with the
      webhook

      **parameters**

      * **caBundle** ``str`` - *(optional)* `caBundle` is a PEM encoded CA bundle which will be used to validate the
        webhook's server certificate. If unspecified, system trust roots on the
        apiserver are used.
      * **service** ``ServiceReference`` - *(optional)* `service` is a reference to the service for this webhook. Either `service` or
        `url` must be specified.
        If the webhook is running within the cluster, then you should use `service`.
      * **url** ``str`` - *(optional)* `url` gives the location of the webhook, in standard URL form
        (`scheme://host:port/path`). Exactly one of `url` or `service` must be
        specified.
        The `host` should not refer to a service running in the cluster; use the
        `service` field instead. The host might be resolved via external DNS in some
        apiservers (e.g., `kube-apiserver` cannot resolve in-cluster DNS as that would
        be a layering violation). `host` may also be an IP address.
        Please note that using `localhost` or `127.0.0.1` as a `host` is risky unless
        you take great care to run this webhook on all hosts which run an apiserver
        which might need to make calls to this webhook. Such installs are likely to be
        non-portable, i.e., not easy to turn up in a new cluster.
        The scheme must be "https"; the URL must begin with "https://".
        A path is optional, and if present may be any string permissible in a URL. You
        may use the path to pass an arbitrary string to the webhook, for example, a
        cluster identifier.
        Attempting to use a user or basic auth e.g. "user:password@" is not allowed.
        Fragments ("#...") and query parameters ("?...") are not allowed, either.
    """
    caBundle: 'str' = None
    service: 'ServiceReference' = None
    url: 'str' = None


