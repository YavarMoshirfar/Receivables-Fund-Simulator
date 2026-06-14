"""Simulation orchestration for receivables-backed fund scenarios."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from src.fund import Fund
from src.models import SimulationResult
from src.portfolio import Portfolio
from src.risk import RiskEngine


class Simulator:
    """Combine portfolio, credit risk, and fund economics into one run."""

    def __init__(
        self,
        portfolio: Portfolio,
        risk_engine: RiskEngine,
        fund: Fund,
    ) -> None:
        """Initialize the simulator dependencies."""
        self.portfolio = portfolio
        self.risk_engine = risk_engine
        self.fund = fund

    def run(self) -> SimulationResult:
        """Run the fund simulation and return financial performance metrics."""
        portfolio_size = self.portfolio.total_exposure()
        expected_loss = self.risk_engine.expected_loss(portfolio_size)
        gross_income = self.fund.gross_income()
        funding_cost = self.fund.funding_expense()
        management_fee = self.fund.management_expense()
        net_profit = self.fund.net_profit(expected_loss)
        net_return_percent = (
            float(np.divide(net_profit, portfolio_size) * 100)
            if portfolio_size > 0
            else 0.0
        )

        return SimulationResult(
            portfolio_size=portfolio_size,
            gross_income=gross_income,
            expected_loss=expected_loss,
            funding_cost=funding_cost,
            management_fee=management_fee,
            net_profit=net_profit,
            net_return_percent=net_return_percent,
        )

    def result_dataframe(self) -> pd.DataFrame:
        """Return the simulation result as a one-row Pandas DataFrame."""
        return pd.DataFrame([self.run().to_dict()])

    def income_waterfall_chart(self) -> go.Figure:
        """Return a Plotly waterfall chart of the fund economics."""
        result = self.run()
        return go.Figure(
            go.Waterfall(
                name="Fund economics",
                orientation="v",
                measure=[
                    "relative",
                    "relative",
                    "relative",
                    "relative",
                    "total",
                ],
                x=[
                    "Gross income",
                    "Expected loss",
                    "Funding cost",
                    "Management fee",
                    "Net profit",
                ],
                y=[
                    result.gross_income,
                    -result.expected_loss,
                    -result.funding_cost,
                    -result.management_fee,
                    result.net_profit,
                ],
            )
        ).update_layout(
            title="Receivables Fund Income Waterfall",
            yaxis_title="Amount",
            showlegend=False,
            template="plotly_white",
        )
