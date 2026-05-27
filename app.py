import streamlit as st
import plotly.graph_objects as go

# --- SYSTEM CONFIGURATION & THEMING ---
st.set_page_config(
    page_title="ProTaxCalc AI - Premium Indian Tax Optimization Suite",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Styling
st.markdown("""
    <style>
    .main-header { font-size:42px !important; font-weight: 800; color: #1E3A8A; margin-bottom: 5px; }
    .sub-header { font-size:18px !important; color: #4B5563; margin-bottom: 30px; }
    .card { padding: 24px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); background-color: #FFFFFF; border: 1px solid #E5E7EB; margin-bottom: 20px; }
    .metric-title { font-size: 14px; font-weight: 600; color: #6B7280; text-transform: uppercase; }
    .metric-value { font-size: 28px; font-weight: 700; color: #111827; }
    </style>
    """, unsafe_allow_html=True)

# --- CORE COMPUTATIONAL TAX ENGINES ---
def calculate_new_regime_tax(gross_salary: float, new_regime_deductions: float = 0.0) -> dict:
    standard_deduction = 75000.0
    net_income = max(0.0, gross_salary - standard_deduction - new_regime_deductions)
    
    slabs = [
        (400000, 0.00), (800000, 0.05), (1200000, 0.10),
        (1600000, 0.15), (2000000, 0.20), (2400000, 0.25), (float('inf'), 0.30)
    ]
    
    base_tax = 0.0
    previous_limit = 0.0
    for limit, rate in slabs:
        if net_income > previous_limit:
            taxable_in_slab = min(net_income, limit) - previous_limit
            base_tax += taxable_in_slab * rate
            previous_limit = limit
        else:
            break
            
    rebate = min(base_tax, 60000.0) if net_income <= 1200000.0 else 0.0
    tax_after_rebate = max(0.0, base_tax - rebate)
    cess = tax_after_rebate * 0.04
    
    return {
        "net_income": net_income, "base_tax": base_tax, "rebate": rebate,
        "cess": cess, "total": round(tax_after_rebate + cess)
    }

def calculate_old_regime_tax(gross_salary: float, old_regime_deductions: float = 0.0) -> dict:
    standard_deduction = 50000.0
    net_income = max(0.0, gross_salary - standard_deduction - old_regime_deductions)
    
    slabs = [(250000, 0.00), (500000, 0.05), (1000000, 0.20), (float('inf'), 0.30)]
    
    base_tax = 0.0
    previous_limit = 0.0
    for limit, rate in slabs:
        if net_income > previous_limit:
            taxable_in_slab = min(net_income, limit) - previous_limit
            base_tax += taxable_in_slab * rate
            previous_limit = limit
        else:
            break
            
    rebate = min(base_tax, 12500.0) if net_income <= 500000.0 else 0.0
    tax_after_rebate = max(0.0, base_tax - rebate)
    cess = tax_after_rebate * 0.04
    
    return {
        "net_income": net_income, "base_tax": base_tax, "rebate": rebate,
        "cess": cess, "total": round(tax_after_rebate + cess)
    }

# --- COMMERCIAL SAAS SIDEBAR & MONETIZATION ---
with st.sidebar:
    st.markdown("<div style='font-size:22px; font-weight:700; color:#1E3A8A;'>🔒 Premium Access Tier</div>", unsafe_allow_html=True)
    st.info("💡 You are currently presenting the Premium Enterprise Tax Calculator model.")
    
    # Monetization Widget
    st.markdown("---")
    st.markdown("### 💳 Upgrade Your Account")
    st.markdown("Unlock bulk CSV employee processing, professional PDF report generation, and corporate tax structuring modules.")
    if st.button("🌟 Upgrade to Pro License", use_container_width=True):
        st.link_button("Proceed to Secure Payment Gateway", "https://stripe.com") # Update with your stripe payment link
    st.markdown("---")
    st.caption("Powered by ProTaxCalc AI Engines © 2026. All rights reserved.")

# --- APPLICATION INTERFACE ---
st.markdown("<div class='main-header'>💰 ProTaxCalc AI Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Real-time Indian Income Tax optimization and comparison module</div>", unsafe_allow_html=True)

# Layout Split: Inputs on left, Outputs on right
col_input, col_output = st.columns([1, 2], gap="large")

with col_input:
    st.markdown("### 📊 Enter Financial Profiles")
    
    # Financial Inputs
    gross_input = st.number_input("Annual Gross Salary Income (₹)", min_value=0, max_value=100000000, value=1898492, step=25000)
    
    st.markdown("#### Old Regime Investment Proofs")
    old_ded_input = st.slider("Total Deductions (80C, 80D, HRA, Interest) (₹)", min_value=0, max_value=1000000, value=250000, step=5000)
    
    st.markdown("#### New Regime Allowed Perks")
    new_ded_input = st.slider("Corporate NPS Contribution Deductions (80CCD(2)) (₹)", min_value=0, max_value=500000, value=50000, step=5000)

# Calculate responses instantly
res_new = calculate_new_regime_tax(gross_input, new_ded_input)
res_old = calculate_old_regime_tax(gross_input, old_ded_input)
savings = abs(res_old['total'] - res_new['total'])
best_regime = "New Regime" if res_new['total'] < res_old['total'] else "Old Regime"

with col_output:
    st.markdown("### ⚡ Optimization Assessment")
    
    # Optimization Summary Card
    if res_new['total'] != res_old['total']:
        st.success(f"🎉 **Recommendation:** You save **₹{savings:,}** by selecting the **{best_regime}** this assessment cycle.")
    else:
        st.info("🤝 **Recommendation:** Both frameworks create matching bottom-line tax liabilities.")
        
    # Visual KPI Matrix Layout
    kpi_col1, kpi_col2, kpi_col3 = st.columns(3)
    with kpi_col1:
        st.markdown(f"<div class='card'><span class='metric-title'>🟢 New Regime Payable</span><br><span class='metric-value'>₹{res_new['total']:,}</span></div>", unsafe_allow_html=True)
    with kpi_col2:
        st.markdown(f"<div class='card'><span class='metric-title'>🔵 Old Regime Payable</span><br><span class='metric-value'>₹{res_old['total']:,}</span></div>", unsafe_allow_html=True)
    with kpi_col3:
        st.markdown(f"<div class='card'><span class='metric-title'>🔥 Maximum Savings</span><br><span class='metric-value' style='color:#10B981;'>₹{savings:,}</span></div>", unsafe_allow_html=True)

    # Graphical Comparison Chart
    fig = go.Figure(data=[
        go.Bar(name='New Regime', x=['Net Taxable Income', 'Final Payable Tax'], y=[res_new['net_income'], res_new['total']], marker_color='#10B981'),
        go.Bar(name='Old Regime', x=['Net Taxable Income', 'Final Payable Tax'], y=[res_old['net_income'], res_old['total']], marker_color='#1E3A8A')
    ])
    fig.update_layout(barmode='group', height=350, title_text="Side-by-Side Financial Evaluation Matrix", margin=dict(t=40, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)
