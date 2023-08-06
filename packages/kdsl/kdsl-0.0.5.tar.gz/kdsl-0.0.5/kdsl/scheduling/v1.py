from __future__ import annotations
import kdsl.core.v1_converters
import attr
import kdsl.core.v1
from kdsl.bases import OMIT, K8sObject, K8sResource, OmitEnum
from typing import Union, TypedDict, Sequence, ClassVar, Any, Mapping, Optional


@attr.s(kw_only=True)
class PriorityClass(K8sResource):
    apiVersion: ClassVar[str] = "scheduling.k8s.io/v1"
    kind: ClassVar[str] = "PriorityClass"
    value: int = attr.ib(metadata={"yaml_name": "value"})
    description: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "description"}, default=OMIT
    )
    globalDefault: Union[None, OmitEnum, bool] = attr.ib(
        metadata={"yaml_name": "globalDefault"}, default=OMIT
    )
    metadata: Union[None, OmitEnum, kdsl.core.v1.ObjectMeta] = attr.ib(
        metadata={"yaml_name": "metadata"},
        converter=kdsl.core.v1_converters.optional_converter_ObjectMeta,
        default=OMIT,
    )
    preemptionPolicy: Union[None, OmitEnum, str] = attr.ib(
        metadata={"yaml_name": "preemptionPolicy"}, default=OMIT
    )
