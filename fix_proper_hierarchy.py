"""
Fix the analysis to properly respect administrative hierarchy:
Province → District → Division → Location
AND Constituency (separate electoral boundary)

Match Sub Locations to school Locations, then aggregate by Division and Constituency
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
        
        # Proper code that respects hierarchy
        new_code = """# Geographic Level Equity Analysis - USING ACTUAL CENSUS DATA
# Analyzing by: Division, Location, and Constituency
# RESPECTING ADMINISTRATIVE HIERARCHY: Province → District → Division → Location
# Constituency is a SEPARATE electoral boundary

print("="*80)
print("LOADING ACTUAL CENSUS DATA FOR SCHOOL-AGE POPULATION")
print("="*80)

# Load Sub Locations population data (ACTUAL DATA)
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

# Get Nairobi Sub Locations
nairobi_sub_locs = sub_locs_pop[sub_locs_pop['Region'].astype(str).str.contains('NAIROBI', case=False, na=False)].copy()
nairobi_pop_by_sub_loc = nairobi_sub_locs.groupby('Region')['Total_Clean'].sum().reset_index()
nairobi_pop_by_sub_loc.columns = ['Sub_Location', 'Population']
nairobi_pop_by_sub_loc['Sub_Location_Upper'] = nairobi_pop_by_sub_loc['Sub_Location'].str.upper().str.strip()

print(f"✅ Loaded {len(nairobi_pop_by_sub_loc)} Nairobi Sub Locations with ACTUAL population data")
print(f"   Total population: {nairobi_pop_by_sub_loc['Population'].sum():,.0f}")

# Extract total Nairobi population
nairobi_total_pop = 4397073
school_age_rate = 0.16
nairobi_school_age_pop_total = nairobi_total_pop * school_age_rate

print(f"\\nTotal Nairobi population (census): {nairobi_total_pop:,.0f}")
print(f"Total school-age population (6-14): {nairobi_school_age_pop_total:,.0f}")

total_enrollment_actual = nairobi_schools_clean['TotalEnrol'].sum()
print(f"Total actual enrollment from schools: {total_enrollment_actual:,.0f}")

# ============================================================================
# MATCH SUB LOCATIONS TO SCHOOL LOCATIONS (most granular level)
# Then use school data's Division and Constituency columns for aggregation
# ============================================================================
# Get unique school locations with their Division and Constituency from school data
school_locations = nairobi_schools_clean[['Location', 'Division', 'Costituenc']].drop_duplicates()
school_locations['Location_Upper'] = school_locations['Location'].str.upper().str.strip()

# Match Sub Locations to school Locations
location_matches = []
for idx, sub_loc_row in nairobi_pop_by_sub_loc.iterrows():
    sub_loc_name = sub_loc_row['Sub_Location_Upper']
    pop = sub_loc_row['Population']
    
    # Try exact match first
    exact_matches = school_locations[school_locations['Location_Upper'] == sub_loc_name]
    if len(exact_matches) > 0:
        for _, match in exact_matches.iterrows():
            location_matches.append({
                'Location': match['Location'],
                'Division': match['Division'],
                'Constituency': match['Costituenc'],
                'Population': pop
            })
    else:
        # Try partial match (sub location name contains or is contained in school location)
        for _, school_loc in school_locations.iterrows():
            school_loc_name = school_loc['Location_Upper']
            # Check if names are similar (one contains the other, or vice versa)
            if (sub_loc_name in school_loc_name or school_loc_name in sub_loc_name) and len(sub_loc_name) > 3:
                location_matches.append({
                    'Location': school_loc['Location'],
                    'Division': school_loc['Division'],
                    'Constituency': school_loc['Costituenc'],
                    'Population': pop
                })
                break

location_pop_df = pd.DataFrame(location_matches)

if len(location_pop_df) > 0:
    # Aggregate by Location (sum if multiple Sub Locations match same Location)
    location_pop_agg = location_pop_df.groupby('Location').agg({
        'Population': 'sum',
        'Division': 'first',
        'Constituency': 'first'
    }).reset_index()
    location_pop_agg['School_Age_Pop'] = location_pop_agg['Population'] * school_age_rate
    location_pop_agg['Location_Upper'] = location_pop_agg['Location'].str.upper().str.strip()
    
    print(f"\\n✅ Matched {len(location_pop_agg)} school Locations to Sub Locations with ACTUAL population")
    
    # Aggregate by Division (using Division column from school data)
    division_pop_from_locs = location_pop_df.groupby('Division')['Population'].sum().reset_index()
    division_pop_from_locs['Division_Upper'] = division_pop_from_locs['Division'].str.upper().str.strip()
    division_pop_from_locs['School_Age_Pop'] = division_pop_from_locs['Population'] * school_age_rate
    
    print(f"\\n✅ Aggregated to {len(division_pop_from_locs)} DIVISIONS with ACTUAL population (using school data hierarchy):")
    print(division_pop_from_locs[['Division', 'Population', 'School_Age_Pop']].to_string(index=False))
    
    # Aggregate by Constituency (using Costituenc column from school data)
    constituency_pop_from_locs = location_pop_df.groupby('Constituency')['Population'].sum().reset_index()
    constituency_pop_from_locs['Constituency_Upper'] = constituency_pop_from_locs['Constituency'].str.upper().str.strip()
    constituency_pop_from_locs['School_Age_Pop'] = constituency_pop_from_locs['Population'] * school_age_rate
    
    print(f"\\n✅ Aggregated to {len(constituency_pop_from_locs)} CONSTITUENCIES with ACTUAL population (using school data hierarchy):")
    print(constituency_pop_from_locs[['Constituency', 'Population', 'School_Age_Pop']].to_string(index=False))
else:
    print("\\n⚠️  No location matches found")
    location_pop_agg = pd.DataFrame(columns=['Location', 'Population', 'School_Age_Pop', 'Location_Upper', 'Division', 'Constituency'])
    constituency_pop_from_locs = pd.DataFrame(columns=['Constituency', 'Population', 'School_Age_Pop', 'Constituency_Upper'])
    division_pop_from_locs = pd.DataFrame(columns=['Division', 'Population', 'School_Age_Pop', 'Division_Upper'])

# Function to analyze by geographic level - RESPECTS ADMINISTRATIVE HIERARCHY
def analyze_by_geographic_level(groupby_col, level_name):
    \"\"\"Analyze equity metrics by geographic level - uses ACTUAL Sub Locations population data
    Properly respects: Province → District → Division → Location hierarchy
    Constituency is separate electoral boundary\"\"\"
    
    # Basic aggregations
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
    # Match to Locations, then aggregate by Division/Constituency using school data
    # ============================================================================
    if groupby_col == 'Location':
        # For Location: Use matched Sub Locations population
        analysis['Location_Upper'] = analysis[level_name].str.upper().str.strip()
        analysis = analysis.merge(
            location_pop_agg[['Location_Upper', 'School_Age_Pop']],
            on='Location_Upper',
            how='left'
        )
        
        # For locations without match, distribute by their Division/Constituency
        missing = analysis['School_Age_Pop'].isna() | (analysis['School_Age_Pop'] == 0)
        if missing.sum() > 0:
            # Get Division and Constituency for each location from school data
            loc_to_admin = nairobi_schools_clean.groupby('Location').agg({
                'Division': 'first',
                'Costituenc': 'first'
            }).reset_index()
            loc_to_admin['Location_Upper'] = loc_to_admin['Location'].str.upper().str.strip()
            
            analysis = analysis.merge(loc_to_admin[['Location_Upper', 'Division', 'Costituenc']], on='Location_Upper', how='left')
            
            # Try to fill from Division population first
            analysis = analysis.merge(
                division_pop_from_locs[['Division', 'School_Age_Pop']].rename(columns={'School_Age_Pop': 'Div_School_Age_Pop'}),
                on='Division',
                how='left'
            )
            
            # For missing locations, distribute Division population proportionally
            still_missing = missing & (analysis['Div_School_Age_Pop'].isna() | (analysis['Div_School_Age_Pop'] == 0))
            for div in analysis[still_missing]['Division'].dropna().unique():
                div_mask = (analysis['Division'] == div) & still_missing
                div_locations = analysis[div_mask]
                div_school_age_pop = analysis[analysis['Division'] == div]['Div_School_Age_Pop'].iloc[0] if len(analysis[analysis['Division'] == div]) > 0 else 0
                
                if div_school_age_pop > 0 and len(div_locations) > 0:
                    div_enrollment = div_locations['Total_Enrollment'].sum()
                    if div_enrollment > 0:
                        analysis.loc[div_mask, 'School_Age_Pop'] = (
                            div_school_age_pop * (div_locations['Total_Enrollment'] / div_enrollment)
                        ).values
            
            # For remaining, use enrollment proxy
            still_missing = analysis['School_Age_Pop'].isna() | (analysis['School_Age_Pop'] == 0)
            if still_missing.sum() > 0:
                total_enrollment = analysis['Total_Enrollment'].sum()
                analysis.loc[still_missing, 'School_Age_Pop'] = (
                    nairobi_school_age_pop_total * (analysis.loc[still_missing, 'Total_Enrollment'] / total_enrollment)
                )
            
            analysis = analysis.drop(['Div_School_Age_Pop'], axis=1)
        
        analysis = analysis.drop(['Location_Upper'], axis=1)
        actual_count = (~missing).sum() if 'missing' in locals() else len(analysis[analysis['School_Age_Pop'] > 0])
        print(f"   ✅ Used ACTUAL Sub Locations population for {actual_count} locations")
        
    elif groupby_col == 'Costituenc':
        # For Constituency: Use aggregated Sub Locations population (from school data hierarchy)
        analysis['Constituency_Upper'] = analysis[level_name].str.upper().str.strip()
        analysis = analysis.merge(
            constituency_pop_from_locs[['Constituency_Upper', 'School_Age_Pop']],
            on='Constituency_Upper',
            how='left'
        )
        
        # For constituencies without data, use enrollment proxy
        missing = analysis['School_Age_Pop'].isna() | (analysis['School_Age_Pop'] == 0)
        if missing.sum() > 0:
            total_enrollment = analysis['Total_Enrollment'].sum()
            analysis.loc[missing, 'School_Age_Pop'] = (
                nairobi_school_age_pop_total * (analysis.loc[missing, 'Total_Enrollment'] / total_enrollment)
            )
        
        analysis = analysis.drop(['Constituency_Upper'], axis=1)
        actual_count = (~missing).sum() if 'missing' in locals() else len(analysis) - missing.sum()
        print(f"   ✅ Used ACTUAL Sub Locations population (aggregated by Constituency from school data) for {actual_count} constituencies")
        if missing.sum() > 0:
            print(f"   ⚠️  Used enrollment proxy for {missing.sum()} constituencies (no Sub Locations data)")
        
    elif groupby_col == 'Division':
        # For Division: Use aggregated Sub Locations population (from school data hierarchy)
        analysis = analysis.merge(
            division_pop_from_locs[['Division', 'School_Age_Pop']],
            on='Division',
            how='left'
        )
        
        # For divisions without data, use enrollment proxy
        missing = analysis['School_Age_Pop'].isna() | (analysis['School_Age_Pop'] == 0)
        if missing.sum() > 0:
            total_enrollment = analysis['Total_Enrollment'].sum()
            analysis.loc[missing, 'School_Age_Pop'] = (
                nairobi_school_age_pop_total * (analysis.loc[missing, 'Total_Enrollment'] / total_enrollment)
            )
        
        actual_count = (~missing).sum() if 'missing' in locals() else len(analysis) - missing.sum()
        print(f"   ✅ Used ACTUAL Sub Locations population (aggregated by Division from school data) for {actual_count} divisions")
        if missing.sum() > 0:
            print(f"   ⚠️  Used enrollment proxy for {missing.sum()} divisions (no Sub Locations data)")
    
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
print("Respecting administrative hierarchy: Province → District → Division → Location")
print("Constituency is separate electoral boundary")

division_analysis = analyze_by_geographic_level('Division', 'Division')
location_analysis = analyze_by_geographic_level('Location', 'Location')
constituency_analysis = analyze_by_geographic_level('Costituenc', 'Constituency')"""

        # Replace cell content
        cell['source'] = new_code.split('\n')
        print(f"✓ Updated cell {i} to properly respect administrative hierarchy")
        break

# Save notebook
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("\\n✅ Updated notebook to:")
print("   - Match Sub Locations to school Locations (most granular)")
print("   - Aggregate by Division using school data's Division column")
print("   - Aggregate by Constituency using school data's Costituenc column")
print("   - Respects hierarchy: Province → District → Division → Location")
print("   - Constituency treated as separate electoral boundary")


