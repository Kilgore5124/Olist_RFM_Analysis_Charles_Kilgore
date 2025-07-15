# Import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set the style for plots
sns.set_style("whitegrid")

# Load datasets
# Ensure these files are in the same directory as this script
try:
    customers_df = pd.read_csv('olist_customers_dataset.csv')
    order_items_df = pd.read_csv('olist_order_items_dataset.csv')
    payments_df = pd.read_csv('olist_order_payments_dataset.csv')
    orders_df = pd.read_csv('olist_orders_dataset.csv')
    reviews_df = pd.read_csv('olist_order_reviews_dataset.csv')
    products_df = pd.read_csv('olist_products_dataset.csv')
    sellers_df = pd.read_csv('olist_sellers_dataset.csv')
    geolocation_df = pd.read_csv('olist_geolocation_dataset.csv')
    category_translation_df = pd.read_csv('product_category_name_translation.csv')
except FileNotFoundError as e:
    print(f"Error loading file: {e}. Please ensure all required CSV files are in the correct directory.")
    exit() # Exit if files are not found

# --- Cleaning and Merging ---

# Clean olist_orders_dataset
orders_df = orders_df[orders_df['order_status'] == 'delivered'].copy()
for col in ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date', 'order_delivered_customer_date', 'order_estimated_delivery_date']:
    orders_df[col] = pd.to_datetime(orders_df[col], errors='coerce')
orders_df.dropna(subset=['order_purchase_timestamp'], inplace=True)

# Clean olist_order_payments_dataset
payments_df.dropna(subset=['payment_value'], inplace=True)
payments_df = payments_df[payments_df['payment_value'] > 0].copy()

# Clean olist_order_items_dataset
order_items_df.dropna(subset=['order_id', 'price'], inplace=True)

# Clean olist_customers_dataset
customers_df.drop_duplicates(subset=['customer_id'], inplace=True)

# Clean olist_order_reviews_dataset
reviews_df['review_creation_date'] = pd.to_datetime(reviews_df['review_creation_date'], errors='coerce')
reviews_df['review_answer_timestamp'] = pd.to_datetime(reviews_df['review_answer_timestamp'], errors='coerce')
reviews_df.dropna(subset=['review_score'], inplace=True)

# Clean olist_products_dataset
products_df.drop_duplicates(subset=['product_id'], inplace=True)
products_df = products_df.dropna(subset=['product_id', 'product_category_name'])

# Clean olist_sellers_dataset
sellers_df.drop_duplicates(subset=['seller_id'], inplace=True)

# Clean olist_geolocation_dataset
geolocation_df = geolocation_df.drop_duplicates(subset=['geolocation_zip_code_prefix', 'geolocation_lat', 'geolocation_lng'])

# Clean product_category_name_translation.csv
category_translation_df.dropna(inplace=True)
category_translation_df.drop_duplicates(subset=['product_category_name'], inplace=True)


print("Data loading and initial cleaning complete.")

# Merge the cleaned dataframes
merged_df = pd.merge(orders_df, order_items_df, on='order_id', how='left')
merged_df = pd.merge(merged_df, payments_df, on='order_id', how='left')
merged_df = pd.merge(merged_df, customers_df[['customer_id', 'customer_unique_id']], on='customer_id', how='left')

# Drop rows where crucial information for RFM is missing after merges
merged_df.dropna(subset=['customer_unique_id', 'order_purchase_timestamp', 'payment_value'], inplace=True)

# Ensure 'payment_value' is numeric
merged_df['payment_value'] = pd.to_numeric(merged_df['payment_value'], errors='coerce')
merged_df.dropna(subset=['payment_value'], inplace=True)

print("Cleaned dataframes merged into merged_df.")

# --- Exploratory Data Analysis (EDA) ---
print("\nDescriptive statistics of merged_df:")
# print(merged_df.describe(include='all').to_markdown()) # You can uncomment this to print to console

print(f"\nNumber of unique customer IDs: {merged_df['customer_unique_id'].nunique()}")

print("\nDescriptive statistics of orders per customer:")
orders_per_customer = merged_df.groupby('customer_unique_id')['order_id'].nunique()
# print(orders_per_customer.describe().to_markdown()) # You can uncomment this to print to console


# --- RFM Analysis: Calculating Metrics ---

# Calculate Recency
snapshot_date = merged_df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
recency_df = merged_df.groupby('customer_unique_id')['order_purchase_timestamp'].max().reset_index()
recency_df['Recency'] = (snapshot_date - recency_df['order_purchase_timestamp']).dt.days
recency_df = recency_df[['customer_unique_id', 'Recency']]

# Calculate Frequency
frequency_df = merged_df.groupby('customer_unique_id')['order_id'].nunique().reset_index()
frequency_df.columns = ['customer_unique_id', 'Frequency']

# Calculate Monetary
monetary_df = merged_df.groupby('customer_unique_id')['payment_value'].sum().reset_index()
monetary_df.columns = ['customer_unique_id', 'Monetary']

# Merge RFM metrics into a single DataFrame
rfm_df = recency_df.merge(frequency_df, on='customer_unique_id').merge(monetary_df, on='customer_unique_id')

print("\nRFM metrics calculated.")
# print(rfm_df.head().to_markdown()) # You can uncomment this to print to console

# --- RFM Scoring and Segmentation ---

# Define quantiles
r_quantiles = rfm_df['Recency'].quantile([.25, .5, .75])
f_quantiles = rfm_df['Frequency'].quantile([.25, .5, .75])
m_quantiles = rfm_df['Monetary'].quantile([.25, .5, .75])

# Create RFM scores
rfm_df['R_Score'] = rfm_df['Recency'].apply(lambda x: 4 if x <= r_quantiles.iloc[0] else (3 if x <= r_quantiles.iloc[1] else (2 if x <= r_quantiles.iloc[2] else 1)))
rfm_df['F_Score'] = rfm_df['Frequency'].apply(lambda x: 1 if x <= f_quantiles.iloc[0] else (2 if x <= f_quantiles.iloc[1] else (3 if x <= f_quantiles.iloc[2] else 4)))
rfm_df['M_Score'] = rfm_df['Monetary'].apply(lambda x: 1 if x <= m_quantiles.iloc[0] else (2 if x <= m_quantiles.iloc[1] else (3 if x <= m_quantiles.iloc[2] else 4)))

# Combine scores into RFM Segment string
rfm_df['RFM_Segment'] = rfm_df['R_Score'].astype(str) + rfm_df['F_Score'].astype(str) + rfm_df['M_Score'].astype(str)

# Define segment map
segment_map = {
    r'4[1-4][1-4]': 'Champions',
    r'[1-3][3-4][3-4]': 'Loyal Customers',
    r'[1-3][1-2][3-4]': 'Potential Loyalists',
    r'4[1-2][1-2]': 'New Customers',
    r'[1-2][1-2][1-2]': 'About to Sleep',
    r'[1-2][1-4][1-2]': 'Hibernating',
    r'[1-2][1-2][3-4]': 'At Risk',
    r'3[1-4][1-4]': 'Promising',
    r'[1-2][3-4][3-4]': 'Cannot Lose Them',
}

# Apply segment mapping
rfm_df['Segment'] = rfm_df['RFM_Segment'].replace(segment_map, regex=True)

print("\nRFM scoring and segmentation complete.")

# Calculate segment counts and mean RFM metrics
segment_counts = rfm_df['Segment'].value_counts().reset_index()
segment_counts.columns = ['Segment', 'count']
segment_rfm_mean = rfm_df.groupby('Segment')[['Recency', 'Frequency', 'Monetary']].mean().reset_index()

print("\nCustomer Segment Distribution:")
print(segment_counts.to_markdown())
print("\nMean RFM Metrics by Segment:")
print(segment_rfm_mean.to_markdown())

# --- Visualizations ---

# Distribution of RFM Metrics
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.histplot(data=rfm_df, x='Recency', bins=50, kde=True, ax=axes[0])
axes[0].set_title('Distribution of Recency')
axes[0].set_xlabel('Recency (Days)')
axes[0].set_ylabel('Number of Customers')

sns.histplot(data=rfm_df, x='Frequency', bins=rfm_df['Frequency'].nunique(), kde=False, ax=axes[1])
axes[1].set_title('Distribution of Frequency')
axes[1].set_xlabel('Frequency (Number of Orders)')
axes[1].set_ylabel('Number of Customers')
axes[1].set_xticks(rfm_df['Frequency'].unique())

sns.histplot(data=rfm_df, x='Monetary', bins=50, kde=True, ax=axes[2])
axes[2].set_title('Distribution of Monetary')
axes[2].set_xlabel('Monetary Value')
axes[2].set_ylabel('Number of Customers')

plt.tight_layout()
plt.show()

# Distribution of Customers Across RFM Segments
plt.figure(figsize=(10, 6))
sns.barplot(x='Segment', y='count', data=segment_counts.sort_values('count', ascending=False), palette='viridis')
plt.title('Distribution of Customers Across RFM Segments')
plt.xlabel('Segment')
plt.ylabel('Number of Customers')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# Heatmap of Mean RFM Metrics by Segment
plt.figure(figsize=(10, 6))
heatmap_data = segment_rfm_mean.set_index('Segment')[['Recency', 'Frequency', 'Monetary']].T
sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="YlGnBu")
plt.title('Mean RFM Metrics by Customer Segment')
plt.xlabel('Segment')
plt.ylabel('RFM Metric')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

# Scatter plots for repeat customers (Frequency > 1)
repeat_customers_df = rfm_df[rfm_df['Frequency'] > 1].copy()

if not repeat_customers_df.empty:
    plt.figure(figsize=(12, 7))
    sns.scatterplot(data=repeat_customers_df, x='Recency', y='Monetary', hue='Segment', alpha=0.6)
    plt.title('Recency vs. Monetary for Repeat Customers (>1 Order) by Segment')
    plt.xlabel('Recency (Days)')
    plt.ylabel('Monetary Value')
    plt.legend(title='Segment', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 7))
    sns.scatterplot(data=repeat_customers_df, x='Frequency', y='Monetary', hue='Segment', alpha=0.6)
    plt.title('Frequency vs. Monetary for Repeat Customers (>1 Order) by Segment')
    plt.xlabel('Frequency (Number of Orders)')
    plt.ylabel('Monetary Value')
    plt.legend(title='Segment', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(12, 7))
    sns.scatterplot(data=repeat_customers_df, x='Recency', y='Frequency', hue='Segment', alpha=0.6)
    plt.title('Recency vs. Frequency for Repeat Customers (>1 Order) by Segment')
    plt.xlabel('Recency (Days)')
    plt.ylabel('Frequency (Number of Orders)')
    plt.legend(title='Segment', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()
else:
    print("No repeat customers (Frequency > 1) to plot.")


# --- Data Export ---
# Export the rfm_df DataFrame to a CSV file
rfm_df.to_csv('olist_customer_segmentation.csv', index=False)
print("\nSuccessfully exported 'olist_customer_segmentation.csv'")

# --- Summary and Next Steps ---
print("\n--- Analysis Summary ---")
print("Data Loading and Cleaning: Loaded and cleaned multiple Olist datasets, handling missing values and converting data types.")
print("Exploratory Data Analysis (EDA): Identified key characteristics including the skewed distribution of monetary values and the prevalence of one-time buyers.")
print("RFM Metric Calculation: Computed Recency, Frequency, and Monetary values for each unique customer.")
print("RFM Scoring and Segmentation: Assigned RFM scores based on quantiles and segmented customers into meaningful groups like Champions, Loyal Customers, and Potential Loyalists.")
print("Visualizations: Created plots to visualize RFM distributions, segment sizes, and average RFM metrics by segment.")
print("\n--- Business Implications and Recommendations ---")
print("The analysis highlights the dominance of one-time buyers and provides actionable insights for targeted strategies:")
print("- Prioritize retention of high-value segments (Champions, Loyal Customers) through exclusive programs.")
print("- Focus on converting 'Potential Loyalists' (recent, high-value one-time buyers) into repeat customers with targeted campaigns.")
print("- Implement cost-effective re-engagement for inactive segments ('About to Sleep', 'Hibernating').")
print("\n--- Next Steps ---")
print("The exported 'olist_customer_segmentation.csv' file is ready for integration into CRM systems or further analysis in BI tools like Tableau.")
print("Potential future analyses could include exploring segment preferences for product categories or geographical distribution.")
