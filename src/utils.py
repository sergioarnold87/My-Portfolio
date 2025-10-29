"""
Utility functions for data processing and visualization
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import os


def ensure_data_dirs():
    """Ensure data directories exist"""
    dirs = ['data/bronze', 'data/silver', 'data/gold']
    for d in dirs:
        os.makedirs(d, exist_ok=True)


def format_number(num: float, decimals: int = 2) -> str:
    """Format number with thousand separators"""
    return f"{num:,.{decimals}f}"


def calculate_percentiles(df: pd.DataFrame, column: str) -> Dict[str, float]:
    """Calculate percentiles for a given column"""
    return {
        'p10': df[column].quantile(0.1),
        'p50': df[column].quantile(0.5),
        'p90': df[column].quantile(0.9)
    }


def detect_outliers_iqr(df: pd.DataFrame, column: str) -> pd.Series:
    """Detect outliers using IQR method"""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return (df[column] < lower_bound) | (df[column] > upper_bound)


def arps_decline(qi: float, di: float, b: float, time: np.ndarray) -> np.ndarray:
    """
    Arps decline curve equation
    qi: initial production rate
    di: initial decline rate
    b: decline exponent (0=exponential, 0-1=hyperbolic, 1=harmonic)
    time: time array
    """
    if b == 0:
        return qi * np.exp(-di * time)
    else:
        return qi / ((1 + b * di * time) ** (1/b))


def save_dataframe(df: pd.DataFrame, filepath: str, format: str = 'csv'):
    """Save dataframe in specified format"""
    ensure_data_dirs()
    if format == 'csv':
        df.to_csv(filepath, index=False)
    elif format == 'parquet':
        df.to_parquet(filepath, index=False)
    print(f"✅ Saved {len(df)} records to {filepath}")


def load_dataframe(filepath: str) -> pd.DataFrame:
    """Load dataframe from file"""
    if filepath.endswith('.csv'):
        return pd.read_csv(filepath)
    elif filepath.endswith('.parquet'):
        return pd.read_parquet(filepath)
    else:
        raise ValueError(f"Unsupported file format: {filepath}")
