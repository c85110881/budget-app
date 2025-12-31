import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# ===== Google Sheets 登入 =====
scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# ===== 打開你自己的 Sheet =====
sheet = client.open("Budget Records").sheet1
data = sheet.get_all_records()

df = pd.DataFrame(data)

st.title("📊 每月預算記帳（含 Google Sheets）")

# ===== 顯示現在表格資料 =====
st.dataframe(df)

# ===== 新增支出 =====
date = st.date_input("日期")
item = st.text_input("支出項目")
amt = st.number_input("金額")

if st.button("新增支出"):
    new_row = [str(date), item, amt]
    sheet.append_row(new_row)
    st.success("已儲存到 Google Sheets 🎉")
