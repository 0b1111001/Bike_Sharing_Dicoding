import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import streamlit as st

st.title("Bike Sharing 🚵")
st.caption("Anderson Usman")

# Load data
clean_hour_df = pd.read_csv("https://raw.githubusercontent.com/0b1111001/Bike_Sharing_Dicoding/master/dashboard/clean_hour.csv")
clean_day_df = pd.read_csv("https://raw.githubusercontent.com/0b1111001/Bike_Sharing_Dicoding/master/dashboard/clean_day.csv")

# Display metrics
col1, col2, col3 = st.columns(3)

with col1:
    most_order_day = clean_day_df['count_total_rental'].max()
    st.metric("Most sharing bike in a day 😀", value=most_order_day)

with col2:
    most_order_month = clean_day_df.groupby(by="month")['count_total_rental'].sum().max()
    st.metric("Most sharing bike in a month 🤩", value=most_order_month)

with col3:
    most_order_year = clean_day_df.groupby(by="year")['count_total_rental'].sum().max()
    st.metric("Most sharing bike in a year 😮", value=most_order_year)

total_order = clean_day_df['count_total_rental'].sum()
st.metric("Total bike that has been shared 👏", value=total_order)

# Bar plot for season data
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="season", y="count_total_rental", data=clean_day_df, palette=["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3"])

ax.set_xlabel("Season", fontsize=10)
ax.set_ylabel("Banyak sepeda", fontsize=10)
ax.set_title("Season dengan penyewaan sepeda terbanyak", loc="center", fontsize=30)
ax.tick_params(axis='y', labelsize=10)
ax.tick_params(axis='x', labelsize=10)

ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))
st.pyplot(fig)

# Menyiapkan data untuk divisualisasikan
analysis_df = clean_day_df[['temp', 'atemp', 'humidity', 'wind_speed', 'count_total_rental']]
correlation = analysis_df.corr()

# Visualisasi Data
plt.figure(figsize=(10, 6))
sns.heatmap(correlation, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title("Korelasi antara variabel cuaca dengan jumlah penyewaan sepeda")

# Tampilkan heatmap di dashboard Streamlit
st.pyplot(plt)

# Mapping month names to numbers
month_mapping = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}

date_range = pd.date_range(start="2011-01-01", end="2012-12-31", freq='MS').strftime("%Y-%m").tolist()

# Create a slider for selecting the date range
start_month, end_month = st.select_slider(
    "Select a range of months",
    options=date_range,
    value=(date_range[0], date_range[-1])
)

# Convert month names to numeric
clean_day_df['month_numeric'] = clean_day_df['month'].map(month_mapping)

# Convert selected months back to datetime for filtering
start_date = pd.to_datetime(start_month)
end_date = pd.to_datetime(end_month)

# Filter the data based on the selected date range
filtered_data = clean_day_df[(pd.to_datetime(clean_day_df['year'].astype(str) + '-' + clean_day_df['month'] + '-01') >= start_date) & 
                              (pd.to_datetime(clean_day_df['year'].astype(str) + '-' + clean_day_df['month'] + '-01') <= end_date)]

# Prepare monthly order data
monthly_order = filtered_data.groupby(['year', 'month_numeric'])['count_total_rental'].sum().reset_index()
# Create a 'year_month' column
monthly_order['year_month'] = monthly_order['year'].astype(str) + '-' + monthly_order['month_numeric'].astype(str).str.zfill(2)

# Create the plot using subplots
fig, ax = plt.subplots(figsize=(20, 10))

# Visualize the data
ax.scatter(monthly_order['year_month'], monthly_order['count_total_rental'], c="#90CAF9", s=10, marker='o')
ax.plot(monthly_order['year_month'], monthly_order['count_total_rental'], color="#90CAF9")

# Set titles and labels
ax.set_title('Grafik Jumlah Pelanggan per Bulan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah')
ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability

# Display the plot in Streamlit
st.pyplot(fig)