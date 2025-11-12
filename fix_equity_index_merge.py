"""
Fix the equity_index merge issue where columns might not exist after merge
"""
import json

with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the cell with the equity index constituency level code
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))
    
    if 'COMPOSITE EQUITY INDEX - CONSTITUENCY LEVEL' in source and 'equity_index = constituency_analysis.copy()' in source:
        print(f"Found cell at index {i}")
        
        # The issue is that after merge, if there are no matches, columns won't exist
        # We need to ensure columns are created even if merge doesn't match
        
        # Find the section where we fill missing values
        old_code = """# Drop the temporary upper column
equity_index = equity_index.drop('Constituency_Upper', axis=1)

# Fill missing values
equity_index['Overcrowded_Schools'] = equity_index['Overcrowded_Schools'].fillna(0).astype(int)"""

        new_code = """# Drop the temporary upper column (only if it exists)
if 'Constituency_Upper' in equity_index.columns:
    equity_index = equity_index.drop('Constituency_Upper', axis=1)

# Ensure all required columns exist (create with 0 if they don't exist from merge)
required_cols = ['Overcrowded_Schools', 'High_PTR_Schools', 'Gender_Imbalanced_Schools', 
                 'Girls_Toilet_Deficit_Schools', 'PWD_Inclusive_Count', 'Special_School_Count']
for col in required_cols:
    if col not in equity_index.columns:
        equity_index[col] = 0

# Fill missing values
equity_index['Overcrowded_Schools'] = equity_index['Overcrowded_Schools'].fillna(0).astype(int)"""

        # Replace in the cell source
        cell_source = ''.join(cell['source'])
        if old_code in cell_source:
            cell['source'] = cell_source.replace(old_code, new_code).split('\n')
            # Add newline characters back
            cell['source'] = [line + '\n' if i < len(cell['source'])-1 else line 
                             for i, line in enumerate(cell['source'])]
            print("✅ Fixed the merge issue")
        else:
            # Try a different approach - find the exact location
            lines = cell['source']
            new_lines = []
            skip_next = False
            for j, line in enumerate(lines):
                if skip_next:
                    skip_next = False
                    continue
                    
                # Check if this is the drop line
                if "equity_index = equity_index.drop('Constituency_Upper', axis=1)" in line:
                    new_lines.append("# Drop the temporary upper column (only if it exists)\n")
                    new_lines.append("if 'Constituency_Upper' in equity_index.columns:\n")
                    new_lines.append("    equity_index = equity_index.drop('Constituency_Upper', axis=1)\n")
                    new_lines.append("\n")
                    new_lines.append("# Ensure all required columns exist (create with 0 if they don't exist from merge)\n")
                    new_lines.append("required_cols = ['Overcrowded_Schools', 'High_PTR_Schools', 'Gender_Imbalanced_Schools', \n")
                    new_lines.append("                 'Girls_Toilet_Deficit_Schools', 'PWD_Inclusive_Count', 'Special_School_Count']\n")
                    new_lines.append("for col in required_cols:\n")
                    new_lines.append("    if col not in equity_index.columns:\n")
                    new_lines.append("        equity_index[col] = 0\n")
                    new_lines.append("\n")
                    skip_next = True
                    continue
                    
                new_lines.append(line)
            
            cell['source'] = new_lines
            print("✅ Fixed the merge issue (alternative method)")
        
        break

# Save the notebook
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("✅ Notebook updated successfully")




