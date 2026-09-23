import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv



# GEMINI IMPORT

try:
    from google import genai
    GEMINI_AVAILABLE = True
except Exception:
    GEMINI_AVAILABLE = False


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="AI Business Intelligence Copilot",
    page_icon="🤖",
    layout="wide"
)


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: bold;
    }

    .section-title {
        font-size: 28px;
        font-weight: bold;
        margin-top: 20px;
    }

    .insight-box {
        padding: 20px;
        border-radius: 10px;
        margin-top: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# GEMINI AI SETUP
# ==================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = None

if GEMINI_AVAILABLE and api_key:

    try:
        client = genai.Client(
            api_key=api_key
        )

    except Exception:
        client = None


# ==================================================
# LOAD DATASET
# ==================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "Europe Sales Records.csv"
    )

    # Convert dates
    df["Order Date"] = pd.to_datetime(
        df["Order Date"],
        errors="coerce"
    )

    df["Ship Date"] = pd.to_datetime(
        df["Ship Date"],
        errors="coerce"
    )

    return df


df = load_data()


# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("🔍 Dashboard Filters")


# --------------------------------------------------
# DATE VALUES
# --------------------------------------------------

min_date = df["Order Date"].min().date()
max_date = df["Order Date"].max().date()


# --------------------------------------------------
# RESET FILTERS FUNCTION
# --------------------------------------------------

def reset_filters():

    st.session_state.country_filter = []

    st.session_state.product_filter = []

    st.session_state.channel_filter = []

    st.session_state.date_filter = (
        min_date,
        max_date
    )


# --------------------------------------------------
# DATE FILTER
# --------------------------------------------------

st.sidebar.subheader("📅 Select Date Range")

date_range = st.sidebar.date_input(

    "Order Date",

    value=(min_date, max_date),

    min_value=min_date,

    max_value=max_date,

    key="date_filter"
)


# --------------------------------------------------
# COUNTRY FILTER
# --------------------------------------------------

st.sidebar.subheader("🌍 Select Country")

countries = sorted(
    df["Country"].dropna().unique()
)


selected_countries = st.sidebar.multiselect(

    "Choose options",

    countries,

    key="country_filter"
)


# --------------------------------------------------
# PRODUCT FILTER
# --------------------------------------------------

st.sidebar.subheader("📦 Select Product")

products = sorted(
    df["Item Type"].dropna().unique()
)


selected_products = st.sidebar.multiselect(

    "Choose options",

    products,

    key="product_filter"
)


# --------------------------------------------------
# SALES CHANNEL FILTER
# --------------------------------------------------

st.sidebar.subheader("🛒 Select Sales Channel")

channels = sorted(
    df["Sales Channel"].dropna().unique()
)


selected_channels = st.sidebar.multiselect(

    "Choose options",

    channels,

    key="channel_filter"
)


# --------------------------------------------------
# RESET FILTERS BUTTON
# --------------------------------------------------

st.sidebar.button(

    "🔄 Reset Filters",

    on_click=reset_filters
)


# ==================================================
# APPLY FILTERS
# ==================================================

filtered_df = df.copy()


# DATE FILTER

if len(date_range) == 2:

    start_date = pd.to_datetime(
        date_range[0]
    )

    end_date = pd.to_datetime(
        date_range[1]
    )

    filtered_df = filtered_df[
        (
            filtered_df["Order Date"]
            >= start_date
        )
        &
        (
            filtered_df["Order Date"]
            <= end_date
        )
    ]


# COUNTRY FILTER

if selected_countries:

    filtered_df = filtered_df[
        filtered_df["Country"].isin(
            selected_countries
        )
    ]


# PRODUCT FILTER

if selected_products:

    filtered_df = filtered_df[
        filtered_df["Item Type"].isin(
            selected_products
        )
    ]


# SALES CHANNEL FILTER

if selected_channels:

    filtered_df = filtered_df[
        filtered_df["Sales Channel"].isin(
            selected_channels
        )
    ]


# ==================================================
# CHECK DATA
# ==================================================

if filtered_df.empty:

    st.warning(
        "⚠️ No data available for the selected filters."
    )

    st.stop()


# ==================================================
# CALCULATE KPIs
# ==================================================

total_revenue = filtered_df[
    "Total Revenue"
].sum()


total_profit = filtered_df[
    "Total Profit"
].sum()


total_units = filtered_df[
    "Units Sold"
].sum()


total_orders = filtered_df[
    "Order ID"
].nunique()


profit_margin = (

    total_profit
    /
    total_revenue
    *
    100

) if total_revenue != 0 else 0


average_order_value = (

    total_revenue
    /
    total_orders

) if total_orders != 0 else 0


# ==================================================
# CALCULATE BUSINESS DATA
# ==================================================

country_revenue = (

    filtered_df

    .groupby("Country")[
        "Total Revenue"
    ]

    .sum()

    .reset_index()

    .sort_values(
        by="Total Revenue",
        ascending=False
    )

)


product_revenue = (

    filtered_df

    .groupby("Item Type")[
        "Total Revenue"
    ]

    .sum()

    .reset_index()

    .sort_values(
        by="Total Revenue",
        ascending=False
    )

)


product_profit = (

    filtered_df

    .groupby("Item Type")[
        "Total Profit"
    ]

    .sum()

    .reset_index()

    .sort_values(
        by="Total Profit",
        ascending=False
    )

)


country_units = (

    filtered_df

    .groupby("Country")[
        "Units Sold"
    ]

    .sum()

    .reset_index()

    .sort_values(
        by="Units Sold",
        ascending=False
    )

)


channel_revenue = (

    filtered_df

    .groupby("Sales Channel")[
        "Total Revenue"
    ]

    .sum()

    .reset_index()

    .sort_values(
        by="Total Revenue",
        ascending=False
    )

)


# ==================================================
# TITLE
# ==================================================

st.markdown(
    '<p class="main-title">'
    '🤖 AI-Powered Business Intelligence Copilot'
    '</p>',
    unsafe_allow_html=True
)


st.write(
    "Analyze your sales data using interactive "
    "dashboards and AI-powered business insights."
)



# ---------------------------------------
# BUSINESS OVERVIEW
# ---------------------------------------

st.markdown(
    '<p class="section-title">'
    '📊 Business Overview'
    '</p>',
    unsafe_allow_html=True
)


# Create 6 columns
col1, col2, col3, col4, col5, col6 = st.columns(6)


# Revenue - Show in Millions
col1.metric(
    "💰 Revenue",
    f"${total_revenue / 1_000_000:.2f}M"
)


# Profit - Show in Millions
col2.metric(
    "💵 Profit",
    f"${total_profit / 1_000_000:.2f}M"
)


# Total Units Sold
col3.metric(
    "📦 Units",
    f"{total_units:,}"
)


# Total Orders
col4.metric(
    "🧾 Orders",
    f"{total_orders:,}"
)


# Profit Margin
col5.metric(
    "📈 Profit Margin",
    f"{profit_margin:.2f}%"
)


# Average Order Value
col6.metric(
    "💳 Avg Order",
    f"${average_order_value:,.0f}"
)

# ==================================================
# QUICK BUSINESS INSIGHTS
# ==================================================

st.markdown(
    '<p class="section-title">'
    '⚡ Quick Business Insights'
    '</p>',
    unsafe_allow_html=True
)


top_country = country_revenue.iloc[0]

top_product = product_revenue.iloc[0]

top_profit_product = product_profit.iloc[0]

top_units_country = country_units.iloc[0]

top_channel = channel_revenue.iloc[0]


insight_col1, insight_col2, insight_col3 = st.columns(3)


with insight_col1:

    st.info(
        f"""
🌍 Top Country

**{top_country["Country"]}**

Revenue:
**${top_country["Total Revenue"]:,.0f}**
"""
    )


with insight_col2:

    st.success(
        f"""
🏆 Best Product

**{top_product["Item Type"]}**

Revenue:
**${top_product["Total Revenue"]:,.0f}**
"""
    )


with insight_col3:

    st.warning(
        f"""
📦 Maximum Units Sold

**{top_units_country["Country"]}**

Units:
**{top_units_country["Units Sold"]:,.0f}**
"""
    )


# ==================================================
# DASHBOARD TABS
# ==================================================

tab1, tab2, tab3, tab4 = st.tabs(

    [
        "🌍 Revenue Analysis",
        "💰 Profit Analysis",
        "📈 Trends",
        "📊 Data Preview"
    ]

)


# ==================================================
# TAB 1 - REVENUE
# ==================================================

with tab1:


    st.subheader(
        "🌍 Revenue by Country"
    )


    fig_country = px.bar(

        country_revenue,

        x="Country",

        y="Total Revenue",

        title="Total Revenue by Country",

        labels={
            "Country": "Country",
            "Total Revenue": "Revenue ($)"
        }

    )


    st.plotly_chart(
        fig_country,
        use_container_width=True
    )


    st.subheader(
        "🏆 Product Revenue"
    )


    fig_product = px.bar(

        product_revenue,

        x="Item Type",

        y="Total Revenue",

        title="Revenue by Product",

        labels={
            "Item Type": "Product",
            "Total Revenue": "Revenue ($)"
        }

    )


    st.plotly_chart(
        fig_product,
        use_container_width=True
    )


    st.subheader(
        "🛒 Revenue by Sales Channel"
    )


    fig_channel = px.bar(

        channel_revenue,

        x="Sales Channel",

        y="Total Revenue",

        title="Revenue by Sales Channel"

    )


    st.plotly_chart(
        fig_channel,
        use_container_width=True
    )


# ==================================================
# TAB 2 - PROFIT
# ==================================================

with tab2:


    st.subheader(
        "💰 Profit by Product"
    )


    fig_profit = px.bar(

        product_profit,

        x="Item Type",

        y="Total Profit",

        title="Total Profit by Product",

        labels={
            "Item Type": "Product",
            "Total Profit": "Profit ($)"
        }

    )


    st.plotly_chart(
        fig_profit,
        use_container_width=True
    )


    st.subheader(
        "📊 Profit Distribution"
    )


    fig_pie = px.pie(

        product_profit,

        names="Item Type",

        values="Total Profit",

        title="Profit Contribution by Product"

    )


    st.plotly_chart(
        fig_pie,
        use_container_width=True
    )


# ==================================================
# TAB 3 - TRENDS
# ==================================================

with tab3:


    st.subheader(
        "📈 Monthly Revenue Trend"
    )


    monthly_revenue = (

        filtered_df

        .set_index("Order Date")

        .resample("ME")[
            "Total Revenue"
        ]

        .sum()

        .reset_index()

    )


    fig_month = px.line(

        monthly_revenue,

        x="Order Date",

        y="Total Revenue",

        title="Monthly Revenue Trend"

    )


    st.plotly_chart(
        fig_month,
        use_container_width=True
    )


    st.subheader(
        "📦 Units Sold by Country"
    )


    fig_units = px.bar(

        country_units.head(15),

        x="Country",

        y="Units Sold",

        title="Top Countries by Units Sold"

    )


    st.plotly_chart(
        fig_units,
        use_container_width=True
    )


# ==================================================
# TAB 4 - DATA PREVIEW
# ==================================================

with tab4:


    st.subheader(
        "📊 Filtered Dataset"
    )


    st.dataframe(
        filtered_df,
        use_container_width=True
    )


# ==================================================
# DOWNLOAD BUSINESS REPORT
# ==================================================

st.divider()


st.subheader(
    "📥 Download Business Report"
)


report_data = pd.DataFrame({

    "Metric": [

        "Total Revenue",
        "Total Profit",
        "Profit Margin",
        "Units Sold",
        "Total Orders",
        "Average Order Value",
        "Top Country",
        "Top Product",
        "Most Profitable Product",
        "Top Sales Channel"

    ],

    "Value": [

        f"${total_revenue:,.2f}",

        f"${total_profit:,.2f}",

        f"{profit_margin:.2f}%",

        f"{total_units:,}",

        f"{total_orders:,}",

        f"${average_order_value:,.2f}",

        top_country["Country"],

        top_product["Item Type"],

        top_profit_product["Item Type"],

        top_channel["Sales Channel"]

    ]

})


csv = report_data.to_csv(
    index=False
).encode("utf-8")


st.download_button(

    label="📥 Download Business Summary Report",

    data=csv,

    file_name="business_report.csv",

    mime="text/csv"

)


# ==================================================
# LOCAL AI INSIGHT FUNCTION
# ==================================================

def get_local_insight(question):


    question_lower = question.lower()


    # ----------------------------------------------
    # DETECT PRODUCT IN QUESTION
    # ----------------------------------------------

    detected_product = None


    for product in products:

        if product.lower() in question_lower:

            detected_product = product

            break


    # ----------------------------------------------
    # COUNTRY WITH MAXIMUM UNITS
    # ----------------------------------------------

    if (

        "country" in question_lower

        and

        (
            "maximum unit" in question_lower
            or
            "max unit" in question_lower
            or
            "most unit" in question_lower
            or
            "maximum units" in question_lower
            or
            "units sold" in question_lower
        )

    ):


        units_df = filtered_df.copy()


        # Filter product if detected

        if detected_product:

            units_df = units_df[
                units_df["Item Type"]
                == detected_product
            ]


        country_product_units = (

            units_df

            .groupby("Country")[
                "Units Sold"
            ]

            .sum()

            .reset_index()

            .sort_values(
                by="Units Sold",
                ascending=False
            )

        )


        top = country_product_units.iloc[0]


        if detected_product:

            return f"""
# 📊 Business Insights

## 🌍 Country with Maximum Units Sold

**{top["Country"]}** sold the maximum number of units of **{detected_product}**.

📦 **Units Sold: {top["Units Sold"]:,.0f}**

This result is based on your currently selected filters.
"""


        else:

            return f"""
# 📊 Business Insights

## 🌍 Country with Maximum Units Sold

**{top["Country"]}** sold the maximum number of units.

📦 **Units Sold: {top["Units Sold"]:,.0f}**

This result is based on your currently selected filters.
"""


    # ----------------------------------------------
    # TOP COUNTRY BY REVENUE
    # ----------------------------------------------

    elif (

        "country" in question_lower

        and

        (
            "highest revenue" in question_lower
            or
            "top country" in question_lower
            or
            "best country" in question_lower
            or
            "maximum revenue" in question_lower
        )

    ):


        return f"""
# 📊 Business Insights

## 🌍 Top Performing Country

**{top_country["Country"]}** generated the highest revenue.

💰 **Revenue: ${top_country["Total Revenue"]:,.0f}**

This result is based on your currently selected filters.
"""


    # ----------------------------------------------
    # PRODUCT REVENUE
    # ----------------------------------------------

    elif (

        "product" in question_lower
        or
        "item" in question_lower

    ) and (

        "highest" in question_lower
        or
        "top" in question_lower
        or
        "best" in question_lower
        or
        "maximum" in question_lower

    ):


        return f"""
# 📊 Business Insights

## 🏆 Best Performing Product

**{top_product["Item Type"]}** generated the highest revenue.

💰 **Revenue: ${top_product["Total Revenue"]:,.0f}**

This result is based on your currently selected filters.
"""


    # ----------------------------------------------
    # TOTAL REVENUE
    # ----------------------------------------------

    elif (

        "total revenue" in question_lower

        or

        question_lower.strip()
        == "revenue"

    ):


        return f"""
# 💰 Revenue Analysis

## Total Revenue

### ${total_revenue:,.0f}

📊 Average Order Value:

### ${average_order_value:,.0f}

This result is based on your currently selected filters.
"""


    # ----------------------------------------------
    # PROFIT
    # ----------------------------------------------

    elif (

        "profit" in question_lower

    ):


        return f"""
# 💵 Profit Analysis

## Total Profit

### ${total_profit:,.0f}

---

## 🏆 Most Profitable Product

**{top_profit_product["Item Type"]}**

💰 Profit:

### ${top_profit_product["Total Profit"]:,.0f}

---

📈 Profit Margin:

### {profit_margin:.2f}%
"""


    # ----------------------------------------------
    # SALES CHANNEL
    # ----------------------------------------------

    elif (

        "channel" in question_lower

        or

        "online" in question_lower

        or

        "offline" in question_lower

    ):


        return f"""
# 🛒 Sales Channel Analysis

## Best Sales Channel

**{top_channel["Sales Channel"]}**

generated the highest revenue.

💰 Revenue:

### ${top_channel["Total Revenue"]:,.0f}
"""


    # ----------------------------------------------
    # UNITS SOLD
    # ----------------------------------------------

    elif (

        "units" in question_lower

        or

        "unit sold" in question_lower

    ):


        return f"""
# 📦 Units Sold Analysis

## Total Units Sold

### {total_units:,}

---

## 🌍 Country with Maximum Units

**{top_units_country["Country"]}**

📦 Units:

### {top_units_country["Units Sold"]:,.0f}
"""


    # ----------------------------------------------
    # ORDERS
    # ----------------------------------------------

    elif (

        "order" in question_lower

    ):


        return f"""
# 🧾 Order Analysis

## Total Orders

### {total_orders:,}

---

💳 Average Order Value

### ${average_order_value:,.0f}
"""


    # ----------------------------------------------
    # OVERALL INSIGHTS
    # ----------------------------------------------

    else:


        return f"""
# 📊 Business Insights

## 🌍 Top Country

**{top_country["Country"]}**

💰 Revenue: **${top_country["Total Revenue"]:,.0f}**

---

## 🏆 Top Product

**{top_product["Item Type"]}**

💰 Revenue: **${top_product["Total Revenue"]:,.0f}**

---

## 💵 Most Profitable Product

**{top_profit_product["Item Type"]}**

💰 Profit: **${top_profit_product["Total Profit"]:,.0f}**

---

## 📦 Maximum Units Sold

**{top_units_country["Country"]}**

📦 Units: **{top_units_country["Units Sold"]:,.0f}**

---

## 🛒 Best Sales Channel

**{top_channel["Sales Channel"]}**

---

## 📈 Overall Performance

💰 Total Revenue: **${total_revenue:,.0f}**

💵 Total Profit: **${total_profit:,.0f}**

📦 Units Sold: **{total_units:,}**

🧾 Total Orders: **{total_orders:,}**

📈 Profit Margin: **{profit_margin:.2f}%**
"""


# ==================================================
# AI COPILOT
# ==================================================

st.divider()


st.markdown(
    '<p class="section-title">'
    '🤖 Ask AI About Your Business'
    '</p>',
    unsafe_allow_html=True
)


st.write(
    "Choose a suggested question or write your own question."
)


# ==================================================
# SUGGESTED QUESTIONS
# ==================================================

st.subheader(
    "💡 Suggested Questions"
)


question_col1, question_col2 = st.columns(2)


with question_col1:

    if st.button(
        "🌍 Which country generated the highest revenue?"
    ):

        st.session_state.question = (
            "Which country generated the highest revenue?"
        )


    if st.button(
        "📦 Which country sold the maximum units?"
    ):

        st.session_state.question = (
            "Which country sold the maximum units?"
        )


    if st.button(
        "🏆 Which product generated the highest revenue?"
    ):

        st.session_state.question = (
            "Which product generated the highest revenue?"
        )


    if st.button(
        "💵 Which product is most profitable?"
    ):

        st.session_state.question = (
            "Which product is most profitable?"
        )


with question_col2:

    if st.button(
        "💰 What is the total revenue?"
    ):

        st.session_state.question = (
            "What is the total revenue?"
        )


    if st.button(
        "📈 What is the profit margin?"
    ):

        st.session_state.question = (
            "What is the profit margin?"
        )


    if st.button(
        "🛒 Which sales channel generated the highest revenue?"
    ):

        st.session_state.question = (
            "Which sales channel generated the highest revenue?"
        )


    if st.button(
        "📊 Give me overall business insights"
    ):

        st.session_state.question = (
            "Give me overall business insights"
        )


# ==================================================
# MORE EXAMPLE QUESTIONS
# ==================================================

with st.expander(
    "📚 View More Questions You Can Ask"
):

    st.markdown(
        """
### 🌍 Country Questions

- Which country generated the highest revenue?
- Which country generated the lowest revenue?
- Which country sold the maximum units?
- Which country sold maximum units of Meat?
- Which country sold maximum units of Clothes?

### 📦 Product Questions

- Which product generated the highest revenue?
- Which product is most profitable?
- Which product sold the most units?
- Which product generated the least revenue?

### 💰 Revenue Questions

- What is the total revenue?
- What is the total profit?
- What is the profit margin?
- What is the average order value?

### 🛒 Sales Questions

- Which sales channel generated the highest revenue?
- How many total orders are there?
- How many units were sold?

### 📊 Business Questions

- Give me overall business insights
- What are the top business opportunities?
- Which product performs best?
- How is the business performing?
        """
    )


# ==================================================
# QUESTION INPUT
# ==================================================

question = st.text_input(

    "Ask a question about your sales data:",

    placeholder=(
        "Example: Which country sold the maximum units of Meat?"
    ),

    key="question"

)


# ==================================================
# GET AI INSIGHT
# ==================================================

if st.button(
    "Get AI Insight 🚀",
    type="primary"
):


    if not question:

        st.warning(
            "⚠️ Please enter a question first."
        )


    else:


        # ==========================================
        # DATA SUMMARY
        # ==========================================

        top_countries_text = (

            country_revenue

            .head(10)

            .to_string(
                index=False
            )

        )


        top_products_text = (

            product_revenue

            .head(10)

            .to_string(
                index=False
            )

        )


        top_profit_text = (

            product_profit

            .head(10)

            .to_string(
                index=False
            )

        )


        top_units_text = (

            country_units

            .head(10)

            .to_string(
                index=False
            )

        )


        data_summary = f"""

BUSINESS SUMMARY

Total Revenue:
${total_revenue:,.2f}

Total Profit:
${total_profit:,.2f}

Profit Margin:
{profit_margin:.2f}%

Total Units Sold:
{total_units:,}

Total Orders:
{total_orders:,}

Average Order Value:
${average_order_value:,.2f}


TOP COUNTRIES BY REVENUE

{top_countries_text}


TOP PRODUCTS BY REVENUE

{top_products_text}


TOP PRODUCTS BY PROFIT

{top_profit_text}


TOP COUNTRIES BY UNITS SOLD

{top_units_text}

"""


        prompt = f"""

You are an AI Business Intelligence Assistant.

Analyze the following sales data.

{data_summary}

User Question:

{question}

Instructions:

1. Give a clear and direct answer.
2. Use simple business language.
3. Mention important numbers.
4. Give useful business insights.
5. Keep the answer concise.
6. Do not invent data.
7. Only use the provided data.
8. Mention that results are based on selected filters.

"""


        # ==========================================
        # TRY GEMINI
        # ==========================================

        ai_success = False


        if client is not None:


            try:


                with st.spinner(
                    "🤖 AI is analyzing your business data..."
                ):


                    response = (

                        client.models.generate_content(

                            model=os.getenv(
                                "GEMINI_MODEL",
                                "gemini-2.5-flash"
                            ),

                            contents=prompt

                        )

                    )


                    st.success(
                        "🤖 AI Insight Generated!"
                    )


                    st.markdown(
                        response.text
                    )


                    ai_success = True


            except Exception as e:


                error_message = str(e)


                if (

                    "429" in error_message

                    or

                    "RESOURCE_EXHAUSTED"
                    in error_message

                ):


                    st.warning(
                        "⚠️ AI request limit reached."
                    )


                    st.info(
                        "Gemini API quota is temporarily "
                        "exhausted. Showing insights from "
                        "your dataset instead."
                    )


                elif "503" in error_message:


                    st.warning(
                        "⚠️ Gemini AI is currently busy."
                    )


                    st.info(
                        "Showing insights from your dataset "
                        "instead."
                    )


                else:


                    st.warning(
                        "⚠️ Gemini AI is temporarily unavailable."
                    )


                    st.info(
                        "Showing insights from your dataset "
                        "instead."
                    )


        # ==========================================
        # LOCAL FALLBACK
        # ==========================================

        if not ai_success:


            local_insight = get_local_insight(
                question
            )


            st.markdown(
                local_insight
            )


# ==================================================
# FOOTER
# ==================================================

st.divider()


st.caption(
    "🤖 AI Business Intelligence Copilot | "
    "Built with Streamlit, Plotly, Pandas & Gemini AI"
)