"""Tests for model specification lookup, including device-reported model names."""

# ruff: noqa: PT009

from __future__ import annotations

import unittest

from custom_components.systemair.const import MODEL_SPECS, normalise_model_name, resolve_model_specs

VTR_300_MAX_AIRFLOW = 351


class TestResolveModelSpecs(unittest.TestCase):
    """Model specs must resolve from catalogue keys and from what units actually report."""

    def test_device_reported_name_resolves(self) -> None:
        """A unit reporting "SAVE VTR 300 R" must resolve to the VTR 300/B R specs."""
        specs = resolve_model_specs("SAVE VTR 300 R", {})
        self.assertIsNotNone(specs)
        self.assertEqual(specs["max_airflow_m3h"], VTR_300_MAX_AIRFLOW)

    def test_device_reported_name_resolves_for_both_handings(self) -> None:
        """Handing must not affect resolution."""
        for model in ("SAVE VTR 300 L", "SAVE VTR 300 R"):
            self.assertIsNotNone(resolve_model_specs(model, {}), model)

    def test_exact_catalogue_key_still_resolves(self) -> None:
        """The existing exact lookup must be unchanged."""
        self.assertEqual(resolve_model_specs("VTR 300/B R", {})["max_airflow_m3h"], VTR_300_MAX_AIRFLOW)

    def test_default_model_still_resolves(self) -> None:
        """The fallback model used when none is configured must keep working."""
        self.assertIsNotNone(resolve_model_specs("VSR 300", {}))

    def test_alias_still_takes_precedence(self) -> None:
        """Device-profile aliases must still be honoured."""
        self.assertEqual(
            resolve_model_specs("WHATEVER", {"WHATEVER": "VTR 300/B R"})["max_airflow_m3h"],
            VTR_300_MAX_AIRFLOW,
        )

    def test_unknown_model_returns_none(self) -> None:
        """An unrecognised model must still return None rather than a wrong match."""
        self.assertIsNone(resolve_model_specs("Not A Real Unit 999", {}))

    def test_normalisation_is_unambiguous(self) -> None:
        """No two catalogue models may normalise to the same key."""
        normalised = [normalise_model_name(key) for key in MODEL_SPECS]
        self.assertEqual(len(normalised), len(set(normalised)))


if __name__ == "__main__":
    unittest.main()
