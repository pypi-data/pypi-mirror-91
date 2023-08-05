# autogenerated module
from dataclasses import dataclass, field
from typing import List

from ..core.dataclasses_dict import DataclassDictMixIn

from . import meta_v1


@dataclass
class LocalSubjectAccessReview(DataclassDictMixIn):
    """LocalSubjectAccessReview checks whether or not a user or group can perform an
      action in a given namespace. Having a namespace scoped resource makes it much
      easier to grant namespace scoped policy that includes permissions checking.

      **parameters**

      * **spec** ``SubjectAccessReviewSpec`` - Spec holds information about the request being evaluated.  spec.namespace must
        be equal to the namespace you made the request against.  If empty, it is
        defaulted.
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* 
      * **status** ``SubjectAccessReviewStatus`` - *(optional)* Status is filled in by the server and indicates whether the request is allowed
        or not
    """
    spec: 'SubjectAccessReviewSpec'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    status: 'SubjectAccessReviewStatus' = None


@dataclass
class NonResourceAttributes(DataclassDictMixIn):
    """NonResourceAttributes includes the authorization attributes available for
      non-resource requests to the Authorizer interface

      **parameters**

      * **path** ``str`` - *(optional)* Path is the URL path of the request
      * **verb** ``str`` - *(optional)* Verb is the standard HTTP verb
    """
    path: 'str' = None
    verb: 'str' = None


@dataclass
class NonResourceRule(DataclassDictMixIn):
    """NonResourceRule holds information that describes a rule for the non-resource

      **parameters**

      * **verbs** ``List[str]`` - Verb is a list of kubernetes non-resource API verbs, like: get, post, put,
        delete, patch, head, options.  "*" means all.
      * **nonResourceURLs** ``List[str]`` - *(optional)* NonResourceURLs is a set of partial urls that a user should have access to.
        *s are allowed, but only as the full, final step in the path.  "*" means all.
    """
    verbs: 'List[str]'
    nonResourceURLs: 'List[str]' = None


@dataclass
class ResourceAttributes(DataclassDictMixIn):
    """ResourceAttributes includes the authorization attributes available for
      resource requests to the Authorizer interface

      **parameters**

      * **group** ``str`` - *(optional)* Group is the API Group of the Resource.  "*" means all.
      * **name** ``str`` - *(optional)* Name is the name of the resource being requested for a "get" or deleted for a
        "delete". "" (empty) means all.
      * **namespace** ``str`` - *(optional)* Namespace is the namespace of the action being requested.  Currently, there is
        no distinction between no namespace and all namespaces "" (empty) is defaulted
        for LocalSubjectAccessReviews "" (empty) is empty for cluster-scoped resources
        "" (empty) means "all" for namespace scoped resources from a
        SubjectAccessReview or SelfSubjectAccessReview
      * **resource** ``str`` - *(optional)* Resource is one of the existing resource types.  "*" means all.
      * **subresource** ``str`` - *(optional)* Subresource is one of the existing resource types.  "" means none.
      * **verb** ``str`` - *(optional)* Verb is a kubernetes resource API verb, like: get, list, watch, create,
        update, delete, proxy.  "*" means all.
      * **version** ``str`` - *(optional)* Version is the API Version of the Resource.  "*" means all.
    """
    group: 'str' = None
    name: 'str' = None
    namespace: 'str' = None
    resource: 'str' = None
    subresource: 'str' = None
    verb: 'str' = None
    version: 'str' = None


@dataclass
class ResourceRule(DataclassDictMixIn):
    """ResourceRule is the list of actions the subject is allowed to perform on
      resources. The list ordering isn't significant, may contain duplicates, and
      possibly be incomplete.

      **parameters**

      * **verbs** ``List[str]`` - Verb is a list of kubernetes resource API verbs, like: get, list, watch,
        create, update, delete, proxy.  "*" means all.
      * **apiGroups** ``List[str]`` - *(optional)* APIGroups is the name of the APIGroup that contains the resources.  If
        multiple API groups are specified, any action requested against one of the
        enumerated resources in any API group will be allowed.  "*" means all.
      * **resourceNames** ``List[str]`` - *(optional)* ResourceNames is an optional white list of names that the rule applies to.  An
        empty set means that everything is allowed.  "*" means all.
      * **resources** ``List[str]`` - *(optional)* Resources is a list of resources this rule applies to.  "*" means all in the
        specified apiGroups.
         "*/foo" represents the subresource 'foo' for all resources in the specified
        apiGroups.
    """
    verbs: 'List[str]'
    apiGroups: 'List[str]' = None
    resourceNames: 'List[str]' = None
    resources: 'List[str]' = None


@dataclass
class SelfSubjectAccessReview(DataclassDictMixIn):
    """SelfSubjectAccessReview checks whether or the current user can perform an
      action.  Not filling in a spec.namespace means "in all namespaces".  Self is a
      special case, because users should always be able to check whether they can
      perform an action

      **parameters**

      * **spec** ``SelfSubjectAccessReviewSpec`` - Spec holds information about the request being evaluated.  user and groups
        must be empty
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* 
      * **status** ``SubjectAccessReviewStatus`` - *(optional)* Status is filled in by the server and indicates whether the request is allowed
        or not
    """
    spec: 'SelfSubjectAccessReviewSpec'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    status: 'SubjectAccessReviewStatus' = None


@dataclass
class SelfSubjectAccessReviewSpec(DataclassDictMixIn):
    """SelfSubjectAccessReviewSpec is a description of the access request.  Exactly
      one of ResourceAuthorizationAttributes and NonResourceAuthorizationAttributes
      must be set

      **parameters**

      * **nonResourceAttributes** ``NonResourceAttributes`` - *(optional)* NonResourceAttributes describes information for a non-resource access request
      * **resourceAttributes** ``ResourceAttributes`` - *(optional)* ResourceAuthorizationAttributes describes information for a resource access
        request
    """
    nonResourceAttributes: 'NonResourceAttributes' = None
    resourceAttributes: 'ResourceAttributes' = None


@dataclass
class SelfSubjectRulesReview(DataclassDictMixIn):
    """SelfSubjectRulesReview enumerates the set of actions the current user can
      perform within a namespace. The returned list of actions may be incomplete
      depending on the server's authorization mode, and any errors experienced
      during the evaluation. SelfSubjectRulesReview should be used by UIs to
      show/hide actions, or to quickly let an end user reason about their
      permissions. It should NOT Be used by external systems to drive authorization
      decisions as this raises confused deputy, cache lifetime/revocation, and
      correctness concerns. SubjectAccessReview, and LocalAccessReview are the
      correct way to defer authorization decisions to the API server.

      **parameters**

      * **spec** ``SelfSubjectRulesReviewSpec`` - Spec holds information about the request being evaluated.
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* 
      * **status** ``SubjectRulesReviewStatus`` - *(optional)* Status is filled in by the server and indicates the set of actions a user can
        perform.
    """
    spec: 'SelfSubjectRulesReviewSpec'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    status: 'SubjectRulesReviewStatus' = None


@dataclass
class SelfSubjectRulesReviewSpec(DataclassDictMixIn):
    """

      **parameters**

      * **namespace** ``str`` - *(optional)* Namespace to evaluate rules for. Required.
    """
    namespace: 'str' = None


@dataclass
class SubjectAccessReview(DataclassDictMixIn):
    """SubjectAccessReview checks whether or not a user or group can perform an
      action.

      **parameters**

      * **spec** ``SubjectAccessReviewSpec`` - Spec holds information about the request being evaluated
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* 
      * **status** ``SubjectAccessReviewStatus`` - *(optional)* Status is filled in by the server and indicates whether the request is allowed
        or not
    """
    spec: 'SubjectAccessReviewSpec'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    status: 'SubjectAccessReviewStatus' = None


@dataclass
class SubjectAccessReviewSpec(DataclassDictMixIn):
    """SubjectAccessReviewSpec is a description of the access request.  Exactly one
      of ResourceAuthorizationAttributes and NonResourceAuthorizationAttributes must
      be set

      **parameters**

      * **extra** ``dict`` - *(optional)* Extra corresponds to the user.Info.GetExtra() method from the authenticator.
        Since that is input to the authorizer it needs a reflection here.
      * **group** ``List[str]`` - *(optional)* Groups is the groups you're testing for.
      * **nonResourceAttributes** ``NonResourceAttributes`` - *(optional)* NonResourceAttributes describes information for a non-resource access request
      * **resourceAttributes** ``ResourceAttributes`` - *(optional)* ResourceAuthorizationAttributes describes information for a resource access
        request
      * **uid** ``str`` - *(optional)* UID information about the requesting user.
      * **user** ``str`` - *(optional)* User is the user you're testing for. If you specify "User" but not "Group",
        then is it interpreted as "What if User were not a member of any groups
    """
    extra: 'dict' = None
    group: 'List[str]' = None
    nonResourceAttributes: 'NonResourceAttributes' = None
    resourceAttributes: 'ResourceAttributes' = None
    uid: 'str' = None
    user: 'str' = None


@dataclass
class SubjectAccessReviewStatus(DataclassDictMixIn):
    """SubjectAccessReviewStatus

      **parameters**

      * **allowed** ``bool`` - Allowed is required. True if the action would be allowed, false otherwise.
      * **denied** ``bool`` - *(optional)* Denied is optional. True if the action would be denied, otherwise false. If
        both allowed is false and denied is false, then the authorizer has no opinion
        on whether to authorize the action. Denied may not be true if Allowed is true.
      * **evaluationError** ``str`` - *(optional)* EvaluationError is an indication that some error occurred during the
        authorization check. It is entirely possible to get an error and be able to
        continue determine authorization status in spite of it. For instance, RBAC can
        be missing a role, but enough roles are still present and bound to reason
        about the request.
      * **reason** ``str`` - *(optional)* Reason is optional.  It indicates why a request was allowed or denied.
    """
    allowed: 'bool'
    denied: 'bool' = None
    evaluationError: 'str' = None
    reason: 'str' = None


@dataclass
class SubjectRulesReviewStatus(DataclassDictMixIn):
    """SubjectRulesReviewStatus contains the result of a rules check. This check can
      be incomplete depending on the set of authorizers the server is configured
      with and any errors experienced during evaluation. Because authorization rules
      are additive, if a rule appears in a list it's safe to assume the subject has
      that permission, even if that list is incomplete.

      **parameters**

      * **incomplete** ``bool`` - Incomplete is true when the rules returned by this call are incomplete. This
        is most commonly encountered when an authorizer, such as an external
        authorizer, doesn't support rules evaluation.
      * **nonResourceRules** ``List[NonResourceRule]`` - NonResourceRules is the list of actions the subject is allowed to perform on
        non-resources. The list ordering isn't significant, may contain duplicates,
        and possibly be incomplete.
      * **resourceRules** ``List[ResourceRule]`` - ResourceRules is the list of actions the subject is allowed to perform on
        resources. The list ordering isn't significant, may contain duplicates, and
        possibly be incomplete.
      * **evaluationError** ``str`` - *(optional)* EvaluationError can appear in combination with Rules. It indicates an error
        occurred during rule evaluation, such as an authorizer that doesn't support
        rule evaluation, and that ResourceRules and/or NonResourceRules may be
        incomplete.
    """
    incomplete: 'bool'
    nonResourceRules: 'List[NonResourceRule]'
    resourceRules: 'List[ResourceRule]'
    evaluationError: 'str' = None


