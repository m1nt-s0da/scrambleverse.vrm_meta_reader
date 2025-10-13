from typing import TypedDict, Literal

__all__ = ["VRM1Meta", "VRM1Extension"]


class VRM1MetaRequired(TypedDict):
    name: str
    authors: list[str]
    licenseUrl: str


class VRM1Meta(VRM1MetaRequired, total=False):
    version: str
    copyrightInformation: str
    contactInformation: str
    references: list[str]
    thirdPartyLicenses: str
    thumbnailImage: int
    avatarPermission: Literal["onlyAuthor", "onlySeparatelyLicensedPerson", "everyone"]
    allowExcessivelyViolentUsage: bool
    allowExcessivelySexualUsage: bool
    commercialUsage: Literal["personalNonProfit", "personalProfit", "corporation"]
    allowPoliticalOrReligiousUsage: bool
    allowAntisocialOrHateUsage: bool
    creditNotation: Literal["required", "unnecessary"]
    allowRedistribution: bool
    modification: Literal[
        "prohibited", "allowModification", "allowModificationRedistribution"
    ]
    otherLicenseUrl: str


class VRM1Extension(TypedDict):
    meta: VRM1Meta
