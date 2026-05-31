import streamlit as st
import google.generativeai as genai
import pandas as pd
import matplotlib.pyplot as plt

# ==============================================================================
# 1. APPLICATION SETUP & THEME INITIALIZATION (CLEAN ENTERPRISE CREME)
# ==============================================================================
st.set_page_config(
    page_title="FiNav -  Personal Finance Navigator", 
    page_icon="💸", 
    layout="wide"
)


# Custom CSS for an ultra-clean, premium look with targeted element scoping
st.markdown("""
    <style>
    /* App Canvas: Crisp Off-White Cream */
    .stApp {
        background-color: #FDFBF7 !important;
        color: #0F172A !important;
    }
    
    /* Sidebar Layout: Deep Charcoal Solid */
    [data-testid="stSidebar"] {
        background-color: #1E232A !important;
    }
    
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] caption,
    [data-testid="stSidebar"] div {
        color: #FFFFFF !important;
        opacity: 1.0 !important;
    }
    
    /* Navigation Tabs: Professional Typographic Sizing */
    button[data-baseweb="tab"] p {
        color: #475569 !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        font-size: 0.85rem !important;
        letter-spacing: 0.05em;
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #047857 !important;
        font-weight: 700 !important;
    }
    .stTabs [aria-selected="true"] {
        border-bottom-color: #047857 !important;
    }
    
    label, .stMarkdown p, stCaption {
        color: #1E293B !important;
    }
    
    div.stButton > button:not([form]) {
        background-color: #059669 !important;
        border-color: #059669 !important;
        color: white !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 0.05em;
    }
    div.stButton > button:not([form]):hover {
        background-color: #047857 !important;
        border-color: #047857 !important;
    }
    
    div[data-testid="stForm"] button[data-testid="stBaseButton-secondaryFormSubmit"] {
        background-color: #059669 !important;
        color: #FFFFFF !important;
        border: 1px solid #059669 !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.05em !important;
        padding: 0.5rem 1.5rem !important;
        width: 100% !important;
        opacity: 1 !important;
        visibility: visible !important;
    }
    div[data-testid="stForm"] button[data-testid="stBaseButton-secondaryFormSubmit"]:hover {
        background-color: #047857 !important;
        border-color: #047857 !important;
        color: #FFFFFF !important;
    }
    
    div.stDownloadButton > button {
        background-color: #1E293B !important;
        color: #FFFFFF !important;
        border: 1px solid #1E293B !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        font-size: 0.8rem !important;
        letter-spacing: 0.05em !important;
        width: 100% !important;
        opacity: 1 !important;
    }
    div.stDownloadButton > button:hover {
        background-color: #0F172A !important;
        border-color: #0F172A !important;
        color: #FFFFFF !important;
    }
    div.stButton > button[id^="delete_row_"] {
        background-color: #059669 !important;
        color: white !important;
        border: 1px solid #059669 !important;
        font-size: 0.75rem !important;
        padding: 0.2rem 0.5rem !important;
    }
    
    /* Structured Metric Blocks: High-Contrast Emerald */
    .metric-box { 
        background-color: #047857 !important; 
        padding: 22px; 
        border-radius: 8px; 
        border: 1px solid #059669; 
        text-align: left;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
    }
    .metric-box span {
        color: #A7F3D0 !important; 
        font-size: 0.8rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-box h3 { 
        color: #FFFFFF !important; 
        font-weight: 700 !important; 
        font-size: 2.2rem !important;
        margin: 6px 0 0 0 !important;
    }
    /* High Contrast Wealth Accumulation Output Card */
    .wealth-display-card {
        background-color: #FFFFFF !important;
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .wealth-display-card .card-label {
        color: #64748B !important;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .wealth-display-card .card-value {
        color: #1E40AF !important;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        margin: 8px 0 !important;
        line-height: 1.0;
    }
    .wealth-display-card .card-delta {
        color: #059669 !important;
        font-size: 0.85rem;
        font-weight: 500;
    }
    div[data-testid="stNotificationText"] p, div[data-testid="stNotificationText"] {
        color: #1E293B !important;
        font-weight: 500 !important;
    }
    .main-title { 
        color: #065F46; 
        font-weight: 800; 
        letter-spacing: -0.02em;
    }
    </style>
""", unsafe_allow_html=True)

# Secure API Configuration
GEMINI_API_KEY = "AQ.Ab8RN6KrTEZK_8rX7TSF7OlxxZ-DyOjFP5yqJHALMbuow6LSvw"

if GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
    st.error("API Key Missing: Please replace the placeholder string with your key.")
    st.stop()

genai.configure(api_key=GEMINI_API_KEY)
ai_model = genai.GenerativeModel('gemini-3.5-flash')

# ==============================================================================
# 2. RUNTIME STATE MANAGEMENT
# ==============================================================================
if "expense_log" not in st.session_state:
    st.session_state.expense_log = pd.DataFrame([
        {"Category": "Housing", "Description": "Monthly Rent / Lease", "Amount": 1200.0},
        {"Category": "Groceries", "Description": "Supermarket Supplies", "Amount": 350.0},
        {"Category": "Utilities", "Description": "Electricity & Web Infrastructure", "Amount": 180.0},
        {"Category": "Entertainment", "Description": "Streaming Plans & Dining", "Amount": 150.0},
    ])

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ==============================================================================
# 3. GLOBAL USER PROFILE SIDEBAR 
# ==============================================================================
with st.sidebar:
    st.markdown("### Global Financial Profile")
    st.markdown("<p style='color: #FFFFFF !important; opacity: 1.0 !important;'>Establish operational baseline metrics across system models.</p>", unsafe_allow_html=True)
    
    monthly_income = st.number_input("Monthly Net Income ($)", min_value=1.0, value=4500.0, step=100.0)
    savings_target = st.number_input("Target Monthly Savings ($)", min_value=1.0, value=1000.0, step=50.0)
    investment_risk = st.selectbox("Investment Risk Tolerance", ["Conservative", "Moderate", "Aggressive"])
    
    st.divider()
    st.markdown("### Architecture Specs")
    st.markdown("""
    <div style='color: #FFFFFF !important; opacity: 1.0 !important; font-size: 0.85rem; line-height: 1.6;'>
        <b>Deployment Context:</b> Hugging Face Spaces<br><br>
        <b>Data Core:</b> SessionState Cache<br><br>
        <b>Core Intelligence:</b> Gemini 3.5 Flash Engine
    </div>
    """, unsafe_allow_html=True)

# ==============================================================================
# 4. PRIMARY NAVIGATION DASHBOARD & FUNCTIONAL PIPELINES
# ==============================================================================
st.markdown("<h1 class='main-title'>FiNav: Personal Finance Navigator</h1>", unsafe_allow_html=True)
st.markdown("##### Real-time automated financial auditing, dynamic budgeting vectors, and conversational predictive wealth advisory.")
st.write("")

tab_planner, tab_expenses, tab_advisor, tab_investment = st.tabs([
    "Strategic Planner", 
    "Expense Matrix", 
    "AI Strategy Advisor", 
    "Predictive Growth"
])

# ------------------------------------------------------------------------------
# TAB 1: STRATEGIC BUDGET PLANNER
# ------------------------------------------------------------------------------
with tab_planner:
    st.subheader("Budget Allocation Metrics & Structural Health")
    
    total_expenses = st.session_state.expense_log["Amount"].sum()
    net_remaining = monthly_income - total_expenses
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-box'><span>Total Monthly Inflow</span><h3>${monthly_income:,.2f}</h3></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-box'><span>Logged Operational Outflow</span><h3>${total_expenses:,.2f}</h3></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-box'><span>Net Liquid Capital</span><h3>${net_remaining:,.2f}</h3></div>", unsafe_allow_html=True)
        
    st.write("")
    
    st.markdown("#### Monthly Savings Goal Progress")
    progress_percentage = min(max(net_remaining / savings_target, 0.0), 1.0)
    
    if net_remaining >= savings_target:
        st.success(f"System Notification: Current surplus of ${net_remaining:,.2f} meets or exceeds the designated target savings target baseline of ${savings_target:,.2f}.")
    else:
        st.progress(progress_percentage)
        st.info(f"Progress Tracking: ${net_remaining:,.2f} preserved out of your ${savings_target:,.2f} goal requirement.")
        
    st.write("")
    col_chart, col_audit = st.columns([1, 1])
    
    with col_chart:
        st.markdown("#### Allocation Distribution")
        if not st.session_state.expense_log.empty:
            chart_data = st.session_state.expense_log.groupby("Category")["Amount"].sum()
            if net_remaining > 0:
                chart_data["Unallocated Savings"] = net_remaining
                
            fig, ax = plt.subplots(figsize=(5, 4), facecolor='none')
            ax.pie(chart_data, labels=chart_data.index, autopct='%1.1f%%', startangle=140, colors=['#064E3B', '#047857', '#059669', '#10B981', '#34D399', '#A7F3D0'])
            ax.axis('equal')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()
            
    with col_audit:
        st.markdown("#### Automated System Allocation Audit")
        if st.button("Execute Core Financial Audit", type="primary"):
            with st.spinner("Compiling profile allocation matrices..."):
                prompt = f"""
                You are a Senior Chartered Financial Analyst (CFA). Audit this financial profile:
                - Gross Monthly Income: ${monthly_income}
                - Real-time Logged Expenses: ${total_expenses}
                - Net Disposable Capital: ${net_remaining}
                - Stated Savings Goal Target: ${savings_target}
                
                Provide a structured executive audit statement in Markdown. Include exactly these headers:
                ### Portfolio Health Assessment
                Rate their spending model efficiency from 1 to 100 with clear, data-backed reasoning. Do not use any emojis in your response.
                ### High-Impact Optimization Tactics
                Provide exactly 2 highly customized cost reduction workflows to help them securely hit their {savings_target} requirement. Do not use any emojis in your response.
                """
                response = ai_model.generate_content(prompt)
                st.markdown(response.text)

# ------------------------------------------------------------------------------
# TAB 2: EXPENSE AUDIT MATRIX
# ------------------------------------------------------------------------------
with tab_expenses:
    st.subheader("Granular Transaction Ledger & Entry Controls")
    col_input, col_table = st.columns([1, 2])
    
    with col_input:
        st.markdown("##### Commit New Ledger Line Entry")
        with st.form("transaction_entry_form", clear_on_submit=True):
            category = st.selectbox("Expense Class", ["Housing", "Groceries", "Utilities", "Entertainment", "Insurance", "Misc"])
            description = st.text_input("Line-Item Description", placeholder="e.g., Target department run")
            amount = st.number_input("Transaction Value ($)", min_value=0.01, step=5.0)
            
            submitted = st.form_submit_button("Commit Entry")
            if submitted:
                new_row = {"Category": category, "Description": description, "Amount": amount}
                st.session_state.expense_log = pd.concat([st.session_state.expense_log, pd.DataFrame([new_row])], ignore_index=True)
                st.rerun()
                
        st.divider()
        st.markdown("##### Ledger Data Extraction")
        csv_export_bytes = st.session_state.expense_log.to_csv(index=False)
        st.download_button(
            label="Export Ledger Report (CSV)",
            data=csv_export_bytes,
            file_name="finai_expense_ledger_report.csv",
            mime="text/csv"
        )
                
    with col_table:
        st.markdown("##### Operational Transaction Stream Caches")
        
        if not st.session_state.expense_log.empty:
            for index, row in st.session_state.expense_log.iterrows():
                col_data, col_delete = st.columns([5, 1])
                col_data.write(f"**[{row['Category']}]** {row['Description']} — ${row['Amount']:,.2f}")
                if col_delete.button("Remove", key=f"delete_row_{index}"):
                    st.session_state.expense_log = st.session_state.expense_log.drop(index).reset_index(drop=True)
                    st.rerun()
        else:
            st.info("The local transaction cache is completely empty. Input entries to populate.")
            
        if st.button("Purge Session Cache Memory"):
            st.session_state.expense_log = pd.DataFrame(columns=["Category", "Description", "Amount"])
            st.rerun()

# ------------------------------------------------------------------------------
# TAB 3: CONVERSATIONAL AI STRATEGY ADVISOR
# ------------------------------------------------------------------------------
with tab_advisor:
    st.subheader("Conversational Financial Analytics Pipeline")
    
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    if user_query := st.chat_input("Inquire regarding structural investment vectors, micro-cost reduction, or tax optimization..."):
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        
        engineered_context = f"""
        Persona Role: Senior Enterprise Financial Advisor.
        Active Operational Metadata Parameters: Gross Income ${monthly_income}, Outflows: ${total_expenses}, Savings Strategy Metric: {savings_target}.
        User Query Objective: {user_query}
        Provide highly professional, rigorous analytical frameworks in clear English. Do not use emojis anywhere in your answer. Clearly disclaim that your outputs represent informational structures rather than certified asset management mandates.
        """
        
        with st.chat_message("assistant"):
            with st.spinner("Processing tactical scenario variables..."):
                response = ai_model.generate_content(engineered_context)
                st.markdown(response.text)
        st.session_state.chat_history.append({"role": "assistant", "content": response.text})

# ------------------------------------------------------------------------------
# TAB 4: PREDICTIVE WEALTH HORIZON
# ------------------------------------------------------------------------------
with tab_investment:
    st.subheader("Predictive Horizon Valuations & Compound Accumulation Curves")
    col_inv_inputs, col_inv_outputs = st.columns([1, 1])
    
    with col_inv_inputs:
        st.markdown("##### Portfolio Micro-Growth Parameters")
        horizon_years = st.slider("Investment Allocation Horizon (Years)", min_value=1, max_value=30, value=10)
        expected_yield = st.slider("Target Compound Annual Yield Assumptions (%)", min_value=1.0, max_value=15.0, value=7.0, step=0.5)
        
        annual_contribution_base = max(0.0, net_remaining) * 12
        
        horizon_years_list = list(range(0, horizon_years + 1))
        portfolio_trajectory_valuation = [0.0]
        
        for current_year in range(1, horizon_years + 1):
            compounded_value = (portfolio_trajectory_valuation[-1] + annual_contribution_base) * (1 + (expected_yield / 100))
            portfolio_trajectory_valuation.append(compounded_value)
            
        final_extrapolated_wealth = portfolio_trajectory_valuation[-1]
            
    with col_inv_outputs:
        st.markdown("##### Extrapolated Yield Capitalization Runways")
        
        # Output card solid contrast
        st.markdown(f"""
        <div class="wealth-display-card">
            <div class="card-label">Modeled Future Horizon Wealth Balance</div>
            <div class="card-value">${final_extrapolated_wealth:,.2f}</div>
            <div class="card-delta">↑ Based on recurring ${annual_contribution_base:,.2f}/yr deposits</div>
        </div>
        """, unsafe_allow_html=True)
        
        fig_line, ax_line = plt.subplots(figsize=(6, 3.5), facecolor='none')
        ax_line.plot(horizon_years_list, portfolio_trajectory_valuation, marker='o', color='#059669', linewidth=2)
        ax_line.set_xlabel("Timeline Horizon Vector (Years)", color='#1E293B')
        ax_line.set_ylabel("Portfolio Capital Valuation Base ($)", color='#1E293B')
        ax_line.set_title("Extrapolated Compound Capital Growth Curve", color='#1E293B', fontweight='bold')
        ax_line.grid(True, linestyle='--', alpha=0.5)
        ax_line.set_facecolor('#FDFBF7')
        plt.tight_layout()
        st.pyplot(fig_line)
        plt.close()
        
        if st.button("Generate Asset Allocation Map"):
            with st.spinner("Analyzing market trajectories..."):
                asset_prompt = f"""
                You are a Managing Director of Portfolio Optimization. Evaluate this specific tracking matrix profile:
                - Timeline Allocation Target Horizon: {horizon_years} Years
                - Target Return Allocation Requirements: {expected_yield}% Annually
                - Designated Operational Profile Risk Class: {investment_risk}
                - Modeled Capital Accumulation Asset Base at Horizon: ${final_extrapolated_wealth:,.2f}
                
                Detail a macroeconomic asset-class distribution layout model (e.g., precise percentage allocations across Equities, Fixed Income Bonds, sovereign Treasuries) tailored precisely for a portfolio structured inside a {investment_risk} strategy profile. Do not use emojis in your response.
                """
                response_investment = ai_model.generate_content(asset_prompt)
                st.info(f"Target Asset Allocation Strategy Framework: {investment_risk}")
                st.markdown(response_investment.text)

st.markdown("---")