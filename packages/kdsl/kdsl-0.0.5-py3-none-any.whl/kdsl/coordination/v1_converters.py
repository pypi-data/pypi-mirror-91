from __future__ import annotations
from kdsl.bases import OMIT, OmitEnum
from typing import Union, Literal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.coordination.v1


def optional_converter_LeaseSpec(
    value: Union[kdsl.coordination.v1.LeaseSpecUnion, OmitEnum, None]
) -> Union[kdsl.coordination.v1.LeaseSpec, OmitEnum, None]:
    import kdsl.coordination.v1

    return kdsl.coordination.v1.LeaseSpec(**value) if isinstance(value, dict) else value


def required_converter_LeaseSpec(
    value: kdsl.coordination.v1.LeaseSpecUnion,
) -> kdsl.coordination.v1.LeaseSpec:
    import kdsl.coordination.v1

    return kdsl.coordination.v1.LeaseSpec(**value) if isinstance(value, dict) else value
