import streamlit as st
import matplotlib.pyplot as plt
from datetime import date

# ===== 中文字型設定（解決亂碼）=====
plt.rcParams["font.sans-serif"] = ["Noto Sans CJK TC"]
plt.rcParams["axes.unicode_minus"] = False

st.set_page_config(page_title="每月預算記帳", layout="centered")
st.title("📊 每月預算記帳")

# ===== 初始化 =====
if "budget" not in st.session_state:
    st.session_state.budget = 20000
if "remaining" not in st.session_state:
    st.session_state.remaining = 20000
if "records" not in st.session_state:
    st.session_state.records = []

# ===== 設定預算 =====
st.subheader("🔧 設定每月預算")

budget_input = st.number_input(
    "每月可花費金額",
    min_value=0,
    value=st.session_state.budget,
    step=100
)

if st.button("設定 / 重設預算"):
    st.session_state.budget = budget_input
    st.session_state.remaining = budget_input
    st.session_state.records = []
    st.success("預算已重設")

# ===== 新增支出 =====
st.subheader("🧾 新增支出")

col1, col2 = st.columns(2)

with col1:
    expense_date = st.date_input("日期", value=date.today())

with col2:
    expense_amount = st.number_input("金額", min_value=0, step=50)

expense_note = st.text_input("支出項目（例如：午餐 / 車票）")

if st.button("新增"):
    st.session_state.records.append({
        "date": expense_date.strftime("%Y-%m-%d"),
        "item": expense_note,
        "amount": expense_amount
    })
    st.session_state.remaining -= expense_amount

# ===== 顯示剩餘 =====
st.markdown(
    f"## 💰 剩餘金額： **{st.session_state.remaining:,} 元**"
)

# ===== 長條圖（變瘦）=====
fig, ax = plt.subplots()

color = "green" if st.session_state.remaining >= 0 else "red"

ax.bar(
    ["剩餘預算"],
    [max(st.session_state.remaining, 0)],
    color=color,
    width=0.3   # ← 關鍵：讓 bar 變瘦
)

ax.set_ylim(0, st.session_state.budget)
ax.set_ylabel("金額")
ax.set_title("本月可用餘額")

ax.text(
    0,
    st.session_state.budget * 0.5,
    f"{st.session_state.remaining:,} 元",
    ha="center",
    fontsize=14
)

st.pyplot(fig)

# ===== 支出紀錄 =====
st.subheader("📋 支出紀錄")

if st.session_state.records:
    st.table(st.session_state.records)
else:
    st.write("尚無支出紀錄")
