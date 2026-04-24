import streamlit as st
from inference.predict_freight import predict_freight_cost
from inference.predict_invoice_flag import predict_invoice_flag

st.set_page_config(
    page_title="Vendor Invoice Intelligence",
    page_icon="🧾",
    layout="wide"
)

st.markdown("""
<style>
    /* Base */
    [data-testid="stAppViewContainer"] {
        background: #0f1117;
        color: #e0e0e0;
    }
    [data-testid="stSidebar"] {
        background: #161b27;
        border-right: 1px solid #2a2f3e;
    }

    /* Cards */
    .card {
        background: #1a1f2e;
        border: 1px solid #2a2f3e;
        border-radius: 12px;
        padding: 28px 32px;
        margin-bottom: 20px;
    }

    /* Page title */
    .page-title {
        font-size: 2rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 4px;
    }
    .page-subtitle {
        font-size: 1rem;
        color: #7a8099;
        margin-bottom: 24px;
    }

    /* Section header */
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #a0aec0;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 16px;
    }

    /* Result boxes */
    .result-safe {
        background: #0d2b1f;
        border: 1px solid #1a6b45;
        border-radius: 10px;
        padding: 20px 24px;
        color: #4ade80;
        font-size: 1.1rem;
        font-weight: 600;
        text-align: center;
    }
    .result-flag {
        background: #2b0d0d;
        border: 1px solid #6b1a1a;
        border-radius: 10px;
        padding: 20px 24px;
        color: #f87171;
        font-size: 1.1rem;
        font-weight: 600;
        text-align: center;
    }
    .result-freight {
        background: #0d1f2b;
        border: 1px solid #1a4f6b;
        border-radius: 10px;
        padding: 20px 24px;
        color: #60a5fa;
        font-size: 1.3rem;
        font-weight: 700;
        text-align: center;
    }

    /* Inputs */
    [data-testid="stNumberInput"] input {
        background: #0f1117 !important;
        border: 1px solid #2a2f3e !important;
        border-radius: 8px !important;
        color: #e0e0e0 !important;
    }

    /* Button */
    [data-testid="stFormSubmitButton"] button {
        background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 10px 28px !important;
        font-weight: 600 !important;
        width: 100%;
        transition: opacity 0.2s;
    }
    [data-testid="stFormSubmitButton"] button:hover {
        opacity: 0.85 !important;
    }

    /* Sidebar radio */
    [data-testid="stRadio"] label {
        color: #a0aec0 !important;
        font-size: 0.95rem;
    }

    /* Divider */
    hr { border-color: #2a2f3e !important; }

    /* Hide default header */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🧾 Invoice Intelligence")
    st.markdown("<hr>", unsafe_allow_html=True)
    selected_model = st.radio(
        "Select Module",
        ["🚚 Freight Cost Prediction", "🚨 Invoice Risk Flagging"],
        label_visibility="collapsed"
    )
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style='color:#7a8099; font-size:0.85rem; line-height:1.8'>
    📋 Improved cost forecasting<br>
    📊 Reduced invoice anomalies<br>
    ⚙️ Faster finance operations
    </div>
    """, unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("<div class='page-title'>Vendor Invoice Intelligence Portal</div>", unsafe_allow_html=True)
st.markdown("<div class='page-subtitle'>AI-driven freight cost prediction & invoice risk flagging</div>", unsafe_allow_html=True)

# ── Freight Cost Prediction ───────────────────────────────────────────────────
if selected_model == "🚚 Freight Cost Prediction":
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>Freight Cost Prediction</div>", unsafe_allow_html=True)
    st.markdown("Predict freight cost from invoice value to support budgeting and vendor negotiations.")

    with st.form("freight_form"):
        dollars = st.number_input("💲 Invoice Dollars", min_value=1.0, value=18500.0)
        submitted = st.form_submit_button("Predict Freight Cost")

    if submitted:
        result = predict_freight_cost({"Dollars": [dollars]})["Predicted_Freight"][0]
        st.markdown(f"<div class='result-freight'>📦 Estimated Freight Cost &nbsp;|&nbsp; ${result:,.2f}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ── Invoice Risk Flagging ─────────────────────────────────────────────────────
else:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>Invoice Risk Flagging</div>", unsafe_allow_html=True)
    st.markdown("Detect invoices that require manual approval based on abnormal cost or delivery patterns.")

    with st.form("invoice_flag_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            invoice_quantity   = st.number_input("Invoice Quantity",    min_value=1,   value=50)
            freight            = st.number_input("Freight Cost",        min_value=0.0, value=1.73)
        with col2:
            invoice_dollars    = st.number_input("Invoice Dollars",     min_value=1.0, value=352.95)
            total_item_qty     = st.number_input("Total Item Quantity", min_value=1,   value=162)
        with col3:
            total_item_dollars = st.number_input("Total Item Dollars",  min_value=1.0, value=2476.0)

        submitted = st.form_submit_button("Evaluate Invoice Risk")

    if submitted:
        input_data = {
            "invoice_quantity":    [invoice_quantity],
            "invoice_dollars":     [invoice_dollars],
            "Freight":             [freight],
            "total_item_quantity": [total_item_qty],
            "total_item_dollars":  [total_item_dollars],
        }
        is_flagged = bool(predict_invoice_flag(input_data)["Predicted_Flag"][0])

        if is_flagged:
            st.markdown("<div class='result-flag'>🚨 Invoice requires MANUAL APPROVAL</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='result-safe'>✅ Invoice is SAFE for Auto-Approval</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
