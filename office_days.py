import random
import pandas as pd
from fastmcp import FastMCP
from datetime import datetime, date
from pathlib import Path
from typing import Optional, List

mcp = FastMCP("RohitOfficeDates")

# -------------------------------------------------
# Load CSV data into pandas DataFrame
# -------------------------------------------------
CSV_FILE = Path(__file__).parent / "office_days.csv"

if not CSV_FILE.exists():
    raise FileNotFoundError(f"CSV file not found: {CSV_FILE}")

# Read and normalize columns
df = pd.read_csv(CSV_FILE, parse_dates=["date"])
df["year"] = df["year"].astype(int)
df["month"] = df["month"].astype(int)
df = df.sort_values("date").reset_index(drop=True)

# -------------------------------------------------
# Office date tools (using DataFrame)
# -------------------------------------------------
@mcp.tool
def office_dates_for_month(month: int, year: Optional[int] = None) -> List[str]:
    """
    Return all office dates (as ISO strings) for the given month and year.
    Defaults to the current year.
    """
    if year is None:
        year = date.today().year

    mask = (df["year"] == year) & (df["month"] == month)
    dates = df.loc[mask, "date"].dt.date.tolist()

    return [d.isoformat() for d in dates] if len(dates) else []


@mcp.tool
def next_office_date(from_date: Optional[str] = None) -> Optional[str]:
    """
    Return the next office date strictly after from_date (YYYY-MM-DD).
    Defaults to today's date.
    """
    base = datetime.fromisoformat(from_date).date() if from_date else date.today()

    future_dates = df.loc[df["date"].dt.date > base, "date"].dt.date.tolist()
    if not future_dates:
        return None
    return future_dates[0].isoformat()


@mcp.tool
def last_working_day(month: int, year: Optional[int] = None) -> Optional[int]:
    """
    Return the day of the last office date for the given month/year.
    Defaults to current year.
    """
    if year is None:
        year = date.today().year

    mask = (df["year"] == year) & (df["month"] == month)
    month_dates = df.loc[mask, "date"].dt.date.tolist()

    return month_dates[-1].day if month_dates else None


# -------------------------------------------------
# Main function
# -------------------------------------------------
def main():
    """Run MCP server or print quick checks."""
    # print(f"Loaded {len(df)} records from {CSV_FILE.name}")
    # print("Office dates (Nov):", office_dates_for_month(11))
    # print("Next office date:", next_office_date())
    # print("Last working day (Nov):", last_working_day(11))

    # start MCP server for external access
    mcp.run(transport="http", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()