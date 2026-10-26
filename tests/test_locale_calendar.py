import pytest

from arrow import Arrow, get, locales

# Snapshot built-in implementations at collection, before tests register custom locales.
# One declared name per implementation avoids repeating the same data for every alias.
LOCALE_NAMES = sorted({cls.names[0] for cls in locales._locale_map.values()})


@pytest.mark.parametrize("month", range(1, 13), ids=lambda month: f"month-{month:02d}")
@pytest.mark.parametrize("locale_name", LOCALE_NAMES)
def test_full_month_name_round_trip(locale_name, month):
    """A formatted full month name must parse back to its calendar month."""
    original = Arrow(2024, month, 15)
    # Keep DD after MMMM: standalone Vietnamese names have a known prefix-matching
    # limitation (PR #1379). Year conversion is separate (Thai/Lao use Buddhist years).
    date_format = "MMMM DD"
    formatted = original.format(date_format, locale=locale_name)

    parsed = get(formatted, date_format, locale=locale_name)

    assert (parsed.month, parsed.day) == (original.month, original.day)
