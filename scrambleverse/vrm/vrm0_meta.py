from typing import TypedDict, Literal

__all__ = ["VRM0Meta", "VRM0Extension"]


class VRM0MetaRequired(TypedDict):
    allowedUserName: Literal["OnlyAuthor", "ExplicitlyLicensedPerson", "Everyone"]
    author: str
    commercialUssageName: Literal["Disallow", "Allow"]
    licenseName: Literal[
        "Redistribution_Prohibited",
        "CC0",
        "CC_BY",
        "CC_BY_NC",
        "CC_BY_SA",
        "CC_BY_NC_SA",
        "CC_BY_ND",
        "CC_NY_NC_ND",
        "Other",
    ]
    sexualUssageName: Literal["Disallow", "Allow"]
    texture: int
    title: str
    violentUssageName: Literal["Disallow", "Allow"]


class VRM0Meta(VRM0MetaRequired, total=False):
    contactInformation: str
    otherLicenseUrl: str
    otherPermissionUrl: str
    reference: str
    version: str


class VRM0Extension(TypedDict):
    meta: VRM0Meta
