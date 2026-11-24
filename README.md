# Australian ABN, ACN and TFN Validation for Python

[![tests](https://github.com/BusinessAPI/au-identifiers-python/actions/workflows/test.yml/badge.svg)](https://github.com/BusinessAPI/au-identifiers-python/actions/workflows/test.yml) [![MIT licence](https://img.shields.io/badge/licence-MIT-blue.svg)](LICENSE)

Validate and format Australian identifiers in Python: ABN, ACN, ARBN, TFN, Director ID and VIN.

```bash
pip install au-identifiers
```

```python
import au_identifiers as au

au.is_valid_abn("51 824 753 556")              # True
au.format_abn("51824753556")                   # "51 824 753 556"
au.format_acn("004085616")                     # "004 085 616"
au.is_valid_tfn("15195606")                    # True (8-digit, organisation)
au.is_valid_tfn("15195606", individual=True)   # False
au.is_valid_director_id("036 123 456 789 012") # True
au.normalise_vin(" 1hgcm82633a004352 ")        # "1HGCM82633A004352"
```

Each identifier has `is_valid_*` and `normalise_*`. ABN, ACN and ARBN also have `format_*`. `normalise_*` and `format_*` return `None` for invalid input. The ARBN functions are aliases of the ACN ones. Python 3.9+, typed, no dependencies.

## Rules

| | Format | Check |
|---|---|---|
| ABN | 11 digits | ATO modulus 89 |
| ACN, ARBN | 9 digits | ASIC check digit |
| TFN | 8 or 9 digits | ATO modulus 11 |
| Director ID | 15 digits, starts with 036 | Format only |
| VIN | 17 characters, no I, O or Q | Format only (ISO 3779) |

Spaces and hyphens in numbers are ignored. VINs are trimmed and upper-cased. Anything else makes the value invalid. Pass ACNs, TFNs and Director IDs as strings so leading zeros aren't lost.

## How the checks work

### ABN

Subtract 1 from the first digit, multiply the 11 digits by 10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19 and add them up. The ABN is valid if the total divides evenly by 89. For 51 824 753 556 the total is 534, which is 89 x 6.

### ACN and ARBN

Multiply the first 8 digits by 8, 7, 6, 5, 4, 3, 2, 1 and add them up. Take the remainder after dividing by 10 and subtract it from 10 (10 becomes 0). That's the check digit, and it must match the last digit. For 004 085 616 the total is 84, so the check digit is 6.

### TFN

Multiply the 9 digits by 1, 4, 3, 7, 5, 8, 6, 9, 10 and add them up. The TFN is valid if the total divides evenly by 11. For 123 456 782 the total is 253, which is 11 x 23.

8-digit TFNs (organisations only) use the weights 1, 4, 3, 7, 5, 8, 6, 10. A 9-digit TFN with a leading zero is valid if either the 9-digit check or the 8-digit check on the rest passes. Set the individual option for a person's TFN, which is always 9 digits.

### Director ID and VIN

The Director ID check digit method is only given to ATO-registered software providers, so it's a format check here. VINs are checked for 17 characters with no I, O or Q (ISO 3779). Australia doesn't use the VIN check digit.

## Valid isn't registered

These checks run offline and only tell you a number is well formed. To check an ABN or ACN is registered and active, or to register companies, ABNs and business names, use the [Business API ABN lookup and company registration API](https://businessapi.com.au).

Also available for [JavaScript / TypeScript](https://github.com/BusinessAPI/au-identifiers-js), [PHP](https://github.com/BusinessAPI/au-identifiers-php), [.NET](https://github.com/BusinessAPI/au-identifiers-dotnet), [Java](https://github.com/BusinessAPI/au-identifiers-java).

## Licence

MIT
