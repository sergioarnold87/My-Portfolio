"""
Data Observability Module
Implements data quality, freshness, and schema drift monitoring
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime
import plotly.graph_objects as go
from scipy import stats


def calculate_completeness(df: pd.DataFrame) -> Dict[str, float]:
    """Calculate completeness metrics (% of non-null cells)"""
    total_cells = df.shape[0] * df.shape[1]
    non_null_cells = df.count().sum()
    
    completeness_by_column = (df.count() / len(df) * 100).to_dict()
    overall_completeness = (non_null_cells / total_cells * 100)
    
    return {
        'overall_completeness_pct': overall_completeness,
        'by_column': completeness_by_column
    }


def calculate_freshness(df: pd.DataFrame, date_column: str = None) -> Dict[str, any]:
    """Calculate data freshness (days since last update)"""
    if date_column and date_column in df.columns:
        try:
            df[date_column] = pd.to_datetime(df[date_column])
            latest_date = df[date_column].max()
            days_since_update = (datetime.now() - latest_date).days
        except:
            days_since_update = -1
            latest_date = None
    else:
        days_since_update = -1
        latest_date = None
    
    return {
        'days_since_last_update': days_since_update,
        'latest_date': latest_date,
        'status': 'Fresh' if days_since_update <= 7 else 'Stale' if days_since_update <= 30 else 'Very Stale'
    }


def detect_outliers_zscore(df: pd.DataFrame, threshold: float = 3.0) -> Dict[str, any]:
    """Detect outliers using z-score method"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    outlier_counts = {}
    outlier_ratios = {}
    
    for col in numeric_cols:
        z_scores = np.abs(stats.zscore(df[col].dropna()))
        outliers = z_scores > threshold
        outlier_counts[col] = outliers.sum()
        outlier_ratios[col] = (outliers.sum() / len(df) * 100)
    
    total_outliers = sum(outlier_counts.values())
    
    return {
        'total_outliers': total_outliers,
        'outlier_counts': outlier_counts,
        'outlier_ratios': outlier_ratios
    }


def run_quality_checks(df: pd.DataFrame, date_column: str = None) -> Dict[str, any]:
    """Run comprehensive data quality checks"""
    
    completeness = calculate_completeness(df)
    freshness = calculate_freshness(df, date_column)
    outliers = detect_outliers_zscore(df)
    
    quality_score = (
        completeness['overall_completeness_pct'] * 0.5 +
        (100 - min(outliers['total_outliers'] / len(df) * 100, 100)) * 0.3 +
        (100 if freshness['days_since_last_update'] < 0 or freshness['days_since_last_update'] <= 7 else 70) * 0.2
    )
    
    return {
        'quality_score': quality_score,
        'completeness': completeness,
        'freshness': freshness,
        'outliers': outliers,
        'row_count': len(df),
        'column_count': df.shape[1],
        'memory_usage_mb': df.memory_usage(deep=True).sum() / 1024**2
    }


def plot_completeness_chart(completeness_data: Dict) -> go.Figure:
    """Create pie chart for data completeness"""
    overall = completeness_data['overall_completeness_pct']
    
    fig = go.Figure(data=[go.Pie(
        labels=['Complete', 'Missing'],
        values=[overall, 100 - overall],
        hole=0.4,
        marker_colors=['#00CC96', '#EF553B']
    )])
    
    fig.update_layout(
        title="Overall Data Completeness",
        annotations=[dict(text=f'{overall:.1f}%', x=0.5, y=0.5, font_size=20, showarrow=False)]
    )
    
    return fig


def plot_outliers_chart(outlier_data: Dict) -> go.Figure:
    """Create bar chart for outliers per column"""
    outlier_ratios = outlier_data['outlier_ratios']
    
    sorted_items = sorted(outlier_ratios.items(), key=lambda x: x[1], reverse=True)[:15]
    columns = [item[0] for item in sorted_items]
    ratios = [item[1] for item in sorted_items]
    
    fig = go.Figure(data=[go.Bar(
        x=ratios,
        y=columns,
        orientation='h',
        marker_color='#AB63FA'
    )])
    
    fig.update_layout(
        title="Top 15 Columns with Outliers (% of rows)",
        xaxis_title="Outlier Ratio (%)",
        yaxis_title="Column",
        height=500
    )
    
    return fig


def plot_freshness_gauge(freshness_data: Dict) -> go.Figure:
    """Create gauge chart for data freshness"""
    days = freshness_data['days_since_last_update']
    
    if days < 0:
        days = 0
        value_text = "N/A"
    else:
        value_text = f"{days} days"
    
    gauge_value = max(0, 100 - (days / 30 * 100))
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=gauge_value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Data Freshness<br><sub>{value_text} ago</sub>"},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightcoral"},
                {'range': [50, 80], 'color': "lightyellow"},
                {'range': [80, 100], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    return fig
