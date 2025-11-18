import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).parent / "bundles.db"


def get_connection():
    """Open a connection to the local SQLite DB."""
    return sqlite3.connect(DB_PATH)


def init_db():
    """Create table for bundle rules if it doesn't exist."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS bundle_rules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            antecedents TEXT,
            consequents TEXT,
            support REAL,
            confidence REAL,
            lift REAL
        )
        """
    )
    conn.commit()
    conn.close()


def load_rules_from_csv(csv_path: str = "baseline_rules.csv"):
    """Load rules from CSV into the DB (Create/Update)."""
    df = pd.read_csv(csv_path)
    conn = get_connection()

    # ensure we have these columns; adjust if your csv has different names
    cols = ["antecedents", "consequents", "support", "confidence", "lift"]
    df = df[cols]

    df.to_sql("bundle_rules", conn, if_exists="replace", index=False)
    conn.close()
    print(f"Saved {len(df)} rules into SQLite DB at {DB_PATH}")


def get_top_rules(limit: int = 10) -> pd.DataFrame:
    """Read top-N rules from the DB (Read)."""
    conn = get_connection()
    df = pd.read_sql(
        """
        SELECT antecedents, consequents, support, confidence, lift
        FROM bundle_rules
        ORDER BY lift DESC
        LIMIT ?
        """,
        conn,
        params=(limit,),
    )
    conn.close()
    return df


def delete_all_rules():
    """Delete all rules (Delete)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM bundle_rules")
    conn.commit()
    conn.close()
    print("Deleted all rules from DB")


if __name__ == "__main__":
    # Example usage: initialize + load + show top 5
    init_db()
    load_rules_from_csv()
    print(get_top_rules(5))
