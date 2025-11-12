import random
from fastmcp import FastMCP
from datetime import date, datetime, timedelta
import calendar
from typing import Optional

mcp = FastMCP("OfficeDateTool")


# -----------------------------
# existing utility tools
# -----------------------------
@mcp.tool
def dice_roll(n_dice: int) -> list[int]:
    return [random.randint(1, 6) for _ in range(n_dice)]


@mcp.tool
def add_numbers(a: float, b: float) -> float:
    return a + b

@mcp.tool
def last_working_day(month: int) -> int:
    if month < 1 or month > 12:
        raise ValueError("month must be 1..12")
    return 30

@mcp.tool
def next_office_date() -> int:
    return 15

@mcp.tool
def office_dates_for_month(month: int) -> list[int]:
    if month < 1 or month > 12:
        raise ValueError("month must be 1..12")
    return [2,15,17]


def main():
    mcp.run()


if __name__ == "__main__":
    main()
