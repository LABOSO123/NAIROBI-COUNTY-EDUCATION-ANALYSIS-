"""
Compare different notebook versions to show changes over time.
This script analyzes all .ipynb files and shows their structure and differences.
"""

import json
import os
from pathlib import Path
from datetime import datetime

def get_notebook_info(filepath):
    """Extract key information from a notebook file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        # Get file modification time
        mtime = os.path.getmtime(filepath)
        mod_time = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
        
        # Count cells by type
        cells = nb.get('cells', [])
        code_cells = sum(1 for c in cells if c.get('cell_type') == 'code')
        markdown_cells = sum(1 for c in cells if c.get('cell_type') == 'markdown')
        
        # Extract cell sources (first 100 chars) to identify sections
        sections = []
        for cell in cells:
            if cell.get('cell_type') == 'markdown':
                source = ''.join(cell.get('source', []))
                if source.strip():
                    # Get first line or heading
                    first_line = source.strip().split('\n')[0]
                    if first_line.startswith('#'):
                        sections.append(first_line[:80])
        
        return {
            'file': os.path.basename(filepath),
            'modified': mod_time,
            'total_cells': len(cells),
            'code_cells': code_cells,
            'markdown_cells': markdown_cells,
            'sections': sections[:20]  # First 20 sections
        }
    except Exception as e:
        return {
            'file': os.path.basename(filepath),
            'error': str(e)
        }

def compare_notebooks():
    """Compare all notebook files in the current directory."""
    notebooks = [
        'analysis.ipynb',
        'analysis - New Version.ipynb',
        'analysis - HUHHH.ipynb',
        'nairobi-education-analysis.ipynb'
    ]
    
    print("=" * 80)
    print("NOTEBOOK VERSION COMPARISON")
    print("=" * 80)
    print()
    
    results = []
    for nb_file in notebooks:
        if os.path.exists(nb_file):
            info = get_notebook_info(nb_file)
            results.append(info)
        else:
            print(f"⚠️  {nb_file} not found")
    
    # Sort by modification time (oldest first)
    results.sort(key=lambda x: x.get('modified', ''))
    
    print("\n📊 NOTEBOOK SUMMARY (Oldest to Newest):")
    print("-" * 80)
    for i, info in enumerate(results, 1):
        if 'error' in info:
            print(f"\n{i}. {info['file']}")
            print(f"   ❌ Error: {info['error']}")
        else:
            print(f"\n{i}. {info['file']}")
            print(f"   📅 Modified: {info['modified']}")
            print(f"   📝 Total Cells: {info['total_cells']}")
            print(f"   💻 Code Cells: {info['code_cells']}")
            print(f"   📄 Markdown Cells: {info['markdown_cells']}")
            if info['sections']:
                print(f"   📑 Key Sections:")
                for section in info['sections'][:10]:
                    print(f"      - {section}")
    
    # Show differences between current and previous versions
    if len(results) >= 2:
        print("\n" + "=" * 80)
        print("🔍 CHANGES OVER TIME:")
        print("=" * 80)
        
        current = results[-1]
        previous = results[-2]
        
        print(f"\n📈 Growth from '{previous['file']}' to '{current['file']}':")
        print(f"   Cells: {previous['total_cells']} → {current['total_cells']} "
              f"(+{current['total_cells'] - previous['total_cells']})")
        print(f"   Code: {previous['code_cells']} → {current['code_cells']} "
              f"(+{current['code_cells'] - previous['code_cells']})")
        print(f"   Markdown: {previous['markdown_cells']} → {current['markdown_cells']} "
              f"(+{current['markdown_cells'] - previous['markdown_cells']})")
    
    print("\n" + "=" * 80)
    print("💡 TIP: To see detailed changes, initialize git and use 'git diff'")
    print("=" * 80)

if __name__ == '__main__':
    compare_notebooks()




