# autogenerated module
from dataclasses import dataclass, field
from typing import List

from ..core.dataclasses_dict import DataclassDictMixIn

from . import core_v1
from . import batch_v1
from . import meta_v1


@dataclass
class CronJob(DataclassDictMixIn):
    """CronJob represents the configuration of a single cron job.

      **parameters**

      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* Standard object's metadata. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#metadata
      * **spec** ``CronJobSpec`` - *(optional)* Specification of the desired behavior of a cron job, including the schedule.
        More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#spec-and-status
      * **status** ``CronJobStatus`` - *(optional)* Current status of a cron job. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#spec-and-status
    """
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ObjectMeta' = None
    spec: 'CronJobSpec' = None
    status: 'CronJobStatus' = None


@dataclass
class CronJobList(DataclassDictMixIn):
    """CronJobList is a collection of cron jobs.

      **parameters**

      * **items** ``List[CronJob]`` - items is the list of CronJobs.
      * **apiVersion** ``str`` - *(optional)* APIVersion defines the versioned schema of this representation of an object.
        Servers should convert recognized schemas to the latest internal value, and
        may reject unrecognized values. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#resources
      * **kind** ``str`` - *(optional)* Kind is a string value representing the REST resource this object represents.
        Servers may infer this from the endpoint the client submits requests to.
        Cannot be updated. In CamelCase. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#types-kinds
      * **metadata** ``meta_v1.ListMeta`` - *(optional)* Standard list metadata. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#metadata
    """
    items: 'List[CronJob]'
    apiVersion: 'str' = None
    kind: 'str' = None
    metadata: 'meta_v1.ListMeta' = None


@dataclass
class CronJobSpec(DataclassDictMixIn):
    """CronJobSpec describes how the job execution will look like and when it will
      actually run.

      **parameters**

      * **jobTemplate** ``JobTemplateSpec`` - Specifies the job that will be created when executing a CronJob.
      * **schedule** ``str`` - The schedule in Cron format, see https://en.wikipedia.org/wiki/Cron.
      * **concurrencyPolicy** ``str`` - *(optional)* Specifies how to treat concurrent executions of a Job. Valid values are: -
        "Allow" (default): allows CronJobs to run concurrently; - "Forbid": forbids
        concurrent runs, skipping next run if previous run hasn't finished yet; -
        "Replace": cancels currently running job and replaces it with a new one
      * **failedJobsHistoryLimit** ``int`` - *(optional)* The number of failed finished jobs to retain. This is a pointer to distinguish
        between explicit zero and not specified. Defaults to 1.
      * **startingDeadlineSeconds** ``int`` - *(optional)* Optional deadline in seconds for starting the job if it misses scheduled time
        for any reason.  Missed jobs executions will be counted as failed ones.
      * **successfulJobsHistoryLimit** ``int`` - *(optional)* The number of successful finished jobs to retain. This is a pointer to
        distinguish between explicit zero and not specified. Defaults to 3.
      * **suspend** ``bool`` - *(optional)* This flag tells the controller to suspend subsequent executions, it does not
        apply to already started executions.  Defaults to false.
    """
    jobTemplate: 'JobTemplateSpec'
    schedule: 'str'
    concurrencyPolicy: 'str' = None
    failedJobsHistoryLimit: 'int' = None
    startingDeadlineSeconds: 'int' = None
    successfulJobsHistoryLimit: 'int' = None
    suspend: 'bool' = None


@dataclass
class CronJobStatus(DataclassDictMixIn):
    """CronJobStatus represents the current state of a cron job.

      **parameters**

      * **active** ``List[core_v1.ObjectReference]`` - *(optional)* A list of pointers to currently running jobs.
      * **lastScheduleTime** ``meta_v1.Time`` - *(optional)* Information when was the last time the job was successfully scheduled.
    """
    active: 'List[core_v1.ObjectReference]' = None
    lastScheduleTime: 'meta_v1.Time' = None


@dataclass
class JobTemplateSpec(DataclassDictMixIn):
    """JobTemplateSpec describes the data a Job should have when created from a
      template

      **parameters**

      * **metadata** ``meta_v1.ObjectMeta`` - *(optional)* Standard object's metadata of the jobs created from this template. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#metadata
      * **spec** ``batch_v1.JobSpec`` - *(optional)* Specification of the desired behavior of the job. More info:
        https://git.k8s.io/community/contributors/devel/api-conventions.md#spec-and-status
    """
    metadata: 'meta_v1.ObjectMeta' = None
    spec: 'batch_v1.JobSpec' = None


