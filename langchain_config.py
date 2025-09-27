import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from newsapi import NewsApiClient
import streamlit as st

# Load keys #
load_dotenv()

groq_api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
news_api_key = st.secrets.get("NEWS_API_KEY") or os.getenv("NEWS_API_KEY")

# Initialize Groq LLM
llm = ChatGroq(
    api_key=groq_api_key,
    model="llama-3.3-70b-versatile"  
)

# Initialize NewsAPI
newsapi = NewsApiClient(api_key=news_api_key)

def get_news_articles(query, num_articles=5):
    articles = newsapi.get_everything(
        q=query,
        language="en",
        sort_by="relevancy",
        page_size=num_articles  
    )
    return articles["articles"]


def summarize_articles(articles):
    summaries = [article["description"] for article in articles if article["description"]]
    return " ".join(summaries)

def get_summary(query, num_articles=5):
    articles = get_news_articles(query, num_articles)
    return summarize_articles(articles)


# Prompt template
template = """
You are an AI assistant helping an equity research analyst.
Given the following query and the provided news article summaries, provide an overall summary.

Query: {query}
Summaries: {summaries}
"""
prompt = PromptTemplate(template=template, input_variables=["query", "summaries"])

# LangChain pipeline
llm_chain = LLMChain(prompt=prompt, llm=llm)
# LangChain pipeline
llm_chain = LLMChain(prompt=prompt, llm=llm)

if __name__ == "__main__":
    query = "Apple stock performance"
    summaries = get_summary(query)
    response = llm_chain.run({"query": query, "summaries": summaries})

    print("### AI Research Summary ###")
    print(response)
