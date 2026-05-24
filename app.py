import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Uber Eats SL Analytics",
    page_icon="🛵",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={}
)

# ========== CUSTOM LOADER ==========
st.markdown("""
<style>
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .custom-loader {
        border: 3px solid #f3f3f3;
        border-top: 3px solid #06C167;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
</style>
""", unsafe_allow_html=True)

# ========== UBER EATS BRAND CSS ==========
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800;1,9..40,400&display=swap');

    * { font-family: 'DM Sans', sans-serif !important; }

    .stApp { background-color: #F6F6F6 !important; }

    /* ---- FORCE SIDEBAR ALWAYS OPEN ---- */
    section[data-testid="stSidebar"] {
        transform: none !important;
        visibility: visible !important;
        display: block !important;
        min-width: 240px !important;
        width: 240px !important;
    }
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="collapsedControl"] {
        display: none !important;
        visibility: hidden !important;
    }
    .stAppDeployButton { display: none !important; }
    section[data-testid="stSidebar"][aria-expanded="false"] {
        margin-left: 0 !important;
        transform: none !important;
    }

    #MainMenu, footer, header { visibility: hidden; }

    .block-container {
        padding: 1.6rem 2rem !important;
        max-width: 1400px !important;
        background-color: #F6F6F6 !important;
    }

    /* ---- SIDEBAR ---- */
    section[data-testid="stSidebar"] {
        background: #0D0D0D !important;
        border-right: 2px solid #06C167 !important;
        min-width: 240px !important;
        width: 240px !important;
    }

    section[data-testid="stSidebar"] * {
        color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] {
        background-color: #1A1A1A !important;
        border: 1px solid #06C167 !important;
        border-radius: 8px !important;
    }
    section[data-testid="stSidebar"] div[data-baseweb="select"] * {
        color: #FFFFFF !important;
        background-color: #1A1A1A !important;
    }

    section[data-testid="stSidebar"] span[data-baseweb="tag"] {
        background-color: #06C167 !important;
        color: #000000 !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
    }
    section[data-testid="stSidebar"] span[data-baseweb="tag"] * {
        color: #000000 !important;
    }

    section[data-testid="stSidebar"] .stRadio label {
        color: #CCCCCC !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        padding: 0.45rem 0.9rem !important;
        border-radius: 8px !important;
        transition: all 0.15s ease !important;
        background: transparent !important;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        background: #1A1A1A !important;
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] .stRadio [aria-checked="true"] + label,
    section[data-testid="stSidebar"] .stRadio label[data-selected="true"] {
        background: #06C167 !important;
        color: #000000 !important;
        font-weight: 700 !important;
    }

    section[data-testid="stSidebar"] .stCaption {
        color: #757575 !important;
    }

    /* ---- SIDEBAR COLLAPSE BUTTON ---- */
    button[data-testid="collapsedControl"],
    button[data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapsedControl"] > button,
    [data-testid="collapsedControl"] {
        background-color: #06C167 !important;
        color: #000000 !important;
        border-radius: 0 10px 10px 0 !important;
        width: 32px !important;
        min-width: 32px !important;
        height: 56px !important;
        opacity: 1 !important;
        visibility: visible !important;
        z-index: 999999 !important;
        font-size: 0px !important;
    }
    [data-testid="stSidebarCollapsedControl"]::after,
    [data-testid="collapsedControl"]::after {
        content: "▶" !important;
        font-size: 16px !important;
        color: #000000 !important;
    }
    [data-testid="stSidebarCollapsedControl"] svg,
    [data-testid="collapsedControl"] svg {
        display: none !important;
    }

    /* ---- METRIC CARDS ---- */
    [data-testid="metric-container"] {
        background: #FFFFFF !important;
        border: 1px solid #E5E5E5 !important;
        border-left: 4px solid #06C167 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(6,193,103,0.15) !important;
    }
    [data-testid="metric-container"] label {
        font-size: 0.68rem !important;
        font-weight: 700 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.07em !important;
        color: #555555 !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        color: #1A1A1A !important;
    }
    [data-testid="stMetricLabel"] {
        color: #555555 !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        color: #1A1A1A !important;
    }

    /* ---- DASHBOARD HEADER ---- */
    .dashboard-header {
        background: #0D0D0D;
        border-radius: 14px;
        padding: 1.2rem 1.8rem;
        margin-bottom: 1.6rem;
        display: flex;
        align-items: center;
        gap: 1.2rem;
        border: 1px solid #222222;
    }
    .header-icon {
        background: #06C167;
        width: 52px;
        height: 52px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 26px;
        flex-shrink: 0;
    }
    .header-title {
        font-size: 1.45rem !important;
        font-weight: 800 !important;
        color: #FFFFFF !important;
        margin: 0 !important;
        letter-spacing: -0.3px;
    }
    .header-subtitle {
        font-size: 0.78rem !important;
        color: #757575 !important;
        margin-top: 3px !important;
    }

    /* ---- INSIGHT / WARNING BOXES ---- */
    .insight-box {
        background: #E8FAF0;
        border-left: 4px solid #06C167;
        border-radius: 10px;
        padding: 0.85rem 1.1rem;
        margin: 0.8rem 0;
        font-size: 0.84rem;
        line-height: 1.6;
        color: #0D2818 !important;
    }
    .insight-box * { color: #0D2818 !important; }

    .warning-box {
        background: #FFF0EE;
        border-left: 4px solid #FF3B30;
        border-radius: 10px;
        padding: 0.85rem 1.1rem;
        margin: 0.8rem 0;
        font-size: 0.84rem;
        line-height: 1.6;
        color: #4A1410 !important;
    }
    .warning-box * { color: #4A1410 !important; }

    /* ---- SECTION LABELS ---- */
    .section-label {
        font-size: 0.65rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #06C167;
        margin-bottom: 2px;
    }
    .section-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #0D0D0D;
        margin-bottom: 0.7rem;
    }

    /* ---- DIVIDER ---- */
    .custom-divider {
        margin: 1.2rem 0;
        border: none;
        border-top: 1px solid #E5E5E5;
    }

    /* ---- CHART CONTAINERS ---- */
    [data-testid="stPlotlyChart"] {
        background: #FFFFFF !important;
        border-radius: 12px !important;
        border: 1px solid #E5E5E5 !important;
        padding: 0.5rem !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
    }

    /* ---- DATAFRAME ---- */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid #E5E5E5 !important;
    }
    .stDataFrame * { color: #1A1A1A !important; }

    /* ---- MAIN CONTENT TEXT ---- */
    .stMarkdown p, .stMarkdown li { color: #1A1A1A !important; }

    /* ---- SCROLLBAR ---- */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: #F6F6F6; }
    ::-webkit-scrollbar-thumb { background: #06C167; border-radius: 4px; }

    /* ---- ADDITIONAL POLISH ---- */
    
    /* Smooth transitions for interactive elements */
    .stButton > button, .stSelectbox > div, .stMultiselect > div {
        transition: all 0.2s ease !important;
    }
    
    /* Button hover effects */
    .stButton > button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(6,193,103,0.25) !important;
    }
    
    /* Tab styling if you use tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important;
        background: transparent !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #06C167 !important;
        color: #000000 !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #FFFFFF !important;
        border-radius: 10px !important;
        border: 1px solid #E5E5E5 !important;
        font-weight: 600 !important;
    }
    .streamlit-expanderHeader:hover {
        border-color: #06C167 !important;
    }
    
    /* Success/Info/Warning message overrides */
    .stAlert {
        border-radius: 10px !important;
        border-left: 4px solid #06C167 !important;
    }
    .stAlert > div {
        background-color: #E8FAF0 !important;
    }
    
    /* Dataframe hover effect */
    .dataframe tbody tr:hover {
        background-color: #F0FCF5 !important;
    }
    
    /* Loading spinner brand color */
    .stSpinner > div {
        border-top-color: #06C167 !important;
    }
    
    /* Number input styling */
    .stNumberInput input {
        border-radius: 8px !important;
        border: 1px solid #E5E5E5 !important;
    }
    .stNumberInput input:focus {
        border-color: #06C167 !important;
        box-shadow: 0 0 0 2px rgba(6,193,103,0.2) !important;
    }
    
    /* Selectbox dropdown */
    div[data-baseweb="select"] > div {
        border-radius: 8px !important;
        border-color: #E5E5E5 !important;
    }
    div[data-baseweb="select"] > div:hover {
        border-color: #06C167 !important;
    }
    
    /* Radio button group styling */
    .stRadio > div {
        gap: 12px !important;
    }
    
    /* Checkbox styling */
    .stCheckbox label span {
        border-radius: 4px !important;
    }
    .stCheckbox label span:hover {
        border-color: #06C167 !important;
    }
    
    /* Tooltip styling */
    [data-testid="stTooltipContent"] {
        background-color: #0D0D0D !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        font-size: 12px !important;
    }
    
    /* Date input */
    .stDateInput input {
        border-radius: 8px !important;
        border: 1px solid #E5E5E5 !important;
    }
    
    /* Status badges (if you add any) */
    .badge-green {
        background-color: #E8FAF0;
        color: #06C167;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-red {
        background-color: #FFF0EE;
        color: #FF3B30;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
    }
    .badge-orange {
        background-color: #FFF4E6;
        color: #FF9500;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Animation for metric cards on load */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    [data-testid="metric-container"] {
        animation: fadeInUp 0.4s ease-out;
    }
    
    /* Responsive adjustments for mobile */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem !important;
        }
        [data-testid="metric-container"] {
            padding: 0.75rem !important;
        }
        [data-testid="stMetricValue"] {
            font-size: 1.4rem !important;
        }
        .dashboard-header {
            padding: 0.8rem 1.2rem !important;
        }
        .header-title {
            font-size: 1.1rem !important;
        }
    }
    
    /* Print styles (if needed) */
    @media print {
        .stApp {
            background: white !important;
        }
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        [data-testid="stMetricValue"] {
            color: black !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# ========== BRAND COLORS ==========
GREEN       = "#06C167"
GREEN_DARK  = "#05A259"
GREEN_LIGHT = "#A8E6C8"
BLACK       = "#0D0D0D"
WHITE       = "#FFFFFF"
GRAY_MID    = "#757575"
GRAY_LIGHT  = "#F6F6F6"
RED         = "#FF3B30"
ORANGE      = "#FF9500"
TEXT_DARK   = "#1A1A1A"
TEXT_MID    = "#444444"

BRAND_SEQ = [GREEN, GREEN_DARK, "#09D97A", "#04875C", GREEN_LIGHT, "#C8F5E0"]
MULTI_SEQ = [GREEN, BLACK, ORANGE, RED, "#5E5CE6", "#30D158"]

# ========== HELPER FUNCTIONS ==========
def display_header(icon, title, subtitle):
    st.markdown(f"""
    <div class="dashboard-header">
        <div class="header-icon">{icon}</div>
        <div>
            <div class="header-title">{title}</div>
            <div class="header-subtitle">{subtitle}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def insight(text):
    st.markdown(f'<div class="insight-box">💡 <strong>Insight:</strong> {text}</div>', unsafe_allow_html=True)

def warning(text):
    st.markdown(f'<div class="warning-box">⚠️ <strong>Alert:</strong> {text}</div>', unsafe_allow_html=True)

def section(label, title):
    st.markdown(f'<div class="section-label">{label}</div><div class="section-title">{title}</div>', unsafe_allow_html=True)

def divider():
    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

def chart_layout(fig, height=380, legend_top=False, dark_bg=False):
    bg         = BLACK if dark_bg else WHITE
    text_color = WHITE if dark_bg else TEXT_DARK
    grid_color = "#333333" if dark_bg else "#F0F0F0"
    line_color = "#444444" if dark_bg else "#E0E0E0"

    fig.update_layout(
        plot_bgcolor=bg,
        paper_bgcolor=bg,
        font=dict(family="DM Sans", size=12, color=text_color),
        margin=dict(t=48, b=28, l=16, r=16),
        height=height,
        hoverlabel=dict(bgcolor=BLACK, font_size=12, font_family="DM Sans",
                        font_color=WHITE, bordercolor=GREEN),
        xaxis=dict(showgrid=True, gridcolor=grid_color, linecolor=line_color,
                   tickfont=dict(color=text_color, size=11),
                   title_font=dict(color=text_color, size=12), zeroline=False),
        yaxis=dict(showgrid=True, gridcolor=grid_color, linecolor=line_color,
                   tickfont=dict(color=text_color, size=11),
                   title_font=dict(color=text_color, size=12), zeroline=False),
    )
    if legend_top:
        fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02,
                                      xanchor="left", x=0,
                                      font=dict(color=text_color, size=11),
                                      bgcolor="rgba(0,0,0,0)"))
    else:
        fig.update_layout(legend=dict(font=dict(color=text_color, size=11)))

    for trace in fig.data:
        if hasattr(trace, 'textfont'):
            trace.textfont = dict(color=text_color, size=11, family="DM Sans")
        if hasattr(trace, 'textposition') and trace.textposition not in [None, "none"]:
            if hasattr(trace, 'orientation'):
                trace.textposition = "outside"
            trace.textfont = dict(color=TEXT_DARK, size=11, family="DM Sans")
        if hasattr(trace, 'marker') and hasattr(trace.marker, 'line'):
            trace.marker.line = dict(color=bg, width=1)
    return fig

# ========== DATA LOADING ==========
@st.cache_data
def load_data():
    conn        = sqlite3.connect("data/uber_eats_sl.db")
    orders      = pd.read_sql("SELECT * FROM orders", conn)
    restaurants = pd.read_sql("SELECT * FROM restaurants", conn)
    drivers     = pd.read_sql("SELECT * FROM drivers", conn)
    pricing     = pd.read_sql("SELECT * FROM pricing_history", conn)
    conn.close()

    orders["order_date"] = pd.to_datetime(orders["order_date"])
    orders["month"]      = orders["order_date"].dt.strftime("%Y-%m")
    orders["month_num"]  = orders["order_date"].dt.month
    orders["dow"]        = orders["order_date"].dt.day_name()
    orders["hour"]       = orders["order_hour"]
    return orders, restaurants, drivers, pricing

orders, restaurants, drivers, pricing = load_data()

try:
    churn_df = pd.read_csv("data/sql_results/churn_predictions.csv")
except FileNotFoundError:
    churn_df = None

# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("""
    <div style="padding: 1rem 0 0.5rem 0;">
        <div style="display:flex; align-items:center; gap:12px; margin-bottom:8px;">
            <div style="background:#06C167; width:44px; height:44px; border-radius:12px;
                        display:flex; align-items:center; justify-content:center; font-size:22px;">🛵</div>
            <div>
                <div style="font-weight:800; font-size:17px; color:#FFFFFF; letter-spacing:-0.3px;">Uber Eats SL</div>
                <div style="font-size:11px; color:#757575; margin-top:2px;">Analytics Platform</div>
            </div>
        </div>
    </div>
    <hr style="border-color:#222222; margin:10px 0 14px 0;">
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigation",
        ["📊 Marketplace", "💰 Revenue & Pricing", "🏪 Restaurants", "🚴 Driver Ops", "⚠️ Churn Risk"],
        label_visibility="collapsed"
    )

    st.markdown('<hr style="border-color:#222222; margin:16px 0 12px 0;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.1em; color:#06C167; margin-bottom:10px;">🔍 Filters</div>', unsafe_allow_html=True)

    all_zones = sorted(restaurants["zone"].unique())
    all_tiers = sorted(restaurants["pricing_tier"].unique())

    selected_zones = st.multiselect("Zone", all_zones, default=all_zones[:3] if len(all_zones) > 3 else all_zones)
    selected_tiers = st.multiselect("Pricing Tier", all_tiers, default=all_tiers)

    st.markdown('<hr style="border-color:#222222; margin:16px 0 10px 0;">', unsafe_allow_html=True)
    st.caption("Uber Eats Sri Lanka · 2024 Data")

# ========== FILTER DATA ==========
filtered_restaurants = restaurants[
    restaurants["zone"].isin(selected_zones) &
    restaurants["pricing_tier"].isin(selected_tiers)
]
filtered_orders  = orders[orders["restaurant_id"].isin(filtered_restaurants["restaurant_id"])]
delivered_orders = filtered_orders[filtered_orders["status"] == "Delivered"]

# ========== PAGE: MARKETPLACE ==========
if page == "📊 Marketplace":
    display_header("📊", "Marketplace Overview", "Uber Eats Sri Lanka · Full Year 2024")

    total_orders = len(filtered_orders)
    delivered    = len(delivered_orders)
    conversion   = delivered / total_orders * 100 if total_orders else 0
    gmv          = delivered_orders["total_lkr"].sum()
    commission   = delivered_orders["commission_lkr"].sum()
    avg_delivery = delivered_orders["delivery_time_min"].mean()

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    col1.metric("Total Orders",  f"{total_orders:,}")
    col2.metric("Delivered",     f"{delivered:,}")
    col3.metric("Conversion",    f"{conversion:.1f}%")
    col4.metric("GMV",           f"LKR {gmv/1e6:.1f}M")
    col5.metric("Commission",    f"LKR {commission/1e6:.1f}M")
    col6.metric("Avg Delivery",  f"{avg_delivery:.0f} min")

    insight(f"Platform processed <strong>{total_orders:,} orders</strong> with <strong>{conversion:.1f}% conversion</strong>. "
            f"GMV reached <strong>LKR {gmv/1e6:.1f}M</strong>, generating <strong>LKR {commission/1e6:.1f}M</strong> commission.")

    divider()
    section("TREND ANALYSIS", "Monthly GMV & Conversion Rate")

    monthly = filtered_orders.groupby("month").agg(
        total=("order_id", "count"),
        delivered=("status", lambda x: (x == "Delivered").sum()),
        gmv=("total_lkr", lambda x: x[filtered_orders.loc[x.index, "status"] == "Delivered"].sum())
    ).reset_index().sort_values("month")
    monthly["conv"] = monthly["delivered"] / monthly["total"] * 100

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(
        x=monthly["month"], y=monthly["gmv"]/1e6,
        name="GMV (M LKR)", marker_color=GREEN, opacity=0.9,
        hovertemplate="<b>%{x}</b><br>GMV: LKR %{y:.2f}M<extra></extra>"
    ), secondary_y=False)
    fig.add_trace(go.Scatter(
        x=monthly["month"], y=monthly["conv"],
        name="Conversion %", mode="lines+markers",
        line=dict(color=BLACK, width=3),
        marker=dict(size=7, color=BLACK, line=dict(color=WHITE, width=2)),
        hovertemplate="<b>%{x}</b><br>Conversion: %{y:.1f}%<extra></extra>"
    ), secondary_y=True)
    fig.update_layout(
        height=400, plot_bgcolor=WHITE, paper_bgcolor=WHITE,
        font=dict(family="DM Sans", size=12, color=TEXT_DARK),
        margin=dict(t=48, b=28, l=16, r=16),
        hoverlabel=dict(bgcolor=BLACK, font_color=WHITE, font_size=12, bordercolor=GREEN),
        legend=dict(orientation="h", y=1.06, x=0, font=dict(color=TEXT_DARK, size=11)),
        xaxis=dict(gridcolor="#F0F0F0", tickfont=dict(color=TEXT_DARK)),
        yaxis=dict(gridcolor="#F0F0F0", tickfont=dict(color=TEXT_DARK),
                   title_text="GMV (M LKR)", title_font=dict(color=TEXT_DARK)),
        yaxis2=dict(tickfont=dict(color=TEXT_DARK), title_text="Conversion (%)",
                    title_font=dict(color=TEXT_DARK), gridcolor="rgba(0,0,0,0)"),
    )
    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        section("STATUS", "Order Status Breakdown")
        status_counts = filtered_orders["status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        fig_pie = px.pie(status_counts, names="Status", values="Count", hole=0.58,
                         color="Status",
                         color_discrete_map={"Delivered": GREEN, "Cancelled": RED, "Refunded": ORANGE})
        fig_pie.update_traces(
            textinfo="percent+label",
            textfont=dict(size=12, color=WHITE, family="DM Sans"),
            marker=dict(line=dict(color=WHITE, width=3)),
            hovertemplate="<b>%{label}</b><br>%{value:,} orders (%{percent})<extra></extra>"
        )
        fig_pie.update_layout(height=360, plot_bgcolor=WHITE, paper_bgcolor=WHITE,
                               font=dict(family="DM Sans", size=12, color=TEXT_DARK),
                               margin=dict(t=20, b=10, l=10, r=10),
                               legend=dict(font=dict(color=TEXT_DARK, size=11)))
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        section("PAYMENTS", "Orders by Payment Method")
        payment_data = delivered_orders.groupby("payment_method")["order_id"].count().sort_values().reset_index()
        payment_data.columns = ["Method", "Orders"]
        fig_bar = px.bar(payment_data, x="Orders", y="Method", orientation="h",
                         text="Orders", color_discrete_sequence=[GREEN])
        fig_bar.update_traces(
            textfont=dict(color=TEXT_DARK, size=11, family="DM Sans"),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Orders: %{x:,}<extra></extra>"
        )
        chart_layout(fig_bar, 360)
        fig_bar.update_layout(showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

    divider()
    section("DEMAND HEATMAP", "Order Volume by Day & Hour")
    heat_data = delivered_orders.groupby(["dow", "hour"])["order_id"].count().reset_index()
    heat_data.columns = ["Day", "Hour", "Orders"]
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heat_data["Day"] = pd.Categorical(heat_data["Day"], categories=day_order, ordered=True)
    pivot = heat_data.pivot_table(index="Day", columns="Hour", values="Orders", fill_value=0)
    fig_heat = px.imshow(pivot,
                         color_continuous_scale=[[0, "#F0FFF8"], [0.3, GREEN_LIGHT], [0.7, GREEN], [1.0, BLACK]],
                         labels={"x": "Hour of Day", "y": "", "color": "Orders"},
                         aspect="auto", text_auto=True)
    fig_heat.update_traces(
        textfont=dict(size=9, color=TEXT_DARK, family="DM Sans"),
        hovertemplate="<b>%{y} %{x}:00</b><br>Orders: %{z:,}<extra></extra>"
    )
    fig_heat.update_layout(
        height=320, plot_bgcolor=WHITE, paper_bgcolor=WHITE,
        font=dict(family="DM Sans", size=11, color=TEXT_DARK),
        margin=dict(t=24, b=24, l=10, r=10),
        xaxis=dict(tickfont=dict(color=TEXT_DARK, size=10)),
        yaxis=dict(tickfont=dict(color=TEXT_DARK, size=11)),
        coloraxis_colorbar=dict(tickfont=dict(color=TEXT_DARK),
                                title=dict(font=dict(color=TEXT_DARK)))
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    insight("Peak demand: <strong>12–2 PM (lunch)</strong> and <strong>7–9 PM (dinner)</strong>. Weekends show higher volume throughout the day.")

# ========== PAGE: REVENUE & PRICING ==========
elif page == "💰 Revenue & Pricing":
    display_header("💰", "Revenue & Pricing Intelligence", "Commission trends & elasticity modeling")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Commission",     f"LKR {delivered_orders['commission_lkr'].sum()/1e6:.2f}M")
    col2.metric("Avg Commission/Order", f"LKR {delivered_orders['commission_lkr'].mean():,.0f}")
    col3.metric("Avg Order Value",      f"LKR {delivered_orders['total_lkr'].mean():,.0f}")
    col4.metric("Avg Discount",         f"LKR {delivered_orders['discount_lkr'].mean():,.0f}")

    divider()
    col1, col2 = st.columns(2)

    with col1:
        section("BY TIER", "Commission Revenue by Pricing Tier")
        tier_rev  = delivered_orders.merge(filtered_restaurants[["restaurant_id", "pricing_tier"]], on="restaurant_id")
        tier_data = tier_rev.groupby("pricing_tier")["commission_lkr"].sum().reset_index().sort_values("commission_lkr", ascending=False)
        tier_data.columns = ["Pricing Tier", "Commission (LKR)"]
        fig_tier  = px.bar(tier_data, x="Pricing Tier", y="Commission (LKR)",
                           text="Commission (LKR)", color_discrete_sequence=[GREEN])
        fig_tier.update_traces(
            texttemplate="%{y:,.0f}", textposition="outside",
            textfont=dict(color=TEXT_DARK, size=11, family="DM Sans"),
            hovertemplate="<b>%{x}</b><br>Commission: LKR %{y:,.0f}<extra></extra>"
        )
        chart_layout(fig_tier, 360)
        fig_tier.update_layout(showlegend=False)
        st.plotly_chart(fig_tier, use_container_width=True)

    with col2:
        section("BY CATEGORY", "Commission by Food Category")
        cat_rev  = delivered_orders.merge(filtered_restaurants[["restaurant_id", "category"]], on="restaurant_id")
        cat_data = cat_rev.groupby("category")["commission_lkr"].sum().sort_values().reset_index()
        cat_data.columns = ["Category", "Commission (LKR)"]
        fig_cat  = px.bar(cat_data, x="Commission (LKR)", y="Category", orientation="h",
                          text="Commission (LKR)", color_discrete_sequence=[BLACK])
        fig_cat.update_traces(
            texttemplate="%{x:,.0f}", textposition="outside",
            textfont=dict(color=TEXT_DARK, size=11, family="DM Sans"),
            hovertemplate="<b>%{y}</b><br>Commission: LKR %{x:,.0f}<extra></extra>"
        )
        chart_layout(fig_cat, 360)
        fig_cat.update_layout(showlegend=False)
        st.plotly_chart(fig_cat, use_container_width=True)

    divider()
    section("PRICE ELASTICITY", "How Price Changes Affect Order Volume")

    monthly_rest = filtered_orders[filtered_orders["status"] == "Delivered"].groupby(["restaurant_id", "month_num"]).agg(
        orders=("order_id", "count")
    ).reset_index()
    elasticity_data = monthly_rest.merge(
        pricing[["restaurant_id", "month", "avg_item_price_lkr", "category"]],
        left_on=["restaurant_id", "month_num"], right_on=["restaurant_id", "month"]
    )
    elasticity_data["price_change"] = elasticity_data.groupby("restaurant_id")["avg_item_price_lkr"].pct_change() * 100
    elasticity_data["order_change"] = elasticity_data.groupby("restaurant_id")["orders"].pct_change() * 100
    elasticity_data = elasticity_data.dropna()
    elasticity_data = elasticity_data[
        (elasticity_data["price_change"].between(-30, 30)) &
        (elasticity_data["order_change"].between(-60, 60))
    ]
    if len(elasticity_data) > 0:
        fig_elastic = px.scatter(
            elasticity_data, x="price_change", y="order_change", color="category",
            trendline="ols", opacity=0.7, height=420,
            color_discrete_sequence=MULTI_SEQ,
            labels={"price_change": "Price Change (%)", "order_change": "Order Volume Change (%)", "category": "Category"}
        )
        fig_elastic.update_traces(marker=dict(size=7, line=dict(color=WHITE, width=1)),
                                  selector=dict(mode="markers"))
        chart_layout(fig_elastic, 420, legend_top=True)
        st.plotly_chart(fig_elastic, use_container_width=True)
        insight("Each 10% price increase leads to ~5–8% order volume decline. Use this to optimize commission rates.")

    divider()
    section("PRICE TRENDS", "Average Item Price by Category Over Time")
    price_trend = pricing.groupby(["month", "category"])["avg_item_price_lkr"].mean().reset_index()
    price_trend.columns = ["Month", "Category", "Avg Price (LKR)"]
    fig_trend = px.line(price_trend, x="Month", y="Avg Price (LKR)", color="Category",
                        color_discrete_sequence=MULTI_SEQ, markers=True)
    fig_trend.update_traces(line=dict(width=2.5), marker=dict(size=6))
    chart_layout(fig_trend, 380, legend_top=True)
    st.plotly_chart(fig_trend, use_container_width=True)

# ========== PAGE: RESTAURANTS ==========
elif page == "🏪 Restaurants":
    display_header("🏪", "Restaurant Partner Analytics", "Performance & growth signals")

    rest_metrics = filtered_orders.groupby("restaurant_id").agg(
        total_orders=("order_id", "count"),
        conversion=("status", lambda x: (x == "Delivered").mean() * 100),
        avg_value=("total_lkr", "mean"),
        revenue=("commission_lkr", "sum")
    ).reset_index()
    rest_metrics = rest_metrics.merge(
        filtered_restaurants[["restaurant_id", "name", "zone", "category", "pricing_tier", "rating"]],
        on="restaurant_id"
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Restaurants", len(rest_metrics))
    col2.metric("Avg Conversion",     f"{rest_metrics['conversion'].mean():.1f}%")
    col3.metric("Avg Order Value",    f"LKR {rest_metrics['avg_value'].mean():,.0f}")
    col4.metric("Avg Rating",         f"{rest_metrics['rating'].mean():.2f} ⭐")

    divider()
    col1, col2 = st.columns(2)

    with col1:
        section("TOP PERFORMERS", "Top 10 Restaurants by Revenue")
        top_rest = rest_metrics.nlargest(10, "revenue").sort_values("revenue")
        fig_top  = px.bar(top_rest, x="revenue", y="name", orientation="h",
                          text="revenue", color_discrete_sequence=[GREEN])
        fig_top.update_traces(
            texttemplate="LKR %{x:,.0f}", textposition="outside",
            textfont=dict(color=TEXT_DARK, size=10, family="DM Sans"),
            hovertemplate="<b>%{y}</b><br>Revenue: LKR %{x:,.0f}<extra></extra>"
        )
        chart_layout(fig_top, 420)
        fig_top.update_layout(showlegend=False)
        st.plotly_chart(fig_top, use_container_width=True)

    with col2:
        section("DISTRIBUTION", "Conversion Rate Distribution")
        avg_conv = rest_metrics["conversion"].mean()
        fig_hist = px.histogram(rest_metrics, x="conversion", nbins=25,
                                color_discrete_sequence=[GREEN],
                                labels={"conversion": "Conversion Rate (%)", "count": "Restaurants"})
        fig_hist.update_traces(marker_line_color=WHITE, marker_line_width=1,
                               hovertemplate="Conversion: %{x:.1f}%<br>Count: %{y}<extra></extra>")
        fig_hist.add_vline(x=avg_conv, line_dash="dash", line_color=BLACK, line_width=2,
                           annotation_text=f"  Avg: {avg_conv:.1f}%",
                           annotation_font=dict(color=BLACK, size=12),
                           annotation_position="top right")
        chart_layout(fig_hist, 420)
        st.plotly_chart(fig_hist, use_container_width=True)

    divider()
    section("ZONE PERFORMANCE", "Commission by Zone · Color = Avg Conversion Rate")
    zone_data = rest_metrics.groupby("zone").agg(
        total_rev=("revenue", "sum"),
        avg_conv=("conversion", "mean"),
        restaurants=("restaurant_id", "count")
    ).reset_index().sort_values("total_rev", ascending=False)
    fig_zone = px.bar(zone_data, x="zone", y="total_rev", color="avg_conv",
                      color_continuous_scale=[[0, "#C8F5E0"], [0.5, GREEN], [1.0, BLACK]],
                      text=[f"LKR {v/1e6:.1f}M" for v in zone_data["total_rev"]],
                      labels={"zone": "Zone", "total_rev": "Commission (LKR)", "avg_conv": "Conv %"},
                      custom_data=["restaurants", "avg_conv"])
    fig_zone.update_traces(
        textposition="outside",
        textfont=dict(color=TEXT_DARK, size=11, family="DM Sans"),
        hovertemplate=("<b>%{x}</b><br>Commission: LKR %{y:,.0f}<br>"
                       "Restaurants: %{customdata[0]}<br>"
                       "Avg Conversion: %{customdata[1]:.1f}%<extra></extra>")
    )
    chart_layout(fig_zone, 400)
    fig_zone.update_layout(coloraxis_colorbar=dict(
        title="Conv %",
        tickfont=dict(color=TEXT_DARK, size=10),
        title_font=dict(color=TEXT_DARK, size=11)
    ))
    fig_zone.update_xaxes(tickangle=-30)
    st.plotly_chart(fig_zone, use_container_width=True)

# ========== PAGE: DRIVER OPS ==========
elif page == "🚴 Driver Ops":
    display_header("🚴", "Driver & Courier Operations", "Fleet efficiency & cancellation analysis")

    driver_metrics = delivered_orders.merge(
        drivers[["driver_id", "vehicle_type", "zone", "rating"]], on="driver_id"
    )
    driver_summary = driver_metrics.groupby("driver_id").agg(
        trips=("order_id", "count"),
        avg_delivery=("delivery_time_min", "mean"),
        vehicle=("vehicle_type", "first"),
        rating=("rating", "first")
    ).reset_index()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Active Couriers",    len(driver_summary))
    col2.metric("Total Deliveries",   f"{driver_summary['trips'].sum():,}")
    col3.metric("Avg Delivery Time",  f"{driver_summary['avg_delivery'].mean():.0f} min")
    col4.metric("Avg Courier Rating", f"{driver_summary['rating'].mean():.2f} ⭐")

    divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        section("FLEET MIX", "Deliveries by Vehicle Type")
        vehicle_data = driver_summary.groupby("vehicle")["trips"].sum().reset_index()
        vehicle_data.columns = ["Vehicle", "Trips"]
        fig_vehicle = px.pie(vehicle_data, names="Vehicle", values="Trips", hole=0.55,
                             color_discrete_sequence=[GREEN, BLACK, ORANGE])
        fig_vehicle.update_traces(
            textinfo="percent+label",
            textfont=dict(size=11, color=WHITE, family="DM Sans"),
            marker=dict(line=dict(color=WHITE, width=3)),
            hovertemplate="<b>%{label}</b><br>%{value:,} trips (%{percent})<extra></extra>"
        )
        fig_vehicle.update_layout(height=300, plot_bgcolor=WHITE, paper_bgcolor=WHITE,
                                   font=dict(family="DM Sans", size=11, color=TEXT_DARK),
                                   margin=dict(t=20, b=10),
                                   legend=dict(font=dict(color=TEXT_DARK, size=11)))
        st.plotly_chart(fig_vehicle, use_container_width=True)

    with col2:
        section("SPEED", "Avg Delivery Time by Vehicle (min)")
        speed_data = driver_summary.groupby("vehicle")["avg_delivery"].mean().reset_index()
        speed_data.columns = ["Vehicle", "Avg Delivery (min)"]
        fig_speed  = px.bar(speed_data, x="Vehicle", y="Avg Delivery (min)",
                            text="Avg Delivery (min)", color_discrete_sequence=[GREEN])
        fig_speed.update_traces(
            texttemplate="%{y:.0f} min", textposition="outside",
            textfont=dict(color=TEXT_DARK, size=11, family="DM Sans"),
            hovertemplate="<b>%{x}</b><br>Avg: %{y:.1f} min<extra></extra>"
        )
        chart_layout(fig_speed, 300)
        fig_speed.update_layout(showlegend=False)
        st.plotly_chart(fig_speed, use_container_width=True)

    with col3:
        section("RATINGS", "Courier Rating Distribution")
        fig_rating = px.histogram(driver_summary, x="rating", nbins=20,
                                  color_discrete_sequence=[GREEN],
                                  labels={"rating": "Rating", "count": "Couriers"})
        fig_rating.update_traces(marker_line_color=WHITE, marker_line_width=1,
                                 hovertemplate="Rating: %{x:.1f}<br>Count: %{y}<extra></extra>")
        chart_layout(fig_rating, 300)
        st.plotly_chart(fig_rating, use_container_width=True)

    divider()
    col1, col2 = st.columns([2, 1])

    with col1:
        section("CANCELLATION REASONS", "Root Cause Analysis")
        cancel_data = filtered_orders[
            filtered_orders["status"].isin(["Cancelled", "Refunded"])
        ].dropna(subset=["cancel_reason"])
        if len(cancel_data) > 0:
            cancel_summary = cancel_data.groupby("cancel_reason")["order_id"].count().sort_values().reset_index()
            cancel_summary.columns = ["Reason", "Count"]
            fig_cancel = px.bar(cancel_summary, x="Count", y="Reason", orientation="h",
                                text="Count", color_discrete_sequence=[RED])
            fig_cancel.update_traces(
                textposition="outside",
                textfont=dict(color=TEXT_DARK, size=11, family="DM Sans"),
                hovertemplate="<b>%{y}</b><br>Count: %{x:,}<extra></extra>"
            )
            chart_layout(fig_cancel, 340)
            fig_cancel.update_layout(showlegend=False)
            st.plotly_chart(fig_cancel, use_container_width=True)
            warning("'Driver unavailable' and 'Timeout' are supply-side failures. Boost incentives during peak hours.")

    with col2:
        section("TOP COURIERS", "Leaderboard — Top 5")
        top_drivers = driver_summary.nlargest(5, "trips")[
            ["driver_id", "vehicle", "trips", "avg_delivery", "rating"]
        ].copy()
        top_drivers.columns = ["ID", "Vehicle", "Trips", "Avg Time", "Rating"]
        top_drivers["Avg Time"] = top_drivers["Avg Time"].map("{:.0f} min".format)
        top_drivers["Rating"]   = top_drivers["Rating"].map("{:.2f} ⭐".format)
        st.dataframe(top_drivers, use_container_width=True, hide_index=True)

# ========== PAGE: CHURN RISK ==========
elif page == "⚠️ Churn Risk":
    display_header("⚠️", "Restaurant Churn Risk", "ML-powered retention predictions")

    if churn_df is None:
        st.error("Run `python utils/analysis.py` to generate churn predictions first.")
        st.stop()

    churn_merged = churn_df.merge(
        restaurants[["restaurant_id", "name", "zone", "category"]],
        on="restaurant_id", how="left"
    )

    high_risk   = (churn_merged["churn_risk_label"] == "High Risk").sum()
    medium_risk = (churn_merged["churn_risk_label"] == "Medium Risk").sum()
    low_risk    = (churn_merged["churn_risk_label"] == "Low Risk").sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Scored",   len(churn_merged))
    col2.metric("🔴 High Risk",   high_risk,   f"{high_risk/len(churn_merged)*100:.0f}% of total")
    col3.metric("🟡 Medium Risk", medium_risk, f"{medium_risk/len(churn_merged)*100:.0f}% of total")
    col4.metric("🟢 Low Risk",    low_risk,    f"{low_risk/len(churn_merged)*100:.0f}% of total")

    warning(f"{high_risk} restaurants are at HIGH churn risk. Immediate intervention recommended.")

    divider()
    col1, col2 = st.columns(2)

    with col1:
        section("RISK DISTRIBUTION", "Churn Risk Label Breakdown")
        risk_counts = churn_merged["churn_risk_label"].value_counts().reset_index()
        risk_counts.columns = ["Risk", "Count"]
        fig_risk = px.pie(risk_counts, names="Risk", values="Count", hole=0.55,
                          color="Risk",
                          color_discrete_map={"High Risk": RED, "Medium Risk": ORANGE, "Low Risk": GREEN})
        fig_risk.update_traces(
            textinfo="percent+label",
            textfont=dict(size=12, color=WHITE, family="DM Sans"),
            marker=dict(line=dict(color=WHITE, width=3)),
            hovertemplate="<b>%{label}</b><br>%{value} restaurants (%{percent})<extra></extra>"
        )
        fig_risk.update_layout(height=360, plot_bgcolor=WHITE, paper_bgcolor=WHITE,
                                font=dict(family="DM Sans", size=12, color=TEXT_DARK),
                                margin=dict(t=20, b=10),
                                legend=dict(font=dict(color=TEXT_DARK, size=11)))
        st.plotly_chart(fig_risk, use_container_width=True)

    with col2:
        section("RISK METRICS", "Churn Probability Statistics")
        if len(churn_merged) > 0:
            stats_data = {
                "Metric": ["Min Risk", "Avg Risk", "Max Risk", "Median Risk"],
                "Value": [
                    f"{churn_merged['churn_probability'].min():.0%}",
                    f"{churn_merged['churn_probability'].mean():.0%}",
                    f"{churn_merged['churn_probability'].max():.0%}",
                    f"{churn_merged['churn_probability'].median():.0%}"
                ]
            }
            stats_df = pd.DataFrame(stats_data)
            st.dataframe(stats_df, use_container_width=True, hide_index=True)
        else:
            st.warning("No churn data available.")

    divider()
    section("SCORE DISTRIBUTION", "Churn Probability Histogram by Risk Label")
    fig_score = px.histogram(
        churn_merged, x="churn_probability", color="churn_risk_label",
        nbins=30, barmode="overlay", opacity=0.75,
        color_discrete_map={"High Risk": RED, "Medium Risk": ORANGE, "Low Risk": GREEN},
        labels={"churn_probability": "Churn Probability", "count": "Restaurants",
                "churn_risk_label": "Risk Level"}
    )
    fig_score.update_traces(marker_line_color=WHITE, marker_line_width=1,
                            hovertemplate="Prob: %{x:.2f}<br>Count: %{y}<extra></extra>")
    fig_score.add_vline(x=0.5, line_dash="dash", line_color=BLACK, line_width=2,
                        annotation_text="  Threshold: 0.50",
                        annotation_font=dict(color=BLACK, size=12),
                        annotation_position="top right")
    chart_layout(fig_score, 360, legend_top=True)
    st.plotly_chart(fig_score, use_container_width=True)

    divider()
    section("ACTION REQUIRED", "High Risk Restaurants — Immediate Outreach")
    if "category" in churn_merged.columns:
        high_risk_list = churn_merged[churn_merged["churn_risk_label"] == "High Risk"].nlargest(
            15, "churn_probability"
        )[["name", "zone", "category", "total_orders", "conversion_rate", "churn_probability"]].copy()
        high_risk_list["churn_probability"] = high_risk_list["churn_probability"].map("{:.0%}".format)
        high_risk_list["conversion_rate"]   = high_risk_list["conversion_rate"].map("{:.0%}".format)
        high_risk_list.columns = ["Restaurant", "Zone", "Category", "Orders", "Conversion", "Churn Score"]
    else:
        high_risk_list = churn_merged[churn_merged["churn_risk_label"] == "High Risk"].nlargest(
            15, "churn_probability"
        )[["name", "zone", "total_orders", "conversion_rate", "churn_probability"]].copy()
        high_risk_list["churn_probability"] = high_risk_list["churn_probability"].map("{:.0%}".format)
        high_risk_list["conversion_rate"]   = high_risk_list["conversion_rate"].map("{:.0%}".format)
        high_risk_list.columns = ["Restaurant", "Zone", "Orders", "Conversion", "Churn Score"]
    st.dataframe(high_risk_list, use_container_width=True, hide_index=True)

    insight("""<strong>Recommended Actions for High-Risk Partners:</strong><br>
    1. Assign dedicated Partner Success Manager<br>
    2. Offer temporary 5–8% commission reduction<br>
    3. Activate Promoted Listing for 2 weeks<br>
    4. Schedule operational review call<br>
    5. Track weekly for 3 weeks""")