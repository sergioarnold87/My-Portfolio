"""
Machine Learning Pipeline for Production Prediction
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from catboost import CatBoostRegressor
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Tuple, List
import warnings
warnings.filterwarnings('ignore')


class ProductionMLPipeline:
    """ML Pipeline for predicting oil production"""
    
    def __init__(self, target_column: str = 'cum_oil_180_days_m3'):
        self.target_column = target_column
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = None
        self.feature_importance = None
        
    def prepare_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Engineer features for production prediction"""
        df_features = df.copy()
        
        if 'porosity' in df.columns and 'net_pay_m' in df.columns:
            df_features['reservoir_quality_index'] = df_features['porosity'] * df_features['net_pay_m']
        
        if 'proppant_intensity_ton_per_m' in df.columns and 'fluid_intensity_m3_per_m' in df.columns:
            df_features['completion_quality_index'] = (
                df_features['proppant_intensity_ton_per_m'] * 
                df_features['fluid_intensity_m3_per_m']
            )
        
        if 'porosity' in df.columns and 'oil_saturation' in df.columns and 'net_pay_m' in df.columns:
            df_features['hc_pore_volume'] = (
                df_features['porosity'] * 
                df_features['oil_saturation'] * 
                df_features['net_pay_m']
            )
        
        if 'n_stages' in df.columns and 'lateral_length_m' in df.columns:
            df_features['stage_spacing_m'] = df_features['lateral_length_m'] / df_features['n_stages']
        
        if 'n_stages' in df.columns and 'n_clusters_per_stage' in df.columns:
            df_features['total_clusters'] = df_features['n_stages'] * df_features['n_clusters_per_stage']
        
        if 'youngs_modulus_gpa' in df.columns and 'poisson_ratio' in df.columns:
            df_features['brittleness_index'] = (
                df_features['youngs_modulus_gpa'] / (1 + df_features['poisson_ratio'])
            )
        
        return df_features
    
    def select_features(self, df: pd.DataFrame) -> List[str]:
        """Select relevant features for modeling"""
        exclude_cols = [
            'well_id', 'formation', 'proppant_type', 'mesh_size',
            'spud_date', 'completion_date', 'first_production_date',
            'cum_oil_30_days_m3', 'cum_oil_90_days_m3', 
            'cum_oil_180_days_m3', 'cum_oil_365_days_m3',
            'peak_oil_rate_m3_day', 'avg_oil_rate_m3_day',
            'decline_rate_annual', 'b_factor', 'days_online'
        ]
        
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        feature_cols = [col for col in numeric_cols if col not in exclude_cols]
        feature_cols = [col for col in feature_cols if df[col].notna().sum() > 0]
        
        return feature_cols
    
    def train_model(self, df: pd.DataFrame) -> Dict:
        """Train production prediction model"""
        df_features = self.prepare_features(df)
        self.feature_columns = self.select_features(df_features)
        
        X = df_features[self.feature_columns].fillna(0)
        y = df_features[self.target_column]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.model = CatBoostRegressor(
            iterations=500,
            learning_rate=0.05,
            depth=6,
            loss_function='RMSE',
            random_seed=42,
            verbose=False
        )
        
        self.model.fit(X_train_scaled, y_train)
        
        y_pred_train = self.model.predict(X_train_scaled)
        y_pred_test = self.model.predict(X_test_scaled)
        
        self.feature_importance = pd.DataFrame({
            'feature': self.feature_columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        metrics = {
            'train_r2': r2_score(y_train, y_pred_train),
            'test_r2': r2_score(y_test, y_pred_test),
            'train_rmse': np.sqrt(mean_squared_error(y_train, y_pred_train)),
            'test_rmse': np.sqrt(mean_squared_error(y_test, y_pred_test)),
            'train_mae': mean_absolute_error(y_train, y_pred_train),
            'test_mae': mean_absolute_error(y_test, y_pred_test),
            'y_test': y_test,
            'y_pred': y_pred_test
        }
        
        return metrics
    
    def predict_cum_oil(self, df: pd.DataFrame) -> np.ndarray:
        """Predict cumulative oil production"""
        df_features = self.prepare_features(df)
        X = df_features[self.feature_columns].fillna(0)
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def get_feature_importance(self, top_n: int = 15) -> pd.DataFrame:
        """Get top N important features"""
        return self.feature_importance.head(top_n)
    
    def plot_predictions(self, y_true, y_pred) -> go.Figure:
        """Plot actual vs predicted values"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=y_true,
            y=y_pred,
            mode='markers',
            name='Predictions',
            marker=dict(size=8, color='royalblue', opacity=0.6)
        ))
        
        min_val = min(y_true.min(), y_pred.min())
        max_val = max(y_true.max(), y_pred.max())
        
        fig.add_trace(go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode='lines',
            name='Perfect Prediction',
            line=dict(color='red', dash='dash')
        ))
        
        fig.update_layout(
            title="Actual vs Predicted Production (180 days)",
            xaxis_title="Actual (m³)",
            yaxis_title="Predicted (m³)",
            height=600
        )
        
        return fig
    
    def plot_feature_importance(self, top_n: int = 15) -> go.Figure:
        """Plot feature importance"""
        df_imp = self.get_feature_importance(top_n)
        
        fig = go.Figure(data=[go.Bar(
            x=df_imp['importance'],
            y=df_imp['feature'],
            orientation='h',
            marker_color='lightseagreen'
        )])
        
        fig.update_layout(
            title=f"Top {top_n} Feature Importance",
            xaxis_title="Importance",
            yaxis_title="Feature",
            height=600
        )
        
        return fig
