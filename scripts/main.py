import pandas as pd
import matplotlib.pyplot as plt

from utils import (
    load_and_summarize,
    plot_boxplots,
    resample_data,
    plot_time_series,
    analyze_grouped_data,
    plot_pie,
    plot_bar
)
# File paths (relative to the script's location)
musteri_verisi_path = '../data/musteri_verisi_5000_utf8.csv'
satis_verisi_path = '../data/satis_verisi_5000.csv'

# Load datasets
musteri_verisi = load_and_summarize(musteri_verisi_path, "Customer")
satis_verisi = load_and_summarize(satis_verisi_path, "Sales")

# Check for missing values
print("\n---------- MISSING VALUES CHECK ----------")
print("Customer Data Missing Values:")
print(musteri_verisi.isnull().sum())
print("\nSales Data Missing Values:")
print(satis_verisi.isnull().sum())

# Visualize outliers using boxplots
print("\n---------- OUTLIER VISUALIZATION ----------")
print("Boxplots generated for 'fiyat' and 'harcama_miktari' columns.")
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
plot_boxplots(satis_verisi, 'fiyat', 'Price Outliers', axs[0])
plot_boxplots(musteri_verisi, 'harcama_miktari', 'Spending Amount Outliers', axs[1])
plt.show()

# Merge datasets
satis_verisi['tarih'] = pd.to_datetime(satis_verisi['tarih'], format='%Y-%m-%d')
merged_data = pd.merge(satis_verisi, musteri_verisi, on='musteri_id', how='inner')

print("\n---------- MERGED DATASET ----------")
print("Sample of Merged Data:")
print(merged_data.head())
print("\nMerged Dataset Info:")
print(merged_data.info())

# Weekly and monthly sales analysis
weekly_sales = resample_data(merged_data, 'W', 'toplam_satis')
monthly_sales = resample_data(merged_data, 'ME', 'toplam_satis')

print("\n---------- WEEKLY AND MONTHLY SALES ----------")
print("Weekly Sales (First 5 Weeks):")
print(weekly_sales.head())
print("\nMonthly Sales (First 5 Months):")
print(monthly_sales.head())

# Plotting Weekly and Monthly Sales Trend
plot_time_series(weekly_sales, 'Weekly Sales Trend', 'Week', 'Total Sales', 'purple')
plot_time_series(monthly_sales, 'Monthly Sales Trend', 'Month', 'Total Sales', 'orange')

# Category analysis
category_sales = merged_data.groupby('kategori')['toplam_satis'].sum()
category_sales_percentage = (category_sales / category_sales.sum()) * 100

print("\n---------- CATEGORY SALES ANALYSIS ----------")
print("Total Sales by Category:")
print(category_sales)
print("\nCategory Sales Percentage:")
print(category_sales_percentage.round(2))

# Plotting sales for each category by percentage
plot_pie(category_sales_percentage, category_sales_percentage.index, 'Sales Percentage by Product Category')

# Age group analysis
age_bins = [18, 25, 35, 50, float('inf')]
age_labels = ['18-25', '26-35', '36-50', '50+']
merged_data['age_group'] = pd.cut(merged_data['yas'], bins=age_bins, labels=age_labels, right=False)

age_group_sales = merged_data.groupby('age_group', observed=False)['toplam_satis'].sum()

print("\n---------- AGE GROUP SALES ANALYSIS ----------")
print("Total Sales by Age Group:")
print(age_group_sales)

# Plotting total sales by each age interval
plot_bar(age_group_sales, 'Sales Trends by Age Group', 'Age Group', 'Total Sales', 'teal')

# Gender spending analysis
gender_spending = analyze_grouped_data(merged_data, 'cinsiyet', 'harcama_miktari', ['sum', 'mean'])

# Plotting total spending for each gender
plot_bar(gender_spending['sum'], 'Total Spending by Gender', 'Gender', 'Total Spending', ['skyblue', 'lightcoral'])

# Plotting average spending for each gender member
plot_bar(gender_spending['mean'], 'Average Spending by Gender', 'Gender', 'Average Spending', ['skyblue', 'lightcoral'])

# Calculate total spending by city
city_spending = merged_data.groupby('sehir')['harcama_miktari'].sum()

# Sort cities by total spending in descending order
city_spending_sorted = city_spending.sort_values(ascending=False)

# Display the result
print("\n---------- CITY SPENDING ANALYSIS ----------")
print(city_spending_sorted)

plot_bar(data=city_spending,title='Total Spending by City',xlabel='City',ylabel='Total Spending',colors='teal')

# Calculate total spending per customer grouped by city
city_customer_spending = merged_data.groupby(['sehir', 'musteri_id'])['harcama_miktari'].sum()

# Sort customers by spending within each city
top_spending_customers = city_customer_spending.groupby('sehir').max().sort_values(ascending=False)

# Display the result
print("\n---------- TOP SPENDING CUSTOMERS BY CITY ----------")
print(top_spending_customers)

plot_bar(data=top_spending_customers,title='Top Spending Customers by City',xlabel='City',ylabel='Top Customer Spending',colors='orange')

# Group by product and month, and calculate total sales
monthly_sales_by_product = merged_data.groupby(
    [merged_data['tarih'].dt.to_period('M'), 'ürün_adi']
)['toplam_satis'].sum()

# Reset index for easier calculations
monthly_sales_by_product = monthly_sales_by_product.reset_index()
print("\n---------- MONTHLY SALES BY PRODUCT ----------")
print(monthly_sales_by_product.head())


# Calculate percentage change for each product
monthly_sales_by_product['sales_change'] = monthly_sales_by_product.groupby('ürün_adi')['toplam_satis'].pct_change() * 100

# Display the results
print("\n---------- SALES CHANGE PERCENTAGE BY PRODUCT ----------")
print(monthly_sales_by_product.head(20))

# Calculate average sales change percentage for each product
average_sales_change = monthly_sales_by_product.groupby('ürün_adi')['sales_change'].mean()

# Display the results
print("\n---------- AVERAGE SALES CHANGE PERCENTAGE BY PRODUCT ----------")
print(average_sales_change.sort_values(ascending=False).round(2))

top_10_products = average_sales_change.sort_values(ascending=False).head(10)

plot_bar(data=top_10_products,title='Top 10 Products by Average Sales Growth (%)',xlabel='Product',ylabel='Average Growth (%)',colors='green')


