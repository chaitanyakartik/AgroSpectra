import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

# Set random seed for reproducibility
np.random.seed(42)

# ============================================
# 1. ENTITY MASTER DATA (Statistics Panel)
# ============================================

entity_data = {
    'mine_id': ['MN-KA-2023-001', 'MN-KA-2023-002', 'MN-KA-2023-003', 'MN-TN-2023-004', 'MN-TN-2023-005'],
    'mine_name': ['Kolar Gold Fields Site A', 'Bellary Iron Ore Mine', 'Chitradurga Limestone Quarry', 
                  'Salem Magnesite Mine', 'Dharmapuri Bauxite Mine'],
    'latitude': [13.1389, 15.1472, 14.2226, 11.6643, 12.1357],
    'longitude': [78.2981, 76.9214, 76.3986, 78.1460, 78.1582],
    'district': ['Kolar', 'Bellary', 'Chitradurga', 'Salem', 'Dharmapuri'],
    'state': ['Karnataka', 'Karnataka', 'Karnataka', 'Tamil Nadu', 'Tamil Nadu'],
    'country': ['India', 'India', 'India', 'India', 'India'],
    'ownership': ['Private', 'Public', 'Private', 'Public', 'Private'],
    'operator': ['ABC Mining Ltd', 'Karnataka State Mining Corp', 'XYZ Quarries Pvt Ltd', 
                 'Tamil Nadu Minerals Ltd', 'DEF Resources India'],
    'status': ['Active', 'Active', 'Inactive', 'Active', 'Under Observation'],
    'last_detection_date': ['2025-09-15', '2025-09-20', '2024-12-10', '2025-09-18', '2025-08-30'],
    
    # Spatial Characteristics
    'mining_area_ha': [45.3, 128.7, 32.4, 67.8, 89.2],
    'perimeter_length_m': [3200, 5800, 2400, 4100, 4900],
    'elevation_min_m': [720, 450, 680, 320, 540],
    'elevation_max_m': [780, 520, 720, 380, 590],
    'avg_depth_m': [28.5, 45.2, 18.3, 32.7, 38.9],
    'max_depth_m': [42.0, 68.5, 25.0, 48.3, 55.2],
    'estimated_volume_m3': [1290000, 5820000, 593000, 2218000, 3470000],
    
    # Compliance Indicators
    'distance_water_body_km': [2.3, 0.8, 3.5, 1.2, 0.5],
    'distance_forest_km': [1.5, 0.3, 4.2, 2.1, 0.2],
    'distance_habitation_km': [3.8, 2.5, 1.9, 4.2, 2.8],
    'inside_permitted_area': ['Yes', 'Yes', 'Yes', 'No', 'Yes'],
    'expansion_beyond_lease_ha': [0.0, 0.0, 0.0, 8.5, 0.0],
    'permitted_area_ha': [50.0, 150.0, 35.0, 60.0, 95.0],
    'detection_confidence': ['High', 'High', 'Medium', 'High', 'Medium'],
    'days_since_last_survey': [45, 30, 285, 38, 60],
    
    # Metadata
    'imagery_source': ['Sentinel-2', 'Sentinel-2', 'Landsat-8', 'Sentinel-2', 'Sentinel-2'],
    'imagery_date': ['2025-09-10', '2025-09-15', '2024-12-05', '2025-09-12', '2025-08-25'],
    'dem_source': ['Copernicus 30m', 'Copernicus 30m', 'SRTM 30m', 'Copernicus 30m', 'Copernicus 30m'],
    'dem_resolution_m': [30, 30, 30, 30, 30],
    'processing_date': ['2025-09-15', '2025-09-20', '2024-12-10', '2025-09-18', '2025-08-30'],
    'model_version': ['v2.3.1', 'v2.3.1', 'v2.1.0', 'v2.3.1', 'v2.3.0']
}

df_entities = pd.DataFrame(entity_data)

# ============================================
# 2. TEMPORAL MONITORING DATA
# ============================================

# Generate temporal data for each mine (monthly observations over 3 years)
temporal_records = []
start_date = datetime(2022, 10, 1)

for mine_id in df_entities['mine_id']:
    entity_info = df_entities[df_entities['mine_id'] == mine_id].iloc[0]
    current_area = entity_info['mining_area_ha']
    current_depth = entity_info['avg_depth_m']
    current_volume = entity_info['estimated_volume_m3']
    
    # Generate 36 months of data
    for month_offset in range(36):
        obs_date = start_date + timedelta(days=30 * month_offset)
        
        # Simulate growth patterns
        growth_factor = month_offset / 36.0
        area = current_area * (0.6 + 0.4 * growth_factor) + np.random.normal(0, 0.5)
        depth = current_depth * (0.5 + 0.5 * growth_factor) + np.random.normal(0, 1)
        volume = current_volume * (0.4 + 0.6 * growth_factor) + np.random.normal(0, 10000)
        
        # Activity status (90% active for active mines)
        is_active = 'Active' if (entity_info['status'] == 'Active' and np.random.random() > 0.1) else 'Inactive'
        
        # Vegetation loss and bare soil increase
        veg_loss_pct = min(100, 20 + growth_factor * 60 + np.random.normal(0, 5))
        bare_soil_pct = min(100, 15 + growth_factor * 55 + np.random.normal(0, 4))
        
        temporal_records.append({
            'mine_id': mine_id,
            'observation_date': obs_date.strftime('%Y-%m-%d'),
            'mining_area_ha': round(max(0, area), 2),
            'avg_depth_m': round(max(0, depth), 2),
            'estimated_volume_m3': int(max(0, volume)),
            'activity_status': is_active,
            'vegetation_loss_pct': round(veg_loss_pct, 1),
            'bare_soil_increase_pct': round(bare_soil_pct, 1),
            'distance_from_lease_boundary_m': round(np.random.uniform(-50, 300), 1)
        })

df_temporal = pd.DataFrame(temporal_records)

# ============================================
# 3. ELEVATION PROFILE DATA
# ============================================

# Generate elevation profiles for cross-sections
profile_records = []

for mine_id in df_entities['mine_id']:
    entity_info = df_entities[df_entities['mine_id'] == mine_id].iloc[0]
    
    # Create a profile line with 100 points
    profile_length_m = 500
    num_points = 100
    
    for i in range(num_points):
        distance = (i / num_points) * profile_length_m
        
        # Baseline elevation (original terrain)
        baseline_elev = entity_info['elevation_max_m'] - (i / num_points) * 20 + np.random.normal(0, 2)
        
        # Current elevation (after mining) - create a pit shape
        if 0.2 < (i / num_points) < 0.8:  # Mining area
            depth_factor = np.sin((i / num_points - 0.2) / 0.6 * np.pi)
            current_elev = baseline_elev - entity_info['avg_depth_m'] * depth_factor
        else:
            current_elev = baseline_elev
        
        # Calculate slope
        if i > 0:
            prev_elev = profile_records[-1]['current_elevation_m']
            slope_deg = np.degrees(np.arctan((current_elev - prev_elev) / (profile_length_m / num_points)))
        else:
            slope_deg = 0
        
        # Slope stability classification
        if abs(slope_deg) < 15:
            stability = 'Safe'
        elif abs(slope_deg) < 30:
            stability = 'Moderate'
        else:
            stability = 'Critical'
        
        # Water accumulation potential
        water_potential = 'High' if current_elev < (entity_info['elevation_min_m'] + 5) else 'Low'
        
        profile_records.append({
            'mine_id': mine_id,
            'profile_id': f'{mine_id}_PROFILE_001',
            'point_number': i,
            'distance_from_start_m': round(distance, 1),
            'baseline_elevation_m': round(baseline_elev, 2),
            'current_elevation_m': round(current_elev, 2),
            'elevation_difference_m': round(baseline_elev - current_elev, 2),
            'slope_degree': round(slope_deg, 2),
            'slope_stability': stability,
            'water_accumulation_potential': water_potential
        })

df_profiles = pd.DataFrame(profile_records)

# ============================================
# 4. COMPARATIVE STATISTICS (District Level)
# ============================================

district_stats = {
    'district': ['Kolar', 'Bellary', 'Chitradurga', 'Salem', 'Dharmapuri'],
    'state': ['Karnataka', 'Karnataka', 'Karnataka', 'Tamil Nadu', 'Tamil Nadu'],
    'total_mines': [12, 28, 8, 15, 10],
    'avg_expansion_rate_pct_year': [8.5, 12.3, 5.2, 9.8, 15.2],
    'avg_mining_area_ha': [52.3, 98.7, 28.4, 71.2, 65.8],
    'total_violations': [2, 5, 0, 3, 4]
}

df_district_stats = pd.DataFrame(district_stats)

# ============================================
# 5. COMPLIANCE FLAGS & NOTES
# ============================================

compliance_flags = []

for _, entity in df_entities.iterrows():
    flags = []
    
    if entity['inside_permitted_area'] == 'No':
        flags.append({
            'mine_id': entity['mine_id'],
            'flag_type': 'Violation',
            'severity': 'High',
            'description': f"Expansion beyond lease boundary: {entity['expansion_beyond_lease_ha']} ha",
            'action_required': 'Immediate field inspection',
            'flagged_date': '2025-09-20',
            'status': 'Open'
        })
    
    if entity['distance_forest_km'] < 1.0:
        flags.append({
            'mine_id': entity['mine_id'],
            'flag_type': 'Environmental Risk',
            'severity': 'High',
            'description': f"Within {entity['distance_forest_km']} km of forest boundary",
            'action_required': 'Environmental impact assessment required',
            'flagged_date': '2025-09-18',
            'status': 'Under Review'
        })
    
    if entity['distance_water_body_km'] < 1.0:
        flags.append({
            'mine_id': entity['mine_id'],
            'flag_type': 'Water Contamination Risk',
            'severity': 'Medium',
            'description': f"Only {entity['distance_water_body_km']} km from water body",
            'action_required': 'Water quality monitoring',
            'flagged_date': '2025-09-15',
            'status': 'Monitoring'
        })
    
    if entity['days_since_last_survey'] > 180:
        flags.append({
            'mine_id': entity['mine_id'],
            'flag_type': 'Survey Overdue',
            'severity': 'Low',
            'description': f"{entity['days_since_last_survey']} days since last verified survey",
            'action_required': 'Schedule ground verification',
            'flagged_date': '2025-09-10',
            'status': 'Scheduled'
        })
    
    compliance_flags.extend(flags)

df_compliance_flags = pd.DataFrame(compliance_flags)

# ============================================
# SAVE ALL DATASETS
# ============================================

print("=" * 60)
print("MINING SITE MONITORING DUMMY DATASET")
print("=" * 60)
print(f"\n1. Entity Master Data: {len(df_entities)} mines")
print(df_entities[['mine_id', 'mine_name', 'status', 'mining_area_ha', 'inside_permitted_area']].to_string(index=False))

print(f"\n2. Temporal Monitoring Data: {len(df_temporal)} observations")
print(df_temporal.head(10).to_string(index=False))

print(f"\n3. Elevation Profile Data: {len(df_profiles)} profile points")
print(df_profiles.head(10).to_string(index=False))

print(f"\n4. District Statistics: {len(df_district_stats)} districts")
print(df_district_stats.to_string(index=False))

print(f"\n5. Compliance Flags: {len(df_compliance_flags)} flags")
print(df_compliance_flags.to_string(index=False))

# Export to CSV
df_entities.to_csv('mining_entities.csv', index=False)
df_temporal.to_csv('mining_temporal_data.csv', index=False)
df_profiles.to_csv('mining_elevation_profiles.csv', index=False)
df_district_stats.to_csv('district_statistics.csv', index=False)
df_compliance_flags.to_csv('compliance_flags.csv', index=False)

print("\n" + "=" * 60)
print("All datasets exported to CSV files!")
print("=" * 60)

# Generate summary statistics
print("\n\nSUMMARY STATISTICS")
print("-" * 60)
print(f"Total Mining Area Monitored: {df_entities['mining_area_ha'].sum():.1f} ha")
print(f"Total Excavated Volume: {df_entities['estimated_volume_m3'].sum():,} m³")
print(f"Active Mines: {len(df_entities[df_entities['status'] == 'Active'])}")
print(f"Mines with Violations: {len(df_entities[df_entities['inside_permitted_area'] == 'No'])}")
print(f"High Priority Flags: {len(df_compliance_flags[df_compliance_flags['severity'] == 'High'])}")
print(f"Average Expansion Rate: {df_district_stats['avg_expansion_rate_pct_year'].mean():.1f}% per year")