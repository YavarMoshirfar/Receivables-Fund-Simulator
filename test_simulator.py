"""Tests for the full simulation workflow."""

from src.fund import Fund
from src.models import Receivable
from src.portfolio import Portfolio
from src.risk import RiskEngine
from src.simulator import Simulator


def test_simulator_run_returns_expected_metrics() -> None:
    """Simulator should combine portfolio, risk, and fund economics."""
    portfolio = Portfolio([Receivable("INV-001", 1_000_000.0, 60)])
    fund = Fund(
        portfolio_size=portfolio.total_exposure(),
        annual_yield=0.14,
        funding_cost=0.06,
        management_fee=0.015,
    )
    simulator = Simulator(
        portfolio=portfolio,
        risk_engine=RiskEngine(pd=0.03, lgd=0.45),
        fund=fund,
    )

    result = simulator.run()

    assert result.portfolio_size == 1_000_000.0
    assert result.gross_income == 140_000.0
    assert result.expected_loss == 13_500.0
    assert result.funding_cost == 60_000.0
    assert result.management_fee == 15_000.0
    assert result.net_profit == 51_500.0
    assert result.net_return_percent == 5.15


def test_simulator_result_dataframe() -> None:
    """Simulator should expose results as a DataFrame."""
    portfolio = Portfolio([Receivable("INV-001", 1000.0, 30)])
    fund = Fund(
        portfolio_size=portfolio.total_exposure(),
        annual_yield=0.10,
        funding_cost=0.02,
        management_fee=0.01,
    )
    simulator = Simulator(portfolio, RiskEngine(pd=0.01, lgd=0.50), fund)

    frame = simulator.result_dataframe()

    assert list(frame.columns) == [
        "portfolio_size",
        "gross_income",
        "expected_loss",
        "funding_cost",
        "management_fee",
        "net_profit",
        "net_return_percent",
    ]


def test_income_waterfall_chart_returns_plotly_figure() -> None:
    """Simulator should produce a Plotly chart object."""
    portfolio = Portfolio([Receivable("INV-001", 1000.0, 30)])
    fund = Fund(
        portfolio_size=portfolio.total_exposure(),
        annual_yield=0.10,
        funding_cost=0.02,
        management_fee=0.01,
    )
    simulator = Simulator(portfolio, RiskEngine(pd=0.01, lgd=0.50), fund)

    figure = simulator.income_waterfall_chart()

    assert figure.layout.title.text == "Receivables Fund Income Waterfall"
