import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(page_title="每月預算記帳（含 Google Sheets）", layout="centered")
st.title("📊 每月預算記帳")

# === Google Sheets 認證（從 Secrets） ===
gs_creds = json.loads(st.secrets["google_sheets"]["credentials"])
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_dict(gs_creds, scope)
client = gspread.authorize(creds)

# === 打開試算表 ===
sheet_url = st.secrets["google_sheets"]["sheet_url"]
sheet = client.open_by_url(sheet_url).sheet1

# === 讀取現有紀錄 ===
rows = sheet.get_all_records()
df = pd.DataFrame(rows)

st.subheader("📋 歷史支出紀錄")
if not df.empty:
    st.table(df)
else:
    st.write("目前尚無紀錄")

# === 新增支出 ===
st.subheader("➕ 新增支出")
expense_date = st.date_input("日期")
expense_item = st.text_input("支出項目")
expense_amount = st.number_input("金額", min_value=0)

if st.button("儲存到 Google Sheets"):
    new_row = [expense_date.strftime("%Y-%m-%d"),
               expense_item,
               expense_amount]
    sheet.append_row(new_row)
    st.success("已儲存到 Google Sheets 🎉")
    st.experimental_rerun()

# === 顯示長條圖 ===
st.subheader("📊 預算剩餘")
budget = st.number_input("請輸入每月預算", min_value=0, step=1000)
total_spent = df["金額"].sum() if not df.empty else 0
remaining = budget - total_spent

fig, ax = plt.subplots()
color = "green" if remaining >= 0 else "red"
ax.bar(["剩餘"], [max(remaining, 0)], color=color, width=0.3)
ax.set_ylabel("金額")
ax.set_title("剩餘預算")
ax.text(0, max(remaining * 0.5, 0), f"{remaining} 元", ha="center")
st.pyplot(fig)
