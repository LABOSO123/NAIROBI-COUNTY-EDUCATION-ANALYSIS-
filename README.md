# Nairobi County Education Analysis

This repository contains the working files for an in-depth exploration of education access and equity across Nairobi County, Kenya. The project combines census datasets, administrative boundaries, and school infrastructure records to surface actionable insights for planners, policymakers, and advocates.

## Project Goals
- Quantify school-age population distribution across Nairobi sub-counties.
- Assess school density, enrollment, and infrastructure metrics using actual census and school datasets.
- Map geographic disparities to highlight underserved areas and priority interventions.
- Package the workflow in reproducible notebooks and helper scripts.

## Repository Structure
- `analysis - New Version.ipynb` – primary exploratory and visualization notebook.
- `analysis.ipynb`, `analysis - HUHHH.ipynb`, `nairobi-education-analysis.ipynb` – historic or alternative notebook iterations.
- `add_*.py`, `fix_*.py`, `verify_*.py`, etc. – automation scripts that enhance, validate, or repair notebook content and visuals.
- `data/` – raw census tables, school datasets, and the extracted Nairobi sub-county lookup (`Nairobi Sub Counties.csv`).
- `visualizations` (HTML/PNG files in the root) – exported maps and charts from the notebooks.

## Key Data Sources
- `data/ken_adminboundaries_tabulardata.xlsx` – administrative boundaries, filtered to Nairobi sub-counties.
- `data/distribution-of-population-by-sex-and-sub-county-2019-census-volume-ii.csv` – population by sub-county.
- `data/distribution-of-population-by-sex-and-sub-locations-2019-census-volume-ii.csv` – population by sub-location.
- `data/kenya_primary_schools.csv` – school-level infrastructure metrics.
- Additional census extracts covering age, urban/rural splits, disability status, and household characteristics (see filenames in `data/`).

## Getting Started
1. **Clone the repository**
   ```bash
   git clone https://github.com/LABOSO123/NAIROBI-COUNTY-EDUCATION-ANALYSIS-.git
   cd NAIROBI-COUNTY-EDUCATION-ANALYSIS-
   ```
2. **Create a virtual environment (optional but recommended)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```
3. **Install dependencies** – install libraries used in the notebooks (typical stack: `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`, `geopandas`, `openpyxl`, etc.). A formal requirements file has not yet been generated; install packages as they appear when running the notebooks.

## Usage
- Open `analysis - New Version.ipynb` in Jupyter Lab or VS Code to reproduce the latest figures and tables. Run the notebook top-to-bottom to load data, clean it, compute indicators, and generate visualizations.
- Auxiliary scripts (e.g., `verify_data_accuracy.py`, `add_map_display.py`) can be executed to automate updates, validate data integrity, or regenerate specific outputs. Each script prints guidance when run with `python script_name.py`.
- The freshly extracted `data/Nairobi Sub Counties.csv` lists all Nairobi sub-counties with their land areas for easy joins with other datasets.

## Outputs
- Static PNGs such as `nairobi_education_equity_analysis.png` summarize key findings.
- Interactive HTML maps (`nairobi_locations_equity_map.html`, `nairobi_locations_density_map.html`, etc.) provide spatial explorations of school distribution and equity metrics.

## Next Steps
- Document Python dependencies in a `requirements.txt` for quicker environment setup.
- Add unit tests around data cleaning helpers and validation scripts.
- Publish selected visualizations or dashboards for wider stakeholder access.

Contributions, issues, and enhancements are welcome through GitHub pull requests or discussions.
