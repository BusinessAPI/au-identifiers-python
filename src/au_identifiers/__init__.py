"""Validate and format Australian business identifiers: ABN, ACN, ARBN, TFN, Director ID and VIN."""

from __future__ import annotations

import re

__all__ = [
    "is_valid_abn", "normalise_abn", "format_abn",
    "is_valid_acn", "normalise_acn", "format_acn",
    "is_valid_arbn", "normalise_arbn", "format_arbn",
    "is_valid_tfn", "normalise_tfn",
    "is_valid_director_id", "normalise_director_id",
    "is_valid_vin", "normalise_vin",
]
__version__ = "0.1.0"

_SEPARATORS = re.compile(r"[ \t\n\r\v\f-]")
_ABN_WEIGHTS = (10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19)
_ACN_WEIGHTS = (8, 7, 6, 5, 4, 3, 2, 1)
_TFN_WEIGHTS_9 = (1, 4, 3, 7, 5, 8, 6, 9, 10)
_TFN_WEIGHTS_8 = (1, 4, 3, 7, 5, 8, 6, 10)
_VIN = re.compile(r"[A-HJ-NPR-Z0-9]{17}")


def _digits(value: object, lengths: tuple[int, ...]) -> str | None:
    if isinstance(value, bool) or not isinstance(value, (str, int)) or (isinstance(value, int) and value < 0):
        return None
    compact = _SEPARATORS.sub("", str(value))
    if len(compact) not in lengths or not compact.isascii() or not compact.isdigit():
        return None
    return compact


def _sum(digits: str, weights: tuple[int, ...]) -> int:
    return sum(int(d) * w for d, w in zip(digits, weights))


def normalise_abn(value: object) -> str | None:
    abn = _digits(value, (11,))
    if abn is None:
        return None
    # Subtract 1 from the first digit, then the weighted sum must be divisible by 89.
    total = (int(abn[0]) - 1) * _ABN_WEIGHTS[0] + _sum(abn[1:], _ABN_WEIGHTS[1:])
    return abn if total % 89 == 0 else None


def is_valid_abn(value: object) -> bool:
    return normalise_abn(value) is not None


def format_abn(value: object) -> str | None:
    abn = normalise_abn(value)
    return f"{abn[:2]} {abn[2:5]} {abn[5:8]} {abn[8:]}" if abn else None


def normalise_acn(value: object) -> str | None:
    acn = _digits(value, (9,))
    if acn is None:
        return None
    return acn if int(acn[8]) == (10 - _sum(acn, _ACN_WEIGHTS) % 10) % 10 else None


def is_valid_acn(value: object) -> bool:
    return normalise_acn(value) is not None


def format_acn(value: object) -> str | None:
    acn = normalise_acn(value)
    return f"{acn[:3]} {acn[3:6]} {acn[6:]}" if acn else None


normalise_arbn = normalise_acn
is_valid_arbn = is_valid_acn
format_arbn = format_acn


def normalise_tfn(value: object, *, individual: bool = False) -> str | None:
    # 8-digit TFNs (organisations only) have their own weights. A 9-digit TFN with a leading
    # zero passes on either the 9-digit check or the 8-digit check of the rest.
    tfn = _digits(value, (9,) if individual else (8, 9))
    if tfn is None:
        return None
    if len(tfn) == 9 and len(tfn.lstrip("0")) >= 8 and _sum(tfn, _TFN_WEIGHTS_9) % 11 == 0:
        return tfn
    core = tfn.lstrip("0")
    weights = {9: _TFN_WEIGHTS_9, 8: _TFN_WEIGHTS_8}.get(len(core))
    return tfn if weights and _sum(core, weights) % 11 == 0 else None


def is_valid_tfn(value: object, *, individual: bool = False) -> bool:
    return normalise_tfn(value, individual=individual) is not None


def normalise_director_id(value: object) -> str | None:
    # Format only. The check digit method is only given to ATO-registered software providers.
    did = _digits(value, (15,))
    return did if did and did.startswith("036") else None


def is_valid_director_id(value: object) -> bool:
    return normalise_director_id(value) is not None


def normalise_vin(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    vin = value.strip(" \t\n\r\v\f")
    if not vin.isascii():
        return None
    vin = vin.upper()
    return vin if _VIN.fullmatch(vin) else None


def is_valid_vin(value: object) -> bool:
    return normalise_vin(value) is not None
