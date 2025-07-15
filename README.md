# Olist E-commerce Customer Segmentation with RFM Analysis

This project presents a comprehensive customer segmentation analysis of the Olist E-commerce platform using the RFM (Recency, Frequency, Monetary) model. Leveraging a rich dataset of customer transactions, the analysis aims to identify distinct customer groups based on their purchasing behavior – specifically, how recently they purchased, how often they purchase, and how much they spend.

## Project Overview

This project leverages the Olist E-commerce Dataset, a comprehensive public dataset of transactions on Olist, the largest Brazilian department store. The dataset encompasses various aspects of the e-commerce process, including order details, customer information, payment data, product specifics, seller information, and customer reviews. The central focus of this analysis is the application of the RFM model to segment the customer base.

The **RFM model** is a data-driven marketing approach that segments customers based on three key dimensions:

*   **Recency (R):** Measures how recently a customer made a purchase.
*   **Frequency (F):** Quantifies how often a customer makes purchases.
*   **Monetary (M):** Represents the total amount of money a customer has spent.

By calculating and combining these three metrics, we assign an RFM score to each customer and group them into distinct segments.

## Data Source

The dataset used in this analysis is the **Olist E-commerce Public Dataset**, available on [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).

To replicate this analysis, you will need to download the following CSV files from the Kaggle page and place them in the same directory as the analysis script:

*   `olist_customers_dataset.csv`
*   `olist_orders_dataset.csv`
*   `olist_order_items_dataset.csv`
*   `olist_products_dataset.csv`
*   `olist_sellers_dataset.csv`
*   `olist_order_reviews_dataset.csv`
*   `olist_order_payments_dataset.csv`
*   `product_category_name_translation.csv`
*   `olist_geolocation_dataset.csv`

## Project Objectives

The key objectives guiding this RFM analysis and customer segmentation project are to:

1.  **Data Acquisition and Preparation:** Load, clean, and merge relevant datasets.
2.  **RFM Metric Calculation:** Compute Recency, Frequency, and Monetary values for each customer.
3.  **Customer Segmentation:** Apply the RFM model to segment the customer base.
4.  **Segment Characterization and Analysis:** Analyze the characteristics of each segment.
5.  **Actionable Business Recommendations:** Develop tailored strategies for each segment.
6.  **Visualization and Communication:** Create visualizations to communicate findings effectively.
7.  **Reproducibility:** Structure the project for easy replication.

## Analysis Steps

The analysis follows these key steps:

1.  **Data Loading, Cleaning, and Merging:** Loading the raw data, cleaning individual datasets (handling missing values, correcting data types, filtering), and merging them into a single DataFrame for RFM analysis.
2.  **Exploratory Data Analysis (EDA):** Examining the distributions of key variables like payment value and order frequency to understand the customer base's characteristics (notably the prevalence of one-time buyers).
3.  **RFM Analysis: Calculating Metrics:** Computing Recency, Frequency, and Monetary values for each unique customer.
4.  **RFM Scoring and Segmentation:** Assigning RFM scores based on quantiles and grouping customers into predefined segments (e.g., Champions, Loyal Customers, Potential Loyalists).
5.  **Visualization:** Generating plots to visualize the distribution of RFM metrics, segment sizes, and average RFM characteristics by segment.
6.  **Business Implications and Recommendations:** Providing actionable insights and tailored strategies for each customer segment based on their RFM profiles.
7.  **Data Export:** Exporting the final customer segmentation data to a CSV file for external use.

## Business Implications and Recommendations

The RFM segmentation provides a data-driven framework for understanding the customer base and developing targeted strategies. By recognizing the distinct characteristics and behaviors of each segment, businesses can allocate resources more effectively, personalize marketing messages, improve customer engagement, and ultimately drive revenue growth and enhance customer lifetime value (CLTV). The analysis revealed the dominance of one-time buyers, highlighting an opportunity for conversion strategies, while also identifying valuable segments like Champions and Loyal Customers for retention focus.

## Files in this Repository

*   `rfm_analysis.py`: Python script containing the code for data loading, cleaning, merging, RFM calculation, scoring, segmentation, and data export.
*   `README.md`: This file, providing an overview of the project.
*   `olist_customer_segmentation.csv`: (This file will be generated after running `rfm_analysis.py`) The output CSV file containing the RFM metrics, scores, and segments for each customer.

## How to Run the Analysis

1.  Download the required CSV files from the [Kaggle dataset page](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce).
2.  Place the downloaded CSV files and the `rfm_analysis.py` script in the same directory.
3.  Ensure you have the necessary Python libraries installed (`pandas`, `numpy`, `matplotlib`, `seaborn`). You can install them using pip:
    ```bash
    pip install pandas numpy matplotlib seaborn
    ```
4.  Run the Python script from your terminal:
    ```bash
    python rfm_analysis.py
    ```
5.  The script will perform the analysis and generate the `olist_customer_segmentation.csv` file in the same directory.

## Summary of Findings

(Include the content from the "Summary: Data Analysis Key Findings" and "Insights and Next Steps" markdown cells here)
