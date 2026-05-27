import streamlit as st
import plotly.express as px
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Advanced Tax Analytics Dashboard", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .main-title {font-size:32px; font-weight:700; color:#1E3A8A; text-align:center; margin-bottom:25px;}
    .custom-card {
        background-color: #F0F4F8; 
        color: #1E3A8A !important; 
        padding: 20px; 
        border-radius: 12px; 
        border-left: 6px solid #1E3A8A;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    .custom-card h2 { color: #1E3A8A !important; margin: 5px 0 0 0; font-size: 28px;}
    .custom-card b { font-size: 14px; text-transform: uppercase; color: #4B5563;}
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='main-title'>📊 Advanced Income Tax Calculator & Analytics Dashboard</div>", unsafe_allow_html=True)

# ----------------- SIDEBAR INPUTS -----------------
st.sidebar.header("👤 User Financial Profile")
gross_income = st.sidebar.number_input("Gross Annual Income (₹)", min_value=0, value=1500000, step=50000)

# OLD REGIME DEDUCTIONS BLOCK
st.sidebar.write("---")
st.sidebar.subheader("🏛️ Old Regime Deductions")
investments_80c = st.sidebar.number_input("Section 80C (PPF, ELSS, LIC) (₹)", min_value=0, max_value=150000, value=150000, step=10000)
other_deductions = st.sidebar.number_input("Other Deductions (HRA, Medical 80D) (₹)", min_value=0, value=50000, step=5000)

# NEW REGIME DEDUCTIONS BLOCK
st.sidebar.write("---")
st.sidebar.subheader("📉 New Regime Deductions")
nps_80ccd = st.sidebar.number_input("Employer NPS Contribution 80CCD(2) (₹)", min_value=0, value=0, step=5000)

# Fixed Standard Deductions
std_deduction_old = 50000
std_deduction_new = 75000 

# ----------------- PERFECTED TAX LOGIC -----------------
def calculate_taxes(income, invest_80c, other_ded, nps_ded):
    # 1. Old Regime Calculation
    old_taxable = max(0, income - invest_80c - other_ded - std_deduction_old)
    old_tax = 0
    
    if old_taxable > 1000000:
        old_tax += (old_taxable - 1000000) * 0.30
        old_tax += 100000  # Tax for 5L to 10L (500000 * 0.20)
        old_tax += 12500   # Tax for 2.5L to 5L (250000 * 0.05)
    elif old_taxable > 500000:
        old_tax += (old_taxable - 500000) * 0.20
        old_tax += 12500   # Tax for 2.5L to 5L (250000 * 0.05)
    elif old_taxable > 250000:
        old_tax += (old_taxable - 250000) * 0.05

    # Rebate under Sec 87A ONLY if taxable income is up to ₹5,00,000
    if old_taxable <= 500000:
        old_tax = 0
        
    old_tax_final = old_tax + (old_tax * 0.04) # Health & Education Cess

    # 2. Corrected New Regime Calculation (FY 2025-26 Slabs)
    new_taxable = max(0, income - nps_ded - std_deduction_new)
    new_tax = 0
    
    # Slab calculation logic split properly
    if new_taxable > 2400000:
        new_tax += (new_taxable - 2400000) * 0.30
        new_tax += 300000 # Sum of all lower slabs till 24L
    elif new_taxable > 2000000:
        new_tax += (new_taxable - 2000000) * 0.25
        new_tax += 200000
    elif new_taxable > 1600000:
        new_tax += (new_taxable - 1600000) * 0.20
        new_tax += 120000
    elif new_taxable > 1200000:
        new_tax += (new_taxable - 1200000) * 0.15
        new_tax += 60000
    elif new_taxable > 800000:
        new_tax += (new_taxable - 800000) * 0.10
        new_tax += 20000
    elif new_taxable > 400000:
        new_tax += (new_taxable - 400000) * 0.05

    # Rebate under Sec 87A ONLY if taxable income is up to ₹12,00,000
    if new_taxable <= 1200000:
        new_tax = 0
        
    new_tax_final = new_tax + (new_tax * 0.04) # Health & Education Cess

    return old_tax_final, new_tax_final, old_taxable, new_taxable

# Execution Call
old_tax, new_tax, old_taxable, new_taxable = calculate_taxes(gross_income, investments_80c, other_deductions, nps_80ccd)
best_regime = "New Regime" if new_tax <= old_tax else "Old Regime"
savings = abs(old_tax - new_tax)

# ----------------- MAIN DASHBOARD KPI CARDS -----------------
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"<div class='custom-card'><b>📉 New Regime Tax</b><h2>₹{new_tax:,.2f}</h2></div>", unsafe_allow_html=True)
with col2:
    st.markdown(f"<div class='custom-card'><b>🏛️ Old Regime Tax</b><h2>₹{old_tax:,.2f}</h2></div>", unsafe_allow_html=True)
with col3:
    color_border = "#10B981" if savings > 0 else "#1E3A8A"
    st.markdown(f"<div class='custom-card' style='border-left-color:{color_border};'><b>💡 Best Option: {best_regime}</b><h2>Saves ₹{savings:,.2f}</h2></div>", unsafe_allow_html=True)

st.write("---")

# ----------------- PLOTLY CHARTS -----------------
st.subheader("📈 Regime Comparison & Salary Breakdown")
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    df_compare = pd.DataFrame({"Regime": ["Old Regime", "New Regime"], "Tax Amount (₹)": [old_tax, new_tax]})
    fig_bar = px.bar(df_compare, x="Regime", y="Tax Amount (₹)", color="Regime",
                     text_auto='.2s', title="Tax Liability Comparison",
                     color_discrete_sequence=["#1E3A8A", "#10B981"])
    fig_bar.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=350)
    st.plotly_chart(fig_bar, use_container_width=True)

with chart_col2:
    selected_tax = new_tax if best_regime == "New Regime" else old_tax
    take_home = gross_income - selected_tax
    df_pie = pd.DataFrame({"Component": ["Take-Home", "Tax Paid"], "Amount (₹)": [take_home, selected_tax]})
    fig_pie = px.pie(df_pie, names="Component", values="Amount (₹)", 
                     title=f"Salary Breakdown ({best_regime})",
                     color_discrete_sequence=["#34D399", "#EF4444"], hole=0.4)
    fig_pie.update_layout(margin=dict(l=20, r=20, t=40, b=20), height=350)
    st.plotly_chart(fig_pie, use_container_width=True)

# ----------------- MONTHLY IN-HAND SECTION -----------------
st.write("---")
st.subheader("💵 In-Hand Monthly Salary Calculator")
chosen_tax = new_tax if best_regime == "New Regime" else old_tax

monthly_gross = gross_income / 12
monthly_tax = chosen_tax / 12
monthly_take_home = monthly_gross - monthly_tax

mc1, mc2, mc3 = st.columns(3)
mc1.markdown(f"<div class='custom-card' style='border-left-color:#6B7280;'><b>Monthly Gross</b><h2>₹{monthly_gross:,.2f}</h2></div>", unsafe_allow_html=True)
mc2.markdown(f"<div class='custom-card' style='border-left-color:#EF4444;'><b>Monthly Tax</b><h2>₹{monthly_tax:,.2f}</h2></div>", unsafe_allow_html=True)
mc3.markdown(f"<div class='custom-card' style='border-left-color:#34D399;'><b>Net Take-Home</b><h2>₹{monthly_take_home:,.2f}</h2></div>", unsafe_allow_html=True)

# ----------------- SMART ADVICE SYSTEM -----------------
st.write("---")
st.subheader("🔒 Smart Tax-Saving Optimization Insights")

st.info(f"📋 **Taxable Income Summary:** Old Regime Taxable Income is **₹{old_taxable:,}** | New Regime Taxable Income is **₹{new_taxable:,}**.")

if best_regime == "New Regime" and new_tax == 0:
    st.success("🎉 **Great News!** Aapki net taxable income New Regime ke ₹12 Lakhs rebate bracket ke andar aati hai, isliye aapko koi tax nahi dena padega!")
elif best_regime == "New Regime":
    st.info("💡 **Insight:** Aap New Regime me hain jisme basic investment exemptions nahi milti. Tax kam karne ke liye aap corporate standard NPS 80CCD(2) scheme ka benefit employer ke through claim kar sakte hain.")
else:
    st.warning("⚠️ **Tax Saving Opportunity Found:** Aap Old Regime me hain.")
    if investments_80c < 150000:
        shortfall = 150000 - investments_80c
        st.success(f"💡 **Action Item:** Agar aap Section 80C me **₹{shortfall:,}** aur invest karte hain, toh aapka tax aur kam ho jayega!")
