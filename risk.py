"""Credit risk calculations for receivables portfolios."""

from __future__ import annotations

from dataclasses import dataclass


def _validate_rate(value: float, name: str) -> None:
    """Validate that a probability-style rate is between 0 and 1."""
    if not 0 <= value <= 1:
        raise ValueError(f"{name} must be between 0 and 1.")


@dataclass(frozen=True, slots=True)
class RiskEngine:
    """Expected-loss engine using probability of default and loss severity.

    Attributes:
        pd: Probability of default expressed as a decimal, e.g. 0.03 for 3%.
        lgd: Loss given default expressed as a decimal, e.g. 0.40 for 40%.
    """

    pd: float
    lgd: float

    def __post_init__(self) -> None:
        """Validate risk assumptions."""
        _validate_rate(self.pd, "pd")
        _validate_rate(self.lgd, "lgd")

    def expected_loss(self, exposure: float) -> float:
        """Calculate expected credit loss.

        Formula:
            Expected Loss = PD x LGD x Exposure
        """
        if exposure < 0:
            raise ValueError("exposure must be greater than or equal to zero.")
        return float(self.pd * self.lgd * exposure)
