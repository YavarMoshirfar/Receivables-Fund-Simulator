"""Tests for portfolio construction and analytics."""

import pandas as pd
import pytest

from src.models import Receivable
from src.portfolio import Portfolio


def test_portfolio_total_exposure_and_weighted_average_tenor() -> None:
    """Portfolio should calculate total exposure and weighted tenor."""
    portfolio = Portfolio(
        [
            Receivable(invoice_id="INV-001", amount=1000.0, tenor_days=30),
            Receivable(invoice_id="INV-002", amount=3000.0, tenor_days=60),
        ]
    )

    assert portfolio.total_exposure() == 4000.0
    assert portfolio.weighted_average_tenor() == 52.5


def test_empty_portfolio_weighted_average_tenor_is_zero() -> None:
    """Empty portfolios should return zero weighted average tenor."""
    assert Portfolio().weighted_average_tenor() == 0.0


def test_portfolio_rejects_non_receivable() -> None:
    """Portfolio should only accept Receivable instances."""
    portfolio = Portfolio()

    with pytest.raises(TypeError):
        portfolio.add_receivable("not-a-receivable")  # type: ignore[arg-type]


def test_portfolio_from_dataframe() -> None:
    """Portfolio should load receivables from a DataFrame."""
    frame = pd.DataFrame(
        [
            {"invoice_id": "INV-001", "amount": 1000.0, "tenor_days": 30},
            {"invoice_id": "INV-002", "amount": 2000.0, "tenor_days": 45},
        ]
    )

    portfolio = Portfolio.from_dataframe(frame)

    assert portfolio.total_exposure() == 3000.0
    assert len(portfolio.receivables) == 2


def test_portfolio_from_dataframe_requires_columns() -> None:
    """Portfolio should validate required DataFrame columns."""
    with pytest.raises(ValueError):
        Portfolio.from_dataframe(pd.DataFrame([{"invoice_id": "INV-001"}]))
