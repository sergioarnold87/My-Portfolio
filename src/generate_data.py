"""
Synthetic Data Generator for Vaca Muerta Wells
Uses SDV and Faker to create realistic well data
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
from typing import Dict, List
import os
from src.utils import arps_decline, save_dataframe, ensure_data_dirs

fake = Faker()
Faker.seed(42)
np.random.seed(42)


class SyntheticDataGenerator:
    """Generate synthetic well data for Vaca Muerta formation"""
    
    def __init__(self, n_wells: int = 100):
        self.n_wells = n_wells
        ensure_data_dirs()
    
    def generate_reservoir_properties(self) -> pd.DataFrame:
        """Generate reservoir properties for synthetic wells"""
        data = {
            'well_id': [f'VM-{i:04d}' for i in range(1, self.n_wells + 1)],
            'latitude': np.random.uniform(-39.5, -37.0, self.n_wells),
            'longitude': np.random.uniform(-70.5, -68.0, self.n_wells),
            'formation': np.random.choice(['Vaca Muerta', 'Vaca Muerta Superior'], self.n_wells),
            'porosity': np.random.uniform(0.04, 0.12, self.n_wells),
            'permeability_nd': np.random.lognormal(mean=-3, sigma=1.5, size=self.n_wells),
            'water_saturation': np.random.uniform(0.20, 0.45, self.n_wells),
            'net_pay_m': np.random.uniform(50, 250, self.n_wells),
            'toc_percent': np.random.uniform(2.0, 8.0, self.n_wells),
            'vitrinite_reflectance': np.random.uniform(0.8, 1.4, self.n_wells),
            'youngs_modulus_gpa': np.random.uniform(20, 45, self.n_wells),
            'poisson_ratio': np.random.uniform(0.15, 0.30, self.n_wells),
            'initial_pressure_mpa': np.random.uniform(40, 65, self.n_wells),
            'temperature_c': np.random.uniform(90, 140, self.n_wells)
        }
        
        df = pd.DataFrame(data)
        df['oil_saturation'] = 1 - df['water_saturation']
        
        return df
    
    def generate_fracturing_jobs(self, reservoir_df: pd.DataFrame) -> pd.DataFrame:
        """Generate hydraulic fracturing job parameters"""
        n = len(reservoir_df)
        
        data = {
            'well_id': reservoir_df['well_id'],
            'spud_date': [fake.date_between(start_date='-3y', end_date='-6m') for _ in range(n)],
            'completion_date': [fake.date_between(start_date='-2y', end_date='today') for _ in range(n)],
            'lateral_length_m': np.random.uniform(1500, 3000, n),
            'n_stages': np.random.randint(25, 55, n),
            'n_clusters_per_stage': np.random.randint(4, 8, n),
            'cluster_spacing_m': np.random.uniform(15, 30, n),
            'proppant_total_ton': np.random.uniform(1500, 4500, n),
            'fluid_total_m3': np.random.uniform(15000, 40000, n),
            'avg_rate_bpm': np.random.uniform(60, 100, n),
            'avg_pressure_mpa': np.random.uniform(60, 95, n),
            'slickwater_percent': np.random.uniform(70, 100, n),
            'proppant_type': np.random.choice(['White Sand', 'Brown Sand', 'Ceramic'], n),
            'mesh_size': np.random.choice(['30/50', '40/70', '100'], n),
        }
        
        df = pd.DataFrame(data)
        
        # Calculate intensities
        df['proppant_intensity_ton_per_m'] = df['proppant_total_ton'] / df['lateral_length_m']
        df['fluid_intensity_m3_per_m'] = df['fluid_total_m3'] / df['lateral_length_m']
        
        return df
    
    def generate_production_data(self, reservoir_df: pd.DataFrame, 
                                 frac_df: pd.DataFrame) -> pd.DataFrame:
        """Generate production data using a simple heuristic (lightweight, stable)

        This replacement avoids heavy numeric loops and external dependencies
        during tests while keeping realistic-looking cumulative metrics.
        """

        production_records = []

        # iterate by row to keep indexing aligned and readable
        for idx, row in reservoir_df.iterrows():
            well_id = row['well_id']
            porosity = row['porosity']
            net_pay = row['net_pay_m']
            oil_sat = row['oil_saturation']

            # Find matching frac row (assumes one-to-one ordering)
            frac_row = frac_df[frac_df['well_id'] == well_id].iloc[0]
            proppant_int = frac_row['proppant_intensity_ton_per_m']
            fluid_int = frac_row['fluid_intensity_m3_per_m']

            # Simple engineered indices
            reservoir_quality = porosity * net_pay
            completion_quality = proppant_int * (fluid_int / 1000.0)

            # Heuristic base for cumulative oil at 180 days (m3)
            base = reservoir_quality * completion_quality * oil_sat * 0.02
            noise = np.random.normal(1.0, 0.25)
            cum_oil_180 = max(0.0, base * noise)

            # Provide a few additional descriptive metrics for compatibility
            peak_oil = max(5.0, (base * 1000.0) * np.random.uniform(0.8, 1.4))
            avg_oil = max(1.0, cum_oil_180 / 180.0)

            production_records.append({
                'well_id': well_id,
                'first_production_date': frac_row['completion_date'],
                'days_online': 180,
                'cum_oil_30_days_m3': float(cum_oil_180 * 0.2),
                'cum_oil_90_days_m3': float(cum_oil_180 * 0.55),
                'cum_oil_180_days_m3': float(cum_oil_180),
                'cum_oil_365_days_m3': float(cum_oil_180 * 1.6),
                'peak_oil_rate_m3_day': float(peak_oil),
                'avg_oil_rate_m3_day': float(avg_oil),
                'decline_rate_annual': float(np.random.uniform(0.4, 1.2)),
                'b_factor': float(np.random.uniform(0.3, 0.9))
            })

        return pd.DataFrame(production_records)
    
    def generate_all(self) -> Dict[str, pd.DataFrame]:
        """Generate all synthetic datasets"""
        print(f"🧬 Generating synthetic data for {self.n_wells} wells...")
        
        reservoir_df = self.generate_reservoir_properties()
        print(f"✅ Generated {len(reservoir_df)} reservoir property records")
        
        frac_df = self.generate_fracturing_jobs(reservoir_df)
        print(f"✅ Generated {len(frac_df)} fracturing job records")
        
        production_df = self.generate_production_data(reservoir_df, frac_df)
        print(f"✅ Generated {len(production_df)} production records")
        
        master_df = reservoir_df.merge(frac_df, on='well_id').merge(production_df, on='well_id')
        
        save_dataframe(reservoir_df, 'data/bronze/reservoir_properties.csv')
        save_dataframe(frac_df, 'data/bronze/fracturing_jobs.csv')
        save_dataframe(production_df, 'data/bronze/production_data.csv')
        save_dataframe(master_df, 'data/bronze/wells_synth.csv')
        
        print(f"\n🎉 Synthetic data generation complete!")
        print(f"📊 Master dataset: {master_df.shape[0]} rows × {master_df.shape[1]} columns")
        
        return {
            'reservoir': reservoir_df,
            'fracturing': frac_df,
            'production': production_df,
            'master': master_df
        }


if __name__ == "__main__":
    generator = SyntheticDataGenerator(n_wells=150)
    datasets = generator.generate_all()
