from typing import Any, Callable, Dict, Optional, Union

import attr

from ..types import UNSET, Unset
from ..util.serialization import is_not_none


@attr.s(auto_attribs=True)
class ClientApplication:
    """  """

    latest_version: str
    name: str
    supported: bool
    details_uri: Union[Unset, str] = UNSET
    minimum_version: Union[Unset, str] = UNSET

    def to_dict(self, pick_by_predicate: Optional[Callable[[Any], bool]] = is_not_none) -> Dict[str, Any]:
        latest_version = self.latest_version
        name = self.name
        supported = self.supported
        details_uri = self.details_uri
        minimum_version = self.minimum_version

        dct = {
            "latestVersion": latest_version,
            "name": name,
            "supported": supported,
            "detailsUri": details_uri,
            "minimumVersion": minimum_version,
        }
        if pick_by_predicate is not None:
            dct = {k: v for k, v in dct.items() if pick_by_predicate(v)}
        return dct

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "ClientApplication":
        latest_version = d["latestVersion"]

        name = d["name"]

        supported = d["supported"]

        details_uri = d.get("detailsUri")

        minimum_version = d.get("minimumVersion")

        return ClientApplication(
            latest_version=latest_version,
            name=name,
            supported=supported,
            details_uri=details_uri,
            minimum_version=minimum_version,
        )
