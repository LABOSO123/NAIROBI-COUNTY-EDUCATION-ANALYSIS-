"""
Check the actual distribution of Schools_per_1000 values to verify if color coding is appropriate
"""
print("="*80)
print("CHECKING MAP DATA DISTRIBUTION - Are thresholds appropriate?")
print("="*80)

# This would need to be run in the notebook context, but let's create a diagnostic
print("""
To verify the map color coding, we need to check:

1. ACTUAL DISTRIBUTION of Schools_per_1000 values:
   - How many locations have < 0.5 (should be red - education desert)
   - How many have 0.5-1.0 (should be orange - moderate)
   - How many have > 1.0 (should be green - adequate)

2. CURRENT COLOR THRESHOLDS:
   - Red: < 0.5 schools per 1000
   - Orange: 0.5-1.0 schools per 1000
   - Green: > 1.0 schools per 1000

3. POTENTIAL ISSUES:
   - If most are green, the threshold might be too low
   - Kenya standard might be different
   - Population matching might be underestimating school-age population
   - Some locations might have missing/incomplete data

RECOMMENDATION: Add a diagnostic cell to show the actual distribution
""")

print("\nSuggested diagnostic code to add:")
print("-" * 80)
print("""
# Check actual distribution of Schools_per_1000
print("\\n📊 ACTUAL DISTRIBUTION OF Schools_per_1000:")
print(f"   Total locations: {len(location_analysis)}")
print(f"   Education Deserts (< 0.5): {len(location_analysis[location_analysis['Schools_per_1000'] < 0.5])}")
print(f"   Moderate Need (0.5-1.0): {len(location_analysis[(location_analysis['Schools_per_1000'] >= 0.5) & (location_analysis['Schools_per_1000'] < 1.0)])}")
print(f"   Adequate (> 1.0): {len(location_analysis[location_analysis['Schools_per_1000'] >= 1.0])}")

print("\\n📊 STATISTICS:")
print(location_analysis['Schools_per_1000'].describe())

print("\\n📊 TOP 10 LOCATIONS BY Schools_per_1000 (highest density):")
print(location_analysis.nlargest(10, 'Schools_per_1000')[['Location', 'School_Count', 'School_Age_Pop', 'Schools_per_1000']])

print("\\n📊 BOTTOM 10 LOCATIONS BY Schools_per_1000 (lowest density):")
print(location_analysis.nsmallest(10, 'Schools_per_1000')[['Location', 'School_Count', 'School_Age_Pop', 'Schools_per_1000']])

# Check if population matching is working
print("\\n📊 POPULATION DATA QUALITY:")
print(f"   Locations with actual census population: {(location_analysis['School_Age_Pop'] > 0).sum()}")
print(f"   Locations with missing/zero population: {(location_analysis['School_Age_Pop'] == 0).sum()}")
""")

print("="*80)




