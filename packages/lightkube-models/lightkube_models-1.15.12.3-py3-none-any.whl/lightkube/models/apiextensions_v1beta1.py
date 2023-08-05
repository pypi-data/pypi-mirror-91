# autogenerated module
from dataclasses import dataclass, field
from typing import List

from ..core.dataclasses_dict import DataclassDictMixIn

from typing import Dict
from . import meta_v1
from typing import Any


@dataclass
class CustomResourceColumnDefinition(DataclassDictMixIn):
    """CustomResourceColumnDefinition specifies a column for server side printing.

      **parameters**

      * **JSONPath** ``str`` - JSONPath is a simple JSON path, i.e. with array notation.
      * **name** ``str`` - name is a human readable name for the column.
      * **type** ``str`` - type is an OpenAPI type definition for this column. See
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#data-types
        for more.
      * **description** ``str`` - *(optional)* description is a human readable description of this column.
      * **format** ``str`` - *(optional)* format is an optional OpenAPI type definition for this column. The 'name'
        format is applied to the primary identifier column to assist in clients
        identifying column is the resource name. See
        https://github.com/OAI/OpenAPI-Specification/blob/master/versions/2.0.md#data-types
        for more.
      * **priority** ``int`` - *(optional)* priority is an integer defining the relative importance of this column
        compared to others. Lower numbers are considered higher priority. Columns that
        may be omitted in limited space scenarios should be given a higher priority.
    """
    JSONPath: 'str'
    name: 'str'
    type: 'str'
    description: 'str' = None
    format: 'str' = None
    priority: 'int' = None


@dataclass
class CustomResourceConversion(DataclassDictMixIn):
    """CustomResourceConversion describes how to convert different versions of a CR.

      **parameters**

      * **strategy** ``str`` - `strategy` specifies the conversion strategy. Allowed values are: - `None`:
        The converter only change the apiVersion and would not touch any other field
        in the CR. - `Webhook`: API Server will call to an external webhook to do the
        conversion. Additional information
          is needed for this option. This requires spec.preserveUnknownFields to be
        false.
      * **conversionReviewVersions** ``List[str]`` - *(optional)* ConversionReviewVersions is an ordered list of preferred `ConversionReview`
        versions the Webhook expects. API server will try to use first version in the
        list which it supports. If none of the versions specified in this list
        supported by API server, conversion will fail for this object. If a persisted
        Webhook configuration specifies allowed versions and does not include any
        versions known to the API Server, calls to the webhook will fail. Default to
        `['v1beta1']`.
      * **webhookClientConfig** ``WebhookClientConfig`` - *(optional)* `webhookClientConfig` is the instructions for how to call the webhook if
        strategy is `Webhook`. This field is alpha-level and is only honored by
        servers that enable the CustomResourceWebhookConversion feature.
    """
    strategy: 'str'
    conversionReviewVersions: 'List[str]' = None
    webhookClientConfig: 'WebhookClientConfig' = None


@dataclass
class CustomResourceDefinition(DataclassDictMixIn):
    """CustomResourceDefinition represents a resource that should be exposed on the
      API server.  Its name MUST be in the format <.spec.name>.<.spec.group>.

      **parameters**

      * **spec** ``CustomResourceDefinitionSpec`` - Spec describes how the user wants the resources to appear
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* 
      * **status** ``CustomResourceDefinitionStatus`` - *(optional)* Status indicates the actual state of the CustomResourceDefinition
    """
    spec: 'CustomResourceDefinitionSpec'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    status: 'CustomResourceDefinitionStatus' = None


@dataclass
class CustomResourceDefinitionCondition(DataclassDictMixIn):
    """CustomResourceDefinitionCondition contains details for the current condition
      of this pod.

      **parameters**

      * **status** ``str`` - Status is the status of the condition. Can be True, False, Unknown.
      * **type** ``str`` - Type is the type of the condition. Types include Established, NamesAccepted
        and Terminating.
      * **lastTransitionTime** ``meta_v1.Time`` - *(optional)* Last time the condition transitioned from one status to another.
      * **message** ``str`` - *(optional)* Human-readable message indicating details about last transition.
      * **reason** ``str`` - *(optional)* Unique, one-word, CamelCase reason for the condition's last transition.
    """
    status: 'str'
    type: 'str'
    lastTransitionTime: 'meta_v1.Time' = None
    message: 'str' = None
    reason: 'str' = None


@dataclass
class CustomResourceDefinitionList(DataclassDictMixIn):
    """CustomResourceDefinitionList is a list of CustomResourceDefinition objects.

      **parameters**

      * **items** ``List[CustomResourceDefinition]`` - Items individual CustomResourceDefinitions
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ListMeta`` - *(optional)* 
    """
    items: 'List[CustomResourceDefinition]'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ListMeta' = None


@dataclass
class CustomResourceDefinitionNames(DataclassDictMixIn):
    """CustomResourceDefinitionNames indicates the names to serve this
      CustomResourceDefinition

      **parameters**

      * **kind** ``str`` - Kind is the serialized kind of the resource.  It is normally CamelCase and
        singular.
      * **plural** ``str`` - Plural is the plural name of the resource to serve.  It must match the name of
        the CustomResourceDefinition-registration too: plural.group and it must be all
        lowercase.
      * **categories** ``List[str]`` - *(optional)* Categories is a list of grouped resources custom resources belong to (e.g.
        'all')
      * **listKind** ``str`` - *(optional)* ListKind is the serialized kind of the list for this resource.  Defaults to
        <kind>List.
      * **shortNames** ``List[str]`` - *(optional)* ShortNames are short names for the resource.  It must be all lowercase.
      * **singular** ``str`` - *(optional)* Singular is the singular name of the resource.  It must be all lowercase
        Defaults to lowercased <kind>
    """
    kind: 'str'
    plural: 'str'
    categories: 'List[str]' = None
    listKind: 'str' = None
    shortNames: 'List[str]' = None
    singular: 'str' = None


@dataclass
class CustomResourceDefinitionSpec(DataclassDictMixIn):
    """CustomResourceDefinitionSpec describes how a user wants their resource to
      appear

      **parameters**

      * **group** ``str`` - Group is the group this resource belongs in
      * **names** ``CustomResourceDefinitionNames`` - Names are the names used to describe this custom resource
      * **scope** ``str`` - Scope indicates whether this resource is cluster or namespace scoped.  Default
        is namespaced
      * **additionalPrinterColumns** ``List[CustomResourceColumnDefinition]`` - *(optional)* AdditionalPrinterColumns are additional columns shown e.g. in kubectl next to
        the name. Defaults to a created-at column. Optional, the global columns for
        all versions. Top-level and per-version columns are mutually exclusive.
      * **conversion** ``CustomResourceConversion`` - *(optional)* `conversion` defines conversion settings for the CRD.
      * **preserveUnknownFields** ``bool`` - *(optional)* preserveUnknownFields disables pruning of object fields which are not
        specified in the OpenAPI schema. apiVersion, kind, metadata and known fields
        inside metadata are always preserved. Defaults to true in v1beta and will
        default to false in v1.
      * **subresources** ``CustomResourceSubresources`` - *(optional)* Subresources describes the subresources for CustomResource Optional, the
        global subresources for all versions. Top-level and per-version subresources
        are mutually exclusive.
      * **validation** ``CustomResourceValidation`` - *(optional)* Validation describes the validation methods for CustomResources Optional, the
        global validation schema for all versions. Top-level and per-version schemas
        are mutually exclusive.
      * **version** ``str`` - *(optional)* Version is the version this resource belongs in Should be always first item in
        Versions field if provided. Optional, but at least one of Version or Versions
        must be set. Deprecated: Please use `Versions`.
      * **versions** ``List[CustomResourceDefinitionVersion]`` - *(optional)* Versions is the list of all supported versions for this resource. If Version
        field is provided, this field is optional. Validation: All versions must use
        the same validation schema for now. i.e., top level Validation field is
        applied to all of these versions. Order: The version name will be used to
        compute the order. If the version string is "kube-like", it will sort above
        non "kube-like" version strings, which are ordered lexicographically.
        "Kube-like" versions start with a "v", then are followed by a number (the
        major version), then optionally the string "alpha" or "beta" and another
        number (the minor version). These are sorted first by GA > beta > alpha (where
        GA is a version with no suffix such as beta or alpha), and then by comparing
        major version, then minor version. An example sorted list of versions: v10,
        v2, v1, v11beta2, v10beta3, v3beta1, v12alpha1, v11alpha2, foo1, foo10.
    """
    group: 'str'
    names: 'CustomResourceDefinitionNames'
    scope: 'str'
    additionalPrinterColumns: 'List[CustomResourceColumnDefinition]' = None
    conversion: 'CustomResourceConversion' = None
    preserveUnknownFields: 'bool' = None
    subresources: 'CustomResourceSubresources' = None
    validation: 'CustomResourceValidation' = None
    version: 'str' = None
    versions: 'List[CustomResourceDefinitionVersion]' = None


@dataclass
class CustomResourceDefinitionStatus(DataclassDictMixIn):
    """CustomResourceDefinitionStatus indicates the state of the
      CustomResourceDefinition

      **parameters**

      * **acceptedNames** ``CustomResourceDefinitionNames`` - AcceptedNames are the names that are actually being used to serve discovery
        They may be different than the names in spec.
      * **conditions** ``List[CustomResourceDefinitionCondition]`` - Conditions indicate state for particular aspects of a CustomResourceDefinition
      * **storedVersions** ``List[str]`` - StoredVersions are all versions of CustomResources that were ever persisted.
        Tracking these versions allows a migration path for stored versions in etcd.
        The field is mutable so the migration controller can first finish a migration
        to another version (i.e. that no old objects are left in the storage), and
        then remove the rest of the versions from this list. None of the versions in
        this list can be removed from the spec.Versions field.
    """
    acceptedNames: 'CustomResourceDefinitionNames'
    conditions: 'List[CustomResourceDefinitionCondition]'
    storedVersions: 'List[str]'


@dataclass
class CustomResourceDefinitionVersion(DataclassDictMixIn):
    """CustomResourceDefinitionVersion describes a version for CRD.

      **parameters**

      * **name** ``str`` - Name is the version name, e.g. “v1”, “v2beta1”, etc.
      * **served** ``bool`` - Served is a flag enabling/disabling this version from being served via REST
        APIs
      * **storage** ``bool`` - Storage flags the version as storage version. There must be exactly one
        flagged as storage version.
      * **additionalPrinterColumns** ``List[CustomResourceColumnDefinition]`` - *(optional)* AdditionalPrinterColumns are additional columns shown e.g. in kubectl next to
        the name. Defaults to a created-at column. Top-level and per-version columns
        are mutually exclusive. Per-version columns must not all be set to identical
        values (top-level columns should be used instead) This field is alpha-level
        and is only honored by servers that enable the CustomResourceWebhookConversion
        feature. NOTE: CRDs created prior to 1.13 populated the top-level
        additionalPrinterColumns field by default. To apply an update that changes to
        per-version additionalPrinterColumns, the top-level additionalPrinterColumns
        field must be explicitly set to null
      * **schema** ``CustomResourceValidation`` - *(optional)* Schema describes the schema for CustomResource used in validation, pruning,
        and defaulting. Top-level and per-version schemas are mutually exclusive.
        Per-version schemas must not all be set to identical values (top-level
        validation schema should be used instead) This field is alpha-level and is
        only honored by servers that enable the CustomResourceWebhookConversion
        feature.
      * **subresources** ``CustomResourceSubresources`` - *(optional)* Subresources describes the subresources for CustomResource Top-level and
        per-version subresources are mutually exclusive. Per-version subresources must
        not all be set to identical values (top-level subresources should be used
        instead) This field is alpha-level and is only honored by servers that enable
        the CustomResourceWebhookConversion feature.
    """
    name: 'str'
    served: 'bool'
    storage: 'bool'
    additionalPrinterColumns: 'List[CustomResourceColumnDefinition]' = None
    schema: 'CustomResourceValidation' = None
    subresources: 'CustomResourceSubresources' = None


@dataclass
class CustomResourceSubresourceScale(DataclassDictMixIn):
    """CustomResourceSubresourceScale defines how to serve the scale subresource for
      CustomResources.

      **parameters**

      * **specReplicasPath** ``str`` - SpecReplicasPath defines the JSON path inside of a CustomResource that
        corresponds to Scale.Spec.Replicas. Only JSON paths without the array notation
        are allowed. Must be a JSON Path under .spec. If there is no value under the
        given path in the CustomResource, the /scale subresource will return an error
        on GET.
      * **statusReplicasPath** ``str`` - StatusReplicasPath defines the JSON path inside of a CustomResource that
        corresponds to Scale.Status.Replicas. Only JSON paths without the array
        notation are allowed. Must be a JSON Path under .status. If there is no value
        under the given path in the CustomResource, the status replica value in the
        /scale subresource will default to 0.
      * **labelSelectorPath** ``str`` - *(optional)* LabelSelectorPath defines the JSON path inside of a CustomResource that
        corresponds to Scale.Status.Selector. Only JSON paths without the array
        notation are allowed. Must be a JSON Path under .status or .spec. Must be set
        to work with HPA. The field pointed by this JSON path must be a string field
        (not a complex selector struct) which contains a serialized label selector in
        string form. More info:
        https://kubernetes.io/docs/tasks/access-kubernetes-api/custom-resources/custom-resource-definitions#scale-subresource
        If there is no value under the given path in the CustomResource, the status
        label selector value in the /scale subresource will default to the empty
        string.
    """
    specReplicasPath: 'str'
    statusReplicasPath: 'str'
    labelSelectorPath: 'str' = None


CustomResourceSubresourceStatus = Dict


@dataclass
class CustomResourceSubresources(DataclassDictMixIn):
    """CustomResourceSubresources defines the status and scale subresources for
      CustomResources.

      **parameters**

      * **scale** ``CustomResourceSubresourceScale`` - *(optional)* Scale denotes the scale subresource for CustomResources
      * **status** ``CustomResourceSubresourceStatus`` - *(optional)* Status denotes the status subresource for CustomResources
    """
    scale: 'CustomResourceSubresourceScale' = None
    status: 'CustomResourceSubresourceStatus' = None


@dataclass
class CustomResourceValidation(DataclassDictMixIn):
    """CustomResourceValidation is a list of validation methods for CustomResources.

      **parameters**

      * **openAPIV3Schema** ``JSONSchemaProps`` - *(optional)* OpenAPIV3Schema is the OpenAPI v3 schema to be validated against.
    """
    openAPIV3Schema: 'JSONSchemaProps' = None


@dataclass
class ExternalDocumentation(DataclassDictMixIn):
    """ExternalDocumentation allows referencing an external resource for extended
      documentation.

      **parameters**

      * **description** ``str`` - *(optional)* 
      * **url** ``str`` - *(optional)* 
    """
    description: 'str' = None
    url: 'str' = None


JSON = Any


@dataclass
class JSONSchemaProps(DataclassDictMixIn):
    """JSONSchemaProps is a JSON-Schema following Specification Draft 4
      (http://json-schema.org/).

      **parameters**

      * **d_ref** ``str`` - *(optional)* 
      * **d_schema** ``str`` - *(optional)* 
      * **additionalItems** ``JSONSchemaPropsOrBool`` - *(optional)* 
      * **additionalProperties** ``JSONSchemaPropsOrBool`` - *(optional)* 
      * **allOf** ``List[JSONSchemaProps]`` - *(optional)* 
      * **anyOf** ``List[JSONSchemaProps]`` - *(optional)* 
      * **default** ``JSON`` - *(optional)* default is a default value for undefined object fields. Defaulting is an alpha
        feature under the CustomResourceDefaulting feature gate. Defaulting requires
        spec.preserveUnknownFields to be false.
      * **definitions** ``dict`` - *(optional)* 
      * **dependencies** ``dict`` - *(optional)* 
      * **description** ``str`` - *(optional)* 
      * **enum** ``List[JSON]`` - *(optional)* 
      * **example** ``JSON`` - *(optional)* 
      * **exclusiveMaximum** ``bool`` - *(optional)* 
      * **exclusiveMinimum** ``bool`` - *(optional)* 
      * **externalDocs** ``ExternalDocumentation`` - *(optional)* 
      * **format** ``str`` - *(optional)* 
      * **id** ``str`` - *(optional)* 
      * **items** ``JSONSchemaPropsOrArray`` - *(optional)* 
      * **maxItems** ``int`` - *(optional)* 
      * **maxLength** ``int`` - *(optional)* 
      * **maxProperties** ``int`` - *(optional)* 
      * **maximum** ``float`` - *(optional)* 
      * **minItems** ``int`` - *(optional)* 
      * **minLength** ``int`` - *(optional)* 
      * **minProperties** ``int`` - *(optional)* 
      * **minimum** ``float`` - *(optional)* 
      * **multipleOf** ``float`` - *(optional)* 
      * **not_** ``JSONSchemaProps`` - *(optional)* 
      * **nullable** ``bool`` - *(optional)* 
      * **oneOf** ``List[JSONSchemaProps]`` - *(optional)* 
      * **pattern** ``str`` - *(optional)* 
      * **patternProperties** ``dict`` - *(optional)* 
      * **properties** ``dict`` - *(optional)* 
      * **required** ``List[str]`` - *(optional)* 
      * **title** ``str`` - *(optional)* 
      * **type** ``str`` - *(optional)* 
      * **uniqueItems** ``bool`` - *(optional)* 
      * **x_kubernetes_embedded_resource** ``bool`` - *(optional)* x-kubernetes-embedded-resource defines that the value is an embedded
        Kubernetes runtime.Object, with TypeMeta and ObjectMeta. The type must be
        object. It is allowed to further restrict the embedded object. kind,
        apiVersion and metadata are validated automatically.
        x-kubernetes-preserve-unknown-fields is allowed to be true, but does not have
        to be if the object is fully specified (up to kind, apiVersion, metadata).
      * **x_kubernetes_int_or_string** ``bool`` - *(optional)* x-kubernetes-int-or-string specifies that this value is either an integer or a
        string. If this is true, an empty type is allowed and type as child of anyOf
        is permitted if following one of the following patterns:
        1) anyOf:
           - type: integer
           - type: string
        2) allOf:
           - anyOf:
             - type: integer
             - type: string
           - ... zero or more
      * **x_kubernetes_preserve_unknown_fields** ``bool`` - *(optional)* x-kubernetes-preserve-unknown-fields stops the API server decoding step from
        pruning fields which are not specified in the validation schema. This affects
        fields recursively, but switches back to normal pruning behaviour if nested
        properties or additionalProperties are specified in the schema. This can
        either be true or undefined. False is forbidden.
    """
    d_ref: 'str' = field(metadata={"json": "$ref"}, default=None)
    d_schema: 'str' = field(metadata={"json": "$schema"}, default=None)
    additionalItems: 'JSONSchemaPropsOrBool' = None
    additionalProperties: 'JSONSchemaPropsOrBool' = None
    allOf: 'List[JSONSchemaProps]' = None
    anyOf: 'List[JSONSchemaProps]' = None
    default: 'JSON' = None
    definitions: 'dict' = None
    dependencies: 'dict' = None
    description: 'str' = None
    enum: 'List[JSON]' = None
    example: 'JSON' = None
    exclusiveMaximum: 'bool' = None
    exclusiveMinimum: 'bool' = None
    externalDocs: 'ExternalDocumentation' = None
    format: 'str' = None
    id: 'str' = None
    items: 'JSONSchemaPropsOrArray' = None
    maxItems: 'int' = None
    maxLength: 'int' = None
    maxProperties: 'int' = None
    maximum: 'float' = None
    minItems: 'int' = None
    minLength: 'int' = None
    minProperties: 'int' = None
    minimum: 'float' = None
    multipleOf: 'float' = None
    not_: 'JSONSchemaProps' = field(metadata={"json": "not"}, default=None)
    nullable: 'bool' = None
    oneOf: 'List[JSONSchemaProps]' = None
    pattern: 'str' = None
    patternProperties: 'dict' = None
    properties: 'dict' = None
    required: 'List[str]' = None
    title: 'str' = None
    type: 'str' = None
    uniqueItems: 'bool' = None
    x_kubernetes_embedded_resource: 'bool' = field(metadata={"json": "x-kubernetes-embedded-resource"}, default=None)
    x_kubernetes_int_or_string: 'bool' = field(metadata={"json": "x-kubernetes-int-or-string"}, default=None)
    x_kubernetes_preserve_unknown_fields: 'bool' = field(metadata={"json": "x-kubernetes-preserve-unknown-fields"}, default=None)


JSONSchemaPropsOrArray = Any


JSONSchemaPropsOrBool = Any


JSONSchemaPropsOrStringArray = Any


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
class WebhookClientConfig(DataclassDictMixIn):
    """WebhookClientConfig contains the information to make a TLS connection with the
      webhook. It has the same field as
      admissionregistration.v1beta1.WebhookClientConfig.

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


