import json

print("="*60)
print("RESTORING NOTEBOOK WITH ALL CELLS")
print("="*60)

# Load both notebooks
with open('analysis.ipynb', 'r', encoding='utf-8') as f:
    nb_orig = json.load(f)

with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb_new = json.load(f)

print(f"\nOriginal analysis.ipynb: {len(nb_orig['cells'])} cells")
print(f"Current New Version: {len(nb_new['cells'])} cells")

# Start with ALL cells from original analysis.ipynb
restored_cells = nb_orig['cells'].copy()

# Find where to insert new census sections (after PWD section, before Composite Equity)
insert_idx = None
for i, cell in enumerate(restored_cells):
    source = ''.join(cell.get('source', []))
    if 'Composite Equity Index' in source and '##' in source:
        insert_idx = i
        print(f"\nFound insertion point: Cell {i} (before Composite Equity Index)")
        break

if insert_idx is None:
    # Try to find after PWD section
    for i, cell in enumerate(restored_cells):
        source = ''.join(cell.get('source', []))
        if 'PWD Capacity Analysis' in source or ('Estimated PWD' in source and 'capacity gap' in source):
            insert_idx = i + 1
            print(f"\nFound insertion point: Cell {i+1} (after PWD section)")
            break

if insert_idx is None:
    insert_idx = 20  # Default
    print(f"\nUsing default insertion point: Cell {insert_idx}")

# Extract new census sections from New Version
new_sections = []
for cell in nb_new['cells']:
    source = ''.join(cell.get('source', []))
    if any(x in source for x in [
        'LOADING ACTUAL CENSUS DATA',
        'GEOGRAPHIC LEVEL EQUITY ANALYSIS',
        'School Density vs Population Density',
        'EDUCATION DESERTS - CONSTITUENCY',
        'COMPREHENSIVE PRIORITY ANALYSIS',
        'LOCATION-LEVEL ANALYSIS - INTERACTIVE MAP',
        'def analyze_by_geographic_level',
        '17 Nairobi Sub-Counties'
    ]):
        new_sections.append(cell)

print(f"\nFound {len(new_sections)} new census-related cells to insert")

# Insert new sections
for i, new_cell in enumerate(new_sections):
    restored_cells.insert(insert_idx + i, new_cell)
    print(f"  Inserted new section at position {insert_idx + i}")

print(f"\n✅ Final cell count: {len(restored_cells)} cells")

# Save
restored_notebook = nb_orig.copy()
restored_notebook['cells'] = restored_cells

with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(restored_notebook, f, indent=1, ensure_ascii=False)

print("\n✅ NOTEBOOK RESTORED!")
print("="*60)




