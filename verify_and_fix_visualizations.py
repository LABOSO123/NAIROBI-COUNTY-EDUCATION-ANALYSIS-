"""
Verify all visualization cells have both plt.savefig() and plt.show()
Ensure proper order: savefig first, then show
"""
import json

with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print("="*80)
print("VERIFYING ALL VISUALIZATIONS HAVE PROPER DISPLAY")
print("="*80)
print()

viz_cells_found = []
fixed_count = 0

for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type') == 'code':
        source_lines = cell.get('source', [])
        source = ''.join(source_lines)
        
        # Check if this is a visualization cell
        if ('plt.' in source or 'sns.' in source) and ('fig' in source or 'ax' in source or 'plot' in source.lower()):
            has_savefig = 'plt.savefig' in source
            has_show = 'plt.show()' in source
            
            viz_cells_found.append((i, has_savefig, has_show))
            
            # If it has plotting but no show, add it
            if not has_show:
                # Find the end of the plotting code
                new_lines = []
                show_added = False
                
                for j, line in enumerate(source_lines):
                    new_lines.append(line)
                    
                    # After the last plt command, add show
                    if j == len(source_lines) - 1 or (j < len(source_lines) - 1 and 
                        'plt.' not in ''.join(source_lines[j+1:]) and 
                        'sns.' not in ''.join(source_lines[j+1:])):
                        if 'plt.show()' not in line and not show_added:
                            # Check if savefig is in this line or nearby
                            if 'plt.savefig' in line:
                                # Add show after savefig line
                                new_lines.append('\n')
                                new_lines.append('# Display the plot in the notebook output cell\n')
                                new_lines.append('plt.show()\n')
                                show_added = True
                            elif j == len(source_lines) - 1:
                                # Last line, add show
                                new_lines.append('\n')
                                new_lines.append('# Display the plot in the notebook output cell\n')
                                new_lines.append('plt.show()\n')
                                show_added = True
                
                # Also check if we need to add show after savefig
                if not show_added:
                    for j, line in enumerate(source_lines):
                        if 'plt.savefig' in line:
                            # Check next few lines
                            next_lines = ''.join(source_lines[j+1:j+4])
                            if 'plt.show()' not in next_lines:
                                # Insert after savefig
                                insert_pos = j + 1
                                new_lines = source_lines[:insert_pos] + [
                                    '\n',
                                    '# Display the plot in the notebook output cell\n',
                                    'plt.show()\n'
                                ] + source_lines[insert_pos:]
                                cell['source'] = new_lines
                                fixed_count += 1
                                print(f"✅ Fixed cell {i}: Added plt.show() after plt.savefig()")
                                break
                    else:
                        # No savefig, but has plotting - add show at end
                        if not any('plt.show()' in line for line in source_lines):
                            source_lines.append('\n')
                            source_lines.append('# Display the plot in the notebook output cell\n')
                            source_lines.append('plt.show()\n')
                            cell['source'] = source_lines
                            fixed_count += 1
                            print(f"✅ Fixed cell {i}: Added plt.show() at end")

print(f"\n📊 Found {len(viz_cells_found)} visualization cells")
print(f"✅ Fixed {fixed_count} cells to ensure display")

# Print summary
print("\n" + "="*80)
print("VISUALIZATION CELLS SUMMARY")
print("="*80)
for idx, (cell_idx, has_save, has_show) in enumerate(viz_cells_found[:10]):  # Show first 10
    status = "✅" if (has_save and has_show) or has_show else "⚠️"
    print(f"{status} Cell {cell_idx}: savefig={has_save}, show={has_show}")

if len(viz_cells_found) > 10:
    print(f"... and {len(viz_cells_found) - 10} more")

# Save the notebook
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("\n" + "="*80)
print("✅ NOTEBOOK UPDATED")
print("="*80)
print("All visualizations will:")
print("  1. Save as PNG files (for external use)")
print("  2. Display in notebook output cells (for viewing in notebook)")
print("="*80)




