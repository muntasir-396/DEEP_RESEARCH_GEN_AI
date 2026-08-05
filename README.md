# 🔎 DEEP RESEARCH · AI Agent (Neural Engine v3.0)

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Mistral AI](https://img.shields.io/badge/Mistral_AI-F54E42?style=for-the-badge&logo=mistral-ai&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

An automated, AI-powered deep research assistant built with **Streamlit**, **LangGraph**, and **Mistral AI**. This application takes a complex topic or technical hypothesis and autonomously runs a 4-phase research pipeline to generate a well-structured, verified technical report.

## 🚀 How It Works

The AI Agent orchestrates a pipeline consisting of four distinct phases:

1. **Web Discovery (Search Agent)**: Utilizes the **Tavily Search API** to scour global indices for the most relevant and up-to-date information on the requested topic.
2. **Deep Extraction (Reader Agent)**: Navigates to the identified sources and scrapes the core technical data using **BeautifulSoup4**.
3. **Synthesis (Writer Chain)**: A specialized LangChain writer model synthesizes the extracted data into a structured report containing an Introduction, Key Findings, Conclusion, and Sources.
4. **Verification (Critic Chain)**: An independent critic model strictly evaluates the final report, providing a score out of 10, outlining strengths, areas to improve, and a one-line verdict.

## 🛠️ Tech Stack

- **Frontend Interface**: [Streamlit](https://streamlit.io/) for a beautiful, responsive dark-mode UI.
- **LLM Orchestration**: [LangChain](https://python.langchain.com/) & [LangGraph](https://python.langchain.com/docs/langgraph/) (`create_react_agent`) for agentic workflows.
- **Large Language Model**: [Mistral AI](https://mistral.ai/) (`mistral-small-latest` via `langchain-mistralai`).
- **Search Engine**: [Tavily API](https://tavily.com/) for optimized AI web search.
- **Web Scraping**: `beautifulsoup4`, `requests`, and `lxml` for extracting HTML content.
- **Environment Management**: `python-dotenv`.

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/muntasir-396/DEEP_RESEARCH_GEN_AI.git
   cd DEEP_RESEARCH_GEN_AI
   ```

2. **Install the dependencies**:
   Ensure you have Python 3 installed. Then, install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Environment Variables**:
   Copy the example environment file and add your API keys:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and add your keys for Mistral AI and Tavily:
   ```env
   MISTRAL_API_KEY=your_mistral_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   ```

## 💻 Running the App

To launch the Streamlit application, run the following command in your terminal:

```bash
streamlit run app.py
```

Navigate to `http://localhost:8501` in your browser to interact with the Neural Engine.

## 📝 Features

- **Live Progress Tracking**: Watch the UI update in real-time as the agents move from Phase 1 to Phase 4.
- **Critic Review**: Transparent evaluation of the generated report so you know exactly where the AI's research excels or falls short.
- **Export Data**: Easily download the final markdown report directly from the UI.