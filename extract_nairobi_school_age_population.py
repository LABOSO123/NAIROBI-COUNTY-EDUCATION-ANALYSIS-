"""
Extract school-age population (6-14) for Nairobi from urban population file
This will give us actual data instead of estimates
"""
import pandas as pd
import numpy as np

print("="*80)
print("EXTRACTING SCHOOL-AGE POPULATION FROM URBAN POPULATION DATA")
print("="*80)

# Load urban population by age
print("\n1. Loading urban population by age data...")
urban_age = pd.read_csv('data/distribution-of-urban-population-by-age-sex-and-county-kenya-2019-census-volume-iii.csv', encoding='utf-8')

print(f"   File shape: {urban_age.shape}")
print(f"   Columns: {urban_age.columns.tolist()}")

# Find where Nairobi data starts
print("\n2. Finding Nairobi data...")
# The file structure seems to have COUNTY in first column, Age in second
nairobi_rows = []
in_nairobi_section = False

for idx, row in urban_age.iterrows():
    county_val = str(row.iloc[0]).upper()
    if 'NAIROBI' in county_val and pd.notna(row.iloc[0]):
        in_nairobi_section = True
        nairobi_rows.append(idx)
    elif in_nairobi_section and pd.isna(row.iloc[0]):
        # Might be end of Nairobi section or continuation
        continue
    elif in_nairobi_section and 'NAIROBI' not in county_val and pd.notna(row.iloc[0]) and county_val not in ['NAN', 'NONE', '']:
        # Probably moved to next county
        break

print(f"   Found {len(nairobi_rows)} potential Nairobi rows")

# Try a different approach - look for Nairobi in the data
nairobi_mask = urban_age.iloc[:, 0].astype(str).str.contains('NAIROBI', case=False, na=False)
nairobi_data = urban_age[nairobi_mask].copy()

print(f"\n3. Nairobi rows found: {len(nairobi_data)}")
if len(nairobi_data) > 0:
    print("\n   First 30 rows of Nairobi data:")
    print(nairobi_data.head(30).to_string())
    
    # Try to extract ages 6-14
    # The age column seems to be the second column
    age_col = urban_age.columns[1]
    print(f"\n4. Age column: {age_col}")
    print(f"   Sample age values: {nairobi_data[age_col].head(20).tolist()}")

print("\n" + "="*80)
print("NEXT STEP:")
print("="*80)
print("Once we can extract ages 6-14 for Nairobi, we can:")
print("1. Sum them to get total school-age population")
print("2. Use this actual number instead of estimates")
print("3. Still need location-level breakdown, but this is progress!")


