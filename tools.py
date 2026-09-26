from langchain_core.tools import tool
from langchain_core.documents import Document

import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os

from dotenv import load_dotenv
from rich import print

load_dotenv()


# ============================================================
# TAVILY CLIENT
# ============================================================

tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)


# ============================================================
# TOOL 1: WEB SEARCH
# ============================================================

@tool
def web_search(query: str) -> str:
    """
    Search the web for recent and reliable information.

    Returns:
    - Source titles
    - URLs
    - Search snippets
    """

    try:
        results = tavily.search(
            query=query,
            max_results=5
        )

        out = []

        for r in results["results"]:

            out.append(
                f"Title: {r['title']}\n"
                f"URL: {r['url']}\n"
                f"Snippet: {r['content'][:500]}\n"
            )

        return "\n----\n".join(out)

    except Exception as e:

        return f"Web search failed: {str(e)}"


# ============================================================
# TOOL 2: BASIC URL SCRAPER
# ============================================================

@tool
def scrape_url(url: str) -> str:
    """
    Scrape and return clean text content from a URL.

    This version is kept for the existing AI Reader Agent.
    """

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # Remove unnecessary HTML elements
        for tag in soup(
            [
                "script",
                "style",
                "nav",
                "footer",
                "header",
                "aside",
                "form"
            ]
        ):
            tag.decompose()

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        # Limit returned text
        return text[:10000]

    except Exception as e:

        return f"Could not scrape URL: {str(e)}"


# ============================================================
# TOOL 3: RAG DOCUMENT SCRAPER
# ============================================================

def scrape_url_document(url: str):
    """
    Scrape a webpage and convert it into a LangChain Document.

    This function is used by the RAG pipeline.

    The Document contains:

        page_content
            -> actual webpage text

        metadata
            -> information about where the text came from
    """

    try:

        response = requests.get(
            url,
            timeout=10,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        # ----------------------------------------------------
        # Remove unnecessary HTML
        # ----------------------------------------------------

        for tag in soup(
            [
                "script",
                "style",
                "nav",
                "footer",
                "header",
                "aside",
                "form",
                "noscript"
            ]
        ):
            tag.decompose()

        # ----------------------------------------------------
        # Extract clean text
        # ----------------------------------------------------

        text = soup.get_text(
            separator=" ",
            strip=True
        )

        # ----------------------------------------------------
        # Create LangChain Document
        # ----------------------------------------------------

        document = Document(
            page_content=text,
            metadata={
                "source": url
            }
        )

        return document

    except Exception as e:

        print(f"Scraping failed for {url}: {e}")

        # Return an empty document instead of crashing
        return Document(
            page_content="",
            metadata={
                "source": url,
                "error": str(e)
            }
        )


# ============================================================
# HELPER: SCRAPE MULTIPLE URLS
# ============================================================

def scrape_multiple_urls(urls):
    """
    Scrape multiple URLs and return a list of LangChain Documents.

    Example:

        urls = [
            "https://example.com/article1",
            "https://example.com/article2"
        ]

        documents = scrape_multiple_urls(urls)
    """

    documents = []

    for url in urls:

        document = scrape_url_document(url)

        # Only keep documents that contain actual text
        if document.page_content.strip():

            documents.append(document)

    return documents