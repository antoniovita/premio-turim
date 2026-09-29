"""Verificações pequenas das contas e das restrições de unidade."""

from datetime import datetime
from pathlib import Path

from case_math import (
    Basis,
    Currency,
    Money,
    Month,
    Period,
    Rate,
    Unit,
    backtest,
    case_report,
    real_after_tax_rate,
    sale_proceeds,
    usd_return_in_brl,
)


def close(actual: float, expected: float) -> None:
    assert abs(actual - expected) < 1e-9, (actual, expected)


def rejects(operation) -> None:
    try:
        operation()
    except TypeError:
        return
    raise AssertionError("Operacao de tipos incompativeis foi aceita")


brl_300 = Money(300, Currency.BRL, Unit.MILLION, Period.STOCK)
brl_20 = Money(20, Currency.BRL, Unit.MILLION, Period.STOCK)
tax, proceeds = sale_proceeds(brl_300, brl_20, 0.15)
close(tax.as_millions(), 42)
close(proceeds.as_millions(), 258)
rejects(lambda: brl_300 + Money(1, Currency.USD, Unit.MILLION, Period.STOCK))
rejects(lambda: brl_300 + Money(1, Currency.BRL, Unit.MILLION, Period.YEAR))

real = real_after_tax_rate(
    Rate(0.12, Currency.BRL, Period.YEAR, Basis.NOMINAL),
    Rate(0.04, Currency.BRL, Period.YEAR, Basis.NOMINAL),
    0.15,
)
close(real.fraction, 1.102 / 1.04 - 1)
close(usd_return_in_brl(0.10, -0.10), -0.01)

months = [
    Month(datetime(2025, 12, 31), 0, 0, 0, 0, 0.10),
    Month(datetime(2026, 1, 31), 0, 0, 0, 0, 0),
]
close(backtest(months, Currency.BRL, 0, 0.15)["ending_wealth_for_1_initial"], 1.085)

root = Path(__file__).resolve().parents[1]
report = case_report(root / "starter-kit-arena-turim/material/retornos-mensais-2005-2026.xlsx", 0, 0, 0)
facts = report["case_facts_brl_millions"]
close(facts["family_liquidity_after_sale"], 358)
close(facts["illiquid_share_before_sale_pct"], 75)
assert report["backtest"][0]["first_month"] == "2005-01"
assert report["backtest"][0]["last_month"] == "2026-08"
print("Contas, unidades e leitura da planilha: OK")
