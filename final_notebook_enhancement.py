"""
Final comprehensive notebook enhancement - find all sections and add documentation
"""
import json
import re

with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Read the descriptions from the previous script
descriptions = {
    'data_loading': """**What This Section Does:**
This section loads all necessary Python libraries and datasets required for the analysis.

**Libraries Used:**
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computations  
- `matplotlib` & `seaborn`: Data visualization
- `warnings`: Suppress non-critical warnings for cleaner output

**Datasets Loaded:**
1. **Primary Schools Dataset** (`kenya_primary_schools.csv`): Contains information on all primary schools in Kenya
2. **Population Dataset** (`kenya-urban-population-by-sub-county.csv`): Census data for Nairobi sub-counties
3. **Household Size Dataset** (`kenya-average-household-size-by-sub-county.csv`): Average household size by sub-county

**What We're Doing:**
- Importing required Python libraries
- Setting visualization styles
- Loading CSV files into pandas DataFrames
- Filtering for Nairobi County only

**Questions We're Answering:**
- How many schools are in Nairobi?
- What data do we have available for analysis?

**Insights We Hope to Get:**
- Understanding of data availability and completeness
- Foundation for all subsequent analyses""",

    'data_cleaning': """**What This Section Does:**
This section cleans and prepares the data for analysis by handling missing values, standardizing formats, and creating derived indicators.

**Key Cleaning Steps:**
1. Filter Nairobi Schools: Extract only schools within Nairobi County
2. Handle Missing Values: Fill or remove missing data appropriately
3. Standardize Formats: Ensure consistent naming, data types
4. Create Indicators: Build composite metrics (e.g., Infrastructure_Stress, Gender_Balance)

**Derived Indicators Created:**
- `Infrastructure_Stress`: Composite score combining PTR, classroom ratio, toilet ratio
- `Overcrowded_Classrooms`: Binary indicator (ClassroomRatio > 50)
- `High_PTR`: Binary indicator (PupilTeacherRatio > 40)
- `Gender_Imbalance`: Binary indicator (gender difference > 15%)
- `Girls_Toilet_Deficit`: Binary indicator (inadequate girls' toilets)
- `PWD_Inclusive`: Binary indicator (INTEGRATED or SPECIAL SCHOOL)

**What We're Doing:**
- Removing invalid records
- Standardizing geographic names
- Creating boolean flags for analysis
- Calculating ratios and composite scores

**Questions We're Answering:**
- Is the data clean and ready for analysis?
- What's the data quality?

**Insights We Hope to Get:**
- Data quality assessment
- Understanding of data completeness
- Foundation for all subsequent analyses"""
}

# Find all markdown cells and identify sections
print("Scanning notebook for sections...")
sections_found = []

for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type') == 'markdown':
        source = ''.join(cell.get('source', []))
        
        # Look for section headers
        if re.search(r'##\s*\d+\.', source):
            # Extract section number and name
            match = re.search(r'##\s*(\d+)\.\s*(.+)', source)
            if match:
                num = match.group(1)
                name = match.group(2).strip()
                sections_found.append((i, num, name, source))
                print(f"Found section {num}: {name} at cell {i}")

print(f"\nFound {len(sections_found)} sections")

# Now update sections that don't have detailed documentation
updated = 0
for i, num, name, source in sections_found:
    if 'What This Section Does' not in source:
        # Determine which description to use
        desc_key = None
        if 'Data Loading' in name or 'data loading' in name.lower():
            desc_key = 'data_loading'
        elif 'Data Cleaning' in name or 'Cleaning' in name or 'Preprocessing' in name:
            desc_key = 'data_cleaning'
        
        if desc_key and desc_key in descriptions:
            new_source = f"""## {num}. {name}

{descriptions[desc_key]}
"""
            nb['cells'][i]['source'] = new_source.split('\n')
            updated += 1
            print(f"✅ Updated section {num}: {name}")

print(f"\n✅ Updated {updated} sections")

# Save
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("✅ Notebook saved!")




