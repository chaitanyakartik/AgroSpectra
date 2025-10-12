import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import os

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Set style for all plots
sns.set_style("whitegrid")
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Set random seed for reproducibility
np.random.seed(42)

print("=" * 80)
print("GENERATING MINING SITE MONITORING VISUALIZATIONS")
print("=" * 80)

# ============================================
# LOAD DATA (from previously created CSVs)
# ============================================

# Create sample data if CSVs don't exist
entity_data = {
    'mine_id': ['MN-KA-2023-001', 'MN-KA-2023-002', 'MN-KA-2023-003', 'MN-TN-2023-004', 'MN-TN-2023-005'],
    'mine_name': ['Kolar Gold Fields Site A', 'Bellary Iron Ore Mine', 'Chitradurga Limestone Quarry', 
                  'Salem Magnesite Mine', 'Dharmapuri Bauxite Mine'],
    'district': ['Kolar', 'Bellary', 'Chitradurga', 'Salem', 'Dharmapuri'],
    'state': ['Karnataka', 'Karnataka', 'Karnataka', 'Tamil Nadu', 'Tamil Nadu'],
    'mining_area_ha': [45.3, 128.7, 32.4, 67.8, 89.2],
    'avg_depth_m': [28.5, 45.2, 18.3, 32.7, 38.9],
    'max_depth_m': [42.0, 68.5, 25.0, 48.3, 55.2],
    'estimated_volume_m3': [1290000, 5820000, 593000, 2218000, 3470000],
    'status': ['Active', 'Active', 'Inactive', 'Active', 'Under Observation'],
    'inside_permitted_area': ['Yes', 'Yes', 'Yes', 'No', 'Yes'],
    'expansion_beyond_lease_ha': [0.0, 0.0, 0.0, 8.5, 0.0],
    'distance_water_body_km': [2.3, 0.8, 3.5, 1.2, 0.5],
    'distance_forest_km': [1.5, 0.3, 4.2, 2.1, 0.2],
}
df_entities = pd.DataFrame(entity_data)

# Generate temporal data
temporal_records = []
start_date = datetime(2022, 10, 1)

for mine_id in df_entities['mine_id']:
    entity_info = df_entities[df_entities['mine_id'] == mine_id].iloc[0]
    current_area = entity_info['mining_area_ha']
    current_depth = entity_info['avg_depth_m']
    current_volume = entity_info['estimated_volume_m3']
    
    for month_offset in range(36):
        obs_date = start_date + timedelta(days=30 * month_offset)
        growth_factor = month_offset / 36.0
        
        area = current_area * (0.6 + 0.4 * growth_factor) + np.random.normal(0, 0.5)
        depth = current_depth * (0.5 + 0.5 * growth_factor) + np.random.normal(0, 1)
        volume = current_volume * (0.4 + 0.6 * growth_factor) + np.random.normal(0, 10000)
        
        is_active = 'Active' if (entity_info['status'] == 'Active' and np.random.random() > 0.1) else 'Inactive'
        veg_loss_pct = min(100, 20 + growth_factor * 60 + np.random.normal(0, 5))
        bare_soil_pct = min(100, 15 + growth_factor * 55 + np.random.normal(0, 4))
        
        temporal_records.append({
            'mine_id': mine_id,
            'mine_name': entity_info['mine_name'],
            'observation_date': obs_date,
            'year_month': obs_date.strftime('%Y-%m'),
            'mining_area_ha': round(max(0, area), 2),
            'avg_depth_m': round(max(0, depth), 2),
            'estimated_volume_m3': int(max(0, volume)),
            'activity_status': is_active,
            'vegetation_loss_pct': round(veg_loss_pct, 1),
            'bare_soil_increase_pct': round(bare_soil_pct, 1),
        })

df_temporal = pd.DataFrame(temporal_records)

# District statistics
district_stats = {
    'district': ['Kolar', 'Bellary', 'Chitradurga', 'Salem', 'Dharmapuri'],
    'state': ['Karnataka', 'Karnataka', 'Karnataka', 'Tamil Nadu', 'Tamil Nadu'],
    'avg_expansion_rate_pct_year': [8.5, 12.3, 5.2, 9.8, 15.2],
    'avg_mining_area_ha': [52.3, 98.7, 28.4, 71.2, 65.8],
    'total_violations': [2, 5, 0, 3, 4]
}
df_district_stats = pd.DataFrame(district_stats)

# Generate elevation profiles
def generate_elevation_profile(mine_id, entity_info):
    profile_length_m = 500
    num_points = 100
    profile_data = []
    
    for i in range(num_points):
        distance = (i / num_points) * profile_length_m
        baseline_elev = entity_info['elevation_max_m'] - (i / num_points) * 20 + np.random.normal(0, 2)
        
        current_elev = baseline_elev
        if 0.2 < (i / num_points) < 0.8:
            depth_factor = np.sin((i / num_points - 0.2) / 0.6 * np.pi)
            current_elev = baseline_elev - entity_info['avg_depth_m'] * depth_factor
        
        profile_data.append({
            'mine_id': mine_id,
            'distance_m': round(distance, 1),
            'baseline_elevation_m': round(baseline_elev, 2),
            'current_elevation_m': round(current_elev, 2),
            'elevation_difference_m': round(baseline_elev - current_elev, 2)
        })
    
    return pd.DataFrame(profile_data)

# Add elevation max to entities for profile generation
df_entities['elevation_max_m'] = [780, 520, 720, 380, 590]

profile_dfs = {}
for _, entity in df_entities.iterrows():
    profile_dfs[entity['mine_id']] = generate_elevation_profile(entity['mine_id'], entity)

print("\n✓ Data loaded successfully")

# # ============================================
# # VISUALIZATION 1: AREA EXPANSION OVER TIME
# # ============================================
# print("\n[1/15] Creating Area Expansion Over Time chart...")

# fig, ax = plt.subplots(figsize=(14, 6))
# for mine_id in df_entities['mine_id'].head(3):  # Plot first 3 mines
#     mine_data = df_temporal[df_temporal['mine_id'] == mine_id]
#     mine_name = mine_data['mine_name'].iloc[0]
#     ax.plot(mine_data['observation_date'], mine_data['mining_area_ha'], 
#             marker='o', label=mine_name, linewidth=2, markersize=4)

# ax.set_xlabel('Date', fontsize=12, fontweight='bold')
# ax.set_ylabel('Mining Area (ha)', fontsize=12, fontweight='bold')
# ax.set_title('Area Expansion Over Time (Temporal Monitoring)', fontsize=14, fontweight='bold', pad=20)
# ax.legend(loc='upper left', frameon=True, shadow=True)
# ax.grid(True, alpha=0.3)
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.savefig('images/01_area_expansion_over_time.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("   ✓ Saved: images/01_area_expansion_over_time.png")

# # ============================================
# # VISUALIZATION 2: DEPTH CHANGE OVER TIME
# # ============================================
# print("[2/15] Creating Depth Change Over Time chart...")

# fig, ax = plt.subplots(figsize=(14, 6))
# for mine_id in df_entities['mine_id'].head(3):
#     mine_data = df_temporal[df_temporal['mine_id'] == mine_id]
#     mine_name = mine_data['mine_name'].iloc[0]
#     ax.plot(mine_data['observation_date'], mine_data['avg_depth_m'], 
#             marker='s', label=mine_name, linewidth=2, markersize=4)

# ax.set_xlabel('Date', fontsize=12, fontweight='bold')
# ax.set_ylabel('Average Depth (m)', fontsize=12, fontweight='bold')
# ax.set_title('Depth Change Over Time', fontsize=14, fontweight='bold', pad=20)
# ax.legend(loc='upper left', frameon=True, shadow=True)
# ax.grid(True, alpha=0.3)
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.savefig('images/02_depth_change_over_time.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("   ✓ Saved: images/02_depth_change_over_time.png")

# # ============================================
# # VISUALIZATION 3: VOLUME GROWTH OVER TIME
# # ============================================
# print("[3/15] Creating Volume Growth Over Time chart...")

# fig, ax = plt.subplots(figsize=(14, 6))
# for mine_id in df_entities['mine_id'].head(3):
#     mine_data = df_temporal[df_temporal['mine_id'] == mine_id]
#     mine_name = mine_data['mine_name'].iloc[0]
#     ax.plot(mine_data['observation_date'], mine_data['estimated_volume_m3'] / 1000000, 
#             marker='^', label=mine_name, linewidth=2, markersize=4)

# ax.set_xlabel('Date', fontsize=12, fontweight='bold')
# ax.set_ylabel('Excavated Volume (Million m³)', fontsize=12, fontweight='bold')
# ax.set_title('Volume Growth Over Time', fontsize=14, fontweight='bold', pad=20)
# ax.legend(loc='upper left', frameon=True, shadow=True)
# ax.grid(True, alpha=0.3)
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.savefig('images/03_volume_growth_over_time.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("   ✓ Saved: images/03_volume_growth_over_time.png")

# # ============================================
# # VISUALIZATION 4: LAND COVER CHANGE
# # ============================================
# print("[4/15] Creating Land Cover Change chart...")

# selected_mine = 'MN-KA-2023-001'
# mine_data = df_temporal[df_temporal['mine_id'] == selected_mine]
# mine_name = mine_data['mine_name'].iloc[0]

# fig, ax = plt.subplots(figsize=(14, 6))
# ax.plot(mine_data['observation_date'], mine_data['vegetation_loss_pct'], 
#         marker='o', label='Vegetation Loss', linewidth=2.5, color='#e74c3c', markersize=5)
# ax.plot(mine_data['observation_date'], mine_data['bare_soil_increase_pct'], 
#         marker='s', label='Bare Soil Increase', linewidth=2.5, color='#f39c12', markersize=5)

# ax.fill_between(mine_data['observation_date'], mine_data['vegetation_loss_pct'], alpha=0.3, color='#e74c3c')
# ax.fill_between(mine_data['observation_date'], mine_data['bare_soil_increase_pct'], alpha=0.3, color='#f39c12')

# ax.set_xlabel('Date', fontsize=12, fontweight='bold')
# ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
# ax.set_title(f'Land Cover Change Around Site: {mine_name}', fontsize=14, fontweight='bold', pad=20)
# ax.legend(loc='upper left', frameon=True, shadow=True, fontsize=11)
# ax.grid(True, alpha=0.3)
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.savefig('images/04_land_cover_change.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("   ✓ Saved: images/04_land_cover_change.png")

# # ============================================
# # VISUALIZATION 5: ACTIVITY STATUS TIMELINE
# # ============================================
# print("[5/15] Creating Activity Status Timeline...")

# selected_mine = 'MN-KA-2023-001'
# mine_data = df_temporal[df_temporal['mine_id'] == selected_mine].copy()
# mine_data['is_active'] = (mine_data['activity_status'] == 'Active').astype(int)

# fig, ax = plt.subplots(figsize=(14, 4))
# colors = ['#e74c3c' if status == 'Inactive' else '#27ae60' 
#           for status in mine_data['activity_status']]
# ax.bar(mine_data['observation_date'], mine_data['is_active'], color=colors, width=20)

# ax.set_xlabel('Date', fontsize=12, fontweight='bold')
# ax.set_ylabel('Activity Status', fontsize=12, fontweight='bold')
# ax.set_title(f'Active/Inactive Periods Timeline: {mine_data["mine_name"].iloc[0]}', 
#              fontsize=14, fontweight='bold', pad=20)
# ax.set_yticks([0, 1])
# ax.set_yticklabels(['Inactive', 'Active'])
# ax.grid(True, alpha=0.3, axis='x')
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.savefig('images/05_activity_timeline.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("   ✓ Saved: images/05_activity_timeline.png")

# # ============================================
# # VISUALIZATION 6: DISTRICT COMPARISON - EXPANSION RATE
# # ============================================
# print("[6/15] Creating District Expansion Rate Comparison...")

# fig, ax = plt.subplots(figsize=(12, 6))
# bars = ax.bar(df_district_stats['district'], df_district_stats['avg_expansion_rate_pct_year'], 
#               color=sns.color_palette("RdYlGn_r", len(df_district_stats)), edgecolor='black', linewidth=1.5)

# for i, bar in enumerate(bars):
#     height = bar.get_height()
#     ax.text(bar.get_x() + bar.get_width()/2., height,
#             f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=10)

# ax.set_xlabel('District', fontsize=12, fontweight='bold')
# ax.set_ylabel('Average Expansion Rate (% per year)', fontsize=12, fontweight='bold')
# ax.set_title('District Comparison - Average Expansion Rate', fontsize=14, fontweight='bold', pad=20)
# ax.grid(True, alpha=0.3, axis='y')
# plt.tight_layout()
# plt.savefig('images/06_district_expansion_comparison.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("   ✓ Saved: images/06_district_expansion_comparison.png")

# # ============================================
# # VISUALIZATION 7: VIOLATIONS BY DISTRICT
# # ============================================
# print("[7/15] Creating Violations by District chart...")

# fig, ax = plt.subplots(figsize=(12, 6))
# colors_violations = ['#27ae60' if v == 0 else '#e74c3c' for v in df_district_stats['total_violations']]
# bars = ax.bar(df_district_stats['district'], df_district_stats['total_violations'], 
#               color=colors_violations, edgecolor='black', linewidth=1.5)

# for i, bar in enumerate(bars):
#     height = bar.get_height()
#     ax.text(bar.get_x() + bar.get_width()/2., height,
#             f'{int(height)}', ha='center', va='bottom', fontweight='bold', fontsize=11)

# ax.set_xlabel('District', fontsize=12, fontweight='bold')
# ax.set_ylabel('Total Violations', fontsize=12, fontweight='bold')
# ax.set_title('Compliance Violations by District', fontsize=14, fontweight='bold', pad=20)
# ax.grid(True, alpha=0.3, axis='y')
# plt.tight_layout()
# plt.savefig('images/07_violations_by_district.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("   ✓ Saved: images/07_violations_by_district.png")

# # ============================================
# # VISUALIZATION 8: MINING AREA BY DISTRICT
# # ============================================
# print("[8/15] Creating Average Mining Area by District...")

# fig, ax = plt.subplots(figsize=(12, 6))
# sns.barplot(data=df_district_stats, x='district', y='avg_mining_area_ha', 
#             palette='viridis', ax=ax, edgecolor='black', linewidth=1.5)

# for i, v in enumerate(df_district_stats['avg_mining_area_ha']):
#     ax.text(i, v, f'{v:.1f} ha', ha='center', va='bottom', fontweight='bold', fontsize=10)

# ax.set_xlabel('District', fontsize=12, fontweight='bold')
# ax.set_ylabel('Average Mining Area (ha)', fontsize=12, fontweight='bold')
# ax.set_title('Average Mining Area by District', fontsize=14, fontweight='bold', pad=20)
# ax.grid(True, alpha=0.3, axis='y')
# plt.tight_layout()
# plt.savefig('images/08_avg_area_by_district.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("   ✓ Saved: images/08_avg_area_by_district.png")

# # ============================================
# # VISUALIZATION 9: TOP 5 EXPANDING MINES
# # ============================================
# print("[9/15] Creating Top 5 Expanding Mines chart...")

# # Calculate expansion rate for each mine
# df_entities_sorted = df_entities.sort_values('mining_area_ha', ascending=False).head(5)

# fig, ax = plt.subplots(figsize=(12, 6))
# bars = ax.barh(df_entities_sorted['mine_name'], df_entities_sorted['mining_area_ha'], 
#                color=sns.color_palette('rocket_r', len(df_entities_sorted)), 
#                edgecolor='black', linewidth=1.5)

# for i, (idx, row) in enumerate(df_entities_sorted.iterrows()):
#     ax.text(row['mining_area_ha'], i, f"  {row['mining_area_ha']:.1f} ha", 
#             va='center', fontweight='bold', fontsize=10)

# ax.set_xlabel('Mining Area (ha)', fontsize=12, fontweight='bold')
# ax.set_ylabel('Mine Name', fontsize=12, fontweight='bold')
# ax.set_title('Top 5 Largest Mining Sites in Region', fontsize=14, fontweight='bold', pad=20)
# ax.grid(True, alpha=0.3, axis='x')
# plt.tight_layout()
# plt.savefig('images/09_top5_expanding_mines.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("   ✓ Saved: images/09_top5_expanding_mines.png")

# # ============================================
# # VISUALIZATION 10: ELEVATION PROFILE - TERRAIN CROSS SECTION
# # ============================================
# print("[10/15] Creating Elevation Profile - Terrain Cross Section...")

# selected_mine = 'MN-KA-2023-001'
# profile_data = profile_dfs[selected_mine]
# mine_info = df_entities[df_entities['mine_id'] == selected_mine].iloc[0]

# fig, ax = plt.subplots(figsize=(14, 6))
# ax.fill_between(profile_data['distance_m'], profile_data['baseline_elevation_m'], 
#                 alpha=0.3, color='#27ae60', label='Baseline Elevation')
# ax.plot(profile_data['distance_m'], profile_data['baseline_elevation_m'], 
#         linewidth=2.5, color='#27ae60', marker='o', markersize=3)

# ax.fill_between(profile_data['distance_m'], profile_data['current_elevation_m'], 
#                 alpha=0.5, color='#3498db', label='Current Elevation')
# ax.plot(profile_data['distance_m'], profile_data['current_elevation_m'], 
#         linewidth=2.5, color='#3498db', marker='s', markersize=3)

# ax.set_xlabel('Distance from Start (m)', fontsize=12, fontweight='bold')
# ax.set_ylabel('Elevation (m)', fontsize=12, fontweight='bold')
# ax.set_title(f'Terrain Cross-Section: {mine_info["mine_name"]} (Current vs Baseline)', 
#              fontsize=14, fontweight='bold', pad=20)
# ax.legend(loc='upper right', frameon=True, shadow=True, fontsize=11)
# ax.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.savefig('images/10_elevation_profile_cross_section.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("   ✓ Saved: images/10_elevation_profile_cross_section.png")

# # ============================================
# # VISUALIZATION 11: EXCAVATION DEPTH PROFILE
# # ============================================
# print("[11/15] Creating Excavation Depth Profile...")

# fig, ax = plt.subplots(figsize=(14, 6))
# ax.fill_between(profile_data['distance_m'], 0, profile_data['elevation_difference_m'], 
#                 alpha=0.6, color='#e74c3c', label='Excavation Depth')
# ax.plot(profile_data['distance_m'], profile_data['elevation_difference_m'], 
#         linewidth=2.5, color='#c0392b', marker='o', markersize=3)

# max_depth_idx = profile_data['elevation_difference_m'].idxmax()
# max_depth_point = profile_data.loc[max_depth_idx]
# ax.axhline(y=max_depth_point['elevation_difference_m'], color='red', linestyle='--', 
#            linewidth=2, alpha=0.7, label=f'Max Depth: {max_depth_point["elevation_difference_m"]:.1f}m')
# ax.scatter(max_depth_point['distance_m'], max_depth_point['elevation_difference_m'], 
#            color='red', s=200, zorder=5, edgecolor='black', linewidth=2)

# ax.set_xlabel('Distance from Start (m)', fontsize=12, fontweight='bold')
# ax.set_ylabel('Excavation Depth (m)', fontsize=12, fontweight='bold')
# ax.set_title(f'Elevation Difference (Excavation Depth): {mine_info["mine_name"]}', 
#              fontsize=14, fontweight='bold', pad=20)
# ax.legend(loc='upper right', frameon=True, shadow=True, fontsize=11)
# ax.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.savefig('images/11_excavation_depth_profile.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("   ✓ Saved: images/11_excavation_depth_profile.png")

# # # ============================================
# # # VISUALIZATION 12: PROXIMITY TO SENSITIVE ZONES
# # # ============================================
# # print("[12/15] Creating Proximity to Sensitive Zones heatmap...")

# # # Check available columns first
# # print("Available columns:", df_entities.columns.tolist())

# # # Use only the columns that actually exist
# # available_columns = ['mine_name']
# # distance_columns = []

# # # Check for each distance column and add if it exists
# # for col in ['distance_water_body_km', 'distance_forest_km', 'distance_habitation_km']:
# #     if col in df_entities.columns:
# #         distance_columns.append(col)
# #     else:
# #         print(f"Warning: Column '{col}' not found in DataFrame")

# # if distance_columns:
# #     proximity_data = df_entities[['mine_name'] + distance_columns].head()
# #     proximity_data = proximity_data.set_index('mine_name')

# #     fig, ax = plt.subplots(figsize=(12, 6))
# #     sns.heatmap(proximity_data.T, annot=True, fmt='.1f', cmap='RdYlGn', 
# #                 linewidths=2, linecolor='black', cbar_kws={'label': 'Distance (km)'}, 
# #                 ax=ax, vmin=0, vmax=5)

# #     ax.set_xlabel('Mine Name', fontsize=12, fontweight='bold')
# #     ax.set_ylabel('Sensitive Zone Type', fontsize=12, fontweight='bold')
# #     ax.set_title('Proximity to Sensitive Zones (km)', fontsize=14, fontweight='bold', pad=20)
    
# #     # Create labels based on available columns
# #     labels = []
# #     for col in distance_columns:
# #         if 'water' in col.lower():
# #             labels.append('Water Body')
# #         elif 'forest' in col.lower():
# #             labels.append('Forest')
# #         elif 'habitation' in col.lower():
# #             labels.append('Habitation')
# #         else:
# #             labels.append(col.replace('distance_', '').replace('_km', '').title())
    
# #     ax.set_yticklabels(labels, rotation=0)
# #     plt.tight_layout()
# #     plt.savefig('images/12_proximity_sensitive_zones.png', dpi=300, bbox_inches='tight')
# #     plt.close()
# #     print("   ✓ Saved: images/12_proximity_sensitive_zones.png")
# # else:
# #     print("   ⚠ No distance columns found, skipping proximity visualization")
# # ============================================
# # VISUALIZATION 13: COMPLIANCE STATUS OVERVIEW
# # ============================================
# print("[13/15] Creating Compliance Status Overview...")

# compliance_counts = df_entities['inside_permitted_area'].value_counts()

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# # Pie chart
# colors_pie = ['#27ae60', '#e74c3c']
# explode = (0.05, 0.05)
# wedges, texts, autotexts = ax1.pie(compliance_counts.values, labels=compliance_counts.index, 
#                                      autopct='%1.1f%%', startangle=90, colors=colors_pie,
#                                      explode=explode, textprops={'fontsize': 12, 'fontweight': 'bold'},
#                                      shadow=True)
# ax1.set_title('Compliance Status Distribution', fontsize=14, fontweight='bold', pad=20)

# # Bar chart with violations
# df_violations = df_entities[['mine_name', 'expansion_beyond_lease_ha']].copy()
# df_violations = df_violations[df_violations['expansion_beyond_lease_ha'] > 0]

# if len(df_violations) > 0:
#     bars = ax2.barh(df_violations['mine_name'], df_violations['expansion_beyond_lease_ha'], 
#                     color='#e74c3c', edgecolor='black', linewidth=1.5)
#     for i, bar in enumerate(bars):
#         width = bar.get_width()
#         ax2.text(width, bar.get_y() + bar.get_height()/2., 
#                 f'{width:.1f} ha', ha='left', va='center', fontweight='bold', fontsize=10)
#     ax2.set_xlabel('Expansion Beyond Lease (ha)', fontsize=12, fontweight='bold')
#     ax2.set_ylabel('Mine Name', fontsize=12, fontweight='bold')
#     ax2.set_title('Lease Boundary Violations', fontsize=14, fontweight='bold', pad=20)
#     ax2.grid(True, alpha=0.3, axis='x')
# else:
#     ax2.text(0.5, 0.5, 'No Violations Detected', ha='center', va='center', 
#              fontsize=16, fontweight='bold', transform=ax2.transAxes)
#     ax2.set_title('Lease Boundary Violations', fontsize=14, fontweight='bold', pad=20)

# plt.tight_layout()
# plt.savefig('images/13_compliance_status_overview.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("   ✓ Saved: images/13_compliance_status_overview.png")

# # ============================================
# # VISUALIZATION 14: DEPTH VS AREA SCATTER
# # ============================================
# print("[14/15] Creating Depth vs Area Scatter Plot...")

# fig, ax = plt.subplots(figsize=(12, 8))

# # Create scatter plot
# scatter = ax.scatter(df_entities['mining_area_ha'], df_entities['max_depth_m'], 
#                      s=df_entities['estimated_volume_m3']/10000, 
#                      c=df_entities['mining_area_ha'], cmap='viridis', 
#                      alpha=0.6, edgecolors='black', linewidth=2)

# # Add mine names as labels
# for idx, row in df_entities.iterrows():
#     ax.annotate(row['mine_name'], 
#                 (row['mining_area_ha'], row['max_depth_m']),
#                 xytext=(5, 5), textcoords='offset points',
#                 fontsize=9, fontweight='bold',
#                 bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))

# ax.set_xlabel('Mining Area (ha)', fontsize=12, fontweight='bold')
# ax.set_ylabel('Maximum Depth (m)', fontsize=12, fontweight='bold')
# ax.set_title('Mining Area vs Depth (Bubble size = Excavated Volume)', 
#              fontsize=14, fontweight='bold', pad=20)
# ax.grid(True, alpha=0.3)

# # Add colorbar
# cbar = plt.colorbar(scatter, ax=ax)
# cbar.set_label('Mining Area (ha)', fontsize=10, fontweight='bold')

# plt.tight_layout()
# plt.savefig('images/14_depth_vs_area_scatter.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("   ✓ Saved: images/14_depth_vs_area_scatter.png")

# # ============================================
# # VISUALIZATION 15: MULTI-YEAR PROFILE COMPARISON
# # ============================================
# print("[15/15] Creating Multi-Year Profile Comparison...")

# selected_mine = 'MN-KA-2023-001'
# profile_data = profile_dfs[selected_mine].copy()
# mine_info = df_entities[df_entities['mine_id'] == selected_mine].iloc[0]

# # Simulate historical profiles
# profile_data['year_2023'] = profile_data.apply(
#     lambda row: row['baseline_elevation_m'] - (row['elevation_difference_m'] * 0.4), axis=1)
# profile_data['year_2024'] = profile_data.apply(
#     lambda row: row['baseline_elevation_m'] - (row['elevation_difference_m'] * 0.7), axis=1)
# profile_data['year_2025'] = profile_data['current_elevation_m']

# fig, ax = plt.subplots(figsize=(14, 6))
# ax.plot(profile_data['distance_m'], profile_data['baseline_elevation_m'], 
#         linewidth=2.5, color='gray', linestyle='--', label='Baseline (Original)', alpha=0.7)
# ax.plot(profile_data['distance_m'], profile_data['year_2023'], 
#         linewidth=2, color='#3498db', label='2023', marker='o', markersize=2)
# ax.plot(profile_data['distance_m'], profile_data['year_2024'], 
#         linewidth=2, color='#f39c12', label='2024', marker='s', markersize=2)
# ax.plot(profile_data['distance_m'], profile_data['year_2025'], 
#         linewidth=2.5, color='#e74c3c', label='2025 (Current)', marker='^', markersize=2)

# ax.fill_between(profile_data['distance_m'], profile_data['baseline_elevation_m'], 
#                 profile_data['year_2025'], alpha=0.2, color='red')

# ax.set_xlabel('Distance from Start (m)', fontsize=12, fontweight='bold')
# ax.set_ylabel('Elevation (m)', fontsize=12, fontweight='bold')
# ax.set_title(f'Multi-Year Profile Comparison: {mine_info["mine_name"]} (Deepening Trend)', 
#              fontsize=14, fontweight='bold', pad=20)
# ax.legend(loc='upper right', frameon=True, shadow=True, fontsize=11)
# ax.grid(True, alpha=0.3)
# plt.tight_layout()
# plt.savefig('images/15_multi_year_profile_comparison.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("   ✓ Saved: images/15_multi_year_profile_comparison.png")

# # ============================================
# # VISUALIZATION 16: STATISTICS SUMMARY TABLE
# # ============================================
# print("[16/15] Creating Statistics Summary Table...")

# fig, ax = plt.subplots(figsize=(14, 8))
# ax.axis('tight')
# ax.axis('off')

# # Prepare data for selected mine
# selected_mine = 'MN-KA-2023-001'
# mine_info = df_entities[df_entities['mine_id'] == selected_mine].iloc[0]

# table_data = [
#     ['ENTITY DETAILS', ''],
#     ['Mine ID', mine_info['mine_id']],
#     ['Mine Name', mine_info['mine_name']],
#     ['District', mine_info['district']],
#     ['State', mine_info['state']],
#     ['Status', mine_info['status']],
#     ['', ''],
#     ['SPATIAL CHARACTERISTICS', ''],
#     ['Mining Area', f"{mine_info['mining_area_ha']:.1f} ha"],
#     ['Average Depth', f"{mine_info['avg_depth_m']:.1f} m"],
#     ['Maximum Depth', f"{mine_info['max_depth_m']:.1f} m"],
#     ['Excavated Volume', f"{(mine_info['estimated_volume_m3']/1000000):.2f} M m³"],
#     ['', ''],
#     ['COMPLIANCE INDICATORS', ''],
#     ['Distance to Water Body', f"{mine_info['distance_water_body_km']:.1f} km"],
#     ['Distance to Forest', f"{mine_info['distance_forest_km']:.1f} km"],
#     ['Inside Permitted Area', mine_info['inside_permitted_area']],
#     ['Expansion Beyond Lease', f"{mine_info['expansion_beyond_lease_ha']:.1f} ha"],
# ]

# table = ax.table(cellText=table_data, cellLoc='left', loc='center',
#                 colWidths=[0.4, 0.6])
# table.auto_set_font_size(False)
# table.set_fontsize(11)
# table.scale(1, 2.5)

# # Style the table
# for i, row in enumerate(table_data):
#     if row[1] == '' and row[0] != '':  # Header rows
#         table[(i, 0)].set_facecolor('#34495e')
#         table[(i, 0)].set_text_props(weight='bold', color='white', fontsize=12)
#         table[(i, 1)].set_facecolor('#34495e')
#     elif i % 2 == 0:
#         table[(i, 0)].set_facecolor('#ecf0f1')
#         table[(i, 1)].set_facecolor('#ecf0f1')
    
#     table[(i, 0)].set_text_props(weight='bold')

# plt.title(f'Mining Site Statistics Summary: {mine_info["mine_name"]}', 
#           fontsize=16, fontweight='bold', pad=20)
# plt.savefig('images/16_statistics_summary_table.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("   ✓ Saved: images/16_statistics_summary_table.png")

# # ============================================
# # VISUALIZATION 17: SLOPE STABILITY ANALYSIS
# # ============================================
# print("[17/15] Creating Slope Stability Analysis...")

# # Generate slope data
# profile_data = profile_dfs['MN-KA-2023-001'].copy()
# profile_data['slope'] = profile_data['elevation_difference_m'].diff() / (profile_data['distance_m'].diff())
# profile_data['slope_degree'] = np.degrees(np.arctan(profile_data['slope'].fillna(0)))

# # Classify stability
# def classify_stability(slope):
#     if abs(slope) < 15:
#         return 'Safe'
#     elif abs(slope) < 30:
#         return 'Moderate'
#     else:
#         return 'Critical'

# profile_data['stability'] = profile_data['slope_degree'].apply(classify_stability)

# # Count by stability
# stability_counts = profile_data['stability'].value_counts()

# fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# # Pie chart
# colors_stability = {'Safe': '#27ae60', 'Moderate': '#f39c12', 'Critical': '#e74c3c'}
# colors_list = [colors_stability[cat] for cat in stability_counts.index]
# wedges, texts, autotexts = ax1.pie(stability_counts.values, labels=stability_counts.index, 
#                                      autopct='%1.1f%%', startangle=90, colors=colors_list,
#                                      explode=(0.05, 0.05, 0.1), 
#                                      textprops={'fontsize': 12, 'fontweight': 'bold'},
#                                      shadow=True)
# ax1.set_title('Slope Stability Classification', fontsize=14, fontweight='bold', pad=20)

# # Slope profile with color coding
# for stability_type, color in colors_stability.items():
#     data_subset = profile_data[profile_data['stability'] == stability_type]
#     ax2.scatter(data_subset['distance_m'], data_subset['slope_degree'], 
#                label=stability_type, color=color, s=50, alpha=0.7, edgecolors='black')

# ax2.axhline(y=15, color='orange', linestyle='--', linewidth=2, alpha=0.7, label='Moderate Threshold')
# ax2.axhline(y=30, color='red', linestyle='--', linewidth=2, alpha=0.7, label='Critical Threshold')
# ax2.axhline(y=-15, color='orange', linestyle='--', linewidth=2, alpha=0.7)
# ax2.axhline(y=-30, color='red', linestyle='--', linewidth=2, alpha=0.7)

# ax2.set_xlabel('Distance (m)', fontsize=12, fontweight='bold')
# ax2.set_ylabel('Slope (degrees)', fontsize=12, fontweight='bold')
# ax2.set_title('Slope Analysis Along Profile', fontsize=14, fontweight='bold', pad=20)
# ax2.legend(loc='best', frameon=True, shadow=True)
# ax2.grid(True, alpha=0.3)

# plt.tight_layout()
# plt.savefig('images/17_slope_stability_analysis.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("   ✓ Saved: images/17_slope_stability_analysis.png")

# ============================================
# VISUALIZATION 18: ENTITY VS DISTRICT AVERAGE
# ============================================
print("[18/15] Creating Entity vs District Average comparison...")

selected_mine = 'MN-KA-2023-001'
mine_info = df_entities[df_entities['mine_id'] == selected_mine].iloc[0]
district_info = df_district_stats[df_district_stats['district'] == mine_info['district']].iloc[0]

# Calculate expansion rate for the mine (simulated)
mine_temporal = df_temporal[df_temporal['mine_id'] == selected_mine]
first_area = mine_temporal.iloc[0]['mining_area_ha']
last_area = mine_temporal.iloc[-1]['mining_area_ha']
years = 3
mine_expansion_rate = ((last_area - first_area) / first_area) * 100 / years

comparison_data = pd.DataFrame({
    'Category': ['This Mine', 'District Average'],
    'Expansion Rate': [mine_expansion_rate, district_info['avg_expansion_rate_pct_year']],
    'Mining Area': [mine_info['mining_area_ha'], district_info['avg_mining_area_ha']]
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Expansion rate comparison
bars1 = ax1.bar(comparison_data['Category'], comparison_data['Expansion Rate'],
                color=['#3498db', '#95a5a6'], edgecolor='black', linewidth=2)
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=12)

ax1.set_ylabel('Expansion Rate (% per year)', fontsize=12, fontweight='bold')
ax1.set_title('Expansion Rate Comparison', fontsize=14, fontweight='bold', pad=20)
ax1.grid(True, alpha=0.3, axis='y')

# Mining area comparison
bars2 = ax2.bar(comparison_data['Category'], comparison_data['Mining Area'],
                color=['#e74c3c', '#95a5a6'], edgecolor='black', linewidth=2)
for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height,
            f'{height:.1f} ha', ha='center', va='bottom', fontweight='bold', fontsize=12)

ax2.set_ylabel('Mining Area (ha)', fontsize=12, fontweight='bold')
ax2.set_title('Mining Area Comparison', fontsize=14, fontweight='bold', pad=20)
ax2.grid(True, alpha=0.3, axis='y')

plt.suptitle(f'{mine_info["mine_name"]} vs {mine_info["district"]} District Average', 
             fontsize=16, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('images/18_entity_vs_district_average.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: images/18_entity_vs_district_average.png")

# # ============================================
# # VISUALIZATION 19: LEASE AREA UTILIZATION
# # ============================================
# print("[19/15] Creating Lease Area Utilization chart...")

# df_entities['utilization_pct'] = (df_entities['mining_area_ha'] / df_entities['permitted_area_ha']) * 100
# df_entities['permitted_area_ha'] = [50.0, 150.0, 35.0, 60.0, 95.0]
# df_entities['utilization_pct'] = (df_entities['mining_area_ha'] / df_entities['permitted_area_ha']) * 100

# fig, ax = plt.subplots(figsize=(12, 8))

# mines = df_entities['mine_name']
# y_pos = np.arange(len(mines))

# # Plot permitted area (background)
# ax.barh(y_pos, df_entities['permitted_area_ha'], color='#ecf0f1', 
#         edgecolor='black', linewidth=1.5, label='Permitted Area', alpha=0.7)

# # Plot current mining area
# colors = ['#27ae60' if util <= 100 else '#e74c3c' 
#           for util in df_entities['utilization_pct']]
# ax.barh(y_pos, df_entities['mining_area_ha'], color=colors, 
#         edgecolor='black', linewidth=1.5, label='Current Mining Area')

# # Add percentage labels
# for i, (idx, row) in enumerate(df_entities.iterrows()):
#     ax.text(row['mining_area_ha'] + 2, i, 
#             f"{row['utilization_pct']:.1f}%", 
#             va='center', fontweight='bold', fontsize=10)

# ax.set_yticks(y_pos)
# ax.set_yticklabels(mines)
# ax.set_xlabel('Area (ha)', fontsize=12, fontweight='bold')
# ax.set_title('Lease Area Utilization (Current vs Permitted)', 
#              fontsize=14, fontweight='bold', pad=20)
# ax.legend(loc='lower right', frameon=True, shadow=True)
# ax.grid(True, alpha=0.3, axis='x')
# plt.tight_layout()
# plt.savefig('images/19_lease_area_utilization.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("   ✓ Saved: images/19_lease_area_utilization.png")

# ============================================
# VISUALIZATION 20: COMPREHENSIVE DASHBOARD
# ============================================
print("[20/15] Creating Comprehensive Dashboard Overview...")

selected_mine = 'MN-KA-2023-001'
mine_info = df_entities[df_entities['mine_id'] == selected_mine].iloc[0]
mine_temporal = df_temporal[df_temporal['mine_id'] == selected_mine]
profile_data = profile_dfs[selected_mine]

fig = plt.figure(figsize=(18, 12))
gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)

# Title
fig.suptitle(f'Comprehensive Mining Site Dashboard: {mine_info["mine_name"]}', 
             fontsize=18, fontweight='bold', y=0.98)

# 1. Area over time
ax1 = fig.add_subplot(gs[0, :2])
ax1.plot(mine_temporal['observation_date'], mine_temporal['mining_area_ha'], 
         marker='o', linewidth=2.5, color='#3498db', markersize=4)
ax1.fill_between(mine_temporal['observation_date'], mine_temporal['mining_area_ha'], 
                 alpha=0.3, color='#3498db')
ax1.set_ylabel('Area (ha)', fontweight='bold')
ax1.set_title('Area Expansion Timeline', fontweight='bold', fontsize=12)
ax1.grid(True, alpha=0.3)
ax1.tick_params(axis='x', rotation=45)

# 2. Key metrics
ax2 = fig.add_subplot(gs[0, 2])
ax2.axis('off')
metrics_text = f"""
KEY METRICS

Area: {mine_info['mining_area_ha']:.1f} ha
Depth: {mine_info['max_depth_m']:.1f} m
Volume: {(mine_info['estimated_volume_m3']/1e6):.2f} M m³

Status: {mine_info['status']}
Compliance: {mine_info['inside_permitted_area']}
"""
ax2.text(0.1, 0.5, metrics_text, fontsize=11, fontweight='bold',
         verticalalignment='center', family='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# 3. Elevation profile
ax3 = fig.add_subplot(gs[1, :])
ax3.plot(profile_data['distance_m'], profile_data['baseline_elevation_m'], 
         linewidth=2, color='gray', linestyle='--', label='Baseline', alpha=0.7)
ax3.fill_between(profile_data['distance_m'], profile_data['current_elevation_m'],
                 profile_data['baseline_elevation_m'], alpha=0.4, color='red')
ax3.plot(profile_data['distance_m'], profile_data['current_elevation_m'], 
         linewidth=2.5, color='#e74c3c', label='Current')
ax3.set_xlabel('Distance (m)', fontweight='bold')
ax3.set_ylabel('Elevation (m)', fontweight='bold')
ax3.set_title('Terrain Cross-Section', fontweight='bold', fontsize=12)
ax3.legend()
ax3.grid(True, alpha=0.3)

# 4. Land cover change
ax4 = fig.add_subplot(gs[2, 0])
ax4.plot(mine_temporal['observation_date'], mine_temporal['vegetation_loss_pct'], 
         linewidth=2, color='#e74c3c', label='Veg Loss')
ax4.plot(mine_temporal['observation_date'], mine_temporal['bare_soil_increase_pct'], 
         linewidth=2, color='#f39c12', label='Bare Soil')
ax4.set_ylabel('Percentage (%)', fontweight='bold')
ax4.set_title('Land Cover Change', fontweight='bold', fontsize=11)
ax4.legend(fontsize=8)
ax4.grid(True, alpha=0.3)
ax4.tick_params(axis='x', rotation=45)

# 5. Compliance distances
ax5 = fig.add_subplot(gs[2, 1])
distances = [mine_info['distance_water_body_km'], 
             mine_info['distance_forest_km'], 
             mine_info['distance_habitation_km']]
labels = ['Water', 'Forest', 'Habitation']
colors_dist = ['#e74c3c' if d < 1 else '#f39c12' if d < 2 else '#27ae60' for d in distances]
bars = ax5.barh(labels, distances, color=colors_dist, edgecolor='black', linewidth=1.5)
for i, (bar, dist) in enumerate(zip(bars, distances)):
    ax5.text(dist, i, f' {dist:.1f} km', va='center', fontweight='bold', fontsize=9)
ax5.set_xlabel('Distance (km)', fontweight='bold')
ax5.set_title('Proximity to Sensitive Zones', fontweight='bold', fontsize=11)
ax5.grid(True, alpha=0.3, axis='x')

# 6. Volume growth
ax6 = fig.add_subplot(gs[2, 2])
ax6.plot(mine_temporal['observation_date'], mine_temporal['estimated_volume_m3']/1e6, 
         linewidth=2.5, color='#9b59b6', marker='s', markersize=3)
ax6.fill_between(mine_temporal['observation_date'], mine_temporal['estimated_volume_m3']/1e6, 
                 alpha=0.3, color='#9b59b6')
ax6.set_ylabel('Volume (M m³)', fontweight='bold')
ax6.set_title('Volume Growth', fontweight='bold', fontsize=11)
ax6.grid(True, alpha=0.3)
ax6.tick_params(axis='x', rotation=45)

plt.savefig('images/20_comprehensive_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()
print("   ✓ Saved: images/20_comprehensive_dashboard.png")

# ============================================
# SUMMARY
# ============================================
print("\n" + "=" * 80)
print("ALL VISUALIZATIONS GENERATED SUCCESSFULLY!")
print("=" * 80)
print(f"\nTotal images created: 20")
print(f"Location: ./images/ directory")
print("\nVisualization Categories:")
print("  • Temporal Monitoring (5 charts)")
print("  • Spatial Analysis (4 charts)")
print("  • Compliance Monitoring (4 charts)")
print("  • Elevation Profiles (4 charts)")
print("  • Comparative Analysis (3 charts)")
print("\n" + "=" * 80)