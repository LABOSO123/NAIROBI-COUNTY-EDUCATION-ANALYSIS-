import pandas as pd
import sys
import os

try:
    # Load admin boundaries from Excel
    print("Loading admin boundaries from Excel...")
    excel_path = 'data/ken_adminboundaries_tabulardata.xlsx'
    
    if not os.path.exists(excel_path):
        print(f"Error: File not found: {excel_path}")
        sys.exit(1)
    
    admin_boundaries = pd.read_excel(excel_path, sheet_name='ADM2')
    print(f"Loaded {len(admin_boundaries)} rows from ADM2 sheet")
    print(f"Columns: {list(admin_boundaries.columns)}")
    
    # Extract Nairobi subcounties
    print("\nExtracting Nairobi subcounties...")
    if 'ADM1_EN' not in admin_boundaries.columns:
        print(f"Error: Column 'ADM1_EN' not found. Available columns: {list(admin_boundaries.columns)}")
        sys.exit(1)
    
    nairobi_subcounties = admin_boundaries[admin_boundaries['ADM1_EN'].str.contains('NAIROBI', case=False, na=False)].copy()
    print(f"Found {len(nairobi_subcounties)} Nairobi subcounties")
    
    # Select relevant columns
    if 'ADM2_EN' not in nairobi_subcounties.columns or 'AREA_SQKM' not in nairobi_subcounties.columns:
        print(f"Error: Required columns not found. Available: {list(nairobi_subcounties.columns)}")
        sys.exit(1)
    
    nairobi_subcounties = nairobi_subcounties[['ADM2_EN', 'AREA_SQKM']].copy()
    nairobi_subcounties.columns = ['Sub_County', 'Area_sqkm']
    nairobi_subcounties['Sub_County'] = nairobi_subcounties['Sub_County'].str.strip()
    
    # Save to CSV
    output_file = 'data/Nairobi Sub Counties.csv'
    nairobi_subcounties.to_csv(output_file, index=False)
    
    print(f"\n✅ Successfully extracted {len(nairobi_subcounties)} Nairobi Sub-Counties")
    print(f"✅ Saved to: {output_file}\n")
    print("Nairobi Sub-Counties:")
    print("=" * 50)
    print(nairobi_subcounties.to_string(index=False))
    print("\n" + "=" * 50)
    
except Exception as e:
    print(f"Error: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

