import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import seaborn as sns
import streamlit as st
import urllib
from function import DataAnalyzer, BrazilMapPlotter

sns.set(style='whitegrid')
st.set_option('deprecation.showPyplotGlobalUse', False)

date_cols = ["order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date", "order_purchase_timestamp", "shipping_limit_date"]
ecommerce_data = pd.read_csv("https://raw.githubusercontent.com/Maretaaliana/data-analyst-dicoding/main/dashboard/df.csv")
ecommerce_data.sort_values(by="order_approved_at", inplace=True)
ecommerce_data.reset_index(drop=True, inplace=True)

geo_data = pd.read_csv('https://raw.githubusercontent.com/Maretaaliana/data-analyst-dicoding/main/dashboard/geolocation.csv')
unique_customers_data = geo_data.drop_duplicates(subset='customer_unique_id')

for col in date_cols:
    ecommerce_data[col] = pd.to_datetime(ecommerce_data[col])

min_date_val = ecommerce_data["order_approved_at"].min()
max_date_val = ecommerce_data["order_approved_at"].max()

with st.sidebar:
    col_left, col_center, col_right = st.columns(3)
    with col_left:
        st.write(' ')
    with col_center:
        st.image("https://raw.githubusercontent.com/Maretaaliana/data-analyst-dicoding/main/dashboard/logo2.png", width=100)  # Ganti logo
    with col_right:
        st.write(' ')

    start_date_val, end_date_val = st.date_input(
        label="Pilih Rentang Tanggal",
        value=[min_date_val, max_date_val],
        min_value=min_date_val,
        max_value=max_date_val
    )

main_data = ecommerce_data[(ecommerce_data["order_approved_at"] >= str(start_date_val)) & 
                           (ecommerce_data["order_approved_at"] <= str(end_date_val))]

data_analyzer = DataAnalyzer(main_data)
brazil_map_plotter = BrazilMapPlotter(unique_customers_data, plt, mpimg, urllib, st)

daily_orders_df = data_analyzer.create_daily_orders_df()
total_spend_df = data_analyzer.create_sum_spend_df()
total_order_items_df = data_analyzer.create_sum_order_items_df()
review_scores, common_score = data_analyzer.review_score_df()
customer_state, most_common_state = data_analyzer.create_bystate_df()
order_statuses, common_status = data_analyzer.create_order_status()

st.title("Analisis Data Publik E-Commerce")

st.write("**Ini adalah dasbor untuk menganalisis data publik E-Commerce.**")

st.subheader("Pesanan Harian yang Dikirim")
col1, col2 = st.columns(2)

with col1:
    total_order_val = daily_orders_df["order_count"].sum()
    st.markdown(f"Total Pesanan: **{total_order_val}**")

with col2:
    total_revenue_val = daily_orders_df["revenue"].sum()
    st.markdown(f"Total Pendapatan: **{total_revenue_val}**")

fig_orders, ax_orders = plt.subplots(figsize=(12, 6))
sns.lineplot(
    x=daily_orders_df["order_approved_at"],
    y=daily_orders_df["order_count"],
    marker="o",
    linewidth=2,
    color="#FFA07A" 
)
ax_orders.tick_params(axis="x", rotation=45)
ax_orders.tick_params(axis="y", labelsize=15)
st.pyplot(fig_orders)

st.subheader("Pengeluaran Uang Pelanggan")
col1, col2 = st.columns(2)

with col1:
    total_spend_val = total_spend_df["total_spend"].sum()
    st.markdown(f"Total Pengeluaran: **{total_spend_val}**")

with col2:
    avg_spend_val = total_spend_df["total_spend"].mean()
    st.markdown(f"Rata-rata Pengeluaran: **{avg_spend_val}**")

fig_spend, ax_spend = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=total_spend_df,
    x="order_approved_at",
    y="total_spend",
    marker="o",
    linewidth=2,
    color="#FFA07A" 
)

ax_spend.tick_params(axis="x", rotation=45)
ax_spend.tick_params(axis="y", labelsize=15)
st.pyplot(fig_spend)

st.subheader("Barang Pesanan")
col1, col2 = st.columns(2)

with col1:
    total_items_val = total_order_items_df["product_count"].sum()
    st.markdown(f"Total Barang: **{total_items_val}**")

with col2:
    avg_items_val = total_order_items_df["product_count"].mean()
    st.markdown(f"Rata-rata Barang: **{avg_items_val}**")

fig_items, ax_items = plt.subplots(nrows=1, ncols=2, figsize=(45, 25))

sns.barplot(x="product_count", y="product_category_name_english", data=total_order_items_df.head(5), palette="mako", ax=ax_items[0])  # Ganti palette
ax_items[0].set_ylabel(None)
ax_items[0].set_xlabel("Jumlah Penjualan", fontsize=80)
ax_items[0].set_title("Produk paling laris", loc="center", fontsize=90)
ax_items[0].tick_params(axis ='y', labelsize=55)
ax_items[0].tick_params(axis ='x', labelsize=50)

sns.barplot(x="product_count", y="product_category_name_english", data=total_order_items_df.sort_values(by="product_count", ascending=True).head(5), palette="mako", ax=ax_items[1])  # Ganti palette
ax_items[1].set_ylabel(None)
ax_items[1].set_xlabel("Jumlah Penjualan", fontsize=80)
ax_items[1].invert_xaxis()
ax_items[1].yaxis.set_label_position("right")
ax_items[1].yaxis.tick_right()
ax_items[1].set_title("Produk paling sedikit terjual", loc="center", fontsize=90)
ax_items[1].tick_params(axis='y', labelsize=55)
ax_items[1].tick_params(axis='x', labelsize=50)

st.pyplot(fig_items)

st.subheader("Skor Ulasan")
col1, col2 = st.columns(2)

with col1:
    avg_review_score_val = review_scores.mean()
    st.markdown(f"Rata-rata Skor Ulasan: **{avg_review_score_val:.2f}**")

with col2:
    most_common_review_score_val = review_scores.value_counts().idxmax()
    st.markdown(f"Skor Ulasan Paling Umum: **{most_common_review_score_val}**")

fig_reviews, ax_reviews = plt.subplots(figsize=(12, 6))
colors_reviews = sns.color_palette("mako", len(review_scores))

sns.barplot(x=review_scores.index,
            y=review_scores.values,
            order=review_scores.index,
            palette=colors_reviews)

plt.title("Skor Ulasan Pelanggan untuk Layanan", fontsize=15)
plt.xlabel("Rating")
plt.ylabel("Jumlah")
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

for i, v in enumerate(review_scores.values):
    ax_reviews.text(i, v + 5, str(v), ha='center', va='bottom', fontsize=12, color='black')

st.pyplot(fig_reviews)

st.subheader("Demografi Pelanggan")

most_common_state_val = customer_state.customer_state.value_counts().index[0]
st.markdown(f"Negara Bagian Paling Umum: **{most_common_state_val}**")

fig_state, ax_state = plt.subplots(figsize=(12, 6))
sns.barplot(x=customer_state.customer_state.value_counts().index,
            y=customer_state.customer_count.values, 
            data=customer_state,
            palette="mako"
            )

plt.title("Jumlah pelanggan dari Setiap Negara Bagian", fontsize=15)
plt.xlabel("Negara Bagian")
plt.ylabel("Jumlah Pelanggan")
plt.xticks(fontsize=12)
st.pyplot(fig_state)

st.caption('Mareta Aliana')
