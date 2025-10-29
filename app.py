"""
Vaca Muerta Data Observability & HF Optimization
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from src.generate_data import SyntheticDataGenerator
from src.observability import run_quality_checks, plot_completeness_chart, plot_outliers_chart, plot_freshness_gauge
from src.ml_pipeline import ProductionMLPipeline
from src.utils import ensure_data_dirs, load_dataframe

# Page configuration
st.set_page_config(
    page_title="Vaca Muerta Observability",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)


# Title
st.markdown('<div class="main-header">🛢️ Vaca Muerta Data Observability & HF Optimization</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Synthetic Data Engineering & ML Platform for Unconventional Reservoirs</div>', unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Module:",
    ["🏗️ Synthetic Data", "🔍 Data Observability", "⚙️ Feature Engineering", "📈 Model Predictions"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
**Vaca Muerta Observability Platform**

A comprehensive data engineering and machine learning solution for optimizing hydraulic fracturing operations in unconventional reservoirs.

**Features:**
- Synthetic well data generation
- Real-time data quality monitoring
- Advanced feature engineering
- Production forecasting with ML

**Tech Stack:**
- Python 3.11
- Streamlit
- CatBoost / XGBoost
- SDV, Plotly, Pandas
""")

st.sidebar.markdown("---")
st.sidebar.markdown("**Author:** Sergio Arnold")
st.sidebar.markdown("**Role:** Data & AI Engineer")

# Initialize data directory
ensure_data_dirs()

# Data file path
DATA_FILE = 'data/bronze/wells_synth.csv'


# ==================== PAGE: SYNTHETIC DATA ====================
if page == "🏗️ Synthetic Data":
    st.header("🏗️ Synthetic Data Generation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        Generate realistic synthetic well data for the **Vaca Muerta** formation using:
        - **SDV (Synthetic Data Vault)** for statistical modeling
        - **Faker** for realistic field values
        - **Arps Decline Curves** for production simulation
        """)
    
    with col2:
        n_wells = st.number_input("Number of Wells", min_value=10, max_value=500, value=150, step=10)
        generate_button = st.button("🧬 Generate Data", type="primary", use_container_width=True)
    
    if generate_button:
        with st.spinner(f"Generating {n_wells} synthetic wells..."):
            generator = SyntheticDataGenerator(n_wells=n_wells)
            datasets = generator.generate_all()
            st.success(f"✅ Successfully generated {n_wells} wells!")
            
            # Display sample data
            st.subheader("Master Dataset Preview")
            st.dataframe(datasets['master'].head(20), use_container_width=True)
            
            # Statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Wells", f"{len(datasets['master']):,}")
            with col2:
                st.metric("Total Columns", f"{datasets['master'].shape[1]}")
            with col3:
                st.metric("Avg Production (180d)", f"{datasets['master']['cum_oil_180_days_m3'].mean():.1f} m³")
            with col4:
                st.metric("Avg Lateral Length", f"{datasets['master']['lateral_length_m'].mean():.0f} m")
    
    # Load existing data if available
    if os.path.exists(DATA_FILE):
        st.markdown("---")
        st.subheader("📊 Existing Dataset Visualization")
        
        df = load_dataframe(DATA_FILE)
        
        tab1, tab2, tab3 = st.tabs(["📍 Spatial Distribution", "📊 Production Histograms", "🔗 Correlations"])
        
        with tab1:
            if 'latitude' in df.columns and 'longitude' in df.columns:
                fig = px.scatter_mapbox(
                    df,
                    lat='latitude',
                    lon='longitude',
                    color='cum_oil_180_days_m3',
                    size='cum_oil_180_days_m3',
                    hover_data=['well_id', 'formation'],
                    title="Well Locations (colored by 180-day production)",
                    mapbox_style="open-street-map",
                    zoom=6,
                    height=600
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                fig = px.histogram(df, x='cum_oil_180_days_m3', nbins=30, 
                                   title="Cumulative Oil Production @ 180 Days")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.histogram(df, x='proppant_intensity_ton_per_m', nbins=30,
                                   title="Proppant Intensity Distribution")
                st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            numeric_cols = ['porosity', 'net_pay_m', 'lateral_length_m', 
                           'proppant_intensity_ton_per_m', 'cum_oil_180_days_m3']
            corr_data = df[numeric_cols].corr()
            
            fig = px.imshow(corr_data, 
                           text_auto='.2f',
                           aspect="auto",
                           title="Feature Correlation Matrix",
                           color_continuous_scale='RdBu_r')
            st.plotly_chart(fig, use_container_width=True)


# ==================== PAGE: DATA OBSERVABILITY ====================
elif page == "🔍 Data Observability":
    st.header("🔍 Data Observability & Quality Monitoring")
    
    if not os.path.exists(DATA_FILE):
        st.warning("⚠️ No data found. Please generate synthetic data first.")
    else:
        df = load_dataframe(DATA_FILE)
        
        # Run quality checks
        with st.spinner("Running data quality checks..."):
            results = run_quality_checks(df, date_column='completion_date')
        
        st.success("✅ Quality checks complete!")
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Quality Score",
                f"{results['quality_score']:.1f}%",
                delta="Good" if results['quality_score'] > 90 else "Review"
            )
        
        with col2:
            st.metric(
                "Completeness",
                f"{results['completeness']['overall_completeness_pct']:.1f}%"
            )
        
        with col3:
            st.metric(
                "Total Outliers",
                f"{results['outliers']['total_outliers']:,}"
            )
        
        with col4:
            st.metric(
                "Memory Usage",
                f"{results['memory_usage_mb']:.2f} MB"
            )
        
        st.markdown("---")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Data Completeness")
            fig_completeness = plot_completeness_chart(results['completeness'])
            st.plotly_chart(fig_completeness, use_container_width=True)
            
            st.subheader("Data Freshness")
            fig_freshness = plot_freshness_gauge(results['freshness'])
            st.plotly_chart(fig_freshness, use_container_width=True)
        
        with col2:
            st.subheader("Outlier Detection (Z-Score > 3)")
            fig_outliers = plot_outliers_chart(results['outliers'])
            st.plotly_chart(fig_outliers, use_container_width=True)
        
        # Missing values table
        st.markdown("---")
        st.subheader("📋 Missing Values Analysis")
        
        missing_data = pd.DataFrame({
            'Column': df.columns,
            'Missing Count': df.isnull().sum().values,
            'Missing %': (df.isnull().sum().values / len(df) * 100).round(2)
        })
        missing_data = missing_data[missing_data['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
        
        if len(missing_data) > 0:
            st.dataframe(missing_data, use_container_width=True)
        else:
            st.success("✅ No missing values detected!")


# ==================== PAGE: FEATURE ENGINEERING ====================
elif page == "⚙️ Feature Engineering":
    st.header("⚙️ Feature Engineering & Analysis")
    
    if not os.path.exists(DATA_FILE):
        st.warning("⚠️ No data found. Please generate synthetic data first.")
    else:
        df = load_dataframe(DATA_FILE)
        
        st.markdown("""
        **Engineered Features:**
        - **Reservoir Quality Index** = Porosity × Net Pay
        - **Completion Quality Index** = Proppant Intensity × Fluid Intensity
        - **HC Pore Volume** = Porosity × Oil Saturation × Net Pay
        - **Brittleness Index** = Young's Modulus / (1 + Poisson's Ratio)
        - **Stage Spacing** = Lateral Length / Number of Stages
        """)
        
        # Initialize pipeline
        pipeline = ProductionMLPipeline()
        df_engineered = pipeline.prepare_features(df)
        
        # Display engineered features
        st.subheader("🔧 Engineered Features Preview")
        
        engineered_cols = ['reservoir_quality_index', 'completion_quality_index', 
                          'hc_pore_volume', 'brittleness_index', 'stage_spacing_m']
        
        available_cols = [col for col in engineered_cols if col in df_engineered.columns]
        
        if available_cols:
            st.dataframe(df_engineered[['well_id'] + available_cols].head(20), use_container_width=True)
            
            # Statistical summary
            st.subheader("📊 Statistical Summary")
            st.dataframe(df_engineered[available_cols].describe(), use_container_width=True)
            
            # Distributions
            st.subheader("📈 Feature Distributions")
            
            col1, col2 = st.columns(2)
            
            for idx, col in enumerate(available_cols[:4]):
                if idx % 2 == 0:
                    with col1:
                        fig = px.box(df_engineered, y=col, title=f"{col} Distribution")
                        st.plotly_chart(fig, use_container_width=True)
                else:
                    with col2:
                        fig = px.box(df_engineered, y=col, title=f"{col} Distribution")
                        st.plotly_chart(fig, use_container_width=True)


# ==================== PAGE: MODEL PREDICTIONS ====================
elif page == "📈 Model Predictions":
    st.header("📈 Production Forecasting with Machine Learning")
    
    if not os.path.exists(DATA_FILE):
        st.warning("⚠️ No data found. Please generate synthetic data first.")
    else:
        df = load_dataframe(DATA_FILE)
        
        st.markdown("""
        **Model:** CatBoost Regressor  
        **Target:** Cumulative Oil Production @ 180 Days (m³)  
        **Algorithm:** Gradient Boosting with Categorical Features Support
        """)
        
        train_button = st.button("🚀 Train Model", type="primary", use_container_width=False)
        
        if train_button or 'trained' in st.session_state:
            with st.spinner("Training machine learning model..."):
                pipeline = ProductionMLPipeline()
                metrics = pipeline.train_model(df)
                st.session_state['trained'] = True
                st.session_state['pipeline'] = pipeline
                st.session_state['metrics'] = metrics
            
            st.success("✅ Model training complete!")
            
            # Display metrics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Test R²", f"{metrics['test_r2']:.3f}")
            with col2:
                st.metric("Test RMSE", f"{metrics['test_rmse']:.1f} m³")
            with col3:
                st.metric("Test MAE", f"{metrics['test_mae']:.1f} m³")
            with col4:
                st.metric("Train R²", f"{metrics['train_r2']:.3f}")
            
            st.markdown("---")
            
            # Visualizations
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🎯 Actual vs Predicted")
                fig_pred = pipeline.plot_predictions(metrics['y_test'], metrics['y_pred'])
                st.plotly_chart(fig_pred, use_container_width=True)
            
            with col2:
                st.subheader("🔝 Feature Importance")
                fig_imp = pipeline.plot_feature_importance(top_n=15)
                st.plotly_chart(fig_imp, use_container_width=True)
            
            # Residuals
            st.markdown("---")
            st.subheader("📉 Residual Analysis")
            
            residuals = metrics['y_test'].values - metrics['y_pred']
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.scatter(x=metrics['y_pred'], y=residuals,
                                labels={'x': 'Predicted Values', 'y': 'Residuals'},
                                title="Residual Plot")
                fig.add_hline(y=0, line_dash="dash", line_color="red")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                fig = px.histogram(x=residuals, nbins=30, 
                                  title="Residuals Distribution",
                                  labels={'x': 'Residuals'})
                st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>Vaca Muerta Data Observability Platform</strong> | Built with ❤️ by Sergio Arnold</p>
    <p>Tech Stack: Streamlit • Python • CatBoost • Plotly • Docker</p>
</div>
""", unsafe_allow_html=True)
