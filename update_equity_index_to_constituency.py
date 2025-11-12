"""
Update Composite Equity Index from District to Constituency level
"""
import json

with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the cell with equity index calculation
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))
    
    if 'Aggregate data by District' in source and 'equity_index = nairobi_schools_clean.groupby' in source:
        print(f"Found equity index cell at index {i}")
        
        # Replace the entire cell content
        new_code = """# ================================================================================
# COMPOSITE EQUITY INDEX - CONSTITUENCY LEVEL
# ================================================================================
# Use constituency_analysis which already has actual census population data
# This provides more granular and actionable insights than District level

print("="*80)
print("COMPOSITE EQUITY INDEX - CONSTITUENCY LEVEL")
print("="*80)

# Start with constituency_analysis which has actual population data
equity_index = constituency_analysis.copy()

# Get the constituency column name dynamically
constituency_col = equity_index.columns[0]

# Rename to standardize
if constituency_col != 'Constituency':
    equity_index = equity_index.rename(columns={constituency_col: 'Constituency'})

# Add additional metrics we need for the equity index
# Get counts of schools with issues by constituency
constituency_issues = nairobi_schools_clean.groupby('Costituenc').agg({
    'Overcrowded_Classrooms': 'sum',
    'High_PTR': 'sum',
    'Gender_Imbalance': 'sum',
    'Girls_Toilet_Deficit': 'sum',
    'PWD_Inclusive': 'sum',
    'Is_Special_School': 'sum'
}).reset_index()
constituency_issues.columns = ['Constituency', 'Overcrowded_Schools', 'High_PTR_Schools', 
                               'Gender_Imbalanced_Schools', 'Girls_Toilet_Deficit_Schools',
                               'PWD_Inclusive_Count', 'Special_School_Count']

# Merge with equity_index
equity_index = equity_index.merge(
    constituency_issues[['Constituency', 'Overcrowded_Schools', 'High_PTR_Schools', 
                        'Gender_Imbalanced_Schools', 'Girls_Toilet_Deficit_Schools',
                        'PWD_Inclusive_Count', 'Special_School_Count']],
    on='Constituency',
    how='left'
)

# Fill missing values
equity_index['Overcrowded_Schools'] = equity_index['Overcrowded_Schools'].fillna(0).astype(int)
equity_index['High_PTR_Schools'] = equity_index['High_PTR_Schools'].fillna(0).astype(int)
equity_index['Gender_Imbalanced_Schools'] = equity_index['Gender_Imbalanced_Schools'].fillna(0).astype(int)
equity_index['Girls_Toilet_Deficit_Schools'] = equity_index['Girls_Toilet_Deficit_Schools'].fillna(0).astype(int)
equity_index['PWD_Inclusive_Count'] = equity_index['PWD_Inclusive_Count'].fillna(0).astype(int)
equity_index['Special_School_Count'] = equity_index['Special_School_Count'].fillna(0).astype(int)

print(f"\\n✅ Equity index calculated for {len(equity_index)} CONSTITUENCIES:")
print(equity_index[['Constituency', 'School_Count', 'Total_Enrollment', 'School_Age_Pop', 
                    'Schools_per_1000', 'Avg_Infrastructure_Stress']].to_string(index=False))"""
        
        cell['source'] = new_code.split('\n')
        cell['outputs'] = []  # Clear old outputs
        print(f"✅ Updated cell {i} to use Constituency level")
        break

# Also update the component scores cell
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))
    
    if 'School_Density_Score' in source and 'District' in source:
        print(f"Found component scores cell at index {i}")
        
        # Update references from District to Constituency
        new_source = []
        for line in cell['source']:
            if 'District' in line and 'equity_index' in line:
                line = line.replace('District', 'Constituency')
            new_source.append(line)
        
        cell['source'] = new_source
        print(f"✅ Updated component scores cell {i}")
        break

# Update the final ranking cell
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))
    
    if 'Rank districts by priority' in source or 'Top 10 Priority Districts' in source:
        print(f"Found ranking cell at index {i}")
        
        new_source = []
        for line in cell['source']:
            if 'District' in line:
                line = line.replace('District', 'Constituency')
                line = line.replace('districts', 'constituencies')
            new_source.append(line)
        
        # Add more detailed output
        if 'print("Top 10 Priority' in ''.join(cell['source']):
            new_source.append('\n')
            new_source.append('print("\\n" + "="*80)\n')
            new_source.append('print("TOP PRIORITY CONSTITUENCIES FOR INVESTMENT:")\n')
            new_source.append('print("="*80)\n')
            new_source.append('print(equity_index[["Priority_Rank", "Constituency", "Composite_Equity_Index", \n')
            new_source.append('                    "School_Count", "Schools_per_1000", "Total_Enrollment", \n')
            new_source.append('                    "School_Age_Pop", "Capacity_Gap", "Avg_Infrastructure_Stress"]].to_string(index=False))\n')
        
        cell['source'] = new_source
        print(f"✅ Updated ranking cell {i}")
        break

# Save
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("\n✅ Updated Composite Equity Index to Constituency level!")




