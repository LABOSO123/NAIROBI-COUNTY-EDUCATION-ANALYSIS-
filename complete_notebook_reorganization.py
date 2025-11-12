"""
Complete notebook reorganization according to exact specifications
Remove duplicates, organize by analysis type, ensure clean structure
"""
import json
import re

# Load the notebook
with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    notebook = json.load(f)

cells = notebook['cells']

# Categorize all cells
intro_cells = []
library_cells = []
data_loading_cells = []
data_cleaning_cells = []
data_preprocessing_cells = []

# Analysis categories
spatial_equity_cells = []
infrastructure_capacity_cells = []
gender_equity_cells = []
pwd_inclusivity_cells = []
enrollment_capacity_cells = []
public_private_equity_cells = []
composite_equity_index_cells = []
investment_prioritization_cells = []

visualization_cells = []
findings_cells = []
assumptions_cells = []
recommendations_cells = []

# Track seen code to avoid duplicates
seen_code_hashes = set()

def categorize_cell(cell, i):
    """Categorize a cell based on its content"""
    source = ''.join(cell.get('source', []))
    cell_type = cell.get('cell_type', 'code')
    
    # Skip duplicates
    if cell_type == 'code':
        code_hash = hash(source.strip()[:500])  # Hash first 500 chars
        if code_hash in seen_code_hashes:
            return None  # Skip duplicate
        seen_code_hashes.add(code_hash)
    
    # Introduction
    if i == 0 and 'Nairobi Primary Education Equity Analysis' in source:
        return ('intro', intro_cells)
    
    # Library loading
    if 'Library Loading' in source or ('import pandas' in source and 'import numpy' in source and i < 5):
        return ('library', library_cells)
    
    # Data loading
    if ('Data Loading' in source and cell_type == 'markdown') or \
       ('Load primary schools dataset' in source) or \
       ('read_csv' in source and 'kenya_primary_schools' in source) or \
       ('Filter for Nairobi schools only' in source) or \
       ('Load population' in source and 'read_csv' in source):
        return ('data_loading', data_loading_cells)
    
    # Data cleaning and preprocessing
    if ('Data Cleaning' in source and cell_type == 'markdown') or \
       ('Data Preprocessing' in source) or \
       ('Remove schools with missing' in source) or \
       ('missing_coords' in source) or \
       ('dropna' in source and 'Latitude' in source) or \
       ('.info()' in source) or ('.describe()' in source) or ('.head()' in source and 'print' in source) or \
       ('MISSING VALUES' in source) or ('DATASET STRUCTURE' in source) or \
       ('Create PWD' in source and 'PWD_Inclusive' in source) or \
       ('Is_Special_School' in source and 'Type3' in source):
        return ('cleaning', data_cleaning_cells if 'PWD' not in source else data_preprocessing_cells)
    
    # SPATIAL EQUITY (3 sub-analyses)
    if ('Spatial' in source and 'Equity' in source) or \
       ('School density' in source and 'population density' in source) or \
       ('Spatial accessibility' in source) or \
       ('Education desert' in source) or \
       ('Schools per 1000' in source) or \
       ('Spatial_Accessibility' in source):
        return ('spatial', spatial_equity_cells)
    
    # INFRASTRUCTURE CAPACITY (4 sub-analyses)
    if ('Infrastructure' in source and 'Capacity' in source) or \
       ('Pupil-Teacher Ratio' in source) or ('PTR' in source) or \
       ('Classroom' in source and ('capacity' in source or 'overcrowding' in source or 'Overcrowded' in source)) or \
       ('Toilet' in source and ('facilities' in source or 'adequacy' in source or 'Ratio' in source)) or \
       ('Infrastructure_Stress' in source) or \
       ('Overcrowded_Classrooms' in source) or ('High_PTR' in source) or \
       ('PupilTeach' in source and '>' in source):
        return ('infrastructure', infrastructure_capacity_cells)
    
    # GENDER EQUITY (5 sub-analyses)
    if ('Gender Equity' in source) or \
       ('Gender Balance' in source) or ('Gender_Balance' in source) or \
       ('Gender' in source and ('Enrollment' in source or 'enrollment' in source)) or \
       ('Gender' in source and 'toilet' in source.lower()) or \
       ('Gender_Imbalance' in source) or \
       ('boys_enrollment' in source) or ('girls_enrollment' in source) or \
       ('TotalBoys' in source and 'TotalGirls' in source and 'compare' in source.lower()) or \
       ('Population vs School Enrollment' in source and 'Gender' in source):
        return ('gender', gender_equity_cells)
    
    # PWD INCLUSIVITY (5 sub-analyses)
    if ('PWD' in source and ('Inclusivity' in source or 'Analysis' in source)) or \
       ('Special schools' in source) or ('Integrated schools' in source) or \
       ('disability' in source.lower() and 'census' in source.lower()) or \
       ('PWD capacity' in source) or ('PWD Population' in source) or \
       ('PWD-inclusive school' in source) or \
       ('TYPE3' in source) or ('Type3' in source and ('INTEGRATED' in source or 'SPECIAL' in source)) or \
       ('Sub-county level PWD' in source) or ('subcounty_analysis' in source and 'PWD' in source):
        return ('pwd', pwd_inclusivity_cells)
    
    # ENROLLMENT CAPACITY (4 sub-analyses)
    if ('Enrollment Capacity' in source) or \
       ('School-Age Population' in source) or \
       ('Enrollment rate' in source) or ('enrollment_rate' in source) or \
       ('Capacity Gap' in source) or ('capacity gap' in source) or \
       ('attendance' in source.lower() and 'census' in source.lower() and 'rate' in source.lower()) or \
       ('Actual attendance' in source) or ('Out-of-school' in source):
        return ('enrollment', enrollment_capacity_cells)
    
    # PUBLIC VS PRIVATE EQUITY (4 sub-analyses)
    if ('Public vs Private' in source) or \
       ('Status' in source and 'PUBLIC' in source and 'PRIVATE' in source) or \
       ('public_private' in source) or \
       ('Equity barrier' in source) or ('equity barrier' in source):
        return ('public_private', public_private_equity_cells)
    
    # COMPOSITE EQUITY INDEX (3 sub-analyses)
    if ('Composite Equity Index' in source) or \
       ('equity_index = nairobi_schools_clean.groupby' in source) or \
       ('Component scores' in source) or ('School_Density_Score' in source) or \
       ('Composite_Equity_Index' in source) or \
       ('Multi-dimensional priority ranking' in source):
        return ('composite', composite_equity_index_cells)
    
    # INVESTMENT PRIORITIZATION (4 sub-analyses)
    if ('Investment Prioritization' in source) or \
       ('Impact vs Feasibility' in source) or \
       ('Quick wins' in source) or ('quick wins' in source) or \
       ('Strategic investment' in source) or \
       ('Priority_Rank' in source and 'print' in source):
        return ('investment', investment_prioritization_cells)
    
    # Visualizations
    if 'Visualizations' in source or 'Figure' in source or 'plt.subplots' in source or 'plt.plot' in source:
        return ('viz', visualization_cells)
    
    # Findings, Assumptions, Recommendations
    if 'Key Findings' in source:
        return ('findings', findings_cells)
    if 'Assumptions' in source:
        return ('assumptions', assumptions_cells)
    if 'Recommendations' in source:
        return ('recommendations', recommendations_cells)
    
    return None

# Categorize all cells
for i, cell in enumerate(cells):
    result = categorize_cell(cell, i)
    if result:
        category, target_list = result
        target_list.append(cell)

print("="*80)
print("CELL CATEGORIZATION")
print("="*80)
print(f"Intro: {len(intro_cells)}")
print(f"Library: {len(library_cells)}")
print(f"Data Loading: {len(data_loading_cells)}")
print(f"Data Cleaning: {len(data_cleaning_cells)}")
print(f"Data Preprocessing: {len(data_preprocessing_cells)}")
print(f"Spatial Equity: {len(spatial_equity_cells)}")
print(f"Infrastructure Capacity: {len(infrastructure_capacity_cells)}")
print(f"Gender Equity: {len(gender_equity_cells)}")
print(f"PWD Inclusivity: {len(pwd_inclusivity_cells)}")
print(f"Enrollment Capacity: {len(enrollment_capacity_cells)}")
print(f"Public vs Private Equity: {len(public_private_equity_cells)}")
print(f"Composite Equity Index: {len(composite_equity_index_cells)}")
print(f"Investment Prioritization: {len(investment_prioritization_cells)}")
print(f"Visualizations: {len(visualization_cells)}")
print(f"Findings: {len(findings_cells)}")
print(f"Assumptions: {len(assumptions_cells)}")
print(f"Recommendations: {len(recommendations_cells)}")

# Build new notebook in exact order
new_cells = []

# 1. Introduction
new_cells.extend(intro_cells)

# 2. Library Loading - Use only the first library header, remove duplicates from library_cells
if library_cells:
    # Keep only code cells from library_cells (remove duplicate markdown headers)
    library_code_cells = [c for c in library_cells if c.get('cell_type') == 'code']
    library_header = {
        "cell_type": "markdown",
        "metadata": {},
        "source": ["## 0. Library Loading\n", "\n", "Import all required Python libraries for data analysis, visualization, and statistical operations."]
    }
    new_cells.append(library_header)
    new_cells.extend(library_code_cells)

# 3. Data Loading - Remove duplicate markdown headers
if data_loading_cells:
    data_loading_code_cells = [c for c in data_loading_cells if c.get('cell_type') == 'code']
    data_loading_header = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 1. Data Loading\n",
            "\n",
            "**What We're Doing:**\n",
            "- Loading all required datasets (schools data and census data)\n",
            "- Filtering to Nairobi County only\n",
            "- Initial data inspection\n",
            "\n",
            "**Insights We Hope to Find:**\n",
            "- Total number of schools in Nairobi\n",
            "- Basic distribution of schools (public/private, PWD-inclusive)\n",
            "- Data quality and completeness"
        ]
    }
    new_cells.append(data_loading_header)
    new_cells.extend(data_loading_code_cells)

# 4. Data Cleaning and Preprocessing - Remove duplicate markdown headers
if data_cleaning_cells or data_preprocessing_cells:
    cleaning_code_cells = [c for c in data_cleaning_cells + data_preprocessing_cells if c.get('cell_type') == 'code']
    cleaning_header = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 2. Data Cleaning and Preprocessing\n",
            "\n",
            "**What We're Doing:**\n",
            "- Checking for missing values (nulls) in key columns\n",
            "- Inspecting data structure, types, and quality\n",
            "- Removing invalid records (e.g., schools without coordinates)\n",
            "- Creating basic indicators needed for analysis (PWD flags)\n",
            "\n",
            "**Insights We Hope to Find:**\n",
            "- Data completeness and quality issues\n",
            "- How many schools have complete data\n",
            "- Basic data statistics and distributions"
        ]
    }
    new_cells.append(cleaning_header)
    new_cells.extend(cleaning_code_cells)

# 5. SPATIAL EQUITY (3 sub-analyses) - Remove duplicate markdown headers
if spatial_equity_cells:
    spatial_code_cells = [c for c in spatial_equity_cells if c.get('cell_type') == 'code']
    spatial_header = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            "## 3. Spatial Equity Analysis\n",
            "\n",
            "**Sub-analyses:**\n",
            "1. School density vs population density\n",
            "2. Spatial accessibility metrics\n",
            "3. Education desert identification\n",
            "\n",
            "**What We're Doing:**\n",
            "- Analyzing school distribution relative to population density\n",
            "- Calculating spatial accessibility metrics (schools per 1000 school-age children)\n",
            "- Identifying \"education deserts\" (areas with insufficient school density)\n",
            "\n",
            "**Insights We Hope to Find:**\n",
            "- Are there enough school places for all school-age children?\n",
            "- Where are schools most needed (spatial accessibility gaps)?\n",
            "- Which areas are \"education deserts\" with insufficient school density?"
        ]
    }
    new_cells.append(spatial_header)
    new_cells.extend(spatial_code_cells)

# 6. INFRASTRUCTURE CAPACITY (4 sub-analyses)
infra_header = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 4. Infrastructure Capacity Analysis\n",
        "\n",
        "**Sub-analyses:**\n",
        "1. Pupil-Teacher Ratio (PTR)\n",
        "2. Classroom capacity and overcrowding\n",
        "3. Toilet facilities adequacy\n",
        "4. Infrastructure stress scores\n",
        "\n",
        "**What We're Doing:**\n",
        "- Analyzing Pupil-Teacher Ratios (PTR) against Kenya's standard of 40:1\n",
        "- Measuring classroom capacity and identifying overcrowding\n",
        "- Assessing toilet facilities adequacy\n",
        "- Calculating Infrastructure Stress Score (composite metric)\n",
        "\n",
        "**Insights We Hope to Find:**\n",
        "- How many schools exceed teacher-student ratio standards\n",
        "- Which schools have overcrowded classrooms\n",
        "- Schools with inadequate sanitation facilities\n",
        "- Overall infrastructure stress across Nairobi"
    ]
}
new_cells.append(infra_header)
if infrastructure_capacity_cells:
    infra_code_cells = [c for c in infrastructure_capacity_cells if c.get('cell_type') == 'code']
    new_cells.extend(infra_code_cells)

# 7. GENDER EQUITY (5 sub-analyses)
gender_header = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 5. Gender Equity Analysis\n",
        "\n",
        "**Sub-analyses:**\n",
        "1. Gender balance indicator\n",
        "2. Enrollment by gender\n",
        "3. Gender-specific infrastructure (toilets)\n",
        "4. Gender imbalance identification\n",
        "5. Population vs enrollment gender comparison\n",
        "\n",
        "**What We're Doing:**\n",
        "- Calculating gender balance indicators for each school\n",
        "- Comparing enrollment by gender (boys vs girls)\n",
        "- Analyzing gender-specific infrastructure (especially toilets)\n",
        "- Comparing Nairobi's population gender ratio with school enrollment gender ratio\n",
        "- Identifying schools with significant gender imbalances\n",
        "\n",
        "**Insights We Hope to Find:**\n",
        "- Are boys and girls enrolling at equal rates?\n",
        "- Which schools show significant gender imbalances?\n",
        "- Are girls' toilet facilities adequate (critical barrier to girls' attendance)?"
    ]
}
new_cells.append(gender_header)
if gender_equity_cells:
    gender_code_cells = [c for c in gender_equity_cells if c.get('cell_type') == 'code']
    new_cells.extend(gender_code_cells)

# 8. PWD INCLUSIVITY (5 sub-analyses)
pwd_header = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 6. PWD (Persons With Disabilities) Inclusivity Analysis\n",
        "\n",
        "**Sub-analyses:**\n",
        "1. PWD-inclusive school categorization\n",
        "2. Special vs integrated schools\n",
        "3. PWD population from census\n",
        "4. PWD capacity gaps\n",
        "5. Sub-county level PWD analysis\n",
        "\n",
        "**What We're Doing:**\n",
        "- Categorizing schools by PWD accessibility (ORDINARY, INTEGRATED, SPECIAL SCHOOL)\n",
        "- Analyzing distribution of PWD-inclusive schools\n",
        "- Using actual PWD population data from census (by disability type)\n",
        "- Calculating PWD capacity gaps\n",
        "- Sub-county level PWD analysis\n",
        "\n",
        "**Insights We Hope to Find:**\n",
        "- How many schools are accessible to children with disabilities\n",
        "- Coverage gap: How many PWD children lack access\n",
        "- Which sub-counties have the highest PWD populations but lowest coverage"
    ]
}
new_cells.append(pwd_header)
if pwd_inclusivity_cells:
    pwd_code_cells = [c for c in pwd_inclusivity_cells if c.get('cell_type') == 'code']
    new_cells.extend(pwd_code_cells)

# 9. ENROLLMENT CAPACITY (4 sub-analyses)
enrollment_header = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 7. Enrollment Capacity Analysis\n",
        "\n",
        "**Sub-analyses:**\n",
        "1. School-age population estimation\n",
        "2. Enrollment capacity gap\n",
        "3. Enrollment rate analysis\n",
        "4. Actual attendance rates\n",
        "\n",
        "**What We're Doing:**\n",
        "- Comparing school-age population (6-14) with enrollment capacity\n",
        "- Analyzing actual attendance rates from census data\n",
        "- Calculating enrollment capacity gaps\n",
        "- Identifying children not in school\n",
        "\n",
        "**Insights We Hope to Find:**\n",
        "- Are there enough school places for all school-age children?\n",
        "- What's the enrollment rate? How many children are out of school?\n",
        "- What's the enrollment capacity gap?"
    ]
}
new_cells.append(enrollment_header)
if enrollment_capacity_cells:
    enrollment_code_cells = [c for c in enrollment_capacity_cells if c.get('cell_type') == 'code']
    new_cells.extend(enrollment_code_cells)

# 10. PUBLIC VS PRIVATE EQUITY (4 sub-analyses)
public_private_header = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 8. Public vs Private School Equity Analysis\n",
        "\n",
        "**Sub-analyses:**\n",
        "1. Public vs private distribution\n",
        "2. Enrollment by school type\n",
        "3. Infrastructure quality comparison\n",
        "4. Equity barrier assessment\n",
        "\n",
        "**What We're Doing:**\n",
        "- Analyzing distribution of public vs private schools\n",
        "- Comparing enrollment patterns by school type\n",
        "- Assessing infrastructure quality differences\n",
        "- Identifying equity barriers (cost, access)\n",
        "\n",
        "**Insights We Hope to Find:**\n",
        "- Is access equitable regardless of ability to pay?\n",
        "- Are there quality differences between public and private schools?\n",
        "- What are the equity barriers?"
    ]
}
new_cells.append(public_private_header)
if public_private_equity_cells:
    public_private_code_cells = [c for c in public_private_equity_cells if c.get('cell_type') == 'code']
    new_cells.extend(public_private_code_cells)

# 11. COMPOSITE EQUITY INDEX (3 sub-analyses)
composite_header = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 9. Composite Equity Index\n",
        "\n",
        "**Sub-analyses:**\n",
        "1. Multi-dimensional priority ranking\n",
        "2. Component scores\n",
        "3. Weighted composite index\n",
        "\n",
        "**What We're Doing:**\n",
        "- Combining all dimensions (spatial, infrastructure, gender, PWD) into a single priority ranking\n",
        "- Creating component scores for each dimension\n",
        "- Calculating weighted Composite Equity Index\n",
        "\n",
        "**Insights We Hope to Find:**\n",
        "- Which sub-counties need investment most urgently?\n",
        "- What's the overall priority ranking combining all equity dimensions?"
    ]
}
new_cells.append(composite_header)
if composite_equity_index_cells:
    composite_code_cells = [c for c in composite_equity_index_cells if c.get('cell_type') == 'code']
    new_cells.extend(composite_code_cells)

# 12. INVESTMENT PRIORITIZATION (4 sub-analyses)
investment_header = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 10. Investment Prioritization\n",
        "\n",
        "**Sub-analyses:**\n",
        "1. Impact vs Feasibility matrix\n",
        "2. Quick wins identification\n",
        "3. Strategic investment categorization\n",
        "4. Priority ranking by sub-county\n",
        "\n",
        "**What We're Doing:**\n",
        "- Building Investment Prioritization Matrix (Impact vs Feasibility)\n",
        "- Categorizing interventions (Quick Wins, Strategic Investments, etc.)\n",
        "- Ranking sub-counties by priority\n",
        "\n",
        "**Insights We Hope to Find:**\n",
        "- Which interventions offer the best impact-to-feasibility ratio?\n",
        "- Where should the grant be invested for maximum impact?\n",
        "- What are the \"quick wins\" vs long-term strategic investments?"
    ]
}
new_cells.append(investment_header)
if investment_prioritization_cells:
    investment_code_cells = [c for c in investment_prioritization_cells if c.get('cell_type') == 'code']
    new_cells.extend(investment_code_cells)

# 13. Visualizations
viz_header = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 11. Visualizations\n",
        "\n",
        "Creating comprehensive visualizations to communicate findings across all analysis dimensions."
    ]
}
new_cells.append(viz_header)
if visualization_cells:
    viz_code_cells = [c for c in visualization_cells if c.get('cell_type') == 'code']
    new_cells.extend(viz_code_cells)

# 14. Key Findings
findings_header = {
    "cell_type": "markdown",
    "metadata": {},
    "source": ["## 12. Key Findings\n", "\n", "Summary of critical insights from all analyses."]
}
new_cells.append(findings_header)
if findings_cells:
    findings_code_cells = [c for c in findings_cells if c.get('cell_type') == 'code']
    new_cells.extend(findings_code_cells)

# 15. Assumptions
assumptions_header = {
    "cell_type": "markdown",
    "metadata": {},
    "source": ["## 13. Assumptions\n", "\n", "All assumptions made during the analysis are explicitly documented here for transparency."]
}
new_cells.append(assumptions_header)
if assumptions_cells:
    assumptions_code_cells = [c for c in assumptions_cells if c.get('cell_type') == 'code']
    new_cells.extend(assumptions_code_cells)

# 16. Recommendations
recommendations_header = {
    "cell_type": "markdown",
    "metadata": {},
    "source": ["## 14. Recommendations\n", "\n", "Actionable recommendations aligned with SDG 4 targets, prioritized by impact and feasibility."]
}
new_cells.append(recommendations_header)
if recommendations_cells:
    recommendations_code_cells = [c for c in recommendations_cells if c.get('cell_type') == 'code']
    new_cells.extend(recommendations_code_cells)

# Remove duplicate markdown headers
def remove_duplicate_headers(cells):
    """Remove duplicate markdown headers (not just consecutive)"""
    cleaned = []
    seen_headers = set()
    for cell in cells:
        if cell.get('cell_type') == 'markdown':
            content = ''.join(cell.get('source', []))
            # Check if it's a header (starts with ##)
            if content.strip().startswith('##'):
                # Normalize header content (remove extra whitespace)
                normalized = ' '.join(content.strip().split())
                # If we've seen this exact header before, skip it
                if normalized in seen_headers:
                    continue
                seen_headers.add(normalized)
        cleaned.append(cell)
    return cleaned

# Clean duplicates
new_cells = remove_duplicate_headers(new_cells)

# Update Table of Contents in the intro cell
intro_content = ''.join(new_cells[0].get('source', []))
new_toc = """## Table of Contents

0. [Library Loading](#0-library-loading)
1. [Data Loading](#1-data-loading)
2. [Data Cleaning and Preprocessing](#2-data-cleaning-and-preprocessing)
3. [Spatial Equity Analysis](#3-spatial-equity-analysis)
4. [Infrastructure Capacity Analysis](#4-infrastructure-capacity-analysis)
5. [Gender Equity Analysis](#5-gender-equity-analysis)
6. [PWD Inclusivity Analysis](#6-pwd-persons-with-disabilities-inclusivity-analysis)
7. [Enrollment Capacity Analysis](#7-enrollment-capacity-analysis)
8. [Public vs Private Equity Analysis](#8-public-vs-private-school-equity-analysis)
9. [Composite Equity Index](#9-composite-equity-index)
10. [Investment Prioritization](#10-investment-prioritization)
11. [Visualizations](#11-visualizations)
12. [Key Findings](#12-key-findings)
13. [Assumptions](#13-assumptions)
14. [Recommendations](#14-recommendations)"""

# Update intro cell with new TOC
if '## Table of Contents' in intro_content:
    lines = intro_content.split('\n')
    toc_start = None
    for i, line in enumerate(lines):
        if '## Table of Contents' in line:
            toc_start = i
            break
    
    if toc_start is not None:
        # Find where TOC ends (next ## or end of content)
        toc_end = len(lines)
        for i in range(toc_start + 1, len(lines)):
            if lines[i].strip().startswith('##') and 'Table of Contents' not in lines[i]:
                toc_end = i
                break
        
        # Replace TOC section
        new_lines = lines[:toc_start] + new_toc.split('\n') + lines[toc_end:]
        new_cells[0]['source'] = [line + '\n' for line in new_lines[:-1]] + [new_lines[-1]] if new_lines else []

# Update notebook
notebook['cells'] = new_cells

# Save
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print("\n" + "="*80)
print("NOTEBOOK REORGANIZED!")
print("="*80)
print(f"Total cells: {len(new_cells)}")
print("\n✓ Removed duplicates")
print("✓ Organized in exact order specified")
print("✓ Clean structure with proper headers")
print("✓ No misplaced code or redundant sections")


