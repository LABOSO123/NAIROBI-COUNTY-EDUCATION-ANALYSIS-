"""
Ensure all visualizations display in notebook output cells, not just save as PNG
Make sure plt.show() is called and plots are visible in the notebook
"""
import json
import re

with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print("="*80)
print("ENSURING VISUALIZATIONS DISPLAY IN NOTEBOOK OUTPUT")
print("="*80)
print()

fixed_count = 0

for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type') == 'code':
        source_lines = cell.get('source', [])
        source = ''.join(source_lines)
        
        # Check if this is a visualization cell
        if 'plt.' in source or 'sns.' in source or 'matplotlib' in source:
            # Check if plt.show() is present
            has_show = 'plt.show()' in source or 'plt.show(' in source
            
            # Check if plt.savefig is present
            has_savefig = 'plt.savefig' in source
            
            # If has savefig but no show, or if we need to ensure display
            if has_savefig and not has_show:
                # Find where to insert plt.show()
                new_lines = []
                show_added = False
                
                for j, line in enumerate(source_lines):
                    new_lines.append(line)
                    
                    # After plt.savefig, add plt.show()
                    if 'plt.savefig' in line and not show_added:
                        # Check if next line is already plt.show()
                        if j + 1 < len(source_lines):
                            next_line = source_lines[j + 1].strip()
                            if 'plt.show()' not in next_line:
                                # Add plt.show() after savefig
                                new_lines.append('\n')
                                new_lines.append('# Display the plot in the notebook output\n')
                                new_lines.append('plt.show()\n')
                                show_added = True
                        else:
                            # Last line, add plt.show()
                            new_lines.append('\n')
                            new_lines.append('# Display the plot in the notebook output\n')
                            new_lines.append('plt.show()\n')
                            show_added = True
                
                if show_added:
                    cell['source'] = new_lines
                    fixed_count += 1
                    print(f"✅ Fixed cell {i}: Added plt.show() after plt.savefig()")
            
            # Also ensure plt.tight_layout() is before savefig/show
            if 'plt.savefig' in source or 'plt.show()' in source:
                # Check if tight_layout is present
                if 'plt.tight_layout()' not in source and 'plt.subplots' in source:
                    # This is okay - tight_layout might not always be needed
                    pass
            
            # Ensure %matplotlib inline is set (should be in first cell, but check)
            if i > 0 and '%matplotlib' not in source:
                # Check if it's in an earlier cell
                has_matplotlib_inline = False
                for prev_i in range(i):
                    prev_cell = nb['cells'][prev_i]
                    if prev_cell.get('cell_type') == 'code':
                        prev_source = ''.join(prev_cell.get('source', []))
                        if '%matplotlib inline' in prev_source:
                            has_matplotlib_inline = True
                            break
                
                # If not found and this is a plotting cell, we should ensure it's set
                # But we won't add it here to avoid duplication
                pass

print(f"\n✅ Fixed {fixed_count} visualization cells")

# Also check if %matplotlib inline is in the first code cells
print("\nChecking for %matplotlib inline...")
for i, cell in enumerate(nb['cells'][:10]):  # Check first 10 cells
    if cell.get('cell_type') == 'code':
        source = ''.join(cell.get('source', []))
        if '%matplotlib inline' in source or '%matplotlib' in source:
            print(f"✅ Found %matplotlib inline in cell {i}")
            break
else:
    # Add it to the first code cell with imports
    print("⚠️  %matplotlib inline not found - adding to first code cell")
    for i, cell in enumerate(nb['cells'][:10]):
        if cell.get('cell_type') == 'code':
            source_lines = cell.get('source', [])
            source = ''.join(source_lines)
            if 'import matplotlib' in source or 'import plt' in source:
                # Add after matplotlib import
                new_lines = []
                added = False
                for line in source_lines:
                    new_lines.append(line)
                    if ('import matplotlib' in line or 'import plt' in line) and not added:
                        new_lines.append('%matplotlib inline\n')
                        added = True
                if added:
                    cell['source'] = new_lines
                    print(f"✅ Added %matplotlib inline to cell {i}")
                    break

# Save the notebook
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("\n" + "="*80)
print("✅ NOTEBOOK UPDATED")
print("="*80)
print("All visualizations will now display in notebook output cells")
print("PNG files will also be saved for external use")
print("="*80)




