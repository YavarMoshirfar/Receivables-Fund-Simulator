"""Tests for domain model validation."""

import pytest

from src.models import Receivable, SimulationResult


def test_receivable_accepts_valid_input() -> None:
    """Receivable should store valid invoice fields."""
    receivable = Receivable(invoice_id="INV-001", amount=1000.0, tenor_days=45)

    assert receivable.invoice_id == "INV-001"
    assert receivable.amount == 1000.0
    assert receivable.tenor_days == 45


def test_receivable_rejects_invalid_input() -> None:
    """Receivable should reject empty IDs, nonpositive amounts, and tenors."""
    with pytest.raises(ValueError):
        Receivable(invoice_id="", amount=1000.0, tenor_days=45)
    with pytest.raises(ValueError):
        Receivable(invoice_id="INV-001", amount=0.0, tenor_days=45)
    with pytest.raises(ValueError):
        Receivable(invoice_id="INV-001", amount=1000.0, tenor_days=0)


def test_simulation_result_to_dict() -> None:
    """SimulationResult should convert to a plain dictionary."""
    result = SimulationResult(
        portfolio_size=1000.0,
        gross_income=140.0,
        expected_loss=13.5,
        funding_cost=60.0,
        management_fee=15.0,
        net_profit=51.5,
        net_return_percent=5.15,
    )

    assert result.to_dict()["net_profit"] == 51.5
