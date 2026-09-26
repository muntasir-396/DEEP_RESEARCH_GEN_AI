# Architecture Report: Baseline Inspection & Target Retrieval Engineering

## 1. Current Architecture
The current system (`DEEP_RESEARCH_GEN_AI -old`) is an ephemeral, agentic web-research tool built with LangGraph, LangChain, Tavily API, BeautifulSoup, and Mistral AI (`mistral-small-latest`).

### Data Flow
1. **User Query** is received via CLI (`pipeline.py`) or Streamlit UI (`app.py`).
2. **Search Phase (`Search Agent`)**: LangGraph ReAct agent queries Tavily API for top 5 web results with snippet truncations (300 chars).
3. **Reading Phase (`Reader Agent`)**: Agent selects a single target URL and runs `scrape_url` via `requests` + `BeautifulSoup` (truncated to 3,000 chars).
4. **Synthesis Phase (`Writer Chain`)**: Mistral Small formats the scraped content into a markdown report.
5. **Critique Phase (`Critic Chain`)**: Mistral Small grades the draft from 1–10.

### Key Files
* `tools.py`: Tavily search wrapper (`web_search`) and requests/BS4 scraper (`scrape_url`).
* `agents.py`: Search and reader agent constructors (`create_react_agent`), writer and critic prompts/chains using `ChatMistralAI`.
* `pipeline.py`: Synchronous CLI orchestration script.
* `app.py`: Streamlit UI handling state transitions, step-by-step rendering, and file exports.
* `requirements.txt`: Project dependencies (`langchain`, `langchain-mistralai`, `langgraph`, `tavily-python`, `beautifulsoup4`, `streamlit`, `python-dotenv`).

## 2. Identified Problems & Architectural Gaps
* **No Information Retrieval Layer**: Retrieval relies strictly on external web search APIs (Tavily). No local sparse or dense index exists.
* **No Vector Similarity Search**: No embedding model or vector database is integrated.
* **Primitive Chunking**: Context is cut off using arbitrary character slicing (`[:300]`, `[:3000]`), splitting words and losing semantic boundaries.
* **Absence of Evaluation Framework**: No quantitative IR metrics (Recall@K, MRR, NDCG@K) or ground-truth evaluation datasets exist.
* **Tight Coupling**: UI and CLI directly invoke agent execution loops without an abstraction layer separating document retrieval from response generation.

## 3. Proposed Target Architecture
We will introduce a dedicated `retrieval/` engine leaving existing components intact: