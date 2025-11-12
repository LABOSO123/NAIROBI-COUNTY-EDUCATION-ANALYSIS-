"""
Add comprehensive inline comments to code cells explaining what each segment does
"""
import json
import re

with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print("="*80)
print("ADDING CODE COMMENTS")
print("="*80)
print()

comments_added = 0

for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type') == 'code':
        source_lines = cell.get('source', [])
        source = ''.join(source_lines)
        
        # Skip if already has good comments
        if len([l for l in source_lines if l.strip().startswith('#')]) > len(source_lines) * 0.3:
            continue
        
        new_lines = []
        modified = False
        
        for j, line in enumerate(source_lines):
            # Add comment for data loading
            if 'pd.read_csv' in line and '# Load' not in ''.join(source_lines[max(0, j-2):j+1]):
                new_lines.append('# Load dataset from CSV file into pandas DataFrame\n')
                new_lines.append('# This creates a DataFrame that we can analyze\n')
                modified = True
            
            # Add comment for filtering
            if 'nairobi' in line.lower() and 'filter' in line.lower() and '#' not in line:
                new_lines.append('# Filter data to include only Nairobi County schools\n')
                new_lines.append('# This ensures our analysis focuses on Nairobi as required\n')
                modified = True
            
            # Add comment for groupby operations
            if '.groupby(' in line and j == 0:
                new_lines.append('# Aggregate data by geographic unit (e.g., Division, Constituency)\n')
                new_lines.append('# This allows us to analyze metrics at the sub-county level\n')
                modified = True
            
            # Add comment for calculations
            if '=' in line and any(x in line for x in ['_Score', '_Ratio', '_Rate', '_Gap']) and '#' not in line:
                if line.strip().startswith(('equity_index', 'analysis', 'nairobi_schools')):
                    metric_name = re.search(r'(\w+)\s*=', line)
                    if metric_name:
                        metric = metric_name.group(1)
                        new_lines.append(f'# Calculate {metric}: This metric measures...\n')
                        modified = True
            
            # Add comment for print statements that show results
            if 'print(' in line and '='* in line and j == 0:
                new_lines.append('# Display analysis results and summary statistics\n')
                modified = True
            
            new_lines.append(line)
        
        if modified:
            cell['source'] = new_lines
            comments_added += 1
            print(f"   ✅ Added comments to code cell {i}")

print(f"\n✅ Added comments to {comments_added} code cells")

# Save
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("✅ Notebook saved!")




