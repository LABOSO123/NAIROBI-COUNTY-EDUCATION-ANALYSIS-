import json

print("Loading notebooks...")

# Load current New Version
with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb_new = json.load(f)

# Load original analysis.ipynb
with open('analysis.ipynb', 'r', encoding='utf-8') as f:
    nb_orig = json.load(f)

print(f"Current New Version: {len(nb_new['cells'])} cells")
print(f"Original analysis.ipynb: {len(nb_orig['cells'])} cells")

# The user had 66 cells originally in New Version
# Let's start with the original analysis.ipynb structure (34 cells)
# Then add the new census sections from New Version
# Then check what else might be missing

# Build the restored notebook
restored_cells = []

# Step 1: Add all cells from original analysis.ipynb up to PWD section
for i, cell in enumerate(nb_orig['cells']):
    source = ''.join(cell.get('source', []))
    if 'PWD Capacity Analysis' in source or 'Estimated PWD capacity gap' in source:
        # Add this cell
        restored_cells.append(cell)
        # Then insert new census sections after this
        print(f"Found PWD section at cell {i}, will insert new sections after")
        
        # Step 2: Add new census data cells from New Version
        for j, new_cell in enumerate(nb_new['cells']):
            new_source = ''.join(new_cell.get('source', []))
            if any(x in new_source for x in ['LOADING ACTUAL CENSUS DATA', 'GEOGRAPHIC LEVEL EQUITY', 
                                              'EDUCATION DESERTS', 'LOCATION-LEVEL ANALYSIS', 
                                              'COMPREHENSIVE PRIORITY', 'School Density vs Population Density']):
                restored_cells.append(new_cell)
                print(f"  Added new census cell from New Version")
        
        # Step 3: Continue with remaining original cells
        restored_cells.extend(nb_orig['cells'][i+1:])
        break
    else:
        restored_cells.append(cell)

# If we didn't find the PWD section, just merge everything
if len(restored_cells) < len(nb_orig['cells']):
    print("Didn't find insertion point, merging all cells...")
    restored_cells = nb_orig['cells'].copy()
    
    # Add new census cells at the end before the final sections
    for new_cell in nb_new['cells']:
        new_source = ''.join(new_cell.get('source', []))
        if any(x in new_source for x in ['LOADING ACTUAL CENSUS DATA', 'GEOGRAPHIC LEVEL EQUITY', 
                                          'EDUCATION DESERTS', 'LOCATION-LEVEL ANALYSIS', 
                                          'COMPREHENSIVE PRIORITY']):
            # Insert before Composite Equity Index section
            insert_idx = None
            for idx, cell in enumerate(restored_cells):
                if 'Composite Equity Index' in ''.join(cell.get('source', [])):
                    insert_idx = idx
                    break
            if insert_idx:
                restored_cells.insert(insert_idx, new_cell)
            else:
                restored_cells.append(new_cell)

print(f"\nRestored notebook will have: {len(restored_cells)} cells")

# Save
restored_notebook = nb_orig.copy()
restored_notebook['cells'] = restored_cells

with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(restored_notebook, f, indent=1, ensure_ascii=False)

print("✅ Restored!")




