import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import matplotlib.pyplot as plt

# === Google Sheets 認證設定 ===
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credentials.json", scope
)
client = gspread.authorize(creds)

# === 打開試算表 ===
sheet = client.open_by_url(
    "https://docs.google.com/spreadsheets/d/1ul2If-Fi4QosGojAJVM4fsPNrOdyfNzk6_cpslSc6JI/edit"
).sheet1

# -- 讀取現有資料 --
data = sheet.get_all_records()
df = pd.DataFrame(data)

st.title("📊 每月預算記帳（含 Google Sheets）")

# 顯示現有紀錄
st.subheader("📋 歷史支出紀錄")
if not df.empty:
    st.table(df)
else:
    st.write("目前尚無紀錄")

# 新增資料區塊
st.subheader("➕ 新增支出")
expense_date = st.date_input("日期")
expense_item = st.text_input("項目")
expense_amount = st.number_input("金額", min_value=0)

if st.button("儲存"):
    new_row = [expense_date.strftime("%Y-%m-%d"),
               expense_item,
               expense_amount]
    sheet.append_row(new_row)
    st.success("已儲存到 Google Sheets 🎉")

# 畫長條圖
remaining = st.session_state.get("remaining", 0)
fig, ax = plt.subplots()
ax.bar(["本月剩餘"], [remaining], width=0.3)
ax.set_ylabel("金額")
st.pyplot(fig)
