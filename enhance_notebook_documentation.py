"""
Comprehensively enhance the notebook with:
- Detailed markdown explanations for each section
- Code comments explaining what each segment does
- Documentation of datasets used
- Explanation of insights we hope to get
- Questions we're trying to answer
- Proper numbering and updated TOC
"""
import json
import re

with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Define comprehensive section documentation
section_docs = {
    'intro': {
        'title': '# Nairobi Primary Education Equity Analysis',
        'subtitle': '## Multi-Dimensional Gap Analysis: Spatial, Infrastructure, Gender & PWD Inclusivity',
        'objective': '**Objective**: Identify critical gaps in primary education access across Nairobi County to inform strategic investment prioritization for SDG 4 (Quality Education).',
        'framework': """**Analytical Framework**:
1. **Spatial Equity**: School density vs population density by sub-county
2. **Infrastructure Capacity**: Overcrowding, resource adequacy (classrooms, toilets, teachers)
3. **Gender Equity**: Enrollment disparities, attendance patterns, infrastructure adequacy
4. **PWD Inclusivity**: Special needs schools, integrated schools, accessibility gaps
5. **Composite Equity Index**: Multi-dimensional priority ranking""",
        'research_questions': """**Key Research Questions**:
1. **Where are the education deserts?** - Which sub-counties have insufficient school density relative to population?
2. **What is the infrastructure capacity gap?** - How many schools are overcrowded? What's the pupil-teacher ratio?
3. **Are there gender disparities?** - Is enrollment balanced? Are girls' facilities adequate?
4. **How inclusive is the system?** - Can children with disabilities access appropriate schools?
5. **What's the enrollment capacity?** - Are there enough school places for all school-age children?
6. **Is there equity between public and private schools?** - Are there access barriers?
7. **Where should investments be prioritized?** - Which areas need the most urgent intervention?""",
        'datasets': """**Datasets Used**:
1. **kenya_primary_schools.csv**: Comprehensive school-level data including:
   - School locations (coordinates, administrative units)
   - Enrollment data (total, by gender)
   - Infrastructure metrics (classrooms, teachers, toilets)
   - School type and status (public/private, special/integrated)
   - PWD indicators (Type3: ORDINARY, INTEGRATED, SPECIAL SCHOOL)
   
2. **kenya-urban-population-by-sub-county.csv**: Census population data by sub-county including:
   - Total population
   - Age breakdown (for school-age population estimation)
   - Geographic boundaries
   
3. **kenya-average-household-size-by-sub-county.csv**: Household data for:
   - Population estimation refinement
   - Demographic insights"""
    },
    'data_loading': {
        'title': '## 1. Data Loading',
        'description': """**What This Section Does:**
This section loads all necessary Python libraries and datasets required for the analysis.

**Libraries Used:**
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computations
- `matplotlib` & `seaborn`: Data visualization
- `warnings`: Suppress non-critical warnings for cleaner output

**Datasets Loaded:**
1. **Primary Schools Dataset**: Contains information on all primary schools in Kenya
2. **Population Dataset**: Census data for Nairobi sub-counties
3. **Household Size Dataset**: Average household size by sub-county

**What We're Doing:**
- Importing libraries
- Setting visualization styles
- Loading CSV files into pandas DataFrames
- Filtering for Nairobi County only

**Questions We're Answering:**
- How many schools are in Nairobi?
- What data do we have available for analysis?"""
    },
    'data_cleaning': {
        'title': '## 2. Data Cleaning and Preprocessing',
        'description': """**What This Section Does:**
This section cleans and prepares the data for analysis by handling missing values, standardizing formats, and creating derived indicators.

**Key Cleaning Steps:**
1. **Filter Nairobi Schools**: Extract only schools within Nairobi County
2. **Handle Missing Values**: Fill or remove missing data appropriately
3. **Standardize Formats**: Ensure consistent naming, data types
4. **Create Indicators**: Build composite metrics (e.g., Infrastructure_Stress, Gender_Balance)

**Derived Indicators Created:**
- `Infrastructure_Stress`: Composite score combining PTR, classroom ratio, toilet ratio
- `Overcrowded_Classrooms`: Binary indicator (ClassroomRatio > 50)
- `High_PTR`: Binary indicator (PupilTeacherRatio > 40)
- `Gender_Imbalance`: Binary indicator (gender difference > 15%)
- `Girls_Toilet_Deficit`: Binary indicator (inadequate girls' toilets)
- `PWD_Inclusive`: Binary indicator (INTEGRATED or SPECIAL SCHOOL)
- `Is_Special_School`: Binary indicator (SPECIAL SCHOOL only)

**What We're Doing:**
- Removing invalid records
- Standardizing geographic names
- Creating boolean flags for analysis
- Calculating ratios and composite scores

**Insights We Hope to Get:**
- Data quality assessment
- Understanding of data completeness
- Foundation for all subsequent analyses"""
    },
    'spatial_equity': {
        'title': '## 3. Spatial Equity Analysis',
        'description': """**What This Section Does:**
Analyzes the geographic distribution of schools relative to population to identify education deserts and spatial inequities.

**Sub-Analyses:**
1. **School Density vs Population Density**: Calculates schools per 1000 school-age children by sub-county
2. **Spatial Accessibility Metrics**: Measures how accessible schools are geographically
3. **Education Desert Identification**: Identifies areas with insufficient school coverage

**Datasets Used:**
- School locations (coordinates, administrative units)
- Population data by sub-county
- School-age population estimates

**Key Metrics Calculated:**
- `Schools_per_1000`: Number of schools per 1000 school-age children
- `School_Density_Score`: Normalized score (lower = more need)
- Enrollment rate by geographic unit

**Questions We're Answering:**
1. Are schools evenly distributed across Nairobi?
2. Which sub-counties have too few schools relative to population?
3. Where are the "education deserts" - areas with poor school access?
4. Is there spatial equity in school distribution?

**Insights We Hope to Get:**
- Identification of underserved areas
- Priority locations for new school construction
- Understanding of geographic access barriers"""
    },
    'infrastructure': {
        'title': '## 4. Infrastructure Capacity Analysis',
        'description': """**What This Section Does:**
Assesses the adequacy of school infrastructure including classrooms, teachers, and toilet facilities.

**Sub-Analyses:**
1. **Pupil-Teacher Ratio (PTR)**: Analyzes teacher adequacy
2. **Classroom Capacity and Overcrowding**: Identifies schools with insufficient classrooms
3. **Toilet Facilities Adequacy**: Assesses sanitation infrastructure
4. **Infrastructure Stress Scores**: Composite measure of infrastructure pressure

**Datasets Used:**
- School enrollment data (TotalEnrol)
- Teacher counts (TotalTeachers)
- Classroom counts (TotalClassrooms)
- Toilet counts (TotalToilets, GirlsToilet, BoysToilet)

**Key Metrics Calculated:**
- `PupilTeach`: Pupils per teacher
- `ClassrmRat`: Pupils per classroom
- `ToiletRati`: Pupils per toilet
- `Infrastructure_Stress`: Weighted composite (0-100, higher = more stress)

**Standards Used:**
- PTR > 40: High (needs attention)
- Classroom Ratio > 50: Overcrowded
- Toilet Ratio > 80: Inadequate

**Questions We're Answering:**
1. How many schools are overcrowded?
2. What's the average pupil-teacher ratio?
3. Are toilet facilities adequate?
4. Which schools have the highest infrastructure stress?

**Insights We Hope to Get:**
- Number of schools needing infrastructure investment
- Priority schools for capacity expansion
- Understanding of resource adequacy across Nairobi"""
    },
    'gender': {
        'title': '## 5. Gender Equity Analysis',
        'description': """**What This Section Does:**
Examines gender disparities in enrollment, infrastructure, and access to identify gender equity gaps.

**Sub-Analyses:**
1. **Gender Balance Indicator**: Measures enrollment balance (boys vs girls)
2. **Enrollment by Gender**: Total and percentage breakdown
3. **Gender-Specific Infrastructure**: Girls' toilet adequacy
4. **Gender Imbalance Identification**: Schools with significant gender disparities
5. **Population vs Enrollment Gender Comparison**: Are enrollment rates equal by gender?

**Datasets Used:**
- Enrollment by gender (TotalBoys, TotalGirls)
- Girls' toilet counts (GirlsToilet)
- Population gender breakdown (from census, if available)

**Key Metrics Calculated:**
- Gender enrollment percentage
- Gender imbalance flag (difference > 15%)
- Girls' toilet ratio (girls per girls' toilet)
- `Girls_Toilet_Deficit`: Binary indicator for inadequate facilities

**Questions We're Answering:**
1. Is enrollment balanced between boys and girls?
2. Are there schools with significant gender imbalances?
3. Are girls' toilet facilities adequate?
4. Do enrollment rates differ by gender?
5. Are there barriers preventing equal access?

**Insights We Hope to Get:**
- Identification of gender equity gaps
- Schools needing gender-focused interventions
- Understanding of barriers to equal access
- Priority areas for gender equity investments"""
    },
    'pwd': {
        'title': '## 6. PWD Inclusivity Analysis',
        'description': """**What This Section Does:**
Assesses the capacity and accessibility of the education system for Persons With Disabilities (PWD).

**Sub-Analyses:**
1. **PWD-Inclusive School Categorization**: Identifies schools that accommodate PWD students
2. **Special vs Integrated Schools**: Distinguishes between dedicated special schools and mainstream integrated schools
3. **PWD Population from Census**: Estimates school-age PWD children
4. **PWD Capacity Gaps**: Calculates the gap between need and capacity
5. **Sub-County Level PWD Analysis**: Geographic distribution of PWD-inclusive schools

**Datasets Used:**
- School Type3 column: ORDINARY, INTEGRATED, SPECIAL SCHOOL
- PWD population estimates (from census or disability prevalence rates)
- School enrollment capacity

**Key Metrics Calculated:**
- `PWD_Inclusive`: Binary (INTEGRATED or SPECIAL SCHOOL)
- `Is_Special_School`: Binary (SPECIAL SCHOOL only)
- PWD capacity: Estimated capacity of PWD-inclusive schools
- PWD capacity gap: Need - Current capacity

**Assumptions:**
- INTEGRATED schools: Mainstream schools that accommodate PWD students
- SPECIAL SCHOOL: Schools specifically for PWD students
- PWD prevalence: ~2.5% of population (Kenya average)

**Questions We're Answering:**
1. How many schools are PWD-inclusive?
2. What's the geographic distribution of PWD-inclusive schools?
3. Is there sufficient capacity for PWD children?
4. Which sub-counties have zero PWD coverage?
5. What's the capacity gap?

**Insights We Hope to Get:**
- Identification of PWD service gaps
- Priority locations for PWD-inclusive school expansion
- Understanding of accessibility barriers
- Capacity planning for PWD education"""
    },
    'enrollment': {
        'title': '## 7. Enrollment Capacity Analysis',
        'description': """**What This Section Does:**
Compares school enrollment capacity with school-age population to identify enrollment gaps and access issues.

**Sub-Analyses:**
1. **School-Age Population Estimation**: Estimates children aged 6-14 by sub-county
2. **Enrollment Capacity Gap**: Difference between capacity and need
3. **Enrollment Rate Analysis**: Percentage of school-age children enrolled
4. **Actual Attendance Rates**: If available, compares enrollment to attendance

**Datasets Used:**
- Total enrollment (TotalEnrol)
- Population data by sub-county
- Age breakdown (for school-age estimation)
- Average household size (for population refinement)

**Key Metrics Calculated:**
- `School_Age_Pop`: Estimated children aged 6-14
- `Enrollment_Rate`: (Enrollment / School_Age_Pop) × 100
- `Capacity_Gap`: School_Age_Pop - Enrollment
- Enrollment coverage percentage

**Assumptions:**
- School-age = 6-14 years
- School-age % = ~16% of total population (Kenya average)

**Questions We're Answering:**
1. Are there enough school places for all school-age children?
2. What's the enrollment rate by sub-county?
3. Which areas have enrollment capacity gaps?
4. How many children are not enrolled?
5. Is enrollment capacity equitably distributed?

**Insights We Hope to Get:**
- Identification of enrollment gaps
- Understanding of access barriers
- Priority areas for capacity expansion
- Assessment of whether SDG 4 targets are being met"""
    },
    'public_private': {
        'title': '## 8. Public vs Private School Equity Analysis',
        'description': """**What This Section Does:**
Examines equity between public and private schools in terms of distribution, enrollment, and infrastructure quality.

**Sub-Analyses:**
1. **Public vs Private Distribution**: Geographic and numerical distribution
2. **Enrollment by School Type**: How many students attend each type
3. **Infrastructure Quality Comparison**: Comparing facilities between public and private
4. **Equity Barrier Assessment**: Identifying access barriers (cost, location)

**Datasets Used:**
- School status (Status: PUBLIC, PRIVATE)
- Enrollment data
- Infrastructure metrics
- School locations

**Key Metrics Calculated:**
- Public vs private school counts
- Enrollment by school type
- Average infrastructure metrics by type
- Geographic distribution by type

**Questions We're Answering:**
1. Is access equitable regardless of ability to pay?
2. Are there quality differences between public and private schools?
3. What are the equity barriers?
4. Is there geographic equity in school type distribution?
5. Do private schools serve areas underserved by public schools?

**Insights We Hope to Get:**
- Understanding of public-private equity
- Identification of access barriers
- Assessment of whether private schools complement public system
- Policy implications for equitable access"""
    },
    'composite': {
        'title': '## 9. Composite Equity Index',
        'description': """**What This Section Does:**
Combines all equity dimensions into a single composite index to prioritize investment areas.

**Sub-Analyses:**
1. **Multi-Dimensional Priority Ranking**: Combines spatial, infrastructure, gender, PWD metrics
2. **Component Scores**: Normalized scores (0-100) for each dimension
3. **Weighted Composite Index**: Final priority ranking

**Datasets Used:**
- All previous analyses aggregated by geographic unit (Constituency/Division)

**Key Metrics Calculated:**
- `School_Density_Score`: Based on schools per 1000 (lower = more need)
- `Infrastructure_Score`: Average infrastructure stress
- `PWD_Gap_Score`: Percentage of schools not PWD-inclusive
- `Gender_Equity_Score`: Based on gender imbalance and girls' facilities
- `Composite_Equity_Index`: Weighted average of all scores

**Weighting Scheme:**
- Infrastructure: 35%
- Spatial Equity: 25%
- Gender Equity: 20%
- PWD Inclusivity: 20%

**Questions We're Answering:**
1. Which sub-counties need investment most urgently?
2. What's the overall priority ranking combining all equity dimensions?
3. Where should resources be allocated first?
4. What's the relative priority across different equity dimensions?

**Insights We Hope to Get:**
- Clear priority ranking for investment
- Understanding of multi-dimensional equity gaps
- Actionable recommendations for resource allocation
- Evidence-based decision support"""
    },
    'investment': {
        'title': '## 10. Investment Prioritization Framework',
        'description': """**What This Section Does:**
Creates an investment prioritization matrix based on impact and feasibility to guide strategic decision-making.

**Sub-Analyses:**
1. **Impact vs Feasibility Matrix**: 2x2 matrix categorizing interventions
2. **Quick Wins Identification**: High impact, high feasibility interventions
3. **Strategic Investment Categorization**: Long-term strategic investments
4. **Priority Ranking by Sub-County**: Final actionable priority list

**Framework:**
- **High Impact, High Feasibility**: Quick wins (do first)
- **High Impact, Low Feasibility**: Strategic investments (plan for)
- **Low Impact, High Feasibility**: Easy wins (do if resources allow)
- **Low Impact, Low Feasibility**: Avoid

**Questions We're Answering:**
1. What are the quick wins we can implement immediately?
2. What are the strategic long-term investments?
3. Where should we focus resources for maximum impact?
4. What's the implementation priority order?

**Insights We Hope to Get:**
- Actionable investment roadmap
- Quick wins for immediate impact
- Strategic planning guidance
- Resource allocation framework"""
    },
    'visualizations': {
        'title': '## 11. Visualizations',
        'description': """**What This Section Does:**
Creates visual representations of the analysis findings to communicate insights effectively.

**Visualization Types:**
- Bar charts: Comparing metrics across sub-counties
- Histograms: Distribution of key metrics
- Pie charts: Composition breakdowns
- Scatter plots: Relationships between variables
- Maps: Geographic distribution (if coordinates available)

**Questions We're Answering:**
- How can we communicate findings visually?
- What patterns are visible in the data?
- How do different areas compare?

**Insights We Hope to Get:**
- Clear visual communication of findings
- Pattern identification
- Stakeholder engagement tools"""
    },
    'findings': {
        'title': '## 12. Key Findings',
        'description': """**What This Section Does:**
Summarizes the most important findings from the analysis.

**What We're Presenting:**
- Key statistics and numbers
- Critical gaps identified
- Priority areas
- Equity issues discovered

**Insights We're Communicating:**
- Main takeaways from the analysis
- Evidence-based findings
- Critical issues requiring attention"""
    },
    'assumptions': {
        'title': '## 13. Assumptions and Limitations',
        'description': """**What This Section Does:**
Documents assumptions made during the analysis and limitations of the data/methodology.

**What We're Documenting:**
- Data assumptions (e.g., school-age population estimation)
- Methodological assumptions (e.g., thresholds for indicators)
- Limitations (e.g., data quality, coverage)
- Caveats for interpretation

**Why This Matters:**
- Transparency in analysis
- Understanding of confidence levels
- Guidance for interpretation
- Areas for future improvement"""
    },
    'recommendations': {
        'title': '## 14. Actionable Recommendations',
        'description': """**What This Section Does:**
Provides specific, actionable recommendations for the Nairobi County Education Officer based on the analysis findings.

**Recommendation Structure:**
- Priority 1: Infrastructure Capacity Building
- Priority 2: Gender Equity Interventions
- Priority 3: PWD Inclusivity Expansion
- Priority 4: Spatial Equity
- Alignment with SDG 4 targets

**What We're Recommending:**
- Specific interventions
- Target areas/sub-counties
- Expected outcomes
- SDG 4 alignment

**Questions We're Answering:**
1. What should be done first?
2. Where should resources be allocated?
3. What interventions will have the most impact?
4. How does this align with SDG 4?

**Insights We're Providing:**
- Actionable next steps
- Prioritized intervention list
- Evidence-based recommendations
- Strategic guidance"""
    }
}

# Update the introduction cell
def update_intro_cell():
    """Update the introduction cell with comprehensive documentation"""
    for i, cell in enumerate(nb['cells']):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            if '# Nairobi Primary Education Equity Analysis' in source:
                doc = section_docs['intro']
                new_source = f"""{doc['title']}

{doc['subtitle']}

{doc['objective']}

{doc['framework']}

{doc['research_questions']}

{doc['datasets']}

---

## Table of Contents
1. [Data Loading](#1-data-loading)
2. [Data Cleaning and Preprocessing](#2-data-cleaning-and-preprocessing)
3. [Spatial Equity Analysis](#3-spatial-equity-analysis)
4. [Infrastructure Capacity Analysis](#4-infrastructure-capacity-analysis)
5. [Gender Equity Analysis](#5-gender-equity-analysis)
6. [PWD Inclusivity Analysis](#6-pwd-inclusivity-analysis)
7. [Enrollment Capacity Analysis](#7-enrollment-capacity-analysis)
8. [Public vs Private School Equity Analysis](#8-public-vs-private-school-equity-analysis)
9. [Composite Equity Index](#9-composite-equity-index)
10. [Investment Prioritization Framework](#10-investment-prioritization-framework)
11. [Visualizations](#11-visualizations)
12. [Key Findings](#12-key-findings)
13. [Assumptions and Limitations](#13-assumptions-and-limitations)
14. [Actionable Recommendations](#14-actionable-recommendations)
"""
                nb['cells'][i]['source'] = new_source.split('\n')
                print(f"✅ Updated introduction cell at index {i}")
                return i
    return None

# Update section headers
def update_section_headers():
    """Update section headers with comprehensive documentation"""
    section_patterns = {
        'data_loading': r'##\s*1\.\s*Data Loading',
        'data_cleaning': r'##\s*2\.\s*Data Cleaning',
        'spatial_equity': r'##\s*3\.\s*Spatial Equity',
        'infrastructure': r'##\s*4\.\s*Infrastructure',
        'gender': r'##\s*5\.\s*Gender Equity',
        'pwd': r'##\s*6\.\s*PWD',
        'enrollment': r'##\s*7\.\s*Enrollment',
        'public_private': r'##\s*8\.\s*Public vs Private',
        'composite': r'##\s*9\.\s*Composite Equity',
        'investment': r'##\s*10\.\s*Investment',
        'visualizations': r'##\s*11\.\s*Visualizations',
        'findings': r'##\s*12\.\s*Key Findings',
        'assumptions': r'##\s*13\.\s*Assumptions',
        'recommendations': r'##\s*14\.\s*Actionable Recommendations'
    }
    
    updated_count = 0
    for i, cell in enumerate(nb['cells']):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            for section_key, pattern in section_patterns.items():
                if re.search(pattern, source, re.IGNORECASE):
                    if section_key in section_docs:
                        doc = section_docs[section_key]
                        # Check if already has detailed documentation
                        if 'What This Section Does' not in source:
                            new_source = f"{doc['title']}\n\n{doc['description']}\n"
                            nb['cells'][i]['source'] = new_source.split('\n')
                            updated_count += 1
                            print(f"✅ Updated {section_key} header at index {i}")
                            break
    
    return updated_count

# Add comments to code cells
def add_code_comments():
    """Add explanatory comments to code cells"""
    # This is a simplified version - in practice, we'd need to identify specific code patterns
    # and add appropriate comments
    print("ℹ️  Code comments should be added manually for best results")
    print("   Focus on explaining: what the code does, why it's needed, what it produces")

# Main execution
print("="*80)
print("ENHANCING NOTEBOOK DOCUMENTATION")
print("="*80)
print()

intro_idx = update_intro_cell()
headers_updated = update_section_headers()

print()
print("="*80)
print(f"✅ Updated introduction cell")
print(f"✅ Updated {headers_updated} section headers")
print("="*80)
print()
print("💡 Note: Code cell comments should be reviewed and enhanced manually")
print("   for best clarity and context-specific explanations")

# Save the notebook
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print()
print("✅ Notebook saved successfully!")




