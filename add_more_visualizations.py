"""
Add additional high-value visualizations to the notebook
"""
import json

with open('analysis - New Version.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find where to insert (after existing visualizations or before findings)
insert_idx = None
for i, cell in enumerate(nb['cells']):
    if cell.get('cell_type') == 'markdown':
        source = ''.join(cell.get('source', []))
        if '## 12. Key Findings' in source or '## 12' in source and 'Finding' in source:
            insert_idx = i
            break

if insert_idx is None:
    # Find end of visualizations
    for i in range(len(nb['cells']) - 1, -1, -1):
        cell = nb['cells'][i]
        if cell.get('cell_type') == 'markdown':
            source = ''.join(cell.get('source', []))
            if '## 11' in source and 'Visualization' in source:
                insert_idx = i + 20  # Insert after some cells
                break

if insert_idx is None:
    insert_idx = len(nb['cells']) - 5  # Insert before last few cells

print(f"Inserting at index {insert_idx}")

# Additional visualizations
additional_viz = []

# 1. PWD Coverage Map
additional_viz.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": """### 11.7 PWD Coverage and Capacity Analysis

**What This Visualization Shows:**
Geographic distribution of PWD-inclusive schools and capacity gaps.

**Why This Matters:**
- Visual identification of PWD service deserts
- See where PWD children have access vs where they don't
- Understand capacity gaps geographically
- Prioritize PWD-inclusive school expansion

**How to Interpret:**
- **Green areas**: Good PWD coverage
- **Red areas**: No PWD coverage (service deserts)
- **Size**: Number of PWD-inclusive schools or capacity"""
})

additional_viz.append({
    "cell_type": "code",
    "metadata": {},
    "source": """# PWD Coverage and Capacity Analysis

# Analyze PWD coverage by geographic area
if 'constituency_analysis' in globals() and len(constituency_analysis) > 0:
    pwd_data = constituency_analysis.copy()
    
    # Calculate PWD coverage metrics
    if 'PWD_Inclusive_Count' in pwd_data.columns:
        pwd_coverage = pwd_data.copy()
        pwd_coverage['PWD_Coverage_Pct'] = (pwd_coverage['PWD_Inclusive_Count'] / 
                                           pwd_coverage['School_Count'] * 100).fillna(0)
        
        # Estimate PWD capacity gap
        # Assume each PWD-inclusive school can serve ~50 PWD students
        pwd_coverage['PWD_Capacity'] = pwd_coverage['PWD_Inclusive_Count'] * 50
        pwd_coverage['Estimated_PWD_Children'] = (pwd_coverage['School_Age_Pop'] * 0.025).fillna(0)
        pwd_coverage['PWD_Capacity_Gap'] = (pwd_coverage['Estimated_PWD_Children'] - 
                                           pwd_coverage['PWD_Capacity']).fillna(0)
        
        # Sort by coverage percentage
        pwd_coverage = pwd_coverage.sort_values('PWD_Coverage_Pct', ascending=True)
        
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 14))
        
        geo_col = pwd_coverage.columns[0]
        top_15 = pwd_coverage.head(15)  # Bottom 15 (lowest coverage)
        
        # 1. PWD Coverage Percentage
        colors_coverage = ['red' if pct == 0 else 'orange' if pct < 20 else 'yellow' if pct < 50 else 'green' 
                          for pct in top_15['PWD_Coverage_Pct'].values]
        ax1.barh(range(len(top_15)), top_15['PWD_Coverage_Pct'].values,
                color=colors_coverage, alpha=0.8, edgecolor='black', linewidth=0.5)
        ax1.set_yticks(range(len(top_15)))
        ax1.set_yticklabels(top_15[geo_col].values, fontsize=9)
        ax1.set_xlabel('PWD Coverage (%)', fontsize=11, fontweight='bold')
        ax1.set_title('PWD-Inclusive School Coverage (Bottom 15 Areas)', fontsize=12, fontweight='bold')
        ax1.axvline(x=0, color='red', linestyle='--', alpha=0.5, label='0% (No Coverage)')
        ax1.legend()
        ax1.grid(True, alpha=0.3, axis='x')
        
        # 2. PWD Capacity Gap
        colors_gap = ['red' if gap > 0 else 'green' for gap in top_15['PWD_Capacity_Gap'].values]
        ax2.barh(range(len(top_15)), top_15['PWD_Capacity_Gap'].values,
                color=colors_gap, alpha=0.8, edgecolor='black', linewidth=0.5)
        ax2.set_yticks(range(len(top_15)))
        ax2.set_yticklabels(top_15[geo_col].values, fontsize=9)
        ax2.set_xlabel('PWD Capacity Gap (Children)', fontsize=11, fontweight='bold')
        ax2.set_title('PWD Capacity Gap (Need - Capacity)', fontsize=12, fontweight='bold')
        ax2.axvline(x=0, color='black', linestyle='-', alpha=0.3)
        ax2.grid(True, alpha=0.3, axis='x')
        
        # 3. PWD Schools Distribution
        if 'Special_School_Count' in pwd_coverage.columns:
            x_pos = np.arange(len(top_15))
            width = 0.35
            ax3.bar(x_pos - width/2, top_15['PWD_Inclusive_Count'].fillna(0).values, width,
                   label='Integrated Schools', color='#3498db', alpha=0.8)
            ax3.bar(x_pos + width/2, top_15['Special_School_Count'].fillna(0).values, width,
                   label='Special Schools', color='#e74c3c', alpha=0.8)
            ax3.set_xticks(x_pos)
            ax3.set_xticklabels(top_15[geo_col].values, rotation=45, ha='right', fontsize=9)
            ax3.set_ylabel('Number of Schools', fontsize=11, fontweight='bold')
            ax3.set_title('PWD-Inclusive Schools by Type', fontsize=12, fontweight='bold')
            ax3.legend()
            ax3.grid(True, alpha=0.3, axis='y')
        
        # 4. PWD Coverage Summary
        zero_coverage = (pwd_coverage['PWD_Coverage_Pct'] == 0).sum()
        low_coverage = ((pwd_coverage['PWD_Coverage_Pct'] > 0) & (pwd_coverage['PWD_Coverage_Pct'] < 20)).sum()
        medium_coverage = ((pwd_coverage['PWD_Coverage_Pct'] >= 20) & (pwd_coverage['PWD_Coverage_Pct'] < 50)).sum()
        high_coverage = (pwd_coverage['PWD_Coverage_Pct'] >= 50).sum()
        
        coverage_counts = [zero_coverage, low_coverage, medium_coverage, high_coverage]
        labels_pie = ['No Coverage\n(0%)', 'Low Coverage\n(1-19%)', 'Medium Coverage\n(20-49%)', 'Good Coverage\n(≥50%)']
        colors_pie = ['#e74c3c', '#f39c12', '#f1c40f', '#27ae60']
        ax4.pie(coverage_counts, labels=labels_pie, colors=colors_pie, autopct='%1.1f%%',
               startangle=90, textprops={'fontsize': 10, 'fontweight': 'bold'})
        ax4.set_title('PWD Coverage Status Distribution', fontsize=12, fontweight='bold')
        
        plt.tight_layout()
        plt.savefig('pwd_coverage_analysis.png', dpi=300, bbox_inches='tight')
        print("\\n✅ PWD coverage analysis saved")
        plt.show()
        
        # Summary
        print("\\n" + "="*80)
        print("PWD COVERAGE SUMMARY")
        print("="*80)
        print(f"Areas with NO PWD coverage: {zero_coverage}")
        print(f"Areas with LOW coverage (1-19%): {low_coverage}")
        print(f"Areas with MEDIUM coverage (20-49%): {medium_coverage}")
        print(f"Areas with GOOD coverage (≥50%): {high_coverage}")
        print(f"\\nTotal PWD-inclusive schools: {pwd_coverage['PWD_Inclusive_Count'].sum():.0f}")
        print(f"Estimated PWD capacity: {pwd_coverage['PWD_Capacity'].sum():,.0f} children")
        print(f"Estimated PWD children: {pwd_coverage['Estimated_PWD_Children'].sum():,.0f}")
        print(f"Total PWD capacity gap: {max(0, pwd_coverage['PWD_Capacity_Gap'].sum()):,.0f} children")
    else:
        print("\\n⚠️  PWD_Inclusive_Count column not found in constituency_analysis")
else:
    print("\\n⚠️  constituency_analysis not found. Please run spatial equity analysis first.")"""
})

# 2. Public vs Private Comparison
additional_viz.append({
    "cell_type": "markdown",
    "metadata": {},
    "source": """### 11.8 Public vs Private School Equity Comparison

**What This Visualization Shows:**
Comprehensive comparison between public and private schools including:
- Distribution and enrollment
- Infrastructure quality differences
- Geographic distribution
- Equity barriers

**Why This Matters:**
- Understand equity between school types
- Identify access barriers (cost, quality)
- Assess if private schools complement public system
- Policy implications for equitable access

**How to Interpret:**
- **Side-by-side bars**: Compare public vs private
- **Color differences**: Quality/access differences
- **Geographic patterns**: Where each type is concentrated"""
})

additional_viz.append({
    "cell_type": "code",
    "metadata": {},
    "source": """# Public vs Private School Equity Comparison

# Analyze public vs private school equity
public_private = nairobi_schools_clean.groupby('Status').agg({
    'Name_of_Sc': 'count',
    'TotalEnrol': 'sum',
    'TotalBoys': 'sum',
    'TotalGirls': 'sum',
    'PupilTeach': 'mean',
    'ClassrmRat': 'mean',
    'ToiletRati': 'mean',
    'Infrastructure_Stress': 'mean'
}).reset_index()

public_private.columns = ['Status', 'School_Count', 'Total_Enrollment', 'Total_Boys', 'Total_Girls',
                         'Avg_PTR', 'Avg_Classroom_Ratio', 'Avg_Toilet_Ratio', 'Avg_Infrastructure_Stress']

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(18, 14))

# 1. School Count and Enrollment Comparison
x = np.arange(2)
width = 0.35
statuses = public_private['Status'].values
school_counts = public_private['School_Count'].values
enrollments = public_private['Total_Enrollment'].values

# Normalize for comparison
school_norm = school_counts / school_counts.max() * 100
enroll_norm = enrollments / enrollments.max() * 100

ax1.bar(x - width/2, school_norm, width, label='School Count (normalized)', 
       color='#3498db', alpha=0.8)
ax1.bar(x + width/2, enroll_norm, width, label='Enrollment (normalized)',
       color='#e74c3c', alpha=0.8)
ax1.set_xticks(x)
ax1.set_xticklabels(statuses, fontsize=11, fontweight='bold')
ax1.set_ylabel('Normalized Value (%)', fontsize=11, fontweight='bold')
ax1.set_title('Public vs Private: School Count and Enrollment', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3, axis='y')

# Add actual values
for i, (sc, en) in enumerate(zip(school_counts, enrollments)):
    ax1.text(i - width/2, school_norm[i] + 2, f'{sc:,.0f}', ha='center', fontsize=9, fontweight='bold')
    ax1.text(i + width/2, enroll_norm[i] + 2, f'{en:,.0f}', ha='center', fontsize=9, fontweight='bold')

# 2. Infrastructure Quality Comparison
infra_metrics = ['Avg_PTR', 'Avg_Classroom_Ratio', 'Avg_Toilet_Ratio', 'Avg_Infrastructure_Stress']
infra_labels = ['PTR', 'Classroom Ratio', 'Toilet Ratio', 'Infrastructure Stress']
x_infra = np.arange(len(infra_metrics))
width_infra = 0.35

public_values = [public_private[public_private['Status'] == 'PUBLIC'][m].values[0] 
                if len(public_private[public_private['Status'] == 'PUBLIC']) > 0 else 0 
                for m in infra_metrics]
private_values = [public_private[public_private['Status'] == 'PRIVATE'][m].values[0] 
                 if len(public_private[public_private['Status'] == 'PRIVATE']) > 0 else 0 
                 for m in infra_metrics]

ax2.bar(x_infra - width_infra/2, public_values, width_infra, label='Public', 
       color='#3498db', alpha=0.8)
ax2.bar(x_infra + width_infra/2, private_values, width_infra, label='Private',
       color='#e74c3c', alpha=0.8)
ax2.set_xticks(x_infra)
ax2.set_xticklabels(infra_labels, rotation=45, ha='right', fontsize=10)
ax2.set_ylabel('Metric Value', fontsize=11, fontweight='bold')
ax2.set_title('Infrastructure Quality: Public vs Private', fontsize=12, fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3, axis='y')

# 3. Gender Distribution
public_girls_pct = (public_private[public_private['Status'] == 'PUBLIC']['Total_Girls'].values[0] / 
                   public_private[public_private['Status'] == 'PUBLIC']['Total_Enrollment'].values[0] * 100
                   if len(public_private[public_private['Status'] == 'PUBLIC']) > 0 else 0)
private_girls_pct = (public_private[public_private['Status'] == 'PRIVATE']['Total_Girls'].values[0] / 
                     public_private[public_private['Status'] == 'PRIVATE']['Total_Enrollment'].values[0] * 100
                     if len(public_private[public_private['Status'] == 'PRIVATE']) > 0 else 0)

ax3.bar(['Public', 'Private'], [public_girls_pct, private_girls_pct],
       color=['#3498db', '#e74c3c'], alpha=0.8)
ax3.axhline(y=50, color='green', linestyle='--', alpha=0.5, label='50% (Balanced)')
ax3.set_ylabel('Girls Enrollment (%)', fontsize=11, fontweight='bold')
ax3.set_title('Gender Distribution: Girls Enrollment %', fontsize=12, fontweight='bold')
ax3.set_ylim([0, 60])
ax3.legend()
ax3.grid(True, alpha=0.3, axis='y')

# 4. Summary Statistics
summary_text = f\"\"\"
PUBLIC SCHOOLS:
  Schools: {public_private[public_private['Status'] == 'PUBLIC']['School_Count'].values[0] if len(public_private[public_private['Status'] == 'PUBLIC']) > 0 else 0:,.0f}
  Enrollment: {public_private[public_private['Status'] == 'PUBLIC']['Total_Enrollment'].values[0] if len(public_private[public_private['Status'] == 'PUBLIC']) > 0 else 0:,.0f}
  Avg PTR: {public_private[public_private['Status'] == 'PUBLIC']['Avg_PTR'].values[0] if len(public_private[public_private['Status'] == 'PUBLIC']) > 0 else 0:.1f}

PRIVATE SCHOOLS:
  Schools: {public_private[public_private['Status'] == 'PRIVATE']['School_Count'].values[0] if len(public_private[public_private['Status'] == 'PRIVATE']) > 0 else 0:,.0f}
  Enrollment: {public_private[public_private['Status'] == 'PRIVATE']['Total_Enrollment'].values[0] if len(public_private[public_private['Status'] == 'PRIVATE']) > 0 else 0:,.0f}
  Avg PTR: {public_private[public_private['Status'] == 'PRIVATE']['Avg_PTR'].values[0] if len(public_private[public_private['Status'] == 'PRIVATE']) > 0 else 0:.1f}
\"\"\"
ax4.text(0.1, 0.5, summary_text, fontsize=12, fontweight='bold',
        verticalalignment='center', family='monospace',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
ax4.axis('off')
ax4.set_title('Summary Statistics', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.savefig('public_private_comparison.png', dpi=300, bbox_inches='tight')
print("\\n✅ Public vs Private comparison saved")
plt.show()

print("\\n" + "="*80)
print("PUBLIC VS PRIVATE SCHOOL EQUITY SUMMARY")
print("="*80)
print(public_private.to_string(index=False))"""
})

# Insert additional visualizations
for i, new_cell in enumerate(additional_viz):
    nb['cells'].insert(insert_idx + i, new_cell)

# Save
with open('analysis - New Version.ipynb', 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f"\n✅ Added {len(additional_viz)} additional visualization cells")
print("   - PWD Coverage and Capacity Analysis")
print("   - Public vs Private School Equity Comparison")




