"""
Add diagnostics and adjust map color thresholds to better reflect reality
"""
import json
import re

with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find the map cell
for i, cell in enumerate(nb['cells']):
    source = ''.join(cell.get('source', []))
    
    if 'LOCATION-LEVEL ANALYSIS - INTERACTIVE MAP' in source and 'location_coords =' in source:
        print(f"Found map cell at index {i}")
        
        # Add diagnostics before location_coords
        source_lines = cell['source']
        new_source = []
        
        for j, line in enumerate(source_lines):
            # Add diagnostics before "Get location centroids"
            if 'Get location centroids from school data' in line or 'location_coords = nairobi_schools_clean.groupby' in line:
                new_source.append('# ================================================================================\n')
                new_source.append('# DIAGNOSTIC: Check actual distribution of Schools_per_1000\n')
                new_source.append('# ================================================================================\n')
                new_source.append('print("\\n📊 ACTUAL DISTRIBUTION OF Schools_per_1000:")\n')
                new_source.append(f'print(f"   Total locations: {{len(location_analysis)}}")\n')
                new_source.append(f'print(f"   Education Deserts (< 0.5): {{len(location_analysis[location_analysis[\'Schools_per_1000\'] < 0.5])}}")\n')
                new_source.append(f'print(f"   Moderate Need (0.5-1.0): {{len(location_analysis[(location_analysis[\'Schools_per_1000\'] >= 0.5) & (location_analysis[\'Schools_per_1000\'] < 1.0)])}}")\n')
                new_source.append(f'print(f"   Adequate (> 1.0): {{len(location_analysis[location_analysis[\'Schools_per_1000\'] >= 1.0])}}")\n')
                new_source.append('\n')
                new_source.append('print("\\n📊 STATISTICS:")\n')
                new_source.append('print(location_analysis[\'Schools_per_1000\'].describe())\n')
                new_source.append('\n')
                new_source.append('print("\\n📊 TOP 10 LOCATIONS BY Schools_per_1000 (highest density):")\n')
                new_source.append('print(location_analysis.nlargest(10, \'Schools_per_1000\')[[\'Location\', \'School_Count\', \'School_Age_Pop\', \'Schools_per_1000\']].to_string(index=False))\n')
                new_source.append('\n')
                new_source.append('print("\\n📊 BOTTOM 10 LOCATIONS BY Schools_per_1000 (lowest density - EDUCATION DESERTS):")\n')
                new_source.append('print(location_analysis.nsmallest(10, \'Schools_per_1000\')[[\'Location\', \'School_Count\', \'School_Age_Pop\', \'Schools_per_1000\']].to_string(index=False))\n')
                new_source.append('\n')
                new_source.append('# Check population data quality\n')
                new_source.append('print("\\n📊 POPULATION DATA QUALITY:")\n')
                new_source.append(f'print(f"   Locations with actual census population: {{(location_analysis[\'School_Age_Pop\'] > 0).sum()}}")\n')
                new_source.append(f'print(f"   Locations with missing/zero population: {{(location_analysis[\'School_Age_Pop\'] == 0).sum()}}")\n')
                new_source.append('if (location_analysis[\'School_Age_Pop\'] == 0).sum() > 0:\n')
                new_source.append('    print(f"   ⚠️  WARNING: {len(location_analysis[location_analysis[\'School_Age_Pop\'] == 0])} locations have zero population - these may need investigation")\n')
                new_source.append('\n')
            
            new_source.append(line)
            
            # Update color function
            if 'def get_color(schools_per_1000):' in line:
                # Find where this function ends and update it
                func_end = j
                for k in range(j+1, len(source_lines)):
                    if source_lines[k].strip() and not source_lines[k].strip().startswith(' ') and not source_lines[k].strip().startswith('\t'):
                        func_end = k
                        break
                
                # Replace the function
                new_source = new_source[:-1]  # Remove the def line we just added
                new_source.append('def get_color(schools_per_1000):\n')
                new_source.append('    """Color coding based on Schools_per_1000 - ADJUSTED THRESHOLDS"""\n')
                new_source.append('    if pd.isna(schools_per_1000) or schools_per_1000 == 0:\n')
                new_source.append('        return \'gray\'  # No data\n')
                new_source.append('    elif schools_per_1000 < 0.5:\n')
                new_source.append('        return \'red\'  # Critical - Education desert (< 0.5 per 1000)\n')
                new_source.append('    elif schools_per_1000 < 1.0:\n')
                new_source.append('        return \'orange\'  # Moderate need (0.5-1.0 per 1000)\n')
                new_source.append('    elif schools_per_1000 < 2.0:\n')
                new_source.append('        return \'yellow\'  # Adequate but could improve (1.0-2.0 per 1000)\n')
                new_source.append('    else:\n')
                new_source.append('        return \'green\'  # Good coverage (> 2.0 per 1000)\n')
                
                # Skip the old function lines
                for k in range(j+1, func_end):
                    pass  # Skip old function body
                continue
            
            # Update legend
            if '< 0.5 (Desert)' in line or '< 0.5 (Desert)</p>' in line:
                # Update legend HTML
                legend_start = None
                for k in range(max(0, j-10), j):
                    if 'legend_html' in source_lines[k]:
                        legend_start = k
                        break
                
                if legend_start:
                    # Find legend end
                    legend_end = j
                    for k in range(j, min(len(source_lines), j+20)):
                        if '</div>' in source_lines[k] and '''' in source_lines[k]:
                            legend_end = k
                            break
                    
                    # Replace legend
                    new_source = new_source[:legend_start]
                    new_source.append('legend_html = \'\'\'\n')
                    new_source.append('<div style="position: fixed; bottom: 50px; right: 50px; width: 220px; height: 160px; \n')
                    new_source.append('            background-color: white; border:2px solid grey; z-index:9999; font-size:14px;\n')
                    new_source.append('            padding: 10px">\n')
                    new_source.append('<p><b>Schools per 1000 Children</b></p>\n')
                    new_source.append('<p><i class="fa fa-circle" style="color:red"></i> &lt; 0.5 (Critical Desert)</p>\n')
                    new_source.append('<p><i class="fa fa-circle" style="color:orange"></i> 0.5-1.0 (Moderate Need)</p>\n')
                    new_source.append('<p><i class="fa fa-circle" style="color:yellow"></i> 1.0-2.0 (Adequate)</p>\n')
                    new_source.append('<p><i class="fa fa-circle" style="color:green"></i> &gt; 2.0 (Good Coverage)</p>\n')
                    new_source.append('</div>\n')
                    new_source.append('\'\'\'\n')
                    
                    # Skip old legend lines
                    for k in range(legend_start+1, legend_end+1):
                        pass
                    continue
        
        cell['source'] = new_source
        print(f"✅ Updated cell {i} with diagnostics and adjusted thresholds")
        break

# Save
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("✅ Notebook updated!")




