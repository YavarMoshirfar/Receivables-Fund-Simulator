"""Command-line entry point for the receivables fund simulator."""

from __future__ import annotations

import json
from pathlib import Path

from src.fund import Fund
from src.portfolio import Portfolio
from src.risk import RiskEngine
from src.simulator import Simulator


def build_default_simulator() -> Simulator:
    """Create a simulator using bundled sample data and assumptions."""
    project_root = Path(__file__).resolve().parent
    portfolio = Portfolio.from_csv(str(project_root / "data" / "sample_receivables.csv"))
    portfolio_size = portfolio.total_exposure()

    risk_engine = RiskEngine(pd=0.03, lgd=0.45)
    fund = Fund(
        portfolio_size=portfolio_size,
        annual_yield=0.14,
        funding_cost=0.06,
        management_fee=0.015,
    )
    return Simulator(portfolio=portfolio, risk_engine=risk_engine, fund=fund)


def main() -> None:
    """Run the sample simulation and print JSON output."""
    result = build_default_simulator().run()
    print(json.dumps(result.to_dict(), indent=2))


if __name__ == "__main__":
    main()
