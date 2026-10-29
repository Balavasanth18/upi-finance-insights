import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="UPI Finance Insights", page_icon="💸")
st.title("💸 UPI Personal Finance Insights")

df = pd.read_csv("transactions_clean.csv", parse_dates=["date"])

months = ["All"] + sorted(df["month"].unique().tolist())
choice = st.selectbox("Select month", months)
if choice != "All":
    df = df[df["month"] == choice]

c1, c2, c3 = st.columns(3)
c1.metric("Total spent", f"₹{df['amount'].sum():,.0f}")
c2.metric("Transactions", len(df))
c3.metric("Unusual", int(df["is_unusual"].sum()))

cat = df.groupby("category")["amount"].sum().reset_index()
st.plotly_chart(px.pie(cat, names="category", values="amount",
                       title="Spending by Category"), use_container_width=True)

monthly = df.groupby("month")["amount"].sum().reset_index()
st.plotly_chart(px.bar(monthly, x="month", y="amount",
                       title="Monthly Spending"), use_container_width=True)

st.subheader("⚠️ Unusual transactions")
st.dataframe(df[df["is_unusual"]][["date", "merchant", "amount"]])
