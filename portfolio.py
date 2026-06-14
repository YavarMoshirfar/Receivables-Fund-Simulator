"""Portfolio construction and exposure analytics."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

from src.models import Receivable


class Portfolio:
    """A collection of receivables held by the private credit fund."""

    REQUIRED_COLUMNS: tuple[str, str, str] = ("invoice_id", "amount", "tenor_days")

    def __init__(self, receivables: Iterable[Receivable] | None = None) -> None:
        """Initialize a portfolio with optional existing receivables."""
        self._receivables: list[Receivable] = []
        if receivables is not None:
            for receivable in receivables:
                self.add_receivable(receivable)

    @property
    def receivables(self) -> tuple[Receivable, ...]:
        """Return portfolio receivables as an immutable tuple."""
        return tuple(self._receivables)

    def add_receivable(self, receivable: Receivable) -> None:
        """Add a receivable to the portfolio.

        Args:
            receivable: Validated receivable to add.
        """
        if not isinstance(receivable, Receivable):
            raise TypeError("receivable must be an instance of Receivable.")
        self._receivables.append(receivable)

    def total_exposure(self) -> float:
        """Return the total outstanding exposure across all receivables."""
        return float(sum(receivable.amount for receivable in self._receivables))

    def weighted_average_tenor(self) -> float:
        """Return exposure-weighted average tenor in days.

        Empty portfolios return 0.0 because no exposure exists to weight.
        """
        exposure = self.total_exposure()
        if exposure == 0:
            return 0.0
        weighted_tenor = sum(
            receivable.amount * receivable.tenor_days
            for receivable in self._receivables
        )
        return float(weighted_tenor / exposure)

    def to_dataframe(self) -> pd.DataFrame:
        """Return receivables as a Pandas DataFrame."""
        rows = [
            {
                "invoice_id": receivable.invoice_id,
                "amount": receivable.amount,
                "tenor_days": receivable.tenor_days,
            }
            for receivable in self._receivables
        ]
        return pd.DataFrame(rows, columns=self.REQUIRED_COLUMNS)

    @classmethod
    def from_dataframe(cls, frame: pd.DataFrame) -> "Portfolio":
        """Build a portfolio from a DataFrame with receivable columns."""
        missing_columns = set(cls.REQUIRED_COLUMNS) - set(frame.columns)
        if missing_columns:
            missing = ", ".join(sorted(missing_columns))
            raise ValueError(f"DataFrame is missing required columns: {missing}.")

        receivables = [
            Receivable(
                invoice_id=str(row.invoice_id),
                amount=float(row.amount),
                tenor_days=int(row.tenor_days),
            )
            for row in frame.loc[:, cls.REQUIRED_COLUMNS].itertuples(index=False)
        ]
        return cls(receivables)

    @classmethod
    def from_csv(cls, path: str) -> "Portfolio":
        """Load receivables from a CSV file."""
        return cls.from_dataframe(pd.read_csv(path))
