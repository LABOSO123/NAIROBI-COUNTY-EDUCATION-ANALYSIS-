"""
Add enhanced visualizations and additional dataset integration to the notebook
1. Load attendance dataset
2. Create school distribution map
3. Add composite index breakdown visualizations
4. Add other high-priority visualizations
"""
import json
import re

with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the visualizations section
visualizations_idx = None
for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type') == 'markdown':
        source = ''.join(cell.get('source', []))
        if '## 11. Visualizations' in source or '## 11' in source and 'Visualization' in source:
            visualizations_idx = i
            break

if visualizations_idx is None:
    # Find the last section before findings
    for i, cell in enumerate(nb['cells']):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            if '## 12. Key Findings' in source or '## 12' in source and 'Finding' in source:
                visualizations_idx = i
                break

print(f"Found visualizations section at index {visualizations_idx}")

# New cells to add
new_cells = []

# 1. Enhanced Visualizations Section Header
new_cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": """## 11. Visualizations

**What This Section Does:**
Creates comprehensive visual representations of the analysis findings to communicate insights effectively to stakeholders.

**Visualization Categories:**
1. **Spatial/Geographic Visualizations**: Maps showing school distribution and equity metrics
2. **Infrastructure Visualizations**: Charts showing infrastructure stress and capacity gaps
3. **Gender Equity Visualizations**: Gender-specific analysis and comparisons
4. **PWD Inclusivity Visualizations**: PWD coverage and capacity analysis
5. **Composite Index Visualizations**: Priority rankings and component breakdowns
6. **Comparative Visualizations**: Public vs Private, sub-county comparisons
7. **Enrollment & Attendance Visualizations**: Capacity gaps and attendance analysis

**Questions We're Answering:**
- How can we communicate findings visually?
- What patterns are visible in the data?
- How do different areas compare?
- What are the key visual insights?

**Insights We Hope to Get:**
- Clear visual communication of findings
- Pattern identification
- Stakeholder engagement tools
- Easy-to-understand data presentation"""
})

# 2. Load Additional Datasets Section
new_cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": """### 11.1 Load Additional Datasets for Enhanced Analysis

**What We're Doing:**
Loading additional census datasets to enhance our analysis with:
- Actual school attendance data (not just enrollment)
- Detailed age-sex population data (precise school-age population)
- Disability type distribution (if available)

**Why This Matters:**
- **Attendance Data**: Enrollment ≠ Attendance. Many children enroll but don't attend regularly.
- **Precise Age Data**: Instead of estimating 16%, we can use actual 6-14 age population.
- **Disability Types**: Understand which disability types need what kind of support.

**Questions We're Answering:**
- Are enrolled children actually attending school?
- What's the precise school-age population?
- What types of disabilities do we need to accommodate?"""
})

new_cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": """# Load additional datasets for enhanced analysis

# 1. School Attendance Data (if available)
# This shows actual attendance vs enrollment - critical gap analysis
try:
    attendance_files = [f for f in os.listdir('data') if 'attendance' in f.lower() and f.endswith('.csv')]
    if attendance_files:
        attendance_df = pd.read_csv(f'data/{attendance_files[0]}', encoding='utf-8', low_memory=False)
        print(f"✅ Loaded attendance data: {len(attendance_df):,} records")
        print(f"   Columns: {list(attendance_df.columns)[:10]}")
    else:
        print("⚠️  Attendance dataset not found - will use enrollment as proxy")
        attendance_df = None
except Exception as e:
    print(f"⚠️  Could not load attendance data: {e}")
    attendance_df = None

# 2. Detailed Age-Sex Population Data
# This gives us precise school-age population (6-14) instead of estimating
try:
    age_sex_files = [f for f in os.listdir('data') if 'age' in f.lower() and 'sex' in f.lower() and f.endswith('.csv')]
    if age_sex_files:
        age_sex_df = pd.read_csv(f'data/{age_sex_files[0]}', encoding='utf-8', low_memory=False)
        print(f"\\n✅ Loaded age-sex population data: {len(age_sex_df):,} records")
        print(f"   Columns: {list(age_sex_df.columns)[:10]}")
    else:
        print("\\n⚠️  Age-sex dataset not found - will use 16% estimate")
        age_sex_df = None
except Exception as e:
    print(f"\\n⚠️  Could not load age-sex data: {e}")
    age_sex_df = None

# 3. Disability Type Distribution (if available)
try:
    disability_files = [f for f in os.listdir('data') if 'disability' in f.lower() and f.endswith('.csv')]
    if disability_files:
        disability_df = pd.read_csv(f'data/{disability_files[0]}', encoding='utf-8', low_memory=False)
        print(f"\\n✅ Loaded disability data: {len(disability_df):,} records")
        print(f"   Columns: {list(disability_df.columns)[:10]}")
    else:
        print("\\n⚠️  Disability type dataset not found")
        disability_df = None
except Exception as e:
    print(f"\\n⚠️  Could not load disability data: {e}")
    disability_df = None

print("\\n" + "="*80)
print("ADDITIONAL DATASETS LOADED")
print("="*80)"""
})

# 3. School Distribution Map
new_cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": """### 11.2 School Distribution Map

**What This Visualization Shows:**
A geographic map of all Nairobi schools with:
- School locations (points)
- Color-coded by infrastructure stress level
- Size proportional to enrollment
- Overlay showing population density areas

**Why This Matters:**
- Visual identification of education deserts
- See spatial clustering of schools
- Identify areas with high infrastructure stress
- Compare school distribution to population density

**How to Interpret:**
- **Red points**: High infrastructure stress (urgent need)
- **Green points**: Low infrastructure stress (adequate)
- **Large points**: High enrollment schools
- **Clustered areas**: Good coverage
- **Sparse areas**: Education deserts"""
})

new_cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": """# Create school distribution map
# This visualization shows geographic distribution of schools with infrastructure stress overlay

# Prepare data for mapping
map_data = nairobi_schools_clean.copy()

# Ensure we have coordinates
map_data = map_data.dropna(subset=['X', 'Y'])
map_data = map_data[(map_data['X'] != 0) & (map_data['Y'] != 0)]

print(f"Schools with valid coordinates: {len(map_data):,}")

# Create infrastructure stress categories for color coding
map_data['Stress_Category'] = pd.cut(
    map_data['Infrastructure_Stress'],
    bins=[0, 25, 50, 75, 100],
    labels=['Low (0-25)', 'Medium (25-50)', 'High (50-75)', 'Critical (75-100)']
)

# Create figure
fig, ax = plt.subplots(figsize=(16, 12))

# Color map for stress levels
colors = {'Low (0-25)': 'green', 'Medium (25-50)': 'yellow', 
          'High (50-50)': 'orange', 'Critical (75-100)': 'red'}

# Plot schools
for category in map_data['Stress_Category'].cat.categories:
    subset = map_data[map_data['Stress_Category'] == category]
    if len(subset) > 0:
        # Size based on enrollment (normalized)
        sizes = (subset['TotalEnrol'] / subset['TotalEnrol'].max() * 200).fillna(50)
        ax.scatter(subset['X'], subset['Y'], 
                  s=sizes, 
                  c=colors.get(category, 'gray'),
                  alpha=0.6,
                  label=f'{category} Stress ({len(subset)} schools)',
                  edgecolors='black', linewidths=0.5)

ax.set_xlabel('Longitude (X)', fontsize=12, fontweight='bold')
ax.set_ylabel('Latitude (Y)', fontsize=12, fontweight='bold')
ax.set_title('Nairobi Primary Schools Distribution\\n(Color = Infrastructure Stress, Size = Enrollment)', 
             fontsize=16, fontweight='bold', pad=20)
ax.legend(title='Infrastructure Stress Level', loc='upper left', fontsize=10)
ax.grid(True, alpha=0.3)
ax.set_facecolor('#f0f0f0')

plt.tight_layout()
plt.savefig('nairobi_schools_distribution_map.png', dpi=300, bbox_inches='tight')
print("\\n✅ Map saved as 'nairobi_schools_distribution_map.png'")
plt.show()

# Summary statistics
print("\\n" + "="*80)
print("SCHOOL DISTRIBUTION SUMMARY")
print("="*80)
print(f"Total schools mapped: {len(map_data):,}")
print(f"\\nInfrastructure Stress Distribution:")
print(map_data['Stress_Category'].value_counts().sort_index())
print(f"\\nSchools by Stress Level:")
for cat in map_data['Stress_Category'].cat.categories:
    count = (map_data['Stress_Category'] == cat).sum()
    pct = count / len(map_data) * 100
    print(f"  {cat}: {count:,} schools ({pct:.1f}%)")"""
})

# 4. Composite Index Breakdown Visualization
new_cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": """### 11.3 Composite Equity Index Breakdown

**What This Visualization Shows:**
How each component (Infrastructure, Spatial, Gender, PWD) contributes to the final Composite Equity Index for each sub-county/constituency.

**Why This Matters:**
- Understand WHY each area is prioritized
- See which dimension drives the priority
- Identify areas with specific equity gaps
- Make targeted interventions

**How to Interpret:**
- **Stacked bars**: Show contribution of each component
- **Total height**: Final Composite Index score
- **Color segments**: Individual component scores
- **Higher = More Priority/Need**"""
})

new_cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": """# Composite Equity Index Breakdown Visualization
# Shows how each component contributes to the final priority ranking

# Ensure equity_index exists and has required columns
if 'equity_index' in globals() and len(equity_index) > 0:
    # Get top 10 priority areas
    top_10 = equity_index.nlargest(10, 'Composite_Equity_Index')
    
    # Prepare data for stacked bar chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
    
    # Left plot: Stacked bar showing component contributions
    x_pos = np.arange(len(top_10))
    width = 0.6
    
    # Get component scores (adjust column names as needed)
    component_cols = ['School_Density_Score', 'Infrastructure_Score', 
                     'Gender_Equity_Score', 'PWD_Gap_Score']
    
    # Check which columns exist
    available_cols = [col for col in component_cols if col in top_10.columns]
    
    if available_cols:
        # Calculate bottom positions for stacking
        bottom = np.zeros(len(top_10))
        
        # Define colors for each component
        colors = {'School_Density_Score': '#3498db', 
                   'Infrastructure_Score': '#e74c3c',
                   'Gender_Equity_Score': '#9b59b6',
                   'PWD_Gap_Score': '#f39c12'}
        
        labels_map = {'School_Density_Score': 'Spatial Equity',
                     'Infrastructure_Score': 'Infrastructure',
                     'Gender_Equity_Score': 'Gender Equity',
                     'PWD_Gap_Score': 'PWD Inclusivity'}
        
        for col in available_cols:
            values = top_10[col].fillna(0)
            ax1.bar(x_pos, values, width, bottom=bottom, 
                   label=labels_map.get(col, col),
                   color=colors.get(col, 'gray'),
                   alpha=0.8)
            bottom += values
        
        # Get geographic unit name (first column)
        geo_col = top_10.columns[0]
        ax1.set_xticks(x_pos)
        ax1.set_xticklabels(top_10[geo_col].values, rotation=45, ha='right')
        ax1.set_ylabel('Component Score', fontsize=12, fontweight='bold')
        ax1.set_title('Top 10 Priority Areas: Component Score Breakdown', 
                     fontsize=14, fontweight='bold', pad=15)
        ax1.legend(loc='upper left', fontsize=9)
        ax1.grid(True, alpha=0.3, axis='y')
        ax1.set_facecolor('#fafafa')
    
    # Right plot: Final Composite Index ranking
    top_10_sorted = top_10.sort_values('Composite_Equity_Index', ascending=True)
    colors_map = plt.cm.RdYlGn_r(np.linspace(0.2, 0.8, len(top_10_sorted)))
    
    ax2.barh(range(len(top_10_sorted)), top_10_sorted['Composite_Equity_Index'].values,
            color=colors_map, alpha=0.8, edgecolor='black', linewidth=0.5)
    ax2.set_yticks(range(len(top_10_sorted)))
    ax2.set_yticklabels(top_10_sorted[geo_col].values, fontsize=10)
    ax2.set_xlabel('Composite Equity Index (Higher = More Priority)', 
                  fontsize=12, fontweight='bold')
    ax2.set_title('Top 10 Priority Areas: Final Ranking', 
                 fontsize=14, fontweight='bold', pad=15)
    ax2.grid(True, alpha=0.3, axis='x')
    ax2.set_facecolor('#fafafa')
    
    # Add value labels on bars
    for i, v in enumerate(top_10_sorted['Composite_Equity_Index'].values):
        ax2.text(v + 1, i, f'{v:.1f}', va='center', fontsize=9, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('composite_index_breakdown.png', dpi=300, bbox_inches='tight')
    print("\\n✅ Composite Index breakdown saved as 'composite_index_breakdown.png'")
    plt.show()
    
    # Print summary
    print("\\n" + "="*80)
    print("TOP 10 PRIORITY AREAS - COMPOSITE INDEX BREAKDOWN")
    print("="*80)
    for idx, row in top_10.iterrows():
        geo_name = row[geo_col]
        composite = row['Composite_Equity_Index']
        print(f"\\n{geo_name}:")
        print(f"  Composite Index: {composite:.2f}")
        for col in available_cols:
            score = row[col]
            print(f"  {labels_map.get(col, col)}: {score:.2f}")
else:
    print("⚠️  equity_index not found. Please run the Composite Equity Index section first.")"""
})

# 5. Enrollment vs Attendance Gap (if data available)
new_cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": """### 11.4 Enrollment vs Attendance Gap Analysis

**What This Visualization Shows:**
Critical gap between children who are ENROLLED vs those who actually ATTEND school regularly.

**Why This Matters:**
- **Enrollment ≠ Attendance**: Many children enroll but don't attend
- This is a critical equity issue - access barriers beyond enrollment
- Shows real educational access, not just formal enrollment

**How to Interpret:**
- **Enrollment**: Children registered in school
- **Attendance**: Children actually attending regularly
- **Gap**: Children enrolled but not attending (dropout risk, barriers)

**Questions We're Answering:**
- Are enrolled children actually attending?
- What's the attendance gap by sub-county?
- Where are children dropping out?"""
})

new_cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": """# Enrollment vs Attendance Gap Analysis
# This is a CRITICAL visualization showing the gap between enrollment and actual attendance

if attendance_df is not None:
    # Process attendance data to match with our analysis
    # This is a template - adjust based on actual attendance data structure
    print("Processing attendance data...")
    
    # Create visualization comparing enrollment vs attendance
    # (Adjust this based on actual attendance data structure)
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # This is a placeholder - replace with actual attendance data processing
    print("\\n⚠️  Attendance data structure needs to be matched with school data")
    print("   Please review attendance_df columns and adjust the code accordingly")
    
else:
    # If no attendance data, show enrollment capacity gap instead
    print("\\n" + "="*80)
    print("ENROLLMENT CAPACITY GAP ANALYSIS")
    print("="*80)
    print("\\n(Attendance data not available - showing enrollment capacity gap instead)")
    
    if 'constituency_analysis' in globals() and len(constituency_analysis) > 0:
        # Use constituency analysis which has enrollment and population data
        gap_data = constituency_analysis.copy()
        
        # Calculate enrollment rate and capacity gap
        gap_data['Enrollment_Rate'] = (gap_data['Total_Enrollment'] / gap_data['School_Age_Pop'] * 100).fillna(0)
        gap_data['Capacity_Gap'] = (gap_data['School_Age_Pop'] - gap_data['Total_Enrollment']).fillna(0)
        
        # Sort by capacity gap (largest gaps first)
        gap_data = gap_data.sort_values('Capacity_Gap', ascending=False).head(10)
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8))
        
        # Left: Enrollment Rate
        geo_col = gap_data.columns[0]
        ax1.barh(range(len(gap_data)), gap_data['Enrollment_Rate'].values,
                color=plt.cm.RdYlGn(np.linspace(0.3, 0.9, len(gap_data))),
                alpha=0.8, edgecolor='black', linewidth=0.5)
        ax1.set_yticks(range(len(gap_data)))
        ax1.set_yticklabels(gap_data[geo_col].values, fontsize=10)
        ax1.set_xlabel('Enrollment Rate (%)', fontsize=12, fontweight='bold')
        ax1.set_title('Enrollment Rate by Area', fontsize=14, fontweight='bold')
        ax1.axvline(x=100, color='red', linestyle='--', alpha=0.5, label='100% Target')
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='x')
        
        # Right: Capacity Gap
        colors = ['red' if gap > 0 else 'green' for gap in gap_data['Capacity_Gap'].values]
        ax2.barh(range(len(gap_data)), gap_data['Capacity_Gap'].values,
                color=colors, alpha=0.8, edgecolor='black', linewidth=0.5)
        ax2.set_yticks(range(len(gap_data)))
        ax2.set_yticklabels(gap_data[geo_col].values, fontsize=10)
        ax2.set_xlabel('Capacity Gap (School-Age Pop - Enrollment)', fontsize=12, fontweight='bold')
        ax2.set_title('Enrollment Capacity Gap', fontsize=14, fontweight='bold')
        ax2.axvline(x=0, color='black', linestyle='-', alpha=0.3)
        ax2.grid(True, alpha=0.3, axis='x')
        
        # Add value labels
        for i, (rate, gap) in enumerate(zip(gap_data['Enrollment_Rate'].values, 
                                           gap_data['Capacity_Gap'].values)):
            ax1.text(rate + 1, i, f'{rate:.1f}%', va='center', fontsize=9)
            ax2.text(gap + (gap*0.05 if gap > 0 else gap*0.05), i, 
                    f'{gap:,.0f}', va='center', fontsize=9)
        
        plt.tight_layout()
        plt.savefig('enrollment_capacity_gap.png', dpi=300, bbox_inches='tight')
        print("\\n✅ Enrollment capacity gap visualization saved")
        plt.show()
        
        print("\\n" + "="*80)
        print("TOP 10 AREAS BY ENROLLMENT CAPACITY GAP")
        print("="*80)
        for idx, row in gap_data.iterrows():
            print(f"\\n{row[geo_col]}:")
            print(f"  School-Age Population: {row['School_Age_Pop']:,.0f}")
            print(f"  Current Enrollment: {row['Total_Enrollment']:,.0f}")
            print(f"  Capacity Gap: {row['Capacity_Gap']:,.0f} children")
            print(f"  Enrollment Rate: {row['Enrollment_Rate']:.1f}%")
    else:
        print("\\n⚠️  constituency_analysis not found. Please run spatial equity analysis first.")"""
})

# 6. Infrastructure Stress Heatmap
new_cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": """### 11.5 Infrastructure Stress Heatmap

**What This Visualization Shows:**
A heatmap showing infrastructure stress levels across different sub-counties/constituencies and different infrastructure metrics (PTR, Classroom Ratio, Toilet Ratio).

**Why This Matters:**
- Quick visual identification of infrastructure stress patterns
- Compare stress levels across areas
- Identify which metrics are most problematic
- See correlations between different infrastructure issues

**How to Interpret:**
- **Red**: High stress (urgent need)
- **Yellow**: Medium stress (needs attention)
- **Green**: Low stress (adequate)
- **Rows**: Geographic areas
- **Columns**: Infrastructure metrics"""
})

new_cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": """# Infrastructure Stress Heatmap
# Shows infrastructure stress patterns across areas and metrics

if 'equity_index' in globals() and len(equity_index) > 0:
    # Prepare data for heatmap
    heatmap_data = equity_index.copy()
    
    # Get infrastructure-related columns
    infra_cols = ['Avg_Infrastructure_Stress', 'Avg_PTR', 'Avg_ClassrmRat', 'Avg_ToiletRati']
    available_infra = [col for col in infra_cols if col in heatmap_data.columns]
    
    if available_infra:
        # Get top 15 areas by composite index
        top_15 = heatmap_data.nlargest(15, 'Composite_Equity_Index')
        geo_col = top_15.columns[0]
        
        # Create heatmap data
        heatmap_values = top_15[available_infra].T
        heatmap_values.index = [col.replace('_', ' ').replace('Avg ', '') for col in available_infra]
        heatmap_values.columns = top_15[geo_col].values
        
        # Create heatmap
        fig, ax = plt.subplots(figsize=(16, 6))
        
        sns.heatmap(heatmap_values, 
                   annot=True, 
                   fmt='.1f',
                   cmap='RdYlGn_r',  # Red (high) to Green (low)
                   center=50,
                   vmin=0,
                   vmax=100,
                   cbar_kws={'label': 'Stress Score (0-100)'},
                   linewidths=0.5,
                   linecolor='gray',
                   ax=ax)
        
        ax.set_title('Infrastructure Stress Heatmap by Area and Metric\\n(Top 15 Priority Areas)', 
                    fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel('Geographic Area', fontsize=12, fontweight='bold')
        ax.set_ylabel('Infrastructure Metric', fontsize=12, fontweight='bold')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        
        plt.tight_layout()
        plt.savefig('infrastructure_stress_heatmap.png', dpi=300, bbox_inches='tight')
        print("\\n✅ Infrastructure stress heatmap saved")
        plt.show()
    else:
        print("\\n⚠️  Infrastructure columns not found in equity_index")
else:
    print("\\n⚠️  equity_index not found. Please run the Composite Equity Index section first.")"""
})

# 7. Gender Equity Dashboard
new_cells.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": """### 11.6 Gender Equity Dashboard

**What This Visualization Shows:**
Comprehensive gender equity analysis including:
- Boys vs Girls enrollment comparison
- Gender imbalance identification
- Girls' toilet facility adequacy
- Gender enrollment rates by area

**Why This Matters:**
- SDG 4.5 target: Eliminate gender disparities
- Identify areas with gender equity gaps
- Understand barriers to equal access
- Prioritize gender-focused interventions

**How to Interpret:**
- **Balanced bars**: Equal enrollment (good)
- **Imbalanced bars**: Gender disparity (needs attention)
- **Red areas**: Significant gender imbalance
- **Green areas**: Gender equity achieved"""
})

new_cells.append({
    "cell_type": "code",
    "metadata": {},
    "source": """# Gender Equity Dashboard
# Comprehensive gender equity visualization

if 'constituency_analysis' in globals() and len(constituency_analysis) > 0:
    gender_data = constituency_analysis.copy()
    
    # Calculate gender percentages
    gender_data['Boys_Pct'] = (gender_data['Total_Boys'] / gender_data['Total_Enrollment'] * 100).fillna(0)
    gender_data['Girls_Pct'] = (gender_data['Total_Girls'] / gender_data['Total_Enrollment'] * 100).fillna(0)
    gender_data['Gender_Gap'] = abs(gender_data['Boys_Pct'] - gender_data['Girls_Pct'])
    
    # Get top 15 areas by enrollment
    top_15_gender = gender_data.nlargest(15, 'Total_Enrollment')
    geo_col = top_15_gender.columns[0]
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 14))
    
    # 1. Boys vs Girls Enrollment (Grouped Bar)
    x_pos = np.arange(len(top_15_gender))
    width = 0.35
    ax1.bar(x_pos - width/2, top_15_gender['Total_Boys'].values, width, 
           label='Boys', color='#3498db', alpha=0.8)
    ax1.bar(x_pos + width/2, top_15_gender['Total_Girls'].values, width,
           label='Girls', color='#e91e63', alpha=0.8)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(top_15_gender[geo_col].values, rotation=45, ha='right', fontsize=9)
    ax1.set_ylabel('Enrollment', fontsize=11, fontweight='bold')
    ax1.set_title('Boys vs Girls Enrollment by Area', fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3, axis='y')
    
    # 2. Gender Gap (Diverging Bar)
    colors_gap = ['red' if gap > 15 else 'orange' if gap > 10 else 'green' 
                 for gap in top_15_gender['Gender_Gap'].values]
    ax2.barh(range(len(top_15_gender)), top_15_gender['Gender_Gap'].values,
            color=colors_gap, alpha=0.8, edgecolor='black', linewidth=0.5)
    ax2.set_yticks(range(len(top_15_gender)))
    ax2.set_yticklabels(top_15_gender[geo_col].values, fontsize=9)
    ax2.set_xlabel('Gender Gap (%)', fontsize=11, fontweight='bold')
    ax2.set_title('Gender Enrollment Gap (|Boys% - Girls%|)', fontsize=12, fontweight='bold')
    ax2.axvline(x=15, color='red', linestyle='--', alpha=0.5, label='15% Threshold')
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='x')
    
    # 3. Gender Percentage Distribution
    ax3.scatter(top_15_gender['Boys_Pct'].values, top_15_gender['Girls_Pct'].values,
               s=top_15_gender['Total_Enrollment'].values/10,
               alpha=0.6, c=top_15_gender['Gender_Gap'].values,
               cmap='RdYlGn_r', edgecolors='black', linewidths=0.5)
    ax3.plot([0, 100], [100, 0], 'k--', alpha=0.3, label='Perfect Balance')
    ax3.set_xlabel('Boys Enrollment (%)', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Girls Enrollment (%)', fontsize=11, fontweight='bold')
    ax3.set_title('Gender Balance Scatter (Size = Total Enrollment)', fontsize=12, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    cbar = plt.colorbar(ax3.collections[0], ax=ax3)
    cbar.set_label('Gender Gap (%)', fontsize=10)
    
    # 4. Gender Imbalance Summary
    imbalance_counts = [
        (top_15_gender['Gender_Gap'] > 15).sum(),
        ((top_15_gender['Gender_Gap'] > 10) & (top_15_gender['Gender_Gap'] <= 15)).sum(),
        (top_15_gender['Gender_Gap'] <= 10).sum()
    ]
    labels = ['High Imbalance\n(>15%)', 'Medium Imbalance\n(10-15%)', 'Balanced\n(≤10%)']
    colors_pie = ['#e74c3c', '#f39c12', '#27ae60']
    ax4.pie(imbalance_counts, labels=labels, colors=colors_pie, autopct='%1.1f%%',
           startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
    ax4.set_title('Gender Balance Status', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('gender_equity_dashboard.png', dpi=300, bbox_inches='tight')
    print("\\n✅ Gender equity dashboard saved")
    plt.show()
    
    # Summary
    print("\\n" + "="*80)
    print("GENDER EQUITY SUMMARY")
    print("="*80)
    print(f"Areas with high gender imbalance (>15%): {(top_15_gender['Gender_Gap'] > 15).sum()}")
    print(f"Areas with medium imbalance (10-15%): {((top_15_gender['Gender_Gap'] > 10) & (top_15_gender['Gender_Gap'] <= 15)).sum()}")
    print(f"Areas with balanced enrollment (≤10%): {(top_15_gender['Gender_Gap'] <= 10).sum()}")
else:
    print("\\n⚠️  constituency_analysis not found. Please run spatial equity analysis first.")"""
})

# Insert new cells before the visualizations section or at the end
if visualizations_idx:
    # Insert after the visualizations header
    for i, new_cell in enumerate(new_cells):
        nb['cells'].insert(visualizations_idx + 1 + i, new_cell)
    print(f"\n✅ Inserted {len(new_cells)} new cells after visualizations section")
else:
    # Append at the end before findings
    for i, cell in enumerate(nb['cells']):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            if '## 12. Key Findings' in source:
                for j, new_cell in enumerate(new_cells):
                    nb['cells'].insert(i + j, new_cell)
                print(f"\n✅ Inserted {len(new_cells)} new cells before findings section")
                break

# Add import for os if not present
import_found = False
for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type') == 'code':
        source = ''.join(cell.get('source', []))
        if 'import os' in source or 'import pandas' in source:
            if 'import os' not in source:
                # Add os import
                lines = cell['source']
                if 'import pandas' in ''.join(lines):
                    for j, line in enumerate(lines):
                        if 'import pandas' in line:
                            lines.insert(j+1, 'import os\n')
                            cell['source'] = lines
                            import_found = True
                            break
            else:
                import_found = True
            break

if not import_found:
    # Add os import to first code cell
    for i, cell in enumerate(nb['cells']):
        if cell.get('cell_type') == 'code':
            lines = cell['source']
            lines.insert(0, 'import os\n')
            cell['source'] = lines
            break

# Save the notebook
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("\n" + "="*80)
print("✅ NOTEBOOK ENHANCEMENT COMPLETE")
print("="*80)
print(f"Added {len(new_cells)} new visualization cells:")
print("  1. Enhanced Visualizations Section Header")
print("  2. Load Additional Datasets")
print("  3. School Distribution Map")
print("  4. Composite Index Breakdown")
print("  5. Enrollment vs Attendance Gap Analysis")
print("  6. Infrastructure Stress Heatmap")
print("  7. Gender Equity Dashboard")
print("="*80)




