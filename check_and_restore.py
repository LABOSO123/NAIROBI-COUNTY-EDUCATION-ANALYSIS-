import json

# Check current notebook
with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb_new = json.load(f)

# Check original notebook
with open('analysis.ipynb', 'r', encoding='utf-8') as f:
    nb_orig = json.load(f)

print(f"Current 'New Version' cells: {len(nb_new['cells'])}")
print(f"Original 'analysis.ipynb' cells: {len(nb_orig['cells'])}")

# The user says they had 66 cells originally
# Let me check what's in the original analysis.ipynb and merge it properly
# We need to keep the new census data sections but restore all other missing cells

print("\nRestoring all cells from original notebook...")

# Start with original notebook structure
restored_notebook = nb_orig.copy()

# Find where to insert the new census data sections
# Look for the cell after PWD analysis (around cell 19-20)
insert_position = None
for i, cell in enumerate(restored_notebook['cells']):
    source = ''.join(cell.get('source', []))
    if 'PWD Capacity Analysis' in source or 'Estimated PWD capacity gap' in source:
        insert_position = i + 1
        break

if insert_position is None:
    # If we can't find it, insert after cell 20
    insert_position = 20

print(f"Will insert new sections after cell {insert_position}")

# Get the new census data cells from the current New Version
new_census_cells = []
for i, cell in enumerate(nb_new['cells']):
    source = ''.join(cell.get('source', []))
    if 'LOADING ACTUAL CENSUS DATA' in source or 'GEOGRAPHIC LEVEL EQUITY' in source or 'EDUCATION DESERTS' in source or 'LOCATION-LEVEL ANALYSIS' in source or 'COMPREHENSIVE PRIORITY' in source:
        new_census_cells.append((i, cell))

print(f"Found {len(new_census_cells)} new census-related cells to preserve")

# Create the restored notebook: original cells + new census sections
restored_cells = restored_notebook['cells'][:insert_position].copy()

# Add the new census data cells
for idx, cell in new_census_cells:
    restored_cells.append(cell)

# Add remaining original cells
restored_cells.extend(restored_notebook['cells'][insert_position:])

restored_notebook['cells'] = restored_cells

print(f"Restored notebook will have {len(restored_cells)} cells")

# Save
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(restored_notebook, f, indent=1, ensure_ascii=False)

print("✅ Restored notebook with all original cells + new census sections!")




