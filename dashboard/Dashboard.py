import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt  # Correct import for using subplots
import matplotlib.ticker as ticker
import streamlit as st

st.title("Bike Sharing 🚵")
st.caption("Anderson Usman")

clean_hour_df = pd.read_csv("./clean_hour.csv")
clean_day_df = pd.read_csv("./clean_day.csv")

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

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="season", y="count_total_rental", data=clean_day_df, palette=["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3"])

ax.set_xlabel("Season", fontsize=10)
ax.set_ylabel("Banyak sepeda", fontsize=10)
ax.set_title("Season dengan penyewaan sepeda terbanyak", loc="center", fontsize=30)
ax.tick_params(axis='y', labelsize=10)
ax.tick_params(axis='x', labelsize=10)

ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: f'{int(x):,}'))

st.pyplot(fig)

fig, ax = plt.subplots(figsize=(20, 10))

monthly_order = clean_day_df.groupby(by="date")['count_total_rental'].sum()

ax.scatter(monthly_order.index, monthly_order.values, c="#90CAF9", s=10, marker='o')
ax.plot(monthly_order.index, monthly_order.values, color="#90CAF9")

ax.set_title('Grafik Jumlah Pelanggan per Bulan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Jumlah')
ax.tick_params(axis='x', colors='white')

st.pyplot(fig)