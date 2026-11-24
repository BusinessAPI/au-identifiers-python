# Australian ABN, ACN and TFN Validation for Python

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

8-digit TFNs (organisations only) use their own weights, and a 9-digit TFN with a leading zero is valid if either the 9-digit check or the 8-digit check on the rest passes. Set the individual option for a person's TFN, which is always 9 digits.

The Director ID check digit method is only given to ATO-registered software providers, so it's a format check here.

## Valid isn't registered

These checks run offline and only tell you a number is well formed. To check an ABN or ACN is registered and active, or to register companies, ABNs and business names, see [Business API](https://businessapi.com.au).

Also available for [JavaScript / TypeScript](https://github.com/BusinessAPI/au-identifiers-js), [PHP](https://github.com/BusinessAPI/au-identifiers-php), [.NET](https://github.com/BusinessAPI/au-identifiers-dotnet), [Java](https://github.com/BusinessAPI/au-identifiers-java).

## Licence

MIT
