import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df= pd.read_excel('Supermarket-Sales-Sample-Data.xlsx')
   
df['Ship Date'] = pd.to_datetime(df['Ship Date'])


df['Shipping_Day_of_Week'] = df['Ship Date'].dt.day_name()

df['Day_Type'] = np.where(df['Ship Date'].dt.weekday >= 5, 'Weekend', 'Weekday')
print(df[['Ship Date', 'Shipping_Day_of_Week','Day_Type']].head(10))
print(df.groupby('Day_Type')['Total (USD)'].sum())

calculated_total = (df['Retail Price (USD)'] * df['Order Quantity']) + df['tax(USD)']


difference = round(calculated_total, 2) - round(df['Total (USD)'], 2)


errors = df[difference != 0]

print(f"Total rows with validation errors: {len(errors)}")

df['Month'] = df['Ship Date'].dt.strftime('%B')

# Month ke mutabiq Total Sales ko group karein
monthly_sales = df.groupby('Month')['Total (USD)'].sum().reset_index()

print("--- Monthly Revenue ---")
print(monthly_sales)

day_type_analysis = df.groupby('Day_Type').agg(
    Total_Revenue=('Total (USD)', 'sum'),
    Average_Order_Value=('Total (USD)', 'mean'),
    Total_Orders=('Order No', 'count')
).reset_index()

print("\n--- Weekend vs Weekday Analysis ---")
print(day_type_analysis)
top_customers = df.groupby('Customer Name')['Total (USD)'].sum().reset_index()
top_customers = top_customers.sort_values(by='Total (USD)', ascending=False).head(5)

print("\n--- Top 5 Customers by Revenue ---")
print(top_customers)


plt.figure(figsize=(10, 5))
plt.bar(top_customers['Customer Name'], top_customers['Total (USD)'], color='skyblue')
plt.title('Top 5 Customers by Total Revenue')
plt.xlabel('Customer Name')
plt.ylabel('Total Sales (USD)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

customer_habits = df.groupby('Customer Name').agg(
    Avg_Quantity=('Order Quantity', 'mean'),
    Avg_Item_Price=('Retail Price (USD)', 'mean'),
    Total_Orders=('Order No', 'count')
).reset_index()


print("--- Customer Purchasing Habits (Sample) ---")
print(customer_habits.head())


df['Order Date'] = pd.to_datetime(df['Order Date'])


df['Delivery_Days'] = (df['Ship Date'] - df['Order Date']).dt.days


avg_delivery_time = df['Delivery_Days'].mean()

print("\n--- Shipping Performance ---")
print(f"Average Days to Ship an Order: {avg_delivery_time:.2f} Days")


late_shipments = df[df['Delivery_Days'] > 5]
print(f"Number of delayed shipments (more than 5 days): {len(late_shipments)}")
output_file_name = "Supermarket_Sales_Cleaned_Analysis.xlsx"


df.to_excel(output_file_name, index=False)
