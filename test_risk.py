"""Tests for credit risk calculations."""

import pytest

from src.risk import RiskEngine


def test_expected_loss() -> None:
    """Expected loss should equal PD times LGD times exposure."""
    engine = RiskEngine(pd=0.03, lgd=0.45)

    assert engine.expected_loss(1_000_000.0) == 13_500.0


def test_risk_engine_rejects_invalid_rates() -> None:
    """RiskEngine should reject probabilities outside 0 to 1."""
    with pytest.raises(ValueError):
        RiskEngine(pd=-0.01, lgd=0.45)
    with pytest.raises(ValueError):
        RiskEngine(pd=0.03, lgd=1.1)


def test_expected_loss_rejects_negative_exposure() -> None:
    """Expected loss should reject negative exposure."""
    with pytest.raises(ValueError):
        RiskEngine(pd=0.03, lgd=0.45).expected_loss(-1.0)
