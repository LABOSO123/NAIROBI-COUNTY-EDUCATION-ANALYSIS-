"""
Comprehensive notebook enhancement:
1. Add detailed markdown to ALL sections
2. Add comments to code cells
3. Ensure proper numbering
4. Update TOC
"""
import json
import re

with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Section documentation mapping
section_info = {
    '1': {'name': 'Data Loading', 'key': 'data_loading'},
    '2': {'name': 'Data Cleaning and Preprocessing', 'key': 'data_cleaning'},
    '3': {'name': 'Spatial Equity Analysis', 'key': 'spatial_equity'},
    '4': {'name': 'Infrastructure Capacity Analysis', 'key': 'infrastructure'},
    '5': {'name': 'Gender Equity Analysis', 'key': 'gender'},
    '6': {'name': 'PWD Inclusivity Analysis', 'key': 'pwd'},
    '7': {'name': 'Enrollment Capacity Analysis', 'key': 'enrollment'},
    '8': {'name': 'Public vs Private School Equity Analysis', 'key': 'public_private'},
    '9': {'name': 'Composite Equity Index', 'key': 'composite'},
    '10': {'name': 'Investment Prioritization Framework', 'key': 'investment'},
    '11': {'name': 'Visualizations', 'key': 'visualizations'},
    '12': {'name': 'Key Findings', 'key': 'findings'},
    '13': {'name': 'Assumptions and Limitations', 'key': 'assumptions'},
    '14': {'name': 'Actionable Recommendations', 'key': 'recommendations'}
}

# Detailed descriptions for each section
descriptions = {
    'data_loading': """**What This Section Does:**
This section loads all necessary Python libraries and datasets required for the analysis.

**Libraries Used:**
- `pandas`: Data manipulation and analysis
- `numpy`: Numerical computations  
- `matplotlib` & `seaborn`: Data visualization
- `warnings`: Suppress non-critical warnings for cleaner output

**Datasets Loaded:**
1. **Primary Schools Dataset** (`kenya_primary_schools.csv`): Contains information on all primary schools in Kenya including:
   - School locations (coordinates, administrative units: District, Division, Location, Constituency)
   - Enrollment data (total, by gender: TotalBoys, TotalGirls)
   - Infrastructure metrics (classrooms, teachers, toilets)
   - School type and status (public/private, special/integrated)
   - PWD indicators (Type3: ORDINARY, INTEGRATED, SPECIAL SCHOOL)

2. **Population Dataset** (`kenya-urban-population-by-sub-county.csv`): Census data for Nairobi sub-counties including:
   - Total population by sub-county
   - Age breakdown (for school-age population estimation)
   - Geographic boundaries

3. **Household Size Dataset** (`kenya-average-household-size-by-sub-county.csv`): Average household size by sub-county for:
   - Population estimation refinement
   - Demographic insights

**What We're Doing:**
- Importing required Python libraries
- Setting visualization styles for consistent, professional plots
- Loading CSV files into pandas DataFrames
- Filtering for Nairobi County only (since analysis focuses on Nairobi)

**Questions We're Answering:**
- How many schools are in Nairobi?
- What data do we have available for analysis?
- What's the structure of our datasets?

**Insights We Hope to Get:**
- Understanding of data availability and completeness
- Foundation for all subsequent analyses""",

    'data_cleaning': """**What This Section Does:**
This section cleans and prepares the data for analysis by handling missing values, standardizing formats, and creating derived indicators.

**Key Cleaning Steps:**
1. **Filter Nairobi Schools**: Extract only schools within Nairobi County using District/Province columns
2. **Handle Missing Values**: Fill or remove missing data appropriately (e.g., fill numeric with 0, handle text inconsistencies)
3. **Standardize Formats**: Ensure consistent naming, data types, and geographic unit names
4. **Create Indicators**: Build composite metrics and binary flags for analysis

**Derived Indicators Created:**
- `Infrastructure_Stress`: Composite score (0-100) combining PTR, classroom ratio, toilet ratio
  - Formula: (PTR/60 × 33.3) + (ClassroomRatio/80 × 33.3) + (ToiletRatio/80 × 33.3)
  - Higher score = more infrastructure pressure
- `Overcrowded_Classrooms`: Binary indicator (ClassroomRatio > 50 pupils per classroom)
- `High_PTR`: Binary indicator (PupilTeacherRatio > 40 pupils per teacher)
- `Gender_Imbalance`: Binary indicator (absolute gender difference > 15%)
- `Girls_Toilet_Deficit`: Binary indicator (inadequate girls' toilets based on ratio)
- `PWD_Inclusive`: Binary indicator (Type3 = 'INTEGRATED' or 'SPECIAL SCHOOL')
- `Is_Special_School`: Binary indicator (Type3 = 'SPECIAL SCHOOL' only)

**What We're Doing:**
- Removing invalid records (e.g., missing coordinates, invalid enrollment)
- Standardizing geographic names (uppercase, strip whitespace)
- Creating boolean flags for easy filtering and aggregation
- Calculating ratios and composite scores

**Datasets Used:**
- `nairobi_schools_clean`: Filtered and cleaned Nairobi schools dataset

**Questions We're Answering:**
- Is the data clean and ready for analysis?
- What's the data quality?
- How many valid records do we have?

**Insights We Hope to Get:**
- Data quality assessment
- Understanding of data completeness
- Foundation for all subsequent analyses""",

    'spatial_equity': """**What This Section Does:**
Analyzes the geographic distribution of schools relative to population to identify education deserts and spatial inequities.

**Sub-Analyses:**
1. **School Density vs Population Density**: Calculates schools per 1000 school-age children by geographic unit (Division/Constituency)
2. **Spatial Accessibility Metrics**: Measures how accessible schools are geographically
3. **Education Desert Identification**: Identifies areas with insufficient school coverage relative to population

**Datasets Used:**
- School locations (coordinates: X, Y or Latitude, Longitude)
- Administrative units (Division, Location, Constituency)
- Population data by sub-county (from census)
- School-age population estimates (calculated as ~16% of total population)

**Key Metrics Calculated:**
- `Schools_per_1000`: Number of schools per 1000 school-age children
  - Formula: (School_Count / School_Age_Pop) × 1000
- `School_Density_Score`: Normalized score (0-100, lower = more need)
- `Enrollment_Rate`: Percentage of school-age children enrolled
- `Capacity_Gap`: School_Age_Pop - Total_Enrollment

**Geographic Units Analyzed:**
- Division (administrative sub-unit within Nairobi)
- Location (smaller administrative unit)
- Constituency (electoral boundary)

**Questions We're Answering:**
1. Are schools evenly distributed across Nairobi?
2. Which sub-counties/divisions have too few schools relative to population?
3. Where are the "education deserts" - areas with poor school access?
4. Is there spatial equity in school distribution?
5. Which areas need new schools most urgently?

**Insights We Hope to Get:**
- Identification of underserved areas
- Priority locations for new school construction
- Understanding of geographic access barriers
- Evidence for spatial equity gaps""",

    'infrastructure': """**What This Section Does:**
Assesses the adequacy of school infrastructure including classrooms, teachers, and toilet facilities to identify capacity constraints.

**Sub-Analyses:**
1. **Pupil-Teacher Ratio (PTR)**: Analyzes teacher adequacy across schools
2. **Classroom Capacity and Overcrowding**: Identifies schools with insufficient classrooms
3. **Toilet Facilities Adequacy**: Assesses sanitation infrastructure (total and gender-specific)
4. **Infrastructure Stress Scores**: Composite measure of overall infrastructure pressure

**Datasets Used:**
- School enrollment data (`TotalEnrol`: total enrollment)
- Teacher counts (`TotalTeachers`: number of teachers)
- Classroom counts (`TotalClassrooms`: number of classrooms)
- Toilet counts (`TotalToilets`, `GirlsToilet`, `BoysToilet`: toilet facilities)

**Key Metrics Calculated:**
- `PupilTeach` (PTR): Pupils per teacher
  - Formula: TotalEnrol / TotalTeachers
  - Standard: PTR > 40 indicates high need
- `ClassrmRat`: Pupils per classroom
  - Formula: TotalEnrol / TotalClassrooms
  - Standard: Ratio > 50 indicates overcrowding
- `ToiletRati`: Pupils per toilet
  - Formula: TotalEnrol / TotalToilets
  - Standard: Ratio > 80 indicates inadequate facilities
- `Infrastructure_Stress`: Weighted composite score (0-100, higher = more stress)
  - Formula: (PTR/60 × 33.3) + (ClassroomRatio/80 × 33.3) + (ToiletRatio/80 × 33.3)

**Standards Used:**
- PTR > 40: High (needs attention)
- Classroom Ratio > 50: Overcrowded
- Toilet Ratio > 80: Inadequate

**Questions We're Answering:**
1. How many schools are overcrowded?
2. What's the average pupil-teacher ratio?
3. Are toilet facilities adequate?
4. Which schools have the highest infrastructure stress?
5. What's the overall infrastructure capacity gap?

**Insights We Hope to Get:**
- Number of schools needing infrastructure investment
- Priority schools for capacity expansion
- Understanding of resource adequacy across Nairobi
- Identification of critical infrastructure gaps""",

    'gender': """**What This Section Does:**
Examines gender disparities in enrollment, infrastructure, and access to identify gender equity gaps and barriers.

**Sub-Analyses:**
1. **Gender Balance Indicator**: Measures enrollment balance between boys and girls
2. **Enrollment by Gender**: Total and percentage breakdown (TotalBoys vs TotalGirls)
3. **Gender-Specific Infrastructure**: Girls' toilet adequacy assessment
4. **Gender Imbalance Identification**: Schools with significant gender disparities (>15% difference)
5. **Population vs Enrollment Gender Comparison**: Compares gender breakdown in population vs enrollment

**Datasets Used:**
- Enrollment by gender (`TotalBoys`, `TotalGirls`)
- Girls' toilet counts (`GirlsToilet`)
- Population gender breakdown (from census, if available)
- Total enrollment (`TotalEnrol`)

**Key Metrics Calculated:**
- Gender enrollment percentage: (TotalBoys/TotalEnrol × 100) vs (TotalGirls/TotalEnrol × 100)
- Gender imbalance flag: Absolute difference > 15% between boys and girls
- Girls' toilet ratio: TotalGirls / GirlsToilet
- `Girls_Toilet_Deficit`: Binary indicator for inadequate girls' facilities

**Questions We're Answering:**
1. Is enrollment balanced between boys and girls?
2. Are there schools with significant gender imbalances?
3. Are girls' toilet facilities adequate?
4. Do enrollment rates differ by gender?
5. Are there barriers preventing equal access for girls?
6. How does school enrollment gender breakdown compare to population gender breakdown?

**Insights We Hope to Get:**
- Identification of gender equity gaps
- Schools needing gender-focused interventions
- Understanding of barriers to equal access
- Priority areas for gender equity investments
- Evidence for SDG 4.5 (eliminate gender disparities)""",

    'pwd': """**What This Section Does:**
Assesses the capacity and accessibility of the education system for Persons With Disabilities (PWD) to identify inclusion gaps.

**Sub-Analyses:**
1. **PWD-Inclusive School Categorization**: Identifies schools that accommodate PWD students
2. **Special vs Integrated Schools**: Distinguishes between dedicated special schools and mainstream integrated schools
3. **PWD Population from Census**: Estimates school-age PWD children using prevalence rates
4. **PWD Capacity Gaps**: Calculates the gap between need and current capacity
5. **Sub-County Level PWD Analysis**: Geographic distribution of PWD-inclusive schools

**Datasets Used:**
- School Type3 column: Values are 'ORDINARY', 'INTEGRATED', or 'SPECIAL SCHOOL'
- PWD population estimates (from census or disability prevalence rates ~2.5%)
- School enrollment capacity
- Geographic units (Division, Constituency) for sub-county analysis

**Key Metrics Calculated:**
- `PWD_Inclusive`: Binary indicator (Type3 = 'INTEGRATED' or 'SPECIAL SCHOOL')
- `Is_Special_School`: Binary indicator (Type3 = 'SPECIAL SCHOOL' only)
- PWD capacity: Estimated capacity of PWD-inclusive schools
- PWD capacity gap: Estimated PWD children - Current PWD capacity
- PWD coverage: Percentage of schools that are PWD-inclusive

**Assumptions:**
- INTEGRATED schools: Mainstream schools that accommodate PWD students alongside non-PWD students
- SPECIAL SCHOOL: Schools specifically designed for PWD students
- PWD prevalence: ~2.5% of population (Kenya national average)
- School-age PWD = Total school-age population × 0.025

**Questions We're Answering:**
1. How many schools are PWD-inclusive?
2. What's the geographic distribution of PWD-inclusive schools?
3. Is there sufficient capacity for PWD children?
4. Which sub-counties/divisions have zero PWD coverage?
5. What's the capacity gap (need vs available)?
6. Are PWD children being served equitably?

**Insights We Hope to Get:**
- Identification of PWD service gaps
- Priority locations for PWD-inclusive school expansion
- Understanding of accessibility barriers
- Capacity planning for PWD education
- Evidence for inclusive education gaps""",

    'enrollment': """**What This Section Does:**
Compares school enrollment capacity with school-age population to identify enrollment gaps and access issues.

**Sub-Analyses:**
1. **School-Age Population Estimation**: Estimates children aged 6-14 by sub-county/division
2. **Enrollment Capacity Gap**: Difference between school-age population and current enrollment
3. **Enrollment Rate Analysis**: Percentage of school-age children currently enrolled
4. **Actual Attendance Rates**: If available, compares enrollment to actual attendance

**Datasets Used:**
- Total enrollment (`TotalEnrol`: current school enrollment)
- Population data by sub-county (from census)
- Age breakdown (for school-age estimation, if available)
- Average household size (for population refinement)

**Key Metrics Calculated:**
- `School_Age_Pop`: Estimated children aged 6-14
  - Formula: Total Population × 0.16 (Kenya average: ~16% of population is school-age)
- `Enrollment_Rate`: Percentage enrolled
  - Formula: (TotalEnrol / School_Age_Pop) × 100
- `Capacity_Gap`: Unserved children
  - Formula: School_Age_Pop - TotalEnrol
- Enrollment coverage: Percentage of school-age children with access

**Assumptions:**
- School-age = 6-14 years (primary school age in Kenya)
- School-age % = ~16% of total population (Kenya average)
- If age breakdown unavailable, use 16% estimate

**Questions We're Answering:**
1. Are there enough school places for all school-age children?
2. What's the enrollment rate by sub-county/division?
3. Which areas have enrollment capacity gaps?
4. How many children are not enrolled?
5. Is enrollment capacity equitably distributed?
6. Are we meeting SDG 4.1 (free, equitable quality primary education)?

**Insights We Hope to Get:**
- Identification of enrollment gaps
- Understanding of access barriers
- Priority areas for capacity expansion
- Assessment of whether SDG 4 targets are being met
- Evidence for where new schools or capacity expansion is needed""",

    'public_private': """**What This Section Does:**
Examines equity between public and private schools in terms of distribution, enrollment, and infrastructure quality.

**Sub-Analyses:**
1. **Public vs Private Distribution**: Geographic and numerical distribution of school types
2. **Enrollment by School Type**: How many students attend each type of school
3. **Infrastructure Quality Comparison**: Comparing facilities between public and private schools
4. **Equity Barrier Assessment**: Identifying access barriers (cost, location, quality)

**Datasets Used:**
- School status (`Status`: 'PUBLIC' or 'PRIVATE')
- Enrollment data (`TotalEnrol`)
- Infrastructure metrics (classrooms, teachers, toilets)
- School locations (for geographic distribution analysis)

**Key Metrics Calculated:**
- Public vs private school counts and percentages
- Enrollment by school type (public vs private)
- Average infrastructure metrics by type (PTR, classroom ratio, toilet ratio)
- Geographic distribution by type (which areas have more public vs private)

**Questions We're Answering:**
1. Is access equitable regardless of ability to pay?
2. Are there quality differences between public and private schools?
3. What are the equity barriers (cost, location)?
4. Is there geographic equity in school type distribution?
5. Do private schools serve areas underserved by public schools?
6. Are there infrastructure quality disparities?

**Insights We Hope to Get:**
- Understanding of public-private equity
- Identification of access barriers
- Assessment of whether private schools complement public system
- Policy implications for equitable access
- Evidence for equity gaps between school types""",

    'composite': """**What This Section Does:**
Combines all equity dimensions into a single composite index to prioritize investment areas across multiple equity dimensions.

**Sub-Analyses:**
1. **Multi-Dimensional Priority Ranking**: Combines spatial, infrastructure, gender, PWD metrics
2. **Component Scores**: Normalized scores (0-100) for each dimension
3. **Weighted Composite Index**: Final priority ranking combining all dimensions

**Datasets Used:**
- All previous analyses aggregated by geographic unit (Constituency or Division)
- School counts, enrollment, infrastructure metrics
- Population data for normalization

**Key Metrics Calculated:**
- `School_Density_Score`: Based on schools per 1000 (lower density = higher need, score 0-100)
- `Infrastructure_Score`: Average infrastructure stress (higher stress = higher need, score 0-100)
- `PWD_Gap_Score`: Percentage of schools not PWD-inclusive (lower coverage = higher need, score 0-100)
- `Gender_Equity_Score`: Based on gender imbalance and girls' facilities (more issues = higher need, score 0-100)
- `Composite_Equity_Index`: Weighted average of all scores (higher = more priority/need)

**Weighting Scheme:**
- Infrastructure Capacity: 35% (most critical - affects all students)
- Spatial Equity: 25% (access to schools)
- Gender Equity: 20% (SDG 4.5 target)
- PWD Inclusivity: 20% (inclusive education)

**Normalization:**
All component scores normalized to 0-100 scale where:
- Higher score = More need/Priority
- Lower score = Less need/Priority

**Questions We're Answering:**
1. Which sub-counties/constituencies need investment most urgently?
2. What's the overall priority ranking combining all equity dimensions?
3. Where should resources be allocated first?
4. What's the relative priority across different equity dimensions?
5. How do different areas compare across all equity dimensions?

**Insights We Hope to Get:**
- Clear priority ranking for investment
- Understanding of multi-dimensional equity gaps
- Actionable recommendations for resource allocation
- Evidence-based decision support
- Comprehensive equity assessment""",

    'investment': """**What This Section Does:**
Creates an investment prioritization matrix based on impact and feasibility to guide strategic decision-making.

**Sub-Analyses:**
1. **Impact vs Feasibility Matrix**: 2x2 matrix categorizing interventions
2. **Quick Wins Identification**: High impact, high feasibility interventions
3. **Strategic Investment Categorization**: Long-term strategic investments
4. **Priority Ranking by Sub-County**: Final actionable priority list

**Framework:**
- **High Impact, High Feasibility**: Quick wins (implement first)
  - Example: Expand existing schools, add classrooms
- **High Impact, Low Feasibility**: Strategic investments (plan for long-term)
  - Example: Build new schools in underserved areas
- **Low Impact, High Feasibility**: Easy wins (do if resources allow)
  - Example: Minor infrastructure improvements
- **Low Impact, Low Feasibility**: Avoid (not priority)

**Impact Factors:**
- Number of students affected
- Severity of gap addressed
- Alignment with SDG 4 targets
- Equity improvement potential

**Feasibility Factors:**
- Cost
- Time to implement
- Resource requirements
- Political/social feasibility

**Questions We're Answering:**
1. What are the quick wins we can implement immediately?
2. What are the strategic long-term investments?
3. Where should we focus resources for maximum impact?
4. What's the implementation priority order?
5. How do we balance impact and feasibility?

**Insights We Hope to Get:**
- Actionable investment roadmap
- Quick wins for immediate impact
- Strategic planning guidance
- Resource allocation framework
- Prioritized intervention list""",

    'visualizations': """**What This Section Does:**
Creates visual representations of the analysis findings to communicate insights effectively to stakeholders.

**Visualization Types:**
- **Bar charts**: Comparing metrics across sub-counties/constituencies
- **Histograms**: Distribution of key metrics (PTR, enrollment rates, etc.)
- **Pie charts**: Composition breakdowns (public vs private, PWD coverage, etc.)
- **Scatter plots**: Relationships between variables (e.g., population vs schools)
- **Maps**: Geographic distribution (if coordinates available)

**What We're Visualizing:**
- School distribution across Nairobi
- Infrastructure stress by area
- Gender equity metrics
- PWD coverage gaps
- Enrollment capacity gaps
- Composite equity index rankings

**Questions We're Answering:**
- How can we communicate findings visually?
- What patterns are visible in the data?
- How do different areas compare?
- What are the key visual insights?

**Insights We Hope to Get:**
- Clear visual communication of findings
- Pattern identification
- Stakeholder engagement tools
- Easy-to-understand data presentation""",

    'findings': """**What This Section Does:**
Summarizes the most important findings from the analysis in a clear, concise format.

**What We're Presenting:**
- Key statistics and numbers (e.g., X schools overcrowded, Y% enrollment rate)
- Critical gaps identified (e.g., Z sub-counties with no PWD coverage)
- Priority areas (top 3 constituencies needing investment)
- Equity issues discovered (gender imbalances, spatial inequities)

**Structure:**
- Executive summary of key numbers
- Critical gaps by dimension
- Priority areas
- Equity issues

**Insights We're Communicating:**
- Main takeaways from the analysis
- Evidence-based findings
- Critical issues requiring attention
- Overall equity assessment""",

    'assumptions': """**What This Section Does:**
Documents assumptions made during the analysis and limitations of the data/methodology for transparency.

**What We're Documenting:**
- **Data assumptions**: 
  - School-age population estimation (16% of total population)
  - PWD prevalence (2.5% of population)
  - Geographic unit mappings
- **Methodological assumptions**: 
  - Thresholds for indicators (PTR > 40, ClassroomRatio > 50)
  - Weighting scheme for composite index
  - Normalization methods
- **Limitations**: 
  - Data quality (missing values, inconsistencies)
  - Coverage (some areas may have incomplete data)
  - Temporal (data is from specific time period)
- **Caveats for interpretation**: 
  - Confidence levels
  - Areas requiring additional data
  - Methodological constraints

**Why This Matters:**
- Transparency in analysis
- Understanding of confidence levels
- Guidance for interpretation
- Areas for future improvement
- Reproducibility

**Questions We're Addressing:**
- What assumptions were made?
- What are the limitations?
- How confident can we be in the findings?
- What additional data would improve the analysis?""",

    'recommendations': """**What This Section Does:**
Provides specific, actionable recommendations for the Nairobi County Education Officer based on the analysis findings.

**Recommendation Structure:**
- **Priority 1: Infrastructure Capacity Building**
  - Target schools exceeding PTR standards
  - Construct additional classrooms in overcrowded schools
  - Expand toilet facilities
  - Focus on top priority constituencies
  
- **Priority 2: Gender Equity Interventions**
  - Address gender imbalance in schools
  - Improve girls' toilet facilities
  - Implement targeted enrollment campaigns
  - Ensure gender-responsive infrastructure
  
- **Priority 3: PWD Inclusivity Expansion**
  - Expand PWD-inclusive capacity
  - Establish new integrated schools in areas with zero coverage
  - Address capacity gap
  - Retrofit existing schools with accessibility features
  
- **Priority 4: Spatial Equity**
  - Establish new schools in underserved high-density areas
  - Improve school distribution
  - Prioritize investments in areas with lowest school-to-population ratios

- **Alignment with SDG 4:**
  - Target 4.1: Free, equitable quality primary education
  - Target 4.5: Eliminate gender disparities and ensure equal access
  - Target 4.a: Build and upgrade education facilities

**What We're Recommending:**
- Specific interventions with target numbers
- Target areas/sub-counties/constituencies
- Expected outcomes
- SDG 4 alignment
- Implementation priorities

**Questions We're Answering:**
1. What should be done first?
2. Where should resources be allocated?
3. What interventions will have the most impact?
4. How does this align with SDG 4?
5. What are the quick wins vs strategic investments?

**Insights We're Providing:**
- Actionable next steps
- Prioritized intervention list
- Evidence-based recommendations
- Strategic guidance
- Implementation roadmap"""
}

# Function to add section documentation
def add_section_docs():
    """Add comprehensive documentation to all section headers"""
    updated = 0
    
    for i, cell in enumerate(nb['cells']):
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            
            # Check for section headers (## 1., ## 2., etc.)
            for num, info in section_info.items():
                pattern = rf'##\s*{num}\.\s*{re.escape(info["name"])}'
                if re.search(pattern, source, re.IGNORECASE):
                    # Check if already has detailed documentation
                    if 'What This Section Does' not in source:
                        key = info['key']
                        if key in descriptions:
                            new_source = f"""## {num}. {info['name']}

{descriptions[key]}
"""
                            nb['cells'][i]['source'] = new_source.split('\n')
                            updated += 1
                            print(f"✅ Updated section {num}: {info['name']}")
                            break
    
    return updated

# Function to add code comments (simplified - would need more sophisticated pattern matching)
def add_code_comments():
    """Add explanatory comments to key code cells"""
    # This is a placeholder - in practice, would need to identify specific code patterns
    # and add context-specific comments
    print("ℹ️  Code comments enhancement: Review code cells manually for best results")

# Main execution
print("="*80)
print("COMPREHENSIVE NOTEBOOK ENHANCEMENT")
print("="*80)
print()

sections_updated = add_section_docs()
add_code_comments()

print()
print("="*80)
print(f"✅ Updated {sections_updated} section headers with comprehensive documentation")
print("="*80)

# Save the notebook
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print()
print("✅ Notebook saved successfully!")
print()
print("💡 Next steps:")
print("   - Review code cells and add inline comments explaining what each code block does")
print("   - Ensure all sections are properly numbered")
print("   - Verify TOC links work correctly")




