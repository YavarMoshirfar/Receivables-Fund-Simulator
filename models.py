"""Domain models used by the receivables fund simulator."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Receivable:
    """A single invoice receivable purchased or financed by the fund.

    Attributes:
        invoice_id: Unique invoice identifier.
        amount: Invoice face value or funded exposure.
        tenor_days: Number of days until contractual repayment.
    """

    invoice_id: str
    amount: float
    tenor_days: int

    def __post_init__(self) -> None:
        """Validate receivable inputs after dataclass initialization."""
        if not self.invoice_id.strip():
            raise ValueError("invoice_id must not be empty.")
        if self.amount <= 0:
            raise ValueError("amount must be greater than zero.")
        if self.tenor_days <= 0:
            raise ValueError("tenor_days must be greater than zero.")


@dataclass(frozen=True, slots=True)
class SimulationResult:
    """Output metrics produced by a fund simulation run."""

    portfolio_size: float
    gross_income: float
    expected_loss: float
    funding_cost: float
    management_fee: float
    net_profit: float
    net_return_percent: float

    def to_dict(self) -> dict[str, Any]:
        """Return the simulation result as a plain dictionary."""
        return asdict(self)
