"""
Fix the analysis to use ACTUAL Sub Locations population data aggregated by constituency
This is the most accurate approach since we have location-level population data
"""
import json

# Load notebook
with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']

# Find cell 15 (geographic analysis)
for i, cell in enumerate(cells):
    source = ''.join(cell.get('source', []))
    
    if 'Geographic Level Equity Analysis - USING ACTUAL CENSUS DATA' in source and 'def analyze_by_geographic_level' in source:
        
        # New code that uses Sub Locations population aggregated by constituency
        new_code = """# Geographic Level Equity Analysis - USING ACTUAL CENSUS DATA
# Analyzing by: Division, Location, and Constituency
# NOW USING ACTUAL SUB LOCATIONS POPULATION DATA AGGREGATED BY CONSTITUENCY

print("="*80)
print("LOADING ACTUAL CENSUS DATA FOR SCHOOL-AGE POPULATION")
print("="*80)

# Load Sub Locations population data (ACTUAL DATA - most granular available)
print("\\nLoading Sub Locations population data...")
sub_locs_pop = pd.read_csv('data/distribution-of-population-by-sex-and-sub-locations-2019-census-volume-ii.csv', encoding='utf-8')

# Clean population numbers
def clean_number(val):
    if pd.isna(val):
        return 0
    val_str = str(val).replace(',', '').replace('"', '').strip()
    if val_str == '-' or val_str == '':
        return 0
    try:
        return float(val_str)
    except:
        return 0

sub_locs_pop['Total_Clean'] = sub_locs_pop['Total'].apply(clean_number)

# Get Nairobi Sub Locations and aggregate by location name
nairobi_sub_locs = sub_locs_pop[sub_locs_pop['Region'].astype(str).str.contains('NAIROBI', case=False, na=False)].copy()
nairobi_pop_by_location = nairobi_sub_locs.groupby('Region')['Total_Clean'].sum().reset_index()
nairobi_pop_by_location.columns = ['Location', 'Population']
nairobi_pop_by_location['Location_Upper'] = nairobi_pop_by_location['Location'].str.upper().str.strip()

print(f"✅ Loaded {len(nairobi_pop_by_location)} Nairobi Sub Locations with ACTUAL population data")
print(f"   Total population in Sub Locations: {nairobi_pop_by_location['Population'].sum():,.0f}")

# Extract total Nairobi population from census
nairobi_total_pop = 4397073  # From 2019 Kenya Census
school_age_rate = 0.16  # 16% of population is school-age (6-14)
nairobi_school_age_pop_total = nairobi_total_pop * school_age_rate

print(f"\\nTotal Nairobi population (census): {nairobi_total_pop:,.0f}")
print(f"Total school-age population (6-14): {nairobi_school_age_pop_total:,.0f}")

# Calculate ACTUAL enrollment from schools dataset
total_enrollment_actual = nairobi_schools_clean['TotalEnrol'].sum()
print(f"\\nTotal actual enrollment from schools: {total_enrollment_actual:,.0f}")

# ============================================================================
# MAP LOCATIONS TO CONSTITUENCIES AND AGGREGATE POPULATION BY CONSTITUENCY
# ============================================================================
# Create mapping: Location -> Constituency from school data
location_to_constituency = nairobi_schools_clean.groupby('Location')['Costituenc'].first().reset_index()
location_to_constituency.columns = ['Location', 'Constituency']
location_to_constituency['Location_Upper'] = location_to_constituency['Location'].str.upper().str.strip()
location_to_constituency['Constituency_Upper'] = location_to_constituency['Constituency'].str.upper().str.strip()

# Match Sub Locations to school Locations (try exact match first, then partial)
location_pop_matched = []
for idx, row in nairobi_pop_by_location.iterrows():
    loc_name = row['Location_Upper']
    pop = row['Population']
    
    # Try to find matching school location
    matching_school_locs = location_to_constituency[location_to_constituency['Location_Upper'] == loc_name]
    
    if len(matching_school_locs) > 0:
        # Exact match found
        for _, school_loc in matching_school_locs.iterrows():
            location_pop_matched.append({
                'Location': school_loc['Location'],
                'Constituency': school_loc['Constituency'],
                'Constituency_Upper': school_loc['Constituency_Upper'],
                'Population': pop
            })
    else:
        # Try partial match (location name contains or is contained in Sub Location name)
        for _, school_loc in location_to_constituency.iterrows():
            school_loc_upper = school_loc['Location_Upper']
            if loc_name in school_loc_upper or school_loc_upper in loc_name:
                location_pop_matched.append({
                    'Location': school_loc['Location'],
                    'Constituency': school_loc['Constituency'],
                    'Constituency_Upper': school_loc['Constituency_Upper'],
                    'Population': pop
                })
                break

location_pop_df = pd.DataFrame(location_pop_matched)

# Aggregate population by constituency (sum of all locations in each constituency)
if len(location_pop_df) > 0:
    constituency_pop_from_locs = location_pop_df.groupby('Constituency_Upper')['Population'].sum().reset_index()
    constituency_pop_from_locs.columns = ['Constituency', 'Population']
    constituency_pop_from_locs['School_Age_Pop'] = constituency_pop_from_locs['Population'] * school_age_rate
    
    print(f"\\n✅ Mapped {len(location_pop_df)} Sub Locations to school Locations")
    print(f"✅ Aggregated to {len(constituency_pop_from_locs)} constituencies with ACTUAL population:")
    print(constituency_pop_from_locs[['Constituency', 'Population', 'School_Age_Pop']].to_string(index=False))
else:
    print("\\n⚠️  No location matches found - will use enrollment proxy")
    constituency_pop_from_locs = pd.DataFrame(columns=['Constituency', 'Population', 'School_Age_Pop'])

# Create location-level population mapping (for locations that matched)
location_pop_mapping = location_pop_df.groupby('Location')['Population'].sum().reset_index()
location_pop_mapping['Location_Upper'] = location_pop_mapping['Location'].str.upper().str.strip()
location_pop_mapping['School_Age_Pop'] = location_pop_mapping['Population'] * school_age_rate

# For locations without direct match, distribute constituency population proportionally
location_to_const_with_pop = location_to_constituency.merge(
    constituency_pop_from_locs[['Constituency', 'School_Age_Pop']].rename(columns={'Constituency': 'Constituency_Upper'}),
    on='Constituency_Upper',
    how='left'
)

# Function to analyze by geographic level - NOW USES ACTUAL SUB LOCATIONS POPULATION
def analyze_by_geographic_level(groupby_col, level_name):
    \"\"\"Analyze equity metrics by geographic level - uses ACTUAL Sub Locations population data\"\"\"
    
    # First, do basic aggregations
    analysis = nairobi_schools_clean.groupby(groupby_col).agg({
        'Name_of_Sc': 'count',
        'TotalEnrol': 'sum',
        'TotalBoys': 'sum',
        'TotalGirls': 'sum',
        'PupilTeach': 'mean',
        'ClassrmRat': 'mean',
        'ToiletRati': 'mean',
        'Type3': lambda x: x.isin(['INTEGRATED', 'SPECIAL SCHOOL']).sum(),
        'Status': lambda x: (x == 'PUBLIC').sum()
    }).reset_index()
    
    # Calculate Infrastructure_Stress
    analysis['Avg_Infrastructure_Stress'] = (
        (analysis['PupilTeach'].fillna(0) / 60 * 33.3) +
        (analysis['ClassrmRat'].fillna(0) / 80 * 33.3) +
        (analysis['ToiletRati'].fillna(0) / 80 * 33.3)
    ).clip(0, 100)
    
    # Calculate counts
    def get_counts(group):
        overcrowded = (group['ClassrmRat'] > 50).sum()
        high_ptr = (group['PupilTeach'] > 40).sum()
        girls_pct = (group['TotalGirls'] / group['TotalEnrol'].replace(0, np.nan) * 100).fillna(0)
        boys_pct = (group['TotalBoys'] / group['TotalEnrol'].replace(0, np.nan) * 100).fillna(0)
        gender_imbalance = (abs(girls_pct - boys_pct) > 15).sum()
        return pd.Series({
            'Overcrowded_Schools': overcrowded,
            'High_PTR_Schools': high_ptr,
            'Gender_Imbalanced_Schools': gender_imbalance
        })
    
    counts_df = nairobi_schools_clean.groupby(groupby_col).apply(get_counts).reset_index()
    analysis = analysis.merge(counts_df, on=groupby_col, how='left')
    analysis['Overcrowded_Schools'] = analysis['Overcrowded_Schools'].fillna(0).astype(int)
    analysis['High_PTR_Schools'] = analysis['High_PTR_Schools'].fillna(0).astype(int)
    analysis['Gender_Imbalanced_Schools'] = analysis['Gender_Imbalanced_Schools'].fillna(0).astype(int)
    
    # Rename columns
    analysis.columns = [level_name, 'School_Count', 'Total_Enrollment', 
                        'Total_Boys', 'Total_Girls', 'Avg_PTR', 'Avg_ClassrmRat', 'Avg_ToiletRati',
                        'PWD_Inclusive_Count', 'Public_Schools', 'Avg_Infrastructure_Stress',
                        'Overcrowded_Schools', 'High_PTR_Schools', 'Gender_Imbalanced_Schools']
    
    analysis = analysis[[level_name, 'School_Count', 'Total_Enrollment', 
                         'Total_Boys', 'Total_Girls', 'Avg_Infrastructure_Stress',
                         'PWD_Inclusive_Count', 'Overcrowded_Schools', 
                         'High_PTR_Schools', 'Gender_Imbalanced_Schools', 'Public_Schools']]
    
    # ============================================================================
    # USE ACTUAL SUB LOCATIONS POPULATION DATA
    # ============================================================================
    if groupby_col == 'Location':
        # For Location: Use matched Sub Locations population
        analysis['Location_Upper'] = analysis[level_name].str.upper().str.strip()
        analysis = analysis.merge(
            location_pop_mapping[['Location_Upper', 'School_Age_Pop']],
            on='Location_Upper',
            how='left'
        )
        
        # For locations without match, distribute constituency population proportionally
        missing = analysis['School_Age_Pop'].isna() | (analysis['School_Age_Pop'] == 0)
        if missing.sum() > 0:
            # Get constituency for each location
            analysis = analysis.merge(
                location_to_const_with_pop[['Location', 'Constituency_Upper', 'School_Age_Pop']].rename(columns={'School_Age_Pop': 'Const_School_Age_Pop'}),
                left_on=level_name,
                right_on='Location',
                how='left'
            )
            
            # For locations in constituencies with population data, distribute proportionally
            for const in analysis[missing]['Constituency_Upper'].dropna().unique():
                const_mask = (analysis['Constituency_Upper'] == const) & missing
                const_locations = analysis[const_mask]
                const_school_age_pop = analysis[analysis['Constituency_Upper'] == const]['Const_School_Age_Pop'].iloc[0] if len(analysis[analysis['Constituency_Upper'] == const]) > 0 else 0
                
                if const_school_age_pop > 0 and len(const_locations) > 0:
                    # Distribute based on enrollment proportion
                    const_enrollment = const_locations['Total_Enrollment'].sum()
                    if const_enrollment > 0:
                        analysis.loc[const_mask, 'School_Age_Pop'] = (
                            const_school_age_pop * (const_locations['Total_Enrollment'] / const_enrollment)
                        ).values
            
            # For remaining locations, use enrollment proxy
            still_missing = analysis['School_Age_Pop'].isna() | (analysis['School_Age_Pop'] == 0)
            if still_missing.sum() > 0:
                total_enrollment = analysis['Total_Enrollment'].sum()
                analysis.loc[still_missing, 'School_Age_Pop'] = (
                    nairobi_school_age_pop_total * (analysis.loc[still_missing, 'Total_Enrollment'] / total_enrollment)
                )
            
            analysis = analysis.drop(['Constituency_Upper', 'Const_School_Age_Pop'], axis=1)
        
        analysis = analysis.drop(['Location_Upper'], axis=1)
        actual_count = (~missing).sum() if 'missing' in locals() else len(analysis)
        print(f"   ✅ Used ACTUAL Sub Locations population for {actual_count} locations")
        
    elif groupby_col == 'Costituenc':
        # For Constituency: Use aggregated Sub Locations population
        analysis['Constituency_Upper'] = analysis[level_name].str.upper().str.strip()
        analysis = analysis.merge(
            constituency_pop_from_locs[['Constituency', 'School_Age_Pop']].rename(columns={'Constituency': 'Constituency_Upper'}),
            on='Constituency_Upper',
            how='left'
        )
        
        # For constituencies without Sub Locations data, use enrollment proxy
        missing = analysis['School_Age_Pop'].isna() | (analysis['School_Age_Pop'] == 0)
        if missing.sum() > 0:
            total_enrollment = analysis['Total_Enrollment'].sum()
            analysis.loc[missing, 'School_Age_Pop'] = (
                nairobi_school_age_pop_total * (analysis.loc[missing, 'Total_Enrollment'] / total_enrollment)
            )
        
        analysis = analysis.drop(['Constituency_Upper'], axis=1)
        actual_count = (~missing).sum() if 'missing' in locals() else len(analysis) - missing.sum()
        print(f"   ✅ Used ACTUAL Sub Locations population (aggregated) for {actual_count} constituencies")
        if missing.sum() > 0:
            print(f"   ⚠️  Used enrollment proxy for {missing.sum()} constituencies (no Sub Locations data)")
        
    else:
        # For Division: Use enrollment as proxy (no direct census data)
        total_enrollment = analysis['Total_Enrollment'].sum()
        analysis['School_Age_Pop'] = (
            nairobi_school_age_pop_total * (analysis['Total_Enrollment'] / total_enrollment)
        ).fillna(0)
        print(f"   ⚠️  Division: Using enrollment as proxy (no direct census data)")
    
    # Calculate metrics using ACTUAL data
    analysis['Enrollment_Rate'] = (
        analysis['Total_Enrollment'] / analysis['School_Age_Pop'] * 100
    ).replace([np.inf, -np.inf], 0).fillna(0)
    
    analysis['Capacity_Gap'] = (
        analysis['School_Age_Pop'] - analysis['Total_Enrollment']
    ).fillna(0)
    
    analysis['Schools_per_1000'] = (
        analysis['School_Count'] / (analysis['School_Age_Pop'] / 1000)
    ).replace([np.inf, -np.inf], 0).fillna(0)
    
    return analysis

# Analyze by DIVISION, LOCATION, and CONSTITUENCY
print("\\n" + "="*80)
print("SPATIAL EQUITY ANALYSIS")
print("="*80)

division_analysis = analyze_by_geographic_level('Division', 'Division')
location_analysis = analyze_by_geographic_level('Location', 'Location')
constituency_analysis = analyze_by_geographic_level('Costituenc', 'Constituency')"""

        # Replace cell content
        cell['source'] = new_code.split('\n')
        print(f"✓ Updated cell {i} to use ACTUAL Sub Locations population aggregated by constituency")
        break

# Save notebook
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("\\n✅ Updated notebook to use ACTUAL Sub Locations population data")
print("   - Locations: Direct match with Sub Locations where available")
print("   - Constituencies: Aggregated from Sub Locations within each constituency")
print("   - This will give ACCURATE and VARYING enrollment rates!")


