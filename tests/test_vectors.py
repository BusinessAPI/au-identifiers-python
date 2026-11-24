import json
from pathlib import Path

import pytest

import au_identifiers as au

VECTORS = json.loads((Path(__file__).parent / "vectors.json").read_text())
CHECKS = {"abn": au.is_valid_abn, "acn": au.is_valid_acn, "did": au.is_valid_director_id, "vin": au.is_valid_vin}
FORMATS = {"abn": au.format_abn, "acn": au.format_acn, "vin": au.normalise_vin}


@pytest.mark.parametrize("case", VECTORS["valid"], ids=lambda c: f"{c['type']}:{c['value']!r}")
def test_valid(case):
    if case["type"] == "tfn":
        assert au.is_valid_tfn(case["value"], individual=case.get("individual", False)) is case["valid"]
    else:
        assert CHECKS[case["type"]](case["value"]) is case["valid"]


@pytest.mark.parametrize("case", VECTORS["format"], ids=lambda c: f"{c['type']}:{c['value']!r}")
def test_format(case):
    assert FORMATS[case["type"]](case["value"]) == case["expected"]


def test_arbn_uses_the_acn_check():
    assert au.is_valid_arbn("000 000 019") and not au.is_valid_arbn("000 000 018")


@pytest.mark.parametrize("value", [None, 51824753556.0, True, ["51824753556"], b"51824753556", -51824753556, -123456782])
def test_non_string_input_is_invalid(value):
    assert not au.is_valid_abn(value) and not au.is_valid_tfn(value) and not au.is_valid_vin(value)


def test_integer_input():
    assert au.is_valid_abn(51824753556) and au.normalise_tfn(123456782) == "123456782"


def test_unicode_digits_are_rejected():
    assert not au.is_valid_acn("٠٠٤٠٨٥٦١٦")
