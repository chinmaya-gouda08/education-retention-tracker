import streamlit as st
import pandas as pd
from pathlib import Path


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Student Retention & Welfare Tracker",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# THEME TOGGLE
# ============================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False


st.sidebar.markdown("### 🎨 Appearance")
st.sidebar.toggle(
    "🌙 Dark Mode",
    key="dark_mode",
    help="Switch between light and dark dashboard themes."
)


# ============================================================
# CUSTOM CSS
# ============================================================

if st.session_state.dark_mode:

    page_bg = "#0f172a"
    surface = "#1e293b"
    surface_alt = "#172033"
    text_main = "#f8fafc"
    text_muted = "#cbd5e1"
    border = "#334155"
    header_bg = "#0f172a"
    select_bg = "#1e293b"

else:

    page_bg = "#f8fafc"
    surface = "#ffffff"
    surface_alt = "#ffffff"
    text_main = "#17324d"
    text_muted = "#64748b"
    border = "#e2e8f0"
    header_bg = "#ffffff"
    select_bg = "#ffffff"


st.markdown(
    f"""
    <style>

    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] > .main,
    section.main, .main {{
        background-color: {page_bg} !important;
        color: {text_main} !important;
    }}

    /* Keep the Streamlit top bar clear of the dashboard content. */
    [data-testid="stHeader"] {{
        background-color: {header_bg} !important;
    }}

    /* IMPORTANT: extra top space prevents the title from being hidden
       behind Streamlit's fixed top header. */
    .block-container {{
        padding-top: 4.5rem !important;
        padding-bottom: 2rem !important;
    }}

    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div:first-child,
    [data-testid="stSidebarContent"] {{
        background-color: {surface} !important;
        color: {text_main} !important;
    }}

    [data-testid="stSidebar"] * {{
        color: {text_main} !important;
    }}

    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3,
    [data-testid="stAppViewContainer"] h4,
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stAppViewContainer"] span {{
        color: {text_main};
    }}

    .dashboard-title {{
        font-size: 2.2rem;
        line-height: 1.2;
        font-weight: 700;
        color: {text_main} !important;
        margin-top: 0 !important;
        margin-bottom: 0.25rem;
    }}

    .dashboard-subtitle {{
        font-size: 1rem;
        color: {text_muted} !important;
        margin-bottom: 1.5rem;
    }}

    .section-title {{
        font-size: 1.45rem;
        font-weight: 700;
        color: {text_main} !important;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }}

    /* Sidebar select boxes */
    [data-testid="stSidebar"] [data-baseweb="select"] > div {{
        background-color: {select_bg} !important;
        color: {text_main} !important;
        border-color: {border} !important;
    }}

    [data-testid="stSidebar"] [data-baseweb="select"] input,
    [data-testid="stSidebar"] [data-baseweb="select"] div {{
        color: {text_main} !important;
    }}

    /* KPI cards */
    div[data-testid="stMetric"] {{
        background-color: {surface} !important;
        border: 1px solid {border};
        border-radius: 12px;
        padding: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
    }}

    div[data-testid="stMetricLabel"] {{
        color: {text_muted} !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: {text_main} !important;
    }}

    .insight-box {{
        background-color: {surface} !important;
        border-left: 4px solid #2563eb;
        padding: 15px 18px;
        border-radius: 8px;
        margin-bottom: 10px;
        color: {text_main} !important;
    }}

    /* Streamlit info/status boxes */
    [data-testid="stAlert"] {{
        border-radius: 10px;
    }}

    /* Dataframe container */
    [data-testid="stDataFrame"] {{
        border: 1px solid {border};
        border-radius: 10px;
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "analytical"


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    school_dim = pd.read_csv(
        DATA_DIR / "school_dim.csv"
    )

    attendance = pd.read_csv(
        DATA_DIR / "attendance_monthly.csv"
    )

    mdm = pd.read_csv(
        DATA_DIR / "mdm_monthly.csv"
    )

    infrastructure = pd.read_csv(
        DATA_DIR / "infrastructure_monthly.csv"
    )

    test_scores = pd.read_csv(
        DATA_DIR / "test_scores_analysis.csv"
    )

    return (
        school_dim,
        attendance,
        mdm,
        infrastructure,
        test_scores
    )


try:

    (
        school_dim,
        attendance,
        mdm,
        infrastructure,
        test_scores
    ) = load_data()

except Exception as e:

    st.error(
        "Unable to load dashboard data."
    )

    st.code(str(e))

    st.stop()


# ============================================================
# DATA TYPE PREPARATION
# ============================================================

for df in [
    school_dim,
    attendance,
    mdm,
    infrastructure,
    test_scores
]:

    if "school_id" in df.columns:

        df["school_id"] = (
            df["school_id"]
            .astype(str)
        )

    if "month" in df.columns:

        df["month"] = (
            df["month"]
            .astype(str)
        )


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="dashboard-title">'
    '🎓 Student Retention & Welfare Efficacy Tracker'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Integrated analytics for attendance, student welfare, '
    'infrastructure and learning outcomes'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.title("Dashboard Filters")

st.sidebar.markdown(
    "Use the filters below to explore the education ecosystem."
)


# ============================================================
# DISTRICT FILTER
# ============================================================

districts = sorted(
    school_dim["district"]
    .dropna()
    .astype(str)
    .unique()
)

selected_district = st.sidebar.selectbox(
    "District",
    ["All Districts"] + districts
)


# ============================================================
# BLOCK FILTER
# ============================================================

if selected_district == "All Districts":

    block_source = school_dim.copy()

else:

    block_source = school_dim[
        school_dim["district"] == selected_district
    ].copy()


blocks = sorted(
    block_source["block"]
    .dropna()
    .astype(str)
    .unique()
)

selected_block = st.sidebar.selectbox(
    "Block",
    ["All Blocks"] + blocks
)


# ============================================================
# SCHOOL FILTER
# ============================================================

school_source = block_source.copy()

if selected_block != "All Blocks":

    school_source = school_source[
        school_source["block"] == selected_block
    ]


school_options = (
    school_source
    .sort_values("school_name")
    [
        [
            "school_id",
            "school_name"
        ]
    ]
    .drop_duplicates()
)


school_labels = {
    row["school_id"]:
        f'{row["school_id"]} - {row["school_name"]}'
    for _, row in school_options.iterrows()
}


school_ids = list(
    school_labels.keys()
)


selected_school = st.sidebar.selectbox(
    "School",
    ["All Schools"] + school_ids,
    format_func=lambda x:
        "All Schools"
        if x == "All Schools"
        else school_labels.get(x, x)
)


# ============================================================
# MONTH FILTER
# ============================================================

all_months = sorted(
    set(
        attendance["month"]
        .dropna()
        .astype(str)
    )
    |
    set(
        mdm["month"]
        .dropna()
        .astype(str)
    )
    |
    set(
        infrastructure["month"]
        .dropna()
        .astype(str)
    )
    |
    set(
        test_scores["month"]
        .dropna()
        .astype(str)
    )
)

selected_month = st.sidebar.selectbox(
    "Month",
    ["All Months"] + all_months
)


# ============================================================
# FILTER SCHOOL DIMENSION
# ============================================================

filtered_school_dim = school_dim.copy()


if selected_district != "All Districts":

    filtered_school_dim = filtered_school_dim[
        filtered_school_dim["district"]
        == selected_district
    ]


if selected_block != "All Blocks":

    filtered_school_dim = filtered_school_dim[
        filtered_school_dim["block"]
        == selected_block
    ]


if selected_school != "All Schools":

    filtered_school_dim = filtered_school_dim[
        filtered_school_dim["school_id"]
        == selected_school
    ]


selected_school_ids = set(
    filtered_school_dim["school_id"]
)


# ============================================================
# FILTER ATTENDANCE
# ============================================================

attendance_filtered = attendance[
    attendance["school_id"].isin(
        selected_school_ids
    )
].copy()


if selected_month != "All Months":

    attendance_filtered = attendance_filtered[
        attendance_filtered["month"]
        == selected_month
    ]


# ============================================================
# FILTER MDM
# ============================================================

mdm_filtered = mdm[
    mdm["school_id"].isin(
        selected_school_ids
    )
].copy()


if selected_month != "All Months":

    mdm_filtered = mdm_filtered[
        mdm_filtered["month"]
        == selected_month
    ]


# ============================================================
# FILTER INFRASTRUCTURE
# ============================================================

infra_filtered = infrastructure[
    infrastructure["school_id"].isin(
        selected_school_ids
    )
].copy()


if selected_month != "All Months":

    infra_filtered = infra_filtered[
        infra_filtered["month"]
        == selected_month
    ]


# ============================================================
# FILTER TEST SCORES
# ============================================================

test_filtered = test_scores[
    test_scores["school_id"].isin(
        selected_school_ids
    )
].copy()


if selected_month != "All Months":

    test_filtered = test_filtered[
        test_filtered["month"]
        == selected_month
    ]


# ============================================================
# FILTER SUMMARY
# ============================================================

filter_text = (
    f"Showing data for {len(filtered_school_dim):,} school(s)"
)

if selected_district != "All Districts":

    filter_text += (
        f" | District: {selected_district}"
    )

if selected_block != "All Blocks":

    filter_text += (
        f" | Block: {selected_block}"
    )

if selected_school != "All Schools":

    filter_text += (
        f" | School: {selected_school}"
    )

if selected_month != "All Months":

    filter_text += (
        f" | Month: {selected_month}"
    )

st.info(filter_text)


# ============================================================
# EXECUTIVE OVERVIEW
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📊 Executive Overview'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# KPI 1 - TOTAL SCHOOLS
# ============================================================

total_schools = len(
    filtered_school_dim
)


# ============================================================
# KPI 2 - ATTENDANCE
# ============================================================

if len(attendance_filtered) > 0:

    total_present = pd.to_numeric(
        attendance_filtered[
            "total_students_present"
        ],
        errors="coerce"
    ).sum()

    total_observed = pd.to_numeric(
        attendance_filtered[
            "total_students_observed"
        ],
        errors="coerce"
    ).sum()

    if total_observed > 0:

        overall_attendance = (
            total_present /
            total_observed *
            100
        )

    else:

        overall_attendance = 0

else:

    overall_attendance = 0


# ============================================================
# KPI 3 - PROXY ATTENDANCE
# ============================================================

if len(attendance_filtered) > 0:

    proxy_records = pd.to_numeric(
        attendance_filtered[
            "proxy_attendance_records"
        ],
        errors="coerce"
    ).sum()

    attendance_records = pd.to_numeric(
        attendance_filtered[
            "attendance_records"
        ],
        errors="coerce"
    ).sum()

    if attendance_records > 0:

        proxy_rate = (
            proxy_records /
            attendance_records *
            100
        )

    else:

        proxy_rate = 0

else:

    proxy_rate = 0


# ============================================================
# KPI 4 - MDM COST
# ============================================================

if len(mdm_filtered) > 0:

    mdm_cost = pd.to_numeric(
        mdm_filtered[
            "total_mdm_cost"
        ],
        errors="coerce"
    ).sum()

else:

    mdm_cost = 0


# ============================================================
# KPI 5 - INFRASTRUCTURE DEFICIT
# ============================================================

if len(infra_filtered) > 0:

    infrastructure_deficit = pd.to_numeric(
        infra_filtered[
            "infrastructure_deficit_pct"
        ],
        errors="coerce"
    ).mean()

else:

    infrastructure_deficit = 0


# ============================================================
# KPI 6 - TEST SCORE
# ============================================================

if len(test_filtered) > 0:

    test_filtered[
        "average_score_percentage"
    ] = pd.to_numeric(
        test_filtered[
            "average_score_percentage"
        ],
        errors="coerce"
    )

    average_test_score = (
        test_filtered[
            "average_score_percentage"
        ].mean()
    )

else:

    average_test_score = 0


# ============================================================
# KPI DISPLAY
# ============================================================

k1, k2, k3 = st.columns(3)

with k1:

    st.metric(
        "Total Schools",
        f"{total_schools:,}"
    )

with k2:

    st.metric(
        "Average Attendance",
        f"{overall_attendance:.1f}%"
    )

with k3:

    st.metric(
        "Proxy Attendance Rate",
        f"{proxy_rate:.1f}%"
    )


k4, k5, k6 = st.columns(3)

with k4:

    st.metric(
        "Total MDM Cost",
        f"₹{mdm_cost:,.0f}"
    )

with k5:

    st.metric(
        "Infrastructure Deficit",
        f"{infrastructure_deficit:.1f}%"
    )

with k6:

    st.metric(
        "Average Test Score",
        f"{average_test_score:.1f}%"
    )


# ============================================================
# KEY FINDINGS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '💡 Key Findings'
    '</div>',
    unsafe_allow_html=True
)

finding_col1, finding_col2, finding_col3 = st.columns(3)


# ------------------------------------------------------------
# ATTENDANCE FINDING
# ------------------------------------------------------------

with finding_col1:

    if overall_attendance >= 90:

        attendance_message = (
            "Attendance is strong across the selected schools."
        )

    elif overall_attendance >= 75:

        attendance_message = (
            "Attendance is moderate. Some schools may require "
            "additional retention interventions."
        )

    else:

        attendance_message = (
            "Attendance is relatively low and may indicate "
            "student retention or engagement concerns."
        )

    st.markdown(
        f"""
        <div class="insight-box">
        <b>📅 Attendance</b><br><br>
        Average attendance is
        <b>{overall_attendance:.1f}%</b>.
        <br><br>
        {attendance_message}
        </div>
        """,
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# PROXY ATTENDANCE FINDING
# ------------------------------------------------------------

with finding_col2:

    if proxy_rate <= 3:

        proxy_message = (
            "Proxy attendance anomalies appear relatively limited."
        )

    elif proxy_rate <= 7:

        proxy_message = (
            "Some attendance records show proxy patterns and "
            "should be reviewed."
        )

    else:

        proxy_message = (
            "Proxy attendance is elevated and requires "
            "investigation at school level."
        )

    st.markdown(
        f"""
        <div class="insight-box">
        <b>⚠️ Attendance Integrity</b><br><br>
        Proxy attendance rate is
        <b>{proxy_rate:.1f}%</b>.
        <br><br>
        {proxy_message}
        </div>
        """,
        unsafe_allow_html=True
    )


# ------------------------------------------------------------
# LEARNING FINDING
# ------------------------------------------------------------

with finding_col3:

    if average_test_score >= 75:

        learning_message = (
            "Learning outcomes are relatively strong."
        )

    elif average_test_score >= 60:

        learning_message = (
            "Learning outcomes are moderate and targeted "
            "academic support may improve performance."
        )

    else:

        learning_message = (
            "Learning outcomes are low and require "
            "focused academic intervention."
        )

    st.markdown(
        f"""
        <div class="insight-box">
        <b>📚 Learning Outcomes</b><br><br>
        Average test score is
        <b>{average_test_score:.1f}%</b>.
        <br><br>
        {learning_message}
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# AREAS REQUIRING ATTENTION
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🎯 Areas Requiring Attention'
    '</div>',
    unsafe_allow_html=True
)

attention_col1, attention_col2, attention_col3 = st.columns(3)


# ------------------------------------------------------------
# LOWEST ATTENDANCE DISTRICT
# ------------------------------------------------------------

with attention_col1:

    if len(attendance_filtered) > 0:

        lowest_attendance = (
            attendance_filtered
            .groupby(
                "district",
                as_index=False
            )
            .agg(
                total_present=(
                    "total_students_present",
                    "sum"
                ),
                total_observed=(
                    "total_students_observed",
                    "sum"
                )
            )
        )

        lowest_attendance[
            "attendance_rate"
        ] = (
            lowest_attendance[
                "total_present"
            ]
            /
            lowest_attendance[
                "total_observed"
            ]
            * 100
        )

        lowest_attendance = (
            lowest_attendance
            .sort_values(
                "attendance_rate"
            )
            .iloc[0]
        )

        st.markdown(
            f"""
            <div class="insight-box">
            <b>📉 Lowest Attendance</b><br><br>
            <b>{lowest_attendance["district"]}</b>
            <br>
            Attendance:
            <b>{lowest_attendance["attendance_rate"]:.1f}%</b>
            <br><br>
            This district may require closer review of
            attendance and retention patterns.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "No attendance data available."
        )


# ------------------------------------------------------------
# HIGHEST INFRASTRUCTURE DEFICIT
# ------------------------------------------------------------

with attention_col2:

    if len(infra_filtered) > 0:

        highest_deficit = (
            infra_filtered
            .groupby(
                "district",
                as_index=False
            )
            .agg(
                infrastructure_deficit=(
                    "infrastructure_deficit_pct",
                    "mean"
                )
            )
            .sort_values(
                "infrastructure_deficit",
                ascending=False
            )
            .iloc[0]
        )

        st.markdown(
            f"""
            <div class="insight-box">
            <b>🏫 Highest Infrastructure Deficit</b><br><br>
            <b>{highest_deficit["district"]}</b>
            <br>
            Deficit:
            <b>{highest_deficit["infrastructure_deficit"]:.1f}%</b>
            <br><br>
            Infrastructure gaps in this district
            should be prioritized for review.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "No infrastructure data available."
        )


# ------------------------------------------------------------
# LOWEST LEARNING OUTCOME
# ------------------------------------------------------------

with attention_col3:

    if len(test_filtered) > 0:

        lowest_learning = (
            test_filtered
            .groupby(
                "district",
                as_index=False
            )
            .agg(
                average_score=(
                    "average_score_percentage",
                    "mean"
                )
            )
            .sort_values(
                "average_score"
            )
            .iloc[0]
        )

        st.markdown(
            f"""
            <div class="insight-box">
            <b>📚 Lowest Learning Outcome</b><br><br>
            <b>{lowest_learning["district"]}</b>
            <br>
            Average Score:
            <b>{lowest_learning["average_score"]:.1f}%</b>
            <br><br>
            This district may benefit from
            targeted academic intervention.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info(
            "No test score data available."
        )


# ============================================================
# ATTENDANCE & RETENTION
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📅 Attendance & Retention'
    '</div>',
    unsafe_allow_html=True
)


if len(attendance_filtered) > 0:

    attendance_col1, attendance_col2 = st.columns(2)


    # --------------------------------------------------------
    # MONTHLY ATTENDANCE TREND
    # --------------------------------------------------------

    with attendance_col1:

        attendance_trend = (
            attendance_filtered
            .groupby(
                "month",
                as_index=False
            )
            .agg(
                total_present=(
                    "total_students_present",
                    "sum"
                ),
                total_observed=(
                    "total_students_observed",
                    "sum"
                )
            )
            .sort_values("month")
        )

        attendance_trend[
            "attendance_rate"
        ] = (
            attendance_trend[
                "total_present"
            ]
            /
            attendance_trend[
                "total_observed"
            ]
            * 100
        )

        st.subheader(
            "Monthly Attendance Trend"
        )

        st.line_chart(
            attendance_trend.set_index(
                "month"
            )[
                ["attendance_rate"]
            ],
            height=330
        )


    # --------------------------------------------------------
    # PROXY ATTENDANCE TREND
    # --------------------------------------------------------

    with attendance_col2:

        proxy_trend = (
            attendance_filtered
            .groupby(
                "month",
                as_index=False
            )
            .agg(
                proxy_records=(
                    "proxy_attendance_records",
                    "sum"
                ),
                attendance_records=(
                    "attendance_records",
                    "sum"
                )
            )
            .sort_values("month")
        )

        proxy_trend[
            "proxy_rate"
        ] = (
            proxy_trend[
                "proxy_records"
            ]
            /
            proxy_trend[
                "attendance_records"
            ]
            * 100
        )

        st.subheader(
            "Proxy Attendance Trend"
        )

        st.line_chart(
            proxy_trend.set_index(
                "month"
            )[
                ["proxy_rate"]
            ],
            height=330
        )


    # --------------------------------------------------------
    # DISTRICT ATTENDANCE
    # --------------------------------------------------------

    if selected_district == "All Districts":

        district_attendance = (
            attendance_filtered
            .groupby(
                "district",
                as_index=False
            )
            .agg(
                total_present=(
                    "total_students_present",
                    "sum"
                ),
                total_observed=(
                    "total_students_observed",
                    "sum"
                )
            )
        )

        district_attendance[
            "attendance_rate"
        ] = (
            district_attendance[
                "total_present"
            ]
            /
            district_attendance[
                "total_observed"
            ]
            * 100
        )

        district_attendance = (
            district_attendance
            .sort_values(
                "attendance_rate",
                ascending=False
            )
        )

        st.subheader(
            "Attendance Rate by District"
        )

        st.bar_chart(
            district_attendance.set_index(
                "district"
            )[
                ["attendance_rate"]
            ],
            height=400
        )


else:

    st.info(
        "No attendance data available for the selected filters."
    )


# ============================================================
# MID-DAY MEAL / WELFARE
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🍚 Mid-Day Meal & Welfare'
    '</div>',
    unsafe_allow_html=True
)


if len(mdm_filtered) > 0:

    mdm_col1, mdm_col2 = st.columns(2)


    # --------------------------------------------------------
    # MDM COST TREND
    # --------------------------------------------------------

    with mdm_col1:

        mdm_cost_trend = (
            mdm_filtered
            .groupby(
                "month",
                as_index=False
            )
            .agg(
                total_cost=(
                    "total_mdm_cost",
                    "sum"
                )
            )
            .sort_values("month")
        )

        st.subheader(
            "Monthly MDM Cost"
        )

        st.line_chart(
            mdm_cost_trend.set_index(
                "month"
            ),
            height=330
        )


    # --------------------------------------------------------
    # MDM QUANTITY TREND
    # --------------------------------------------------------

    with mdm_col2:

        mdm_quantity_trend = (
            mdm_filtered
            .groupby(
                "month",
                as_index=False
            )
            .agg(
                quantity_kg=(
                    "total_mdm_quantity_kg",
                    "sum"
                )
            )
            .sort_values("month")
        )

        st.subheader(
            "Monthly MDM Quantity"
        )

        st.line_chart(
            mdm_quantity_trend.set_index(
                "month"
            ),
            height=330
        )


    # --------------------------------------------------------
    # MDM KPIs
    # --------------------------------------------------------

    mdm_col3, mdm_col4, mdm_col5 = st.columns(3)


    with mdm_col3:

        total_quantity = mdm_filtered[
            "total_mdm_quantity_kg"
        ].sum()

        st.metric(
            "Total MDM Quantity",
            f"{total_quantity:,.0f} kg"
        )


    with mdm_col4:

        procurement_records = mdm_filtered[
            "procurement_records"
        ].sum()

        st.metric(
            "Procurement Records",
            f"{procurement_records:,.0f}"
        )


    with mdm_col5:

        vendor_instances = mdm_filtered[
            "unique_vendors"
        ].sum()

        st.metric(
            "Vendor Instances",
            f"{vendor_instances:,.0f}"
        )


else:

    st.info(
        "No MDM data available for the selected filters."
    )


# ============================================================
# INFRASTRUCTURE
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🏫 Infrastructure'
    '</div>',
    unsafe_allow_html=True
)


if len(infra_filtered) > 0:

    infra_col1, infra_col2 = st.columns(2)


    # --------------------------------------------------------
    # DEFICIT TREND
    # --------------------------------------------------------

    with infra_col1:

        deficit_trend = (
            infra_filtered
            .groupby(
                "month",
                as_index=False
            )
            .agg(
                deficit=(
                    "infrastructure_deficit_pct",
                    "mean"
                )
            )
            .sort_values("month")
        )

        st.subheader(
            "Infrastructure Deficit Trend"
        )

        st.line_chart(
            deficit_trend.set_index(
                "month"
            ),
            height=330
        )


    # --------------------------------------------------------
    # FACILITY AVAILABILITY
    # --------------------------------------------------------

    with infra_col2:

        facility_columns = {

            "Electricity":
                "electricity_availability_pct",

            "Drinking Water":
                "drinking_water_availability_pct",

            "Functional Toilet":
                "functional_toilet_availability_pct",

            "Boundary Wall":
                "boundary_wall_availability_pct",

            "Playground":
                "playground_availability_pct"
        }

        facility_data = []

        for facility, column in facility_columns.items():

            if column in infra_filtered.columns:

                value = pd.to_numeric(
                    infra_filtered[column],
                    errors="coerce"
                ).mean()

                facility_data.append(
                    {
                        "Facility": facility,
                        "Availability": value
                    }
                )

        facility_df = pd.DataFrame(
            facility_data
        )

        st.subheader(
            "Facility Availability"
        )

        if len(facility_df) > 0:

            st.bar_chart(
                facility_df.set_index(
                    "Facility"
                )[
                    ["Availability"]
                ],
                height=330
            )


    # --------------------------------------------------------
    # DISTRICT INFRASTRUCTURE
    # --------------------------------------------------------

    if selected_district == "All Districts":

        infra_district = (
            infra_filtered
            .groupby(
                "district",
                as_index=False
            )
            .agg(
                infrastructure_deficit=(
                    "infrastructure_deficit_pct",
                    "mean"
                )
            )
            .sort_values(
                "infrastructure_deficit",
                ascending=False
            )
        )

        st.subheader(
            "Infrastructure Deficit by District"
        )

        st.bar_chart(
            infra_district.set_index(
                "district"
            )[
                ["infrastructure_deficit"]
            ],
            height=400
        )


else:

    st.info(
        "No infrastructure data available for the selected filters."
    )


# ============================================================
# LEARNING OUTCOMES
# ============================================================

st.markdown(
    '<div class="section-title">'
    '📚 Learning Outcomes'
    '</div>',
    unsafe_allow_html=True
)


if len(test_filtered) > 0:

    learning_col1, learning_col2 = st.columns(2)


    # --------------------------------------------------------
    # SUBJECT PERFORMANCE
    # --------------------------------------------------------

    with learning_col1:

        subject_scores = (
            test_filtered
            .groupby(
                "subject",
                as_index=False
            )
            .agg(
                average_score=(
                    "average_score_percentage",
                    "mean"
                )
            )
            .sort_values(
                "average_score",
                ascending=False
            )
        )

        st.subheader(
            "Average Score by Subject"
        )

        st.bar_chart(
            subject_scores.set_index(
                "subject"
            )[
                ["average_score"]
            ],
            height=350
        )


    # --------------------------------------------------------
    # GRADE PERFORMANCE
    # --------------------------------------------------------

    with learning_col2:

        grade_scores = (
            test_filtered
            .groupby(
                "grade",
                as_index=False
            )
            .agg(
                average_score=(
                    "average_score_percentage",
                    "mean"
                )
            )
            .sort_values("grade")
        )

        grade_scores["grade"] = (
            "Grade "
            +
            grade_scores["grade"].astype(str)
        )

        st.subheader(
            "Average Score by Grade"
        )

        st.bar_chart(
            grade_scores.set_index(
                "grade"
            )[
                ["average_score"]
            ],
            height=350
        )


    # --------------------------------------------------------
    # DISTRICT TEST SCORE
    # --------------------------------------------------------

    if selected_district == "All Districts":

        district_scores = (
            test_filtered
            .groupby(
                "district",
                as_index=False
            )
            .agg(
                average_score=(
                    "average_score_percentage",
                    "mean"
                )
            )
            .sort_values(
                "average_score",
                ascending=False
            )
        )

        st.subheader(
            "Average Test Score by District"
        )

        st.bar_chart(
            district_scores.set_index(
                "district"
            )[
                ["average_score"]
            ],
            height=400
        )


else:

    st.info(
        "No test score data available for the selected filters."
    )


# ============================================================

# ============================================================
# DISTRICT PERFORMANCE SUMMARY
# ============================================================

st.markdown(
    '<div class="section-title">📍 District Performance Summary</div>',
    unsafe_allow_html=True
)

if len(filtered_school_dim) > 0:

    district_performance = filtered_school_dim[
        ["district"]
    ].drop_duplicates().copy()

    # Attendance and attendance-integrity metrics
    if len(attendance_filtered) > 0:

        d_att = (
            attendance_filtered
            .groupby("district", as_index=False)
            .agg(
                total_present=("total_students_present", "sum"),
                total_observed=("total_students_observed", "sum"),
                proxy_records=("proxy_attendance_records", "sum"),
                attendance_records=("attendance_records", "sum")
            )
        )

        d_att["Attendance %"] = (
            d_att["total_present"] /
            d_att["total_observed"] * 100
        )

        d_att["Proxy Attendance %"] = (
            d_att["proxy_records"] /
            d_att["attendance_records"] * 100
        )

        district_performance = district_performance.merge(
            d_att[
                ["district", "Attendance %", "Proxy Attendance %"]
            ],
            on="district",
            how="left"
        )

    # Learning metric
    if len(test_filtered) > 0:

        d_test = (
            test_filtered
            .groupby("district", as_index=False)
            .agg(
                **{
                    "Test Score %": (
                        "average_score_percentage",
                        "mean"
                    )
                }
            )
        )

        district_performance = district_performance.merge(
            d_test,
            on="district",
            how="left"
        )

    # Infrastructure metric
    if len(infra_filtered) > 0:

        d_infra = (
            infra_filtered
            .groupby("district", as_index=False)
            .agg(
                **{
                    "Infrastructure Deficit %": (
                        "infrastructure_deficit_pct",
                        "mean"
                    )
                }
            )
        )

        district_performance = district_performance.merge(
            d_infra,
            on="district",
            how="left"
        )

    # Round metrics for clean presentation
    for col in [
        "Attendance %",
        "Test Score %",
        "Infrastructure Deficit %",
        "Proxy Attendance %"
    ]:
        if col in district_performance.columns:
            district_performance[col] = pd.to_numeric(
                district_performance[col],
                errors="coerce"
            ).round(1)

    district_performance = district_performance.sort_values(
        "Attendance %",
        ascending=True,
        na_position="last"
    )

    st.caption(
        "District-level comparison of attendance, learning outcomes, "
        "infrastructure gaps and attendance-integrity signals."
    )

    st.dataframe(
        district_performance,
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Higher attendance and test-score percentages indicate stronger "
        "outcomes. Lower infrastructure deficit is better. Proxy attendance "
        "is an integrity signal for review, not proof of misconduct."
    )

    st.info(
        "Decision use: compare districts first, then use the Priority Schools "
        "section to identify individual schools requiring closer review."
    )

else:

    st.info("No districts match the selected filters.")


# CROSS-DOMAIN ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🔗 Cross-Domain Analysis'
    '</div>',
    unsafe_allow_html=True
)


if (
    len(attendance_filtered) > 0
    and len(infra_filtered) > 0
):

    # --------------------------------------------------------
    # ATTENDANCE BY SCHOOL
    # --------------------------------------------------------

    attendance_school = (
        attendance_filtered
        .groupby(
            "school_id",
            as_index=False
        )
        .agg(
            attendance_rate=(
                "avg_attendance_rate",
                "mean"
            )
        )
    )


    # --------------------------------------------------------
    # INFRASTRUCTURE BY SCHOOL
    # --------------------------------------------------------

    infra_school = (
        infra_filtered
        .groupby(
            "school_id",
            as_index=False
        )
        .agg(
            infrastructure_deficit=(
                "infrastructure_deficit_pct",
                "mean"
            )
        )
    )


    # --------------------------------------------------------
    # MERGE
    # --------------------------------------------------------

    cross_domain = attendance_school.merge(
        infra_school,
        on="school_id",
        how="inner"
    )


    if len(cross_domain) >= 2:

        correlation = (
            cross_domain[
                [
                    "attendance_rate",
                    "infrastructure_deficit"
                ]
            ]
            .corr()
            .iloc[0, 1]
        )


        cross_col1, cross_col2 = st.columns(2)


        with cross_col1:

            st.metric(
                "Attendance vs Infrastructure Correlation",
                f"{correlation:.2f}"
            )

            if correlation < 0:

                st.markdown(
                    """
                    <div class="insight-box">
                    <b>Insight:</b> Schools with higher infrastructure
                    deficits tend to show lower attendance in the selected
                    data. This is a descriptive relationship and does not
                    establish causation.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif correlation > 0:

                st.markdown(
                    """
                    <div class="insight-box">
                    <b>Insight:</b> The selected data shows a positive
                    relationship between infrastructure deficit and
                    attendance. This relationship requires further
                    investigation before drawing causal conclusions.
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    """
                    <div class="insight-box">
                    <b>Insight:</b> The relationship between infrastructure
                    deficit and attendance is weak in the selected data.
                    </div>
                    """,
                    unsafe_allow_html=True
                )


        with cross_col2:

            st.subheader(
                "Infrastructure Deficit vs Attendance"
            )

            chart_data = cross_domain[
                [
                    "infrastructure_deficit",
                    "attendance_rate"
                ]
            ].copy()

            chart_data.columns = [
                "Infrastructure Deficit",
                "Attendance Rate"
            ]

            st.scatter_chart(
                chart_data,
                x="Infrastructure Deficit",
                y="Attendance Rate",
                height=330
            )

else:

    st.info(
        "Cross-domain analysis requires both attendance "
        "and infrastructure data."
    )


# ============================================================
# PRIORITY SCHOOLS
# ============================================================

st.markdown(
    '<div class="section-title">'
    '🚨 Priority Schools'
    '</div>',
    unsafe_allow_html=True
)


if len(filtered_school_dim) > 0:

    priority = filtered_school_dim[
        [
            "school_id",
            "school_name",
            "district",
            "block"
        ]
    ].copy()


    # ========================================================
    # ATTENDANCE
    # ========================================================

    if len(attendance_filtered) > 0:

        attendance_priority = (
            attendance_filtered
            .groupby(
                "school_id",
                as_index=False
            )
            .agg(
                attendance_rate=(
                    "avg_attendance_rate",
                    "mean"
                ),
                proxy_rate=(
                    "proxy_attendance_rate",
                    "mean"
                )
            )
        )

        priority = priority.merge(
            attendance_priority,
            on="school_id",
            how="left"
        )

    else:

        priority["attendance_rate"] = pd.NA
        priority["proxy_rate"] = pd.NA


    # ========================================================
    # INFRASTRUCTURE
    # ========================================================

    if len(infra_filtered) > 0:

        infra_priority = (
            infra_filtered
            .groupby(
                "school_id",
                as_index=False
            )
            .agg(
                infrastructure_deficit=(
                    "infrastructure_deficit_pct",
                    "mean"
                )
            )
        )

        priority = priority.merge(
            infra_priority,
            on="school_id",
            how="left"
        )

    else:

        priority[
            "infrastructure_deficit"
        ] = pd.NA


    # ========================================================
    # LEARNING
    # ========================================================

    if len(test_filtered) > 0:

        learning_priority = (
            test_filtered
            .groupby(
                "school_id",
                as_index=False
            )
            .agg(
                average_score=(
                    "average_score_percentage",
                    "mean"
                )
            )
        )

        priority = priority.merge(
            learning_priority,
            on="school_id",
            how="left"
        )

    else:

        priority["average_score"] = pd.NA


    # ========================================================
    # RISK COMPONENTS
    # ========================================================

    priority["attendance_risk"] = (
        100 -
        pd.to_numeric(
            priority["attendance_rate"],
            errors="coerce"
        )
    )


    priority["learning_risk"] = (
        100 -
        pd.to_numeric(
            priority["average_score"],
            errors="coerce"
        )
    )


    priority["infrastructure_risk"] = (
        pd.to_numeric(
            priority["infrastructure_deficit"],
            errors="coerce"
        )
    )


    priority["proxy_risk"] = (
        pd.to_numeric(
            priority["proxy_rate"],
            errors="coerce"
        )
    )


    # ========================================================
    # HANDLE MISSING VALUES
    # ========================================================

    risk_columns = [
        "attendance_risk",
        "learning_risk",
        "infrastructure_risk",
        "proxy_risk"
    ]

    priority[risk_columns] = (
        priority[risk_columns]
        .fillna(0)
    )


    # ========================================================
    # PRIORITY SCORE
    # ========================================================

    priority["priority_score"] = (
        priority["attendance_risk"] * 0.35
        +
        priority["learning_risk"] * 0.30
        +
        priority["infrastructure_risk"] * 0.25
        +
        priority["proxy_risk"] * 0.10
    )


    # ========================================================
    # PRIORITY LEVEL
    # ========================================================

    def get_priority_level(score):

        if score >= 40:

            return "🔴 High"

        elif score >= 25:

            return "🟠 Medium"

        else:

            return "🟢 Low"


    priority["priority_level"] = (
        priority["priority_score"]
        .apply(get_priority_level)
    )


    priority = priority.sort_values(
        "priority_score",
        ascending=False
    )


    # ========================================================
    # PRIORITY SUMMARY
    # ========================================================

    high_priority = int(
        (priority["priority_level"] == "🔴 High").sum()
    )
    medium_priority = int(
        (priority["priority_level"] == "🟠 Medium").sum()
    )
    low_priority = int(
        (priority["priority_level"] == "🟢 Low").sum()
    )

    p1, p2, p3 = st.columns(3)

    with p1:
        st.metric("🔴 High Priority Schools", f"{high_priority:,}")

    with p2:
        st.metric("🟠 Medium Priority Schools", f"{medium_priority:,}")

    with p3:
        st.metric("🟢 Low Priority Schools", f"{low_priority:,}")

    st.caption(
        "Priority levels are screening categories intended to help "
        "decision-makers focus attention on schools with the greatest "
        "combined gaps."
    )

    # ========================================================
    # DISPLAY TOP 15
    # ========================================================

    st.caption(
        "Priority Score is a screening score based on attendance, "
        "learning outcomes, infrastructure deficit and proxy attendance. "
        "It is not a trained predictive model."
    )


    display_priority = priority.head(
        15
    ).copy()


    display_priority[
        "priority_score"
    ] = (
        display_priority[
            "priority_score"
        ].round(1)
    )


    display_priority[
        "attendance_rate"
    ] = (
        display_priority[
            "attendance_rate"
        ].round(1)
    )


    display_priority[
        "average_score"
    ] = (
        display_priority[
            "average_score"
        ].round(1)
    )


    display_priority[
        "infrastructure_deficit"
    ] = (
        display_priority[
            "infrastructure_deficit"
        ].round(1)
    )


    display_priority[
        "proxy_rate"
    ] = (
        display_priority[
            "proxy_rate"
        ].round(1)
    )


    display_priority = display_priority[
        [
            "school_id",
            "school_name",
            "district",
            "block",
            "priority_level",
            "priority_score",
            "attendance_rate",
            "average_score",
            "infrastructure_deficit",
            "proxy_rate"
        ]
    ]


    display_priority.columns = [
        "School ID",
        "School Name",
        "District",
        "Block",
        "Priority Level",
        "Priority Score",
        "Attendance %",
        "Test Score %",
        "Infrastructure Deficit %",
        "Proxy Attendance %"
    ]


    st.dataframe(
        display_priority,
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "⬇️ Download Priority Schools CSV",
        data=display_priority.to_csv(index=False).encode("utf-8"),
        file_name="priority_schools.csv",
        mime="text/csv"
    )


else:

    st.info(
        "No schools match the selected filters."
    )


# ============================================================
# METHODOLOGY
# ============================================================

with st.expander(
    "ℹ️ Dashboard Methodology & Data Notes"
):

    st.markdown(
        """
        ### Data Sources

        This dashboard integrates five cleaned analytical datasets:

        - School Master
        - Student Attendance
        - Mid-Day Meal Procurement
        - School Infrastructure
        - Test Scores

        ### Attendance Rate

        Attendance is calculated using:

        `Total Students Present / Total Students Observed × 100`

        ### Proxy Attendance Rate

        Proxy attendance is calculated using:

        `Proxy Attendance Records / Attendance Records × 100`

        Proxy attendance anomalies are retained for analysis rather
        than silently deleted.

        ### Infrastructure Deficit

        Infrastructure deficit represents the percentage of checked
        basic amenities that are unavailable.

        ### Test Score

        Test scores were standardized to percentage during the
        data-cleaning stage.

        ### Priority Score

        The screening score combines:

        - Attendance risk: 35%
        - Learning risk: 30%
        - Infrastructure risk: 25%
        - Proxy attendance risk: 10%

        Priority levels:

        - 🔴 High: score >= 40
        - 🟠 Medium: score >= 25
        - 🟢 Low: score < 25

        The priority score is intended to help prioritize schools
        for review. It is not a trained machine-learning prediction.

        ### Interpretation

        Correlations shown in this dashboard represent descriptive
        relationships and should not be interpreted as causal effects.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Student Retention & Welfare Efficacy Tracker | "
    "Education & EdTech Datathon"
)