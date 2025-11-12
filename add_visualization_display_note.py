"""
Add a note at the beginning of the visualizations section explaining that
plots will display in notebook output AND be saved as PNG files
"""
import json

with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the visualizations section header
for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type') == 'markdown':
        source = ''.join(cell.get('source', []))
        if '## 11. Visualizations' in source or '## 11' in source and 'Visualization' in source:
            # Add a note about display
            current_source = cell['source']
            
            # Check if note already exists
            if 'plots will display' not in source.lower() and 'notebook output' not in source.lower():
                # Add note at the end
                note = """\n\n**📊 Display Information:**
- All visualizations will **automatically display** in the notebook output cells below each code cell
- PNG files are also saved for external use (presentations, reports)
- You can see the plots directly in this notebook - no need to open separate files
- Each visualization includes both `plt.savefig()` (saves PNG) and `plt.show()` (displays in notebook)"""
                
                new_source = current_source + [line + '\n' for line in note.split('\n') if line.strip()]
                cell['source'] = new_source
                print(f"✅ Added display information note to visualizations section (cell {i})")
                break

# Also add a reminder in the first visualization code cell
for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type') == 'code':
        source = ''.join(cell.get('source', []))
        # Find first visualization cell (has plt. and is after visualizations section)
        if 'plt.' in source and 'fig' in source and i > 30:  # After section 11
            source_lines = cell['source']
            # Check if it already has a comment about display
            if 'Display' not in ''.join(source_lines[:5]) and 'notebook output' not in source.lower():
                # Add comment at the beginning
                comment = ['# NOTE: This plot will display in the notebook output cell below\n',
                          '#       A PNG file will also be saved for external use\n',
                          '\n']
                cell['source'] = comment + source_lines
                print(f"✅ Added display reminder to first visualization cell (cell {i})")
                break

# Save
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("\n✅ Notebook updated with display information")
print("   Users will now know that plots display in notebook output cells")

