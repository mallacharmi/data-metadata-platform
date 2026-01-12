import pandas as pd

def extract_schema(df: pd.DataFrame):
    """
    Returns column schema
    """
    return [
        {"name": col, "data_type": str(dtype)}
        for col, dtype in df.dtypes.items()
    ]


def compute_column_stats(df: pd.DataFrame):
    """
    Returns simple column statistics
    """
    stats = []
    total_rows = len(df)

    for col in df.columns:
        stats.append({
            "column": col,
            "null_fraction": float(df[col].isna().sum()) / total_rows if total_rows > 0 else 0,
            "distinct_count": int(df[col].nunique())
        })

    return stats
