# AI-Powered Business Intelligence Copilot

An interactive business intelligence dashboard that analyzes sales data and provides AI-powered business insights using Google Gemini.

## 📌 Project Overview

The **AI-Powered Business Intelligence Copilot** is a Streamlit-based business analytics application that helps users understand sales performance through interactive dashboards, KPIs, charts, filters, and an AI assistant.

Users can filter the sales data and ask business-related questions such as:

* Which country generated the highest revenue?
* Which country sold the maximum units?
* Which product generated the highest revenue?
* Which product is most profitable?
* What is the total revenue?
* What is the total profit?
* What is the profit margin?

## 🚀 Features

* 📊 Interactive business dashboard
* 💰 Total Revenue and Profit KPIs
* 📦 Units Sold and Order statistics
* 📈 Profit Margin and Average Order Value
* 🌍 Revenue analysis by country
* 🛍️ Product-wise revenue analysis
* 📅 Monthly revenue trends
* 💵 Product-wise profit analysis
* 🔎 Date, country, product, and sales-channel filters
* 🤖 AI Business Intelligence Copilot using Google Gemini
* 🐼 Pandas-based local analysis fallback
* 📋 Filtered dataset preview

## 🛠️ Technologies Used

* **Python**
* **Pandas**
* **Streamlit**
* **Plotly**
* **Google Gemini API**
* **python-dotenv**
* **Jupyter Notebook**
* **CSV Dataset**

## 📂 Project Structure

```text
AI-Business-Intelligence-Copilot/
│
├── app.py
├── AI_Business_Intelligence_Copilot.ipynb
├── Europe Sales Records.csv
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## ⚙️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/Tejas-hub44/AI-Business-Intelligence-Copilot.git
```

### 2. Open the project folder

```bash
cd AI-Business-Intelligence-Copilot
```

### 3. Install the required libraries

```bash
pip install -r requirements.txt
```

### 4. Create the `.env` file

Create a `.env` file in the project folder and add your Gemini API key:

```text
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

**Do not upload your `.env` file to GitHub.**

### 5. Run the Streamlit application

```bash
streamlit run app.py
```

The dashboard will open in your browser.

## 🤖 AI Copilot

The AI Copilot allows users to ask questions about the business data in natural language.

For example:

```text
Which country generated the highest revenue?
```

The application analyzes the available sales data and returns a business insight.

If Gemini AI is unavailable, the application can use local Pandas-based analysis for supported questions.

## 📊 Dashboard

The dashboard provides:

* Business Overview
* Revenue by Country
* Revenue by Product
* Monthly Revenue Trend
* Profit by Product
* Filtered Dataset
* AI Business Intelligence Copilot

## 🔐 API Key Security

The Gemini API key is stored in a local `.env` file and is excluded from Git using `.gitignore`.

The repository contains `.env.example` as a template so that users can configure their own API key.

## 🎯 Learning Outcomes

Through this project, I worked with:

* Data cleaning and analysis using Pandas
* Data visualization using Plotly
* Interactive dashboards using Streamlit
* API integration
* Generative AI integration using Google Gemini
* Environment variables and API-key security
* Git and GitHub version control
* Business intelligence and data-driven insights

## 👨‍💻 Author

**Tejas Malode**

Computer Science Engineering Student

GitHub: https://github.com/Tejas-hub44
