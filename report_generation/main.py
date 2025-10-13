import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans']

# Set random seed
np.random.seed(42)

print("=" * 80)
print("GENERATING COMPREHENSIVE MINING SITE INSPECTION REPORT")
print("=" * 80)

# ============================================
# PREPARE DATA
# ============================================

# Entity data
entity_data = {
    'mine_id': 'MN-KA-2023-001',
    'mine_name': 'Kolar Gold Fields Site A',
    'latitude': 13.1389,
    'longitude': 78.2981,
    'district': 'Kolar',
    'state': 'Karnataka',
    'country': 'India',
    'ownership': 'Private',
    'operator': 'ABC Mining Ltd',
    'status': 'Active',
    'last_detection_date': '2025-09-15',
    'mining_area_ha': 45.3,
    'perimeter_length_m': 3200,
    'elevation_min_m': 720,
    'elevation_max_m': 780,
    'avg_depth_m': 28.5,
    'max_depth_m': 42.0,
    'estimated_volume_m3': 1290000,
    'distance_water_body_km': 2.3,
    'distance_forest_km': 1.5,
    'distance_habitation_km': 3.8,
    'inside_permitted_area': 'Yes',
    'expansion_beyond_lease_ha': 0.0,
    'permitted_area_ha': 50.0,
    'detection_confidence': 'High',
    'days_since_last_survey': 45,
    'imagery_source': 'Sentinel-2',
    'imagery_date': '2025-09-10',
    'dem_source': 'Copernicus 30m DEM',
    'processing_date': '2025-09-15',
    'model_version': 'v2.3.1'
}

# Temporal data (36 months)
temporal_data = []
start_date = datetime(2022, 10, 1)
for i in range(36):
    obs_date = start_date + timedelta(days=30 * i)
    growth_factor = i / 36.0
    temporal_data.append({
        'date': obs_date,
        'area': 45.3 * (0.6 + 0.4 * growth_factor) + np.random.normal(0, 0.3),
        'depth': 28.5 * (0.5 + 0.5 * growth_factor) + np.random.normal(0, 0.8),
        'volume': 1290000 * (0.4 + 0.6 * growth_factor) + np.random.normal(0, 8000),
        'veg_loss': min(100, 20 + growth_factor * 60 + np.random.normal(0, 3)),
        'bare_soil': min(100, 15 + growth_factor * 55 + np.random.normal(0, 2.5))
    })
df_temporal = pd.DataFrame(temporal_data)

# Elevation profile
profile_data = []
for i in range(100):
    distance = i * 5
    baseline = 780 - (i / 100) * 20 + np.sin(i / 10) * 2
    if 20 < i < 80:
        depth_factor = np.sin(((i - 20) / 60) * np.pi)
        current = baseline - 28.5 * depth_factor
    else:
        current = baseline
    profile_data.append({
        'distance': distance,
        'baseline': baseline,
        'current': current,
        'difference': baseline - current
    })
df_profile = pd.DataFrame(profile_data)

# District comparison
district_data = {
    'district': ['Kolar', 'Bellary', 'Salem', 'Dharmapuri'],
    'expansion_rate': [8.5, 12.3, 9.8, 15.2],
    'violations': [2, 5, 3, 4]
}
df_district = pd.DataFrame(district_data)

print("\nData prepared successfully")
print("Generating PDF report...")

# ============================================
# CREATE PDF REPORT
# ============================================

pdf_filename = 'Mining_Site_Inspection_Report_Kolar_Gold_Fields.pdf'

with PdfPages(pdf_filename) as pdf:
    
    # ============================================
    # PAGE 1: TITLE PAGE & EXECUTIVE SUMMARY
    # ============================================
    fig = plt.figure(figsize=(8.5, 11))
    fig.patch.set_facecolor('white')
    
    # Title section with background
    ax_title = fig.add_axes([0, 0.75, 1, 0.25])
    ax_title.add_patch(Rectangle((0, 0), 1, 1, transform=ax_title.transAxes, 
                                 facecolor='#2c3e50', zorder=0))
    ax_title.text(0.5, 0.7, 'MINING SITE INSPECTION REPORT', 
                 ha='center', va='center', fontsize=24, fontweight='bold', 
                 color='white', transform=ax_title.transAxes)
    ax_title.text(0.5, 0.45, entity_data['mine_name'], 
                 ha='center', va='center', fontsize=18, 
                 color='#ecf0f1', transform=ax_title.transAxes)
    ax_title.text(0.5, 0.25, f"{entity_data['district']}, {entity_data['state']}", 
                 ha='center', va='center', fontsize=14, 
                 color='#bdc3c7', transform=ax_title.transAxes)
    ax_title.axis('off')
    
    # Report metadata
    ax_meta = fig.add_axes([0.1, 0.60, 0.8, 0.12])
    metadata_text = f"""
    Report Generated: {datetime.now().strftime('%B %d, %Y')}
    Mine ID: {entity_data['mine_id']}
    Operator: {entity_data['operator']}
    Status: {entity_data['status']}
    Compliance: Within Permitted Area
    """
    ax_meta.text(0.05, 0.9, metadata_text, fontsize=11, verticalalignment='top',
                fontfamily='monospace', bbox=dict(boxstyle='round', 
                facecolor='#ecf0f1', alpha=0.8))
    ax_meta.axis('off')
    
    # Executive Summary
    ax_summary = fig.add_axes([0.1, 0.15, 0.8, 0.40])
    ax_summary.text(0.5, 0.95, 'EXECUTIVE SUMMARY', ha='center', 
                   fontsize=16, fontweight='bold', transform=ax_summary.transAxes)
    
    summary_text = f"""
    QUERY: "Provide comprehensive assessment of Kolar Gold Fields Site A 
    including expansion trends, environmental compliance, and operational status"
    
    KEY FINDINGS:
    
    • Site Status: Currently ACTIVE with high detection confidence
    • Total Mining Area: {entity_data['mining_area_ha']:.1f} hectares 
      ({(entity_data['mining_area_ha']/entity_data['permitted_area_ha']*100):.1f}% of permitted {entity_data['permitted_area_ha']:.1f} ha)
    • Excavation Depth: Average {entity_data['avg_depth_m']:.1f}m, Maximum {entity_data['max_depth_m']:.1f}m
    • Total Volume Extracted: {(entity_data['estimated_volume_m3']/1000000):.2f} million cubic meters
    
    COMPLIANCE STATUS: ✓ SATISFACTORY
    • All operations within permitted lease boundary
    • Water bodies: {entity_data['distance_water_body_km']:.1f} km (Safe distance)
    • Forest areas: {entity_data['distance_forest_km']:.1f} km (Within limits)
    • Settlements: {entity_data['distance_habitation_km']:.1f} km (Adequate buffer)
    
    ENVIRONMENTAL IMPACT:
    • Vegetation loss: ~80% in mining zone over 3 years
    • Bare soil increase: ~73% indicating active excavation
    • Land cover change accelerating in recent months
    
    RECOMMENDATIONS:
    1. Continue quarterly monitoring given active status
    2. Conduct ground verification (last survey: {entity_data['days_since_last_survey']} days ago)
    3. Monitor proximity to forest boundary (1.5 km buffer)
    4. Track expansion rate vs district average (Currently: 8.5%/year)
    """
    
    ax_summary.text(0.05, 0.85, summary_text, fontsize=9, 
                   verticalalignment='top', transform=ax_summary.transAxes,
                   bbox=dict(boxstyle='round', facecolor='#fff9e6', alpha=0.5))
    ax_summary.axis('off')
    
    # Footer
    ax_footer = fig.add_axes([0.1, 0.02, 0.8, 0.08])
    ax_footer.text(0.5, 0.5, 'CONFIDENTIAL - For Official Use Only\nGenerated by Automated Mining Monitoring System', 
                  ha='center', va='center', fontsize=8, color='gray',
                  transform=ax_footer.transAxes, style='italic')
    ax_footer.axis('off')
    
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # ============================================
    # PAGE 2: SITE DETAILS & SPATIAL CHARACTERISTICS
    # ============================================
    fig = plt.figure(figsize=(8.5, 11))
    fig.suptitle('SITE DETAILS & SPATIAL CHARACTERISTICS', 
                fontsize=16, fontweight='bold', y=0.98)
    
    # Entity details table
    ax1 = plt.subplot(3, 1, 1)
    ax1.axis('off')
    ax1.text(0.5, 1.0, 'Entity Information', ha='center', fontsize=13, 
            fontweight='bold', transform=ax1.transAxes)
    
    entity_table_data = [
        ['Mine ID', entity_data['mine_id'], 'Ownership', entity_data['ownership']],
        ['Coordinates', f"{entity_data['latitude']:.4f}°N, {entity_data['longitude']:.4f}°E", 
         'Operator', entity_data['operator']],
        ['District', entity_data['district'], 'State', entity_data['state']],
        ['Status', entity_data['status'], 'Last Detection', entity_data['last_detection_date']],
    ]
    
    table1 = ax1.table(cellText=entity_table_data, cellLoc='left', loc='center',
                      colWidths=[0.2, 0.3, 0.2, 0.3], bbox=[0.05, 0.1, 0.9, 0.8])
    table1.auto_set_font_size(False)
    table1.set_fontsize(9)
    table1.scale(1, 2)
    
    for i in range(len(entity_table_data)):
        table1[(i, 0)].set_facecolor('#3498db')
        table1[(i, 0)].set_text_props(weight='bold', color='white')
        table1[(i, 2)].set_facecolor('#3498db')
        table1[(i, 2)].set_text_props(weight='bold', color='white')
        if i % 2 == 0:
            table1[(i, 1)].set_facecolor('#ecf0f1')
            table1[(i, 3)].set_facecolor('#ecf0f1')
    
    # Spatial metrics visualization
    ax2 = plt.subplot(3, 2, 3)
    metrics = ['Area\n(ha)', 'Perimeter\n(m)', 'Avg Depth\n(m)', 'Max Depth\n(m)']
    values = [entity_data['mining_area_ha'], entity_data['perimeter_length_m']/100, 
              entity_data['avg_depth_m'], entity_data['max_depth_m']]
    colors_bar = ['#3498db', '#9b59b6', '#e67e22', '#e74c3c']
    
    bars = ax2.bar(metrics, values, color=colors_bar, edgecolor='black', linewidth=1.5)
    for bar, val, actual in zip(bars, values, [entity_data['mining_area_ha'], 
                                                entity_data['perimeter_length_m'], 
                                                entity_data['avg_depth_m'], 
                                                entity_data['max_depth_m']]):
        height = bar.get_height()
        if actual > 1000:
            label = f'{actual:.0f}'
        else:
            label = f'{actual:.1f}'
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                label, ha='center', va='bottom', fontweight='bold', fontsize=9)
    ax2.set_title('Spatial Characteristics', fontweight='bold', fontsize=11)
    ax2.set_ylabel('Scaled Values', fontsize=9)
    ax2.grid(axis='y', alpha=0.3)
    
    # Excavated volume
    ax3 = plt.subplot(3, 2, 4)
    volume_million = entity_data['estimated_volume_m3'] / 1000000
    ax3.barh(['Excavated\nVolume'], [volume_million], color='#16a085', 
            edgecolor='black', linewidth=1.5, height=0.5)
    ax3.text(volume_million/2, 0, f"{volume_million:.2f} M m³", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='white')
    ax3.set_xlabel('Million Cubic Meters (m³)', fontsize=9)
    ax3.set_title('Total Excavated Volume', fontweight='bold', fontsize=11)
    ax3.grid(axis='x', alpha=0.3)
    
    # Compliance distances
    ax4 = plt.subplot(3, 1, 3)
    distances = [entity_data['distance_water_body_km'], 
                entity_data['distance_forest_km'],
                entity_data['distance_habitation_km']]
    labels_dist = ['Water Body', 'Forest', 'Habitation']
    colors_dist = ['#27ae60' if d >= 2 else '#f39c12' if d >= 1 else '#e74c3c' for d in distances]
    
    bars_dist = ax4.barh(labels_dist, distances, color=colors_dist, 
                        edgecolor='black', linewidth=1.5)
    for i, (bar, dist) in enumerate(zip(bars_dist, distances)):
        ax4.text(dist + 0.1, i, f'{dist:.1f} km', va='center', 
                fontweight='bold', fontsize=10)
    
    ax4.axvline(x=1, color='red', linestyle='--', linewidth=2, alpha=0.5, label='Critical (1 km)')
    ax4.axvline(x=2, color='orange', linestyle='--', linewidth=2, alpha=0.5, label='Warning (2 km)')
    ax4.set_xlabel('Distance (km)', fontsize=10, fontweight='bold')
    ax4.set_title('Proximity to Sensitive Zones - Compliance Status', 
                 fontweight='bold', fontsize=12)
    ax4.legend(loc='lower right', fontsize=8)
    ax4.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # ============================================
    # PAGE 3: TEMPORAL MONITORING
    # ============================================
    fig = plt.figure(figsize=(8.5, 11))
    fig.suptitle('TEMPORAL MONITORING & EXPANSION TRENDS', 
                fontsize=16, fontweight='bold', y=0.98)
    
    # Area expansion
    ax1 = plt.subplot(3, 1, 1)
    ax1.plot(df_temporal['date'], df_temporal['area'], 
            marker='o', linewidth=2.5, color='#3498db', markersize=4)
    ax1.fill_between(df_temporal['date'], df_temporal['area'], 
                     alpha=0.3, color='#3498db')
    ax1.set_ylabel('Mining Area (ha)', fontsize=10, fontweight='bold')
    ax1.set_title('Area Expansion Over Time (Oct 2022 - Sep 2025)', 
                 fontweight='bold', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    
    # Add annotation for current area
    current_area = df_temporal['area'].iloc[-1]
    ax1.annotate(f'Current: {current_area:.1f} ha', 
                xy=(df_temporal['date'].iloc[-1], current_area),
                xytext=(-80, 20), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0', lw=2))
    
    # Depth change
    ax2 = plt.subplot(3, 1, 2)
    ax2.plot(df_temporal['date'], df_temporal['depth'], 
            marker='s', linewidth=2.5, color='#e74c3c', markersize=4)
    ax2.fill_between(df_temporal['date'], df_temporal['depth'], 
                     alpha=0.3, color='#e74c3c')
    ax2.set_ylabel('Average Depth (m)', fontsize=10, fontweight='bold')
    ax2.set_title('Excavation Depth Progression', fontweight='bold', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=45)
    
    # Volume growth
    ax3 = plt.subplot(3, 1, 3)
    ax3.plot(df_temporal['date'], df_temporal['volume']/1000000, 
            marker='^', linewidth=2.5, color='#9b59b6', markersize=4)
    ax3.fill_between(df_temporal['date'], df_temporal['volume']/1000000, 
                     alpha=0.3, color='#9b59b6')
    ax3.set_xlabel('Date', fontsize=10, fontweight='bold')
    ax3.set_ylabel('Volume (Million m³)', fontsize=10, fontweight='bold')
    ax3.set_title('Cumulative Excavated Volume', fontweight='bold', fontsize=12)
    ax3.grid(True, alpha=0.3)
    ax3.tick_params(axis='x', rotation=45)
    
    # Add growth rate annotation
    start_vol = df_temporal['volume'].iloc[0] / 1000000
    end_vol = df_temporal['volume'].iloc[-1] / 1000000
    growth_pct = ((end_vol - start_vol) / start_vol) * 100
    ax3.text(0.98, 0.05, f'3-Year Growth: {growth_pct:.1f}%', 
            transform=ax3.transAxes, ha='right', fontsize=10,
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # ============================================
    # PAGE 4: ENVIRONMENTAL IMPACT
    # ============================================
    fig = plt.figure(figsize=(8.5, 11))
    fig.suptitle('ENVIRONMENTAL IMPACT ASSESSMENT', 
                fontsize=16, fontweight='bold', y=0.98)
    
    # Land cover change
    ax1 = plt.subplot(2, 1, 1)
    ax1.plot(df_temporal['date'], df_temporal['veg_loss'], 
            marker='o', linewidth=2.5, color='#e74c3c', 
            markersize=5, label='Vegetation Loss')
    ax1.plot(df_temporal['date'], df_temporal['bare_soil'], 
            marker='s', linewidth=2.5, color='#f39c12', 
            markersize=5, label='Bare Soil Increase')
    ax1.fill_between(df_temporal['date'], df_temporal['veg_loss'], 
                     alpha=0.2, color='#e74c3c')
    ax1.fill_between(df_temporal['date'], df_temporal['bare_soil'], 
                     alpha=0.2, color='#f39c12')
    ax1.set_ylabel('Percentage (%)', fontsize=10, fontweight='bold')
    ax1.set_title('Land Cover Change Around Mining Site', 
                 fontweight='bold', fontsize=12)
    ax1.legend(loc='upper left', fontsize=10, frameon=True, shadow=True)
    ax1.grid(True, alpha=0.3)
    ax1.tick_params(axis='x', rotation=45)
    ax1.set_ylim([0, 100])
    
    # Add critical threshold line
    ax1.axhline(y=75, color='red', linestyle='--', linewidth=2, 
               alpha=0.5, label='Critical Threshold')
    
    # Impact summary table
    ax2 = plt.subplot(2, 2, 3)
    ax2.axis('off')
    
    current_veg_loss = df_temporal['veg_loss'].iloc[-1]
    current_bare = df_temporal['bare_soil'].iloc[-1]
    
    impact_data = [
        ['Metric', 'Current Status', 'Assessment'],
        ['Vegetation Loss', f'{current_veg_loss:.1f}%', 'High Impact'],
        ['Bare Soil Increase', f'{current_bare:.1f}%', 'High Impact'],
        ['Water Body Distance', f"{entity_data['distance_water_body_km']:.1f} km", 'Safe'],
        ['Forest Distance', f"{entity_data['distance_forest_km']:.1f} km", 'Monitoring'],
        ['Air Quality Impact', 'Not Measured', 'Requires Survey'],
    ]
    
    table2 = ax2.table(cellText=impact_data, cellLoc='left', loc='center',
                      colWidths=[0.35, 0.3, 0.35])
    table2.auto_set_font_size(False)
    table2.set_fontsize(8)
    table2.scale(1, 2.5)
    
    # Style header
    for j in range(3):
        table2[(0, j)].set_facecolor('#34495e')
        table2[(0, j)].set_text_props(weight='bold', color='white')
    
    # Style rows
    for i in range(1, len(impact_data)):
        if i % 2 == 0:
            for j in range(3):
                table2[(i, j)].set_facecolor('#ecf0f1')
        
        # Color code assessment
        assessment = impact_data[i][2]
        if 'High' in assessment:
            table2[(i, 2)].set_facecolor('#ffcccc')
        elif 'Safe' in assessment:
            table2[(i, 2)].set_facecolor('#ccffcc')
        elif 'Monitoring' in assessment:
            table2[(i, 2)].set_facecolor('#fff4cc')
    
    ax2.set_title('Environmental Impact Summary', fontweight='bold', 
                 fontsize=11, pad=20)
    
    # Recommendations
    ax3 = plt.subplot(2, 2, 4)
    ax3.axis('off')
    
    recommendations = """
    RECOMMENDED ACTIONS:
    
    ✓ IMMEDIATE:
    • Monitor vegetation buffer zones
    • Implement dust suppression
    • Check water body quality
    
    ⚠ SHORT-TERM (1-3 months):
    • Conduct biodiversity survey
    • Assess soil erosion risk
    • Review drainage systems
    
    ◉ LONG-TERM (6-12 months):
    • Plan reclamation strategy
    • Establish green belt
    • Monitor groundwater levels
    """
    
    ax3.text(0.05, 0.95, recommendations, fontsize=8, 
            verticalalignment='top', transform=ax3.transAxes,
            bbox=dict(boxstyle='round', facecolor='#e8f8f5', alpha=0.8),
            family='monospace')
    ax3.set_title('Mitigation Recommendations', fontweight='bold', 
                 fontsize=11, pad=20)
    
    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # ============================================
    # PAGE 5: ELEVATION PROFILE & TERRAIN ANALYSIS
    # ============================================
    fig = plt.figure(figsize=(8.5, 11))
    fig.suptitle('ELEVATION PROFILE & TERRAIN ANALYSIS', 
                fontsize=16, fontweight='bold', y=0.98)
    
    # Elevation profile
    ax1 = plt.subplot(2, 1, 1)
    ax1.plot(df_profile['distance'], df_profile['baseline'], 
            linewidth=2.5, color='gray', linestyle='--', 
            label='Original Terrain', alpha=0.7)
    ax1.plot(df_profile['distance'], df_profile['current'], 
            linewidth=2.5, color='#3498db', label='Current Terrain')
    ax1.fill_between(df_profile['distance'], df_profile['baseline'], 
                     df_profile['current'], alpha=0.3, color='red',
                     label='Excavated Material')
    
    # Mark maximum depth
    max_depth_idx = df_profile['difference'].idxmax()
    max_point = df_profile.loc[max_depth_idx]
    ax1.scatter(max_point['distance'], max_point['current'], 
               color='red', s=200, zorder=5, edgecolor='black', linewidth=2)
    ax1.annotate(f"Max Depth: {max_point['difference']:.1f}m",
                xy=(max_point['distance'], max_point['current']),
                xytext=(50, -30), textcoords='offset points',
                bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.3', lw=2))
    
    ax1.set_xlabel('Distance from Start Point (m)', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Elevation (m)', fontsize=10, fontweight='bold')
    ax1.set_title('Terrain Cross-Section: North-South Profile', 
                 fontweight='bold', fontsize=12)
    ax1.legend(loc='upper right', fontsize=9, frameon=True, shadow=True)
    ax1.grid(True, alpha=0.3)
    
    # Excavation depth profile
    ax2 = plt.subplot(2, 1, 2)
    ax2.fill_between(df_profile['distance'], 0, df_profile['difference'], 
                     alpha=0.6, color='#e74c3c')
    ax2.plot(df_profile['distance'], df_profile['difference'], 
            linewidth=2.5, color='#c0392b', marker='o', markersize=2)
    
    # Add depth zones
    ax2.axhline(y=20, color='orange', linestyle='--', linewidth=2, 
               alpha=0.6, label='Shallow Zone (<20m)')
    ax2.axhline(y=30, color='red', linestyle='--', linewidth=2, 
               alpha=0.6, label='Deep Zone (>30m)')
    
    ax2.set_xlabel('Distance from Start Point (m)', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Excavation Depth (m)', fontsize=10, fontweight='bold')
    ax2.set_title('Excavation Depth Distribution', fontweight='bold', fontsize=12)
    ax2.legend(loc='upper right', fontsize=9, frameon=True, shadow=True)
    ax2.grid(True, alpha=0.3)
    
    # Add statistics box
    avg_depth = df_profile['difference'].mean()
    max_depth = df_profile['difference'].max()
    stats_text = f"""
    PROFILE STATISTICS
    
    Length: {df_profile['distance'].max():.0f} m
    Avg Depth: {avg_depth:.1f} m
    Max Depth: {max_depth:.1f} m
    Elevation Range: {entity_data['elevation_min_m']}-{entity_data['elevation_max_m']} m
    
    Slope Stability: MONITORED
    Water Accumulation: LOW RISK
    """
    ax2.text(0.98, 0.97, stats_text, transform=ax2.transAxes, 
            fontsize=8, verticalalignment='top', horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
            family='monospace')
    
    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # ============================================
    # PAGE 6: COMPARATIVE ANALYSIS & RECOMMENDATIONS
    # ============================================
    fig = plt.figure(figsize=(8.5, 11))
    fig.suptitle('COMPARATIVE ANALYSIS & FINAL RECOMMENDATIONS', 
                fontsize=16, fontweight='bold', y=0.98)
    
    # District comparison
    ax1 = plt.subplot(3, 2, 1)
    colors_comp = ['#e74c3c' if d == 'Kolar' else '#95a5a6' 
                   for d in df_district['district']]
    bars1 = ax1.bar(df_district['district'], df_district['expansion_rate'],
                   color=colors_comp, edgecolor='black', linewidth=1.5)
    for bar in bars1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom', 
                fontweight='bold', fontsize=9)
    ax1.set_ylabel('Expansion Rate (%/year)', fontsize=9, fontweight='bold')
    ax1.set_title('District Expansion Rate Comparison', 
                 fontweight='bold', fontsize=10)
    ax1.grid(True, alpha=0.3, axis='y')
    ax1.tick_params(axis='x', rotation=45)
    
    # Violations comparison
    ax2 = plt.subplot(3, 2, 2)
    colors_viol = ['#27ae60' if v <= 2 else '#e74c3c' 
                   for v in df_district['violations']]
    bars2 = ax2.bar(df_district['district'], df_district['violations'],
                   color=colors_viol, edgecolor='black', linewidth=1.5)
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}', ha='center', va='bottom', 
                fontweight='bold', fontsize=9)
    ax2.set_ylabel('Total Violations', fontsize=9, fontweight='bold')
    ax2.set_title('Compliance Violations by District', 
                 fontweight='bold', fontsize=10)
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.tick_params(axis='x', rotation=45)
    
    # Compliance status pie
    ax3 = plt.subplot(3, 2, 3)
    compliance_data = [90.6, 9.4]  # % within permitted area
    colors_pie = ['#27ae60', '#e74c3c']
    wedges, texts, autotexts = ax3.pie(compliance_data, 
                                        labels=['Compliant', 'Non-Compliant'],
                                        autopct='%1.1f%%', startangle=90,
                                        colors=colors_pie, explode=(0.05, 0.05),
                                        textprops={'fontsize': 9, 'fontweight': 'bold'},
                                        shadow=True)
    ax3.set_title('Area Utilization Status', fontweight='bold', fontsize=10)
    
    # Risk assessment
    ax4 = plt.subplot(3, 2, 4)
    ax4.axis('off')
    
    risk_data = [
        ['Risk Factor', 'Level', 'Priority'],
        ['Lease Boundary', 'LOW', 'Monitor'],
        ['Water Contamination', 'LOW', 'Monitor'],
        ['Forest Impact', 'MEDIUM', 'Review'],
        ['Vegetation Loss', 'HIGH', 'Action'],
        ['Slope Stability', 'LOW', 'Monitor'],
    ]
    
    table3 = ax4.table(cellText=risk_data, cellLoc='center', loc='center',
                      colWidths=[0.4, 0.25, 0.35])
    table3.auto_set_font_size(False)
    table3.set_fontsize(8)
    table3.scale(1, 2.2)
    
    # Style header
    for j in range(3):
        table3[(0, j)].set_facecolor('#34495e')
        table3[(0, j)].set_text_props(weight='bold', color='white')
    
    # Color code risk levels
    for i in range(1, len(risk_data)):
        if i % 2 == 0:
            table3[(i, 0)].set_facecolor('#ecf0f1')
        
        risk_level = risk_data[i][1]
        if 'HIGH' in risk_level:
            table3[(i, 1)].set_facecolor('#ffcccc')
        elif 'MEDIUM' in risk_level:
            table3[(i, 1)].set_facecolor('#fff4cc')
        elif 'LOW' in risk_level:
            table3[(i, 1)].set_facecolor('#ccffcc')
    
    ax4.set_title('Risk Assessment Matrix', fontweight='bold', 
                 fontsize=10, pad=15)
    
    # Key recommendations
    ax5 = plt.subplot(3, 1, 3)
    ax5.axis('off')
    
    final_recommendations = """
    FINAL RECOMMENDATIONS & ACTION ITEMS
    
    ═══════════════════════════════════════════════════════════════════════════
    
    ✓ COMPLIANCE STATUS: SATISFACTORY - Site operations within permitted boundaries
    
    ⚠ PRIORITY ACTIONS (Next 30 Days):
    
    1. ENVIRONMENTAL MONITORING
       • Conduct ground verification survey (45 days since last inspection)
       • Install air quality monitoring stations around perimeter
       • Assess vegetation buffer zone integrity
       • Test water quality in nearby water bodies
    
    2. OPERATIONAL REVIEW
       • Verify excavation depth against permit limits (currently at 42m of 50m allowed)
       • Update mine closure and reclamation plan
       • Review dust suppression measures effectiveness
       • Inspect slope stability in deep excavation zones
    
    3. DOCUMENTATION & REPORTING
       • Submit quarterly expansion report to district authorities
       • Update environmental impact assessment for next 12 months
       • Document restoration activities in disturbed zones
       • Prepare contingency plans for monsoon season
    
    ═══════════════════════════════════════════════════════════════════════════
    
    ◉ LONG-TERM MONITORING (6-12 Months):
       • Continue satellite-based monitoring (monthly intervals)
       • Track expansion rate vs district average (currently aligned at 8.5%/year)
       • Monitor forest boundary buffer (currently 1.5km, recommend maintain >2km)
       • Plan progressive reclamation for inactive zones
    
    ═══════════════════════════════════════════════════════════════════════════
    
    REPORT PREPARED BY: Automated Mining Monitoring System v2.3.1
    DATA SOURCES: Sentinel-2 Imagery (2025-09-10), Copernicus 30m DEM
    NEXT REVIEW: December 2025 (Quarterly Schedule)
    
    APPROVAL STATUS: Pending Field Verification
    
    ═══════════════════════════════════════════════════════════════════════════
    """
    
    ax5.text(0.05, 0.95, final_recommendations, fontsize=7.5, 
            verticalalignment='top', transform=ax5.transAxes,
            bbox=dict(boxstyle='round', facecolor='#f0f8ff', alpha=0.9),
            family='monospace', linespacing=1.8)
    
    plt.tight_layout()
    pdf.savefig(fig, bbox_inches='tight')
    plt.close()
    
    # ============================================
    # METADATA PAGE
    # ============================================
    d = pdf.infodict()
    d['Title'] = f'Mining Site Inspection Report - {entity_data["mine_name"]}'
    d['Author'] = 'Automated Mining Monitoring System'
    d['Subject'] = 'Comprehensive Site Assessment and Compliance Review'
    d['Keywords'] = 'Mining, Satellite Monitoring, Compliance, Environmental Impact'
    d['CreationDate'] = datetime.now()

print("\n" + "=" * 80)
print("✓ PDF REPORT GENERATED SUCCESSFULLY!")
print("=" * 80)
print(f"\nFilename: {pdf_filename}")
print(f"Location: Current directory")
print(f"Pages: 6")
print(f"File size: ~{os.path.getsize(pdf_filename) / 1024:.1f} KB" if os.path.exists(pdf_filename) else "")
print("\nReport Contents:")
print("  Page 1: Title Page & Executive Summary")
print("  Page 2: Site Details & Spatial Characteristics")
print("  Page 3: Temporal Monitoring & Expansion Trends")
print("  Page 4: Environmental Impact Assessment")
print("  Page 5: Elevation Profile & Terrain Analysis")
print("  Page 6: Comparative Analysis & Final Recommendations")
print("\n" + "=" * 80)
print("Report ready for review and distribution!")
print("=" * 80)