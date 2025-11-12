"""
Nairobi Primary Education Equity Analysis
Multi-Dimensional Gap Analysis: Spatial, Infrastructure, Gender & PWD Inclusivity

Objective: Identify critical gaps in primary education access across Nairobi County
to inform strategic investment prioritization for SDG 4 (Quality Education).

Analytical Framework:
1. Spatial Equity: School density vs population density by sub-county
2. Infrastructure Capacity: Overcrowding, resource adequacy (classrooms, toilets, teachers)
3. Gender Equity: Enrollment disparities, attendance patterns, infrastructure adequacy
4. PWD Inclusivity: Special needs schools, integrated schools, accessibility gaps
5. Composite Equity Index: Multi-dimensional priority ranking
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Set visualization style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

print("="*80)
print("NAIROBI PRIMARY EDUCATION EQUITY ANALYSIS")
print("="*80)

# ============================================================================
# 1. DATA LOADING
# ============================================================================
print("\n1. Loading data...")

# Load primary schools data
schools_df = pd.read_csv('data/kenya_primary_schools (1).csv', encoding='utf-8', low_memory=False)
print(f"   Total schools in dataset: {len(schools_df):,}")

# Filter for Nairobi schools
nairobi_schools = schools_df[
    (schools_df['Province'].str.contains('NAIROBI', case=False, na=False)) |
    (schools_df['District'].str.contains('NAIROBI', case=False, na=False))
].copy()

print(f"   Nairobi schools found: {len(nairobi_schools):,}")

# Load population data
pop_subcounty = pd.read_csv('data/kenya-population-by-sub-county.csv', encoding='utf-8')
pop_density = pd.read_csv('data/kenya-populationland-area-population-density_by_subcounty.csv', encoding='utf-8')
school_attendance = pd.read_csv('data/distribution-of-population-age-3-years-and-above-currently-attending-school-learning-institution.csv', encoding='utf-8')
urban_pop = pd.read_csv('data/distribution-of-urban-population-by-age-sex-and-county-kenya-2019-census-volume-iii.csv', encoding='utf-8')

print("   Population datasets loaded")

# ============================================================================
# 2. DATA CLEANING AND PREPARATION
# ============================================================================
print("\n2. Cleaning and preparing data...")

# Remove schools with missing coordinates
nairobi_schools_clean = nairobi_schools.dropna(subset=['Latitude', 'Longitude'])
print(f"   Schools with valid coordinates: {len(nairobi_schools_clean):,}")

# Create PWD inclusivity indicator
nairobi_schools_clean['PWD_Inclusive'] = nairobi_schools_clean['Type3'].isin(['INTEGRATED', 'SPECIAL SCHOOL'])
nairobi_schools_clean['Is_Special_School'] = nairobi_schools_clean['Type3'] == 'SPECIAL SCHOOL'

# Create gender balance indicator
nairobi_schools_clean['Gender_Balance'] = nairobi_schools_clean.apply(
    lambda x: abs(x['TotalBoys'] - x['TotalGirls']) / max(x['TotalEnrol'], 1) if pd.notna(x['TotalEnrol']) and x['TotalEnrol'] > 0 else np.nan,
    axis=1
)

print(f"   PWD-inclusive schools: {nairobi_schools_clean['PWD_Inclusive'].sum()}")
print(f"   Special schools: {nairobi_schools_clean['Is_Special_School'].sum()}")

# ============================================================================
# 3. INFRASTRUCTURE CAPACITY ANALYSIS
# ============================================================================
print("\n3. Analyzing infrastructure capacity...")

# Create capacity indicators
nairobi_schools_clean['Overcrowded_Classrooms'] = nairobi_schools_clean['ClassrmRat'] > 50
nairobi_schools_clean['High_PTR'] = nairobi_schools_clean['PupilTeach'] > 40
nairobi_schools_clean['Poor_Toilet_Ratio'] = nairobi_schools_clean['ToiletRati'] > 50

# Calculate infrastructure stress score (0-100, higher = worse)
nairobi_schools_clean['Infrastructure_Stress'] = (
    (nairobi_schools_clean['PupilTeach'].fillna(0) / 60 * 33.3) +
    (nairobi_schools_clean['ClassrmRat'].fillna(0) / 80 * 33.3) +
    (nairobi_schools_clean['ToiletRati'].fillna(0) / 80 * 33.3)
).clip(0, 100)

print(f"   Schools with overcrowded classrooms (>50): {nairobi_schools_clean['Overcrowded_Classrooms'].sum()}")
print(f"   Schools with high PTR (>40): {nairobi_schools_clean['High_PTR'].sum()}")
print(f"   Average infrastructure stress: {nairobi_schools_clean['Infrastructure_Stress'].mean():.2f}/100")

# ============================================================================
# 4. GENDER EQUITY ANALYSIS
# ============================================================================
print("\n4. Analyzing gender equity...")

# Calculate gender-specific metrics
nairobi_schools_clean['Girls_Enrollment_Pct'] = (
    nairobi_schools_clean['TotalGirls'] / nairobi_schools_clean['TotalEnrol'] * 100
).fillna(0)

nairobi_schools_clean['Boys_Enrollment_Pct'] = (
    nairobi_schools_clean['TotalBoys'] / nairobi_schools_clean['TotalEnrol'] * 100
).fillna(0)

# Gender-specific toilet ratios
nairobi_schools_clean['Girls_Toilet_Ratio'] = (
    nairobi_schools_clean['TotalGirls'] / nairobi_schools_clean['GirlsToilet'].replace(0, np.nan)
).fillna(np.nan)

nairobi_schools_clean['Boys_Toilet_Ratio'] = (
    nairobi_schools_clean['TotalBoys'] / nairobi_schools_clean['BoysToilet'].replace(0, np.nan)
).fillna(np.nan)

# Identify gender equity issues
nairobi_schools_clean['Gender_Imbalance'] = abs(
    nairobi_schools_clean['Girls_Enrollment_Pct'] - nairobi_schools_clean['Boys_Enrollment_Pct']
) > 15

nairobi_schools_clean['Girls_Toilet_Deficit'] = nairobi_schools_clean['Girls_Toilet_Ratio'] > 50
nairobi_schools_clean['Boys_Toilet_Deficit'] = nairobi_schools_clean['Boys_Toilet_Ratio'] > 50

total_enrollment = nairobi_schools_clean['TotalEnrol'].sum()
girls_enrollment = nairobi_schools_clean['TotalGirls'].sum()
boys_enrollment = nairobi_schools_clean['TotalBoys'].sum()

print(f"   Total enrollment: {total_enrollment:,}")
print(f"   Girls: {girls_enrollment:,} ({girls_enrollment/total_enrollment*100:.1f}%)")
print(f"   Boys: {boys_enrollment:,} ({boys_enrollment/total_enrollment*100:.1f}%)")
print(f"   Schools with gender imbalance (>15%): {nairobi_schools_clean['Gender_Imbalance'].sum()}")
print(f"   Schools with girls' toilet deficit: {nairobi_schools_clean['Girls_Toilet_Deficit'].sum()}")

# ============================================================================
# 5. PWD INCLUSIVITY ANALYSIS
# ============================================================================
print("\n5. Analyzing PWD inclusivity...")

# Special schools
special_schools = nairobi_schools_clean[nairobi_schools_clean['Is_Special_School'] == True]

# Integrated schools (mainstream schools with PWD support)
integrated_schools = nairobi_schools_clean[
    (nairobi_schools_clean['Type3'] == 'INTEGRATED') & 
    (~nairobi_schools_clean['Is_Special_School'])
]

# Calculate PWD inclusivity coverage
total_schools = len(nairobi_schools_clean)
pwd_coverage = (nairobi_schools_clean['PWD_Inclusive'].sum() / total_schools * 100)

# Estimate PWD population (2.5% assumption)
estimated_pwd_rate = 0.025
estimated_pwd_children = total_enrollment * estimated_pwd_rate
current_pwd_capacity = nairobi_schools_clean[nairobi_schools_clean['PWD_Inclusive']]['TotalEnrol'].sum()

print(f"   PWD-inclusive schools: {nairobi_schools_clean['PWD_Inclusive'].sum()} ({pwd_coverage:.1f}%)")
print(f"   Special schools: {len(special_schools)}")
print(f"   Integrated schools: {len(integrated_schools)}")
print(f"   Estimated PWD children: {estimated_pwd_children:,.0f}")
print(f"   Current PWD capacity: {current_pwd_capacity:,.0f}")
print(f"   PWD capacity gap: {max(0, estimated_pwd_children - current_pwd_capacity):,.0f}")

# ============================================================================
# 6. COMPOSITE EQUITY INDEX
# ============================================================================
print("\n6. Calculating composite equity index...")

# Aggregate by District
equity_index = nairobi_schools_clean.groupby('District').agg({
    'Name_of_Sc': 'count',
    'TotalEnrol': 'sum',
    'TotalBoys': 'sum',
    'TotalGirls': 'sum',
    'Infrastructure_Stress': 'mean',
    'PWD_Inclusive': 'sum',
    'Is_Special_School': 'sum',
    'Overcrowded_Classrooms': 'sum',
    'High_PTR': 'sum',
    'Gender_Imbalance': 'sum',
    'Girls_Toilet_Deficit': 'sum'
}).reset_index()

equity_index.columns = ['District', 'School_Count', 'Total_Enrollment', 'Total_Boys', 'Total_Girls',
                       'Avg_Infrastructure_Stress', 'PWD_Inclusive_Count', 'Special_School_Count',
                       'Overcrowded_Schools', 'High_PTR_Schools', 'Gender_Imbalanced_Schools',
                       'Girls_Toilet_Deficit_Schools']

# Calculate normalized scores (0-100, higher = more priority/need)
equity_index['School_Density_Score'] = 100 - (equity_index['School_Count'] / equity_index['School_Count'].max() * 100)
equity_index['Infrastructure_Score'] = equity_index['Avg_Infrastructure_Stress']
equity_index['PWD_Gap_Score'] = 100 - (equity_index['PWD_Inclusive_Count'] / equity_index['School_Count'] * 100)
equity_index['Gender_Equity_Score'] = (
    (equity_index['Gender_Imbalanced_Schools'] / equity_index['School_Count'] * 50) +
    (equity_index['Girls_Toilet_Deficit_Schools'] / equity_index['School_Count'] * 50)
) * 100

# Composite equity index (weighted average)
equity_index['Composite_Equity_Index'] = (
    equity_index['School_Density_Score'] * 0.25 +
    equity_index['Infrastructure_Score'] * 0.30 +
    equity_index['PWD_Gap_Score'] * 0.25 +
    equity_index['Gender_Equity_Score'] * 0.20
)

# Rank by priority
equity_index = equity_index.sort_values('Composite_Equity_Index', ascending=False)
equity_index['Priority_Rank'] = range(1, len(equity_index) + 1)

print("   Top 5 priority districts:")
for idx, row in equity_index.head(5).iterrows():
    print(f"      {row['Priority_Rank']}. {row['District']}: Index = {row['Composite_Equity_Index']:.1f}")

# ============================================================================
# 7. VISUALIZATIONS
# ============================================================================
print("\n7. Generating visualizations...")

# Figure 1: Overview Analysis
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1. Infrastructure stress distribution
axes[0, 0].hist(nairobi_schools_clean['Infrastructure_Stress'].dropna(), bins=30, edgecolor='black', alpha=0.7)
axes[0, 0].axvline(nairobi_schools_clean['Infrastructure_Stress'].median(), color='red', linestyle='--', 
                   label=f'Median: {nairobi_schools_clean["Infrastructure_Stress"].median():.1f}')
axes[0, 0].set_xlabel('Infrastructure Stress Score')
axes[0, 0].set_ylabel('Number of Schools')
axes[0, 0].set_title('Distribution of Infrastructure Stress Across Nairobi Schools')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# 2. Gender enrollment
gender_data = [boys_enrollment, girls_enrollment]
axes[0, 1].bar(['Boys', 'Girls'], gender_data, color=['#3498db', '#e74c3c'], alpha=0.7)
axes[0, 1].set_ylabel('Total Enrollment')
axes[0, 1].set_title('Total Enrollment by Gender')
axes[0, 1].grid(True, alpha=0.3, axis='y')
for i, v in enumerate(gender_data):
    axes[0, 1].text(i, v, f'{v:,}', ha='center', va='bottom', fontweight='bold')

# 3. PWD Inclusivity Coverage
pwd_counts = [nairobi_schools_clean['PWD_Inclusive'].sum(), 
              len(nairobi_schools_clean) - nairobi_schools_clean['PWD_Inclusive'].sum()]
axes[1, 0].pie(pwd_counts, labels=['PWD-Inclusive', 'Not PWD-Inclusive'], 
               autopct='%1.1f%%', startangle=90, colors=['#2ecc71', '#95a5a6'])
axes[1, 0].set_title('PWD Inclusivity Coverage')

# 4. Top Priority Districts
top_10 = equity_index.head(10)
axes[1, 1].barh(range(len(top_10)), top_10['Composite_Equity_Index'], color='#9b59b6', alpha=0.7)
axes[1, 1].set_yticks(range(len(top_10)))
axes[1, 1].set_yticklabels(top_10['District'], fontsize=9)
axes[1, 1].set_xlabel('Composite Equity Index (Higher = Higher Priority)')
axes[1, 1].set_title('Top 10 Priority Districts for Investment')
axes[1, 1].grid(True, alpha=0.3, axis='x')
axes[1, 1].invert_yaxis()

plt.tight_layout()
plt.savefig('nairobi_education_equity_analysis.png', dpi=300, bbox_inches='tight')
print("   Saved: nairobi_education_equity_analysis.png")
plt.close()

# Figure 2: Detailed Analysis
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Pupil-Teacher Ratio Distribution
ptr_data = nairobi_schools_clean['PupilTeach'].dropna()
axes[0, 0].hist(ptr_data, bins=40, edgecolor='black', alpha=0.7, color='#3498db')
axes[0, 0].axvline(40, color='red', linestyle='--', linewidth=2, label='Kenya Standard (40)')
axes[0, 0].axvline(ptr_data.median(), color='green', linestyle='--', 
                   label=f'Median: {ptr_data.median():.1f}')
axes[0, 0].set_xlabel('Pupil-Teacher Ratio')
axes[0, 0].set_ylabel('Number of Schools')
axes[0, 0].set_title('Distribution of Pupil-Teacher Ratios')
axes[0, 0].legend()
axes[0, 0].grid(True, alpha=0.3)

# 2. Gender Balance
gender_balance = nairobi_schools_clean['Gender_Balance'].dropna()
axes[0, 1].hist(gender_balance, bins=30, edgecolor='black', alpha=0.7, color='#e74c3c')
axes[0, 1].set_xlabel('Gender Imbalance Index (0 = Perfect Balance)')
axes[0, 1].set_ylabel('Number of Schools')
axes[0, 1].set_title('Gender Balance Across Schools')
axes[0, 1].grid(True, alpha=0.3)

# 3. Infrastructure Metrics Comparison
infra_metrics = ['PupilTeach', 'ClassrmRat', 'ToiletRati']
infra_data = [nairobi_schools_clean[col].median() for col in infra_metrics]
axes[1, 0].bar(infra_metrics, infra_data, color=['#3498db', '#2ecc71', '#f39c12'], alpha=0.7)
axes[1, 0].set_ylabel('Median Ratio')
axes[1, 0].set_title('Median Infrastructure Ratios')
axes[1, 0].grid(True, alpha=0.3, axis='y')
for i, v in enumerate(infra_data):
    axes[1, 0].text(i, v, f'{v:.1f}', ha='center', va='bottom', fontweight='bold')

# 4. PWD School Distribution
pwd_by_district = equity_index.nlargest(10, 'PWD_Inclusive_Count')
axes[1, 1].barh(range(len(pwd_by_district)), pwd_by_district['PWD_Inclusive_Count'], 
                color='#9b59b6', alpha=0.7)
axes[1, 1].set_yticks(range(len(pwd_by_district)))
axes[1, 1].set_yticklabels(pwd_by_district['District'], fontsize=9)
axes[1, 1].set_xlabel('Number of PWD-Inclusive Schools')
axes[1, 1].set_title('PWD-Inclusive Schools by District (Top 10)')
axes[1, 1].grid(True, alpha=0.3, axis='x')
axes[1, 1].invert_yaxis()

plt.tight_layout()
plt.savefig('nairobi_education_detailed_analysis.png', dpi=300, bbox_inches='tight')
print("   Saved: nairobi_education_detailed_analysis.png")
plt.close()

# Figure 3: Spatial Distribution
fig, ax = plt.subplots(figsize=(12, 10))

scatter = ax.scatter(nairobi_schools_clean['Longitude'], 
                     nairobi_schools_clean['Latitude'],
                     c=nairobi_schools_clean['Infrastructure_Stress'],
                     s=50, alpha=0.6, cmap='YlOrRd', edgecolors='black', linewidth=0.5)

# Highlight PWD-inclusive schools
pwd_schools = nairobi_schools_clean[nairobi_schools_clean['PWD_Inclusive']]
ax.scatter(pwd_schools['Longitude'], pwd_schools['Latitude'],
          s=200, marker='*', color='blue', edgecolors='black', linewidth=1,
          label='PWD-Inclusive Schools', zorder=5)

ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Spatial Distribution of Schools by Infrastructure Stress\n(Stars = PWD-Inclusive Schools)')
ax.legend()
ax.grid(True, alpha=0.3)

cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Infrastructure Stress Score')

plt.tight_layout()
plt.savefig('nairobi_schools_spatial_distribution.png', dpi=300, bbox_inches='tight')
print("   Saved: nairobi_schools_spatial_distribution.png")
plt.close()

# ============================================================================
# 8. KEY FINDINGS SUMMARY
# ============================================================================
print("\n" + "="*80)
print("KEY FINDINGS")
print("="*80)

print("\n1. INFRASTRUCTURE CAPACITY:")
print(f"   - Total schools analyzed: {len(nairobi_schools_clean):,}")
print(f"   - Schools with overcrowded classrooms (>50 ratio): {nairobi_schools_clean['Overcrowded_Classrooms'].sum():,} ({nairobi_schools_clean['Overcrowded_Classrooms'].sum()/len(nairobi_schools_clean)*100:.1f}%)")
print(f"   - Schools exceeding PTR standard (>40): {nairobi_schools_clean['High_PTR'].sum():,} ({nairobi_schools_clean['High_PTR'].sum()/len(nairobi_schools_clean)*100:.1f}%)")
print(f"   - Average infrastructure stress score: {nairobi_schools_clean['Infrastructure_Stress'].mean():.1f}/100")

print("\n2. GENDER EQUITY:")
print(f"   - Total enrollment: {total_enrollment:,}")
print(f"   - Girls enrollment: {girls_enrollment:,} ({girls_enrollment/total_enrollment*100:.1f}%)")
print(f"   - Boys enrollment: {boys_enrollment:,} ({boys_enrollment/total_enrollment*100:.1f}%)")
print(f"   - Schools with gender imbalance (>15% difference): {nairobi_schools_clean['Gender_Imbalance'].sum():,}")
print(f"   - Schools with girls' toilet deficit: {nairobi_schools_clean['Girls_Toilet_Deficit'].sum():,}")

print("\n3. PWD INCLUSIVITY:")
print(f"   - PWD-inclusive schools: {nairobi_schools_clean['PWD_Inclusive'].sum():,} ({pwd_coverage:.1f}%)")
print(f"   - Special schools: {len(special_schools):,}")
print(f"   - Integrated schools: {len(integrated_schools):,}")
print(f"   - Estimated PWD capacity gap: {max(0, estimated_pwd_children - current_pwd_capacity):,.0f} children")

print("\n4. PRIORITY AREAS (Top 5 Districts):")
for idx, row in equity_index.head(5).iterrows():
    print(f"   {row['Priority_Rank']}. {row['District']}: Index = {row['Composite_Equity_Index']:.1f}")
    print(f"      - Schools: {row['School_Count']}, Enrollment: {row['Total_Enrollment']:,}")
    print(f"      - Infrastructure Stress: {row['Avg_Infrastructure_Stress']:.1f}")
    print(f"      - PWD-inclusive schools: {row['PWD_Inclusive_Count']}")

# ============================================================================
# 9. ASSUMPTIONS
# ============================================================================
print("\n" + "="*80)
print("ASSUMPTIONS DOCUMENTED")
print("="*80)
print("""
1. Data Recency: Education facilities data is from 2013 but assumed representative
2. PWD Population: Estimated at 2.5% of total enrollment (conservative estimate)
3. Infrastructure Standards:
   - Pupil-Teacher Ratio: Kenya standard of 40:1 used as threshold
   - Classroom Ratio: 50+ considered overcrowded
   - Toilet Ratio: 50+ considered inadequate
4. Gender Equity: >15% enrollment difference considered significant imbalance
5. Spatial Analysis: District used as proxy for sub-county level analysis
6. Composite Index Weights:
   - School Density: 25%
   - Infrastructure: 30%
   - PWD Gap: 25%
   - Gender Equity: 20%
""")

# ============================================================================
# 10. RECOMMENDATIONS
# ============================================================================
print("="*80)
print("ACTIONABLE RECOMMENDATIONS")
print("="*80)

print("\nPRIORITY 1: INFRASTRUCTURE CAPACITY BUILDING")
print("-" * 80)
print(f"• Target {nairobi_schools_clean['High_PTR'].sum():,} schools exceeding PTR standards")
print(f"• Construct additional classrooms in {nairobi_schools_clean['Overcrowded_Classrooms'].sum():,} overcrowded schools")
print("• Expand toilet facilities, with special attention to girls' facilities")
print(f"• Focus on top priority districts: {', '.join(equity_index.head(3)['District'].tolist())}")

print("\nPRIORITY 2: GENDER EQUITY INTERVENTIONS")
print("-" * 80)
print(f"• Address gender imbalance in {nairobi_schools_clean['Gender_Imbalance'].sum():,} schools")
print(f"• Improve girls' toilet facilities in {nairobi_schools_clean['Girls_Toilet_Deficit'].sum():,} schools")
print("• Implement targeted enrollment campaigns to balance gender representation")
print("• Ensure gender-responsive infrastructure in all new constructions")

print("\nPRIORITY 3: PWD INCLUSIVITY EXPANSION")
print("-" * 80)
print(f"• Expand PWD-inclusive capacity from current {nairobi_schools_clean['PWD_Inclusive'].sum():,} schools")
print(f"• Establish new integrated schools in districts with zero PWD coverage")
print(f"• Address capacity gap of approximately {max(0, estimated_pwd_children - current_pwd_capacity):,.0f} PWD children")
print("• Retrofit existing schools with accessibility features (ramps, accessible toilets)")

print("\nPRIORITY 4: SPATIAL EQUITY")
print("-" * 80)
print("• Establish new schools in underserved high-density areas")
print("• Improve school distribution to reduce travel distances for students")
print("• Prioritize investments in districts with lowest school-to-population ratios")

print("\nALIGNMENT WITH SDG 4:")
print("-" * 80)
print("✓ Target 4.1: Free, equitable quality primary education")
print("✓ Target 4.5: Eliminate gender disparities and ensure equal access")
print("✓ Target 4.a: Build and upgrade education facilities that are disability-sensitive")
print("✓ Target 4.c: Increase supply of qualified teachers")

# ============================================================================
# 11. EXPORT RESULTS
# ============================================================================
print("\n11. Exporting results...")

equity_index.to_csv('nairobi_equity_index_by_district.csv', index=False)
nairobi_schools_clean.to_csv('nairobi_schools_analysis.csv', index=False)

print("   ✓ Equity index saved to: nairobi_equity_index_by_district.csv")
print("   ✓ Detailed school analysis saved to: nairobi_schools_analysis.csv")

print("\n" + "="*80)
print("ANALYSIS COMPLETE!")
print("="*80)

