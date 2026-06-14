"""Tests for fund economics."""

import pytest

from src.fund import Fund


def test_fund_economics() -> None:
    """Fund should calculate gross income, expenses, and net profit."""
    fund = Fund(
        portfolio_size=1_000_000.0,
        annual_yield=0.14,
        funding_cost=0.06,
        management_fee=0.015,
    )

    assert fund.gross_income() == 140_000.0
    assert fund.funding_expense() == 60_000.0
    assert fund.management_expense() == 15_000.0
    assert fund.net_profit(expected_loss=13_500.0) == 51_500.0


def test_fund_rejects_negative_inputs() -> None:
    """Fund should reject negative economics inputs."""
    with pytest.raises(ValueError):
        Fund(
            portfolio_size=-1.0,
            annual_yield=0.14,
            funding_cost=0.06,
            management_fee=0.015,
        )
    with pytest.raises(ValueError):
        Fund(
            portfolio_size=1_000_000.0,
            annual_yield=0.14,
            funding_cost=0.06,
            management_fee=-0.015,
        )


def test_fund_rejects_negative_expected_loss() -> None:
    """Net profit should reject negative expected loss."""
    fund = Fund(
        portfolio_size=1_000_000.0,
        annual_yield=0.14,
        funding_cost=0.06,
        management_fee=0.015,
    )

    with pytest.raises(ValueError):
        fund.net_profit(expected_loss=-1.0)
