import nbformat as nbf
import os

os.makedirs('notebooks', exist_ok=True)
os.makedirs('visualizations', exist_ok=True)

nb = nbf.v4.new_notebook()

code_imports = """
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import warnings
import os
warnings.filterwarnings('ignore')

os.makedirs('../visualizations', exist_ok=True)
"""

code_load = """
df = pd.read_csv('../data/processed/customer_features.csv')
target_col = 'Churn' if 'Churn' in df.columns else 'churn'
print(f"Total customers: {len(df)}")
print(f"Churn rate: {df[target_col].mean()*100:.2f}%")
"""

code_plot1 = """
# 1. Target Variable Distribution
plt.figure(figsize=(8, 6))
df[target_col].value_counts().plot(kind='bar', color=['skyblue', 'salmon'])
plt.title('Churn Distribution')
plt.xlabel('Churn (0=Active, 1=Churned)')
plt.ylabel('Count')
plt.savefig('../visualizations/01_churn_distribution.png')
plt.close()
print("Saved 01_churn_distribution.png")
"""

code_plot2_5 = """
# 2-5. RFM Analysis (4 plots)
for i, col in enumerate(['Recency', 'Frequency', 'Monetary']):
    if col in df.columns:
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=target_col, y=col, data=df, showfliers=False)
        plt.title(f'{col} by Churn Status')
        plt.savefig(f'../visualizations/0{i+2}_{col}_by_churn.png')
        plt.close()
        
        plt.figure(figsize=(10, 6))
        sns.kdeplot(data=df, x=col, hue=target_col, common_norm=False)
        plt.title(f'{col} Distribution by Churn Status')
        plt.xlim(0, df[col].quantile(0.95))
        plt.savefig(f'../visualizations/0{i+5}_{col}_dist.png')
        plt.close()
"""

code_plot6_10 = """
# 6-10. Feature Correlation Analysis
numeric_cols = df.select_dtypes(include=[np.number]).columns
corr_matrix = df[numeric_cols].corr()

plt.figure(figsize=(12, 10))
sns.heatmap(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Feature Correlation Heatmap')
plt.savefig('../visualizations/06_correlation_heatmap.png')
plt.close()

top_corr = corr_matrix[target_col].sort_values(ascending=False).drop(target_col)
plt.figure(figsize=(10, 8))
top_corr.head(10).plot(kind='bar')
plt.title('Top 10 Features Correlated with Churn')
plt.savefig('../visualizations/07_top_correlations.png')
plt.close()
"""

code_plot11_13 = """
# 11-13. Segment Analysis
if 'CustomerSegment' in df.columns:
    seg_churn = df.groupby('CustomerSegment')[target_col].mean()
    plt.figure(figsize=(10, 6))
    seg_churn.plot(kind='bar')
    plt.title('Churn Rate by Customer Segment')
    plt.savefig('../visualizations/11_segment_churn.png')
    plt.close()
"""

code_plot14_15 = """
# 14-15. Temporal Patterns
for col in ['CustomerLifetimeDays', 'Purchases_Last30Days']:
    if col in df.columns:
        plt.figure(figsize=(10, 6))
        sns.boxplot(x=target_col, y=col, data=df)
        plt.title(f'{col} by Churn Status')
        plt.savefig(f'../visualizations/14_15_{col}_by_churn.png')
        plt.close()
"""

code_stats = """
# Statistical Tests
sig_features = []
print("Statistical Tests (T-test):")
for col in numeric_cols:
    if col != target_col:
        churned = df[df[target_col] == 1][col].dropna()
        active = df[df[target_col] == 0][col].dropna()
        if len(churned) > 0 and len(active) > 0:
            t_stat, p_value = stats.ttest_ind(churned, active, equal_var=False)
            if p_value < 0.05:
                sig_features.append((col, p_value))

print(f"Found {len(sig_features)} statistically significant features.")
for f, p in sorted(sig_features, key=lambda x: x[1])[:10]:
    print(f"{f}: p={p:.4e}")
"""

nb['cells'] = [
    nbf.v4.new_code_cell(code_imports),
    nbf.v4.new_code_cell(code_load),
    nbf.v4.new_code_cell(code_plot1),
    nbf.v4.new_code_cell(code_plot2_5),
    nbf.v4.new_code_cell(code_plot6_10),
    nbf.v4.new_code_cell(code_plot11_13),
    nbf.v4.new_code_cell(code_plot14_15),
    nbf.v4.new_code_cell(code_stats)
]

nbf.write(nb, 'notebooks/03_feature_eda.ipynb')
print("Notebook generated.")
