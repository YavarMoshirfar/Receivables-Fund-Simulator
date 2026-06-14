# receivables-fund-simulator

A production-grade Python 3.12 simulation engine for a receivables-backed private credit fund. The project models receivables exposure, expected credit loss, fund income, financing costs, management fees, and net investor-level return.

## What This Project Simulates

Receivables financing is a form of short-duration credit where a fund advances capital against invoices or purchases invoices from sellers. The fund earns an asset yield from the receivables and takes credit risk on the obligors that ultimately repay those invoices.

Private credit refers to non-bank lending or credit investment strategies that are privately originated and negotiated. A receivables-backed private credit fund typically focuses on diversified, short-tenor assets, seeking predictable income while actively managing default risk, advance rates, concentration, and funding costs.

## Project Structure

```text
receivables-fund-simulator/
├── src/
│   ├── __init__.py
│   ├── portfolio.py
│   ├── risk.py
│   ├── fund.py
│   ├── simulator.py
│   └── models.py
├── tests/
├── data/
│   └── sample_receivables.csv
├── notebooks/
├── requirements.txt
├── README.md
└── main.py
```

## Core Concepts

### Receivables Financing

A receivable is an invoice or payment obligation due from a buyer to a seller. In receivables financing, the fund provides liquidity against those expected payments. The key asset metrics are invoice amount, tenor, obligor quality, diversification, and repayment behavior.

### Private Credit

Private credit funds invest in loans or credit assets that are not broadly traded in public markets. The fund's economics are driven by asset yield, credit losses, leverage or funding cost, operating expenses, and fees.

### Expected Loss

Expected loss estimates the average credit loss under a simplified probability framework:

```text
Expected Loss = PD x LGD x Exposure
```

Where:

- `PD` is probability of default.
- `LGD` is loss given default.
- `Exposure` is the funded receivables balance.

### Fund Economics

The simulator calculates:

- Gross income from asset yield.
- Funding expense from financing cost.
- Management expense from management fees.
- Expected credit loss from the risk engine.
- Net profit after expenses and expected loss.
- Net return percentage on portfolio exposure.

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run the Sample Simulation

```bash
python main.py
```

Example output:

```json
{
  "portfolio_size": 1000000.0,
  "gross_income": 140000.0,
  "expected_loss": 13500.0,
  "funding_cost": 60000.0,
  "management_fee": 15000.0,
  "net_profit": 51500.0,
  "net_return_percent": 5.15
}
```

## Usage

```python
from src.fund import Fund
from src.models import Receivable
from src.portfolio import Portfolio
from src.risk import RiskEngine
from src.simulator import Simulator

portfolio = Portfolio()
portfolio.add_receivable(Receivable("INV-001", 1_000_000.0, 60))

risk_engine = RiskEngine(pd=0.03, lgd=0.45)
fund = Fund(
    portfolio_size=portfolio.total_exposure(),
    annual_yield=0.14,
    funding_cost=0.06,
    management_fee=0.015,
)

result = Simulator(portfolio, risk_engine, fund).run()
print(result.to_dict())
```

## Plotly Waterfall Chart

```python
simulator = Simulator(portfolio, risk_engine, fund)
figure = simulator.income_waterfall_chart()
figure.show()
```

## Tests

```bash
pytest
```

## Design Notes

- All public functions and methods include type hints.
- Domain models validate invalid financial inputs early.
- `Portfolio` supports both programmatic construction and CSV/DataFrame loading.
- `SimulationResult` provides typed fields and a `to_dict()` helper for reporting.
