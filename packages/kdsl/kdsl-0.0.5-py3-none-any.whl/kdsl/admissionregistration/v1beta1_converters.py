from __future__ import annotations
from kdsl.bases import OMIT, OmitEnum
from typing import Union, Sequence, Literal, Mapping
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import kdsl.admissionregistration.v1beta1


def optional_converter_RuleWithOperations(
    value: Union[
        kdsl.admissionregistration.v1beta1.RuleWithOperationsUnion, OmitEnum, None
    ]
) -> Union[kdsl.admissionregistration.v1beta1.RuleWithOperations, OmitEnum, None]:
    import kdsl.admissionregistration.v1beta1

    return (
        kdsl.admissionregistration.v1beta1.RuleWithOperations(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_MutatingWebhookItem(
    value: Union[
        kdsl.admissionregistration.v1beta1.MutatingWebhookItemUnion, OmitEnum, None
    ]
) -> Union[kdsl.admissionregistration.v1beta1.MutatingWebhookItem, OmitEnum, None]:
    import kdsl.admissionregistration.v1beta1

    return (
        kdsl.admissionregistration.v1beta1.MutatingWebhookItem(**value)
        if isinstance(value, dict)
        else value
    )


def optional_mlist_converter_ValidatingWebhookItem(
    value: Union[
        Mapping[str, kdsl.admissionregistration.v1beta1.ValidatingWebhookItemUnion],
        OmitEnum,
        None,
    ]
) -> Union[
    Mapping[str, kdsl.admissionregistration.v1beta1.ValidatingWebhookItem],
    OmitEnum,
    None,
]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {
            k: required_converter_ValidatingWebhookItem(v) for k, v in value.items()
        }


def required_converter_WebhookClientConfig(
    value: kdsl.admissionregistration.v1beta1.WebhookClientConfigUnion,
) -> kdsl.admissionregistration.v1beta1.WebhookClientConfig:
    import kdsl.admissionregistration.v1beta1

    return (
        kdsl.admissionregistration.v1beta1.WebhookClientConfig(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ServiceReference(
    value: Union[
        kdsl.admissionregistration.v1beta1.ServiceReferenceUnion, OmitEnum, None
    ]
) -> Union[kdsl.admissionregistration.v1beta1.ServiceReference, OmitEnum, None]:
    import kdsl.admissionregistration.v1beta1

    return (
        kdsl.admissionregistration.v1beta1.ServiceReference(**value)
        if isinstance(value, dict)
        else value
    )


def optional_mlist_converter_MutatingWebhookItem(
    value: Union[
        Mapping[str, kdsl.admissionregistration.v1beta1.MutatingWebhookItemUnion],
        OmitEnum,
        None,
    ]
) -> Union[
    Mapping[str, kdsl.admissionregistration.v1beta1.MutatingWebhookItem], OmitEnum, None
]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return {k: required_converter_MutatingWebhookItem(v) for k, v in value.items()}


def optional_converter_WebhookClientConfig(
    value: Union[
        kdsl.admissionregistration.v1beta1.WebhookClientConfigUnion, OmitEnum, None
    ]
) -> Union[kdsl.admissionregistration.v1beta1.WebhookClientConfig, OmitEnum, None]:
    import kdsl.admissionregistration.v1beta1

    return (
        kdsl.admissionregistration.v1beta1.WebhookClientConfig(**value)
        if isinstance(value, dict)
        else value
    )


def optional_list_converter_RuleWithOperations(
    value: Union[
        Sequence[kdsl.admissionregistration.v1beta1.RuleWithOperationsUnion],
        OmitEnum,
        None,
    ]
) -> Union[
    Sequence[kdsl.admissionregistration.v1beta1.RuleWithOperations], OmitEnum, None
]:
    if value is None:
        return None
    elif value is OMIT:
        return OMIT
    else:
        return [required_converter_RuleWithOperations(x) for x in value]


def required_converter_ValidatingWebhookItem(
    value: kdsl.admissionregistration.v1beta1.ValidatingWebhookItemUnion,
) -> kdsl.admissionregistration.v1beta1.ValidatingWebhookItem:
    import kdsl.admissionregistration.v1beta1

    return (
        kdsl.admissionregistration.v1beta1.ValidatingWebhookItem(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_RuleWithOperations(
    value: kdsl.admissionregistration.v1beta1.RuleWithOperationsUnion,
) -> kdsl.admissionregistration.v1beta1.RuleWithOperations:
    import kdsl.admissionregistration.v1beta1

    return (
        kdsl.admissionregistration.v1beta1.RuleWithOperations(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_MutatingWebhookItem(
    value: kdsl.admissionregistration.v1beta1.MutatingWebhookItemUnion,
) -> kdsl.admissionregistration.v1beta1.MutatingWebhookItem:
    import kdsl.admissionregistration.v1beta1

    return (
        kdsl.admissionregistration.v1beta1.MutatingWebhookItem(**value)
        if isinstance(value, dict)
        else value
    )


def required_converter_ServiceReference(
    value: kdsl.admissionregistration.v1beta1.ServiceReferenceUnion,
) -> kdsl.admissionregistration.v1beta1.ServiceReference:
    import kdsl.admissionregistration.v1beta1

    return (
        kdsl.admissionregistration.v1beta1.ServiceReference(**value)
        if isinstance(value, dict)
        else value
    )


def optional_converter_ValidatingWebhookItem(
    value: Union[
        kdsl.admissionregistration.v1beta1.ValidatingWebhookItemUnion, OmitEnum, None
    ]
) -> Union[kdsl.admissionregistration.v1beta1.ValidatingWebhookItem, OmitEnum, None]:
    import kdsl.admissionregistration.v1beta1

    return (
        kdsl.admissionregistration.v1beta1.ValidatingWebhookItem(**value)
        if isinstance(value, dict)
        else value
    )
