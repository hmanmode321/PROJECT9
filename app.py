import streamlit as st
from datetime import datetime
from langchain_config import llm_chain, get_summary

st.title('📰 Equity Research News Tool')
st.write('Enter your query to get the latest news articles summarized.')

category = st.selectbox("Choose a category (optional)", ["", "Technology", "Business", "Health", "Science", "Sports", "Entertainment"])
query = st.text_input('Query')
if category:
    query = f"{category} {query}"

num_articles = st.slider("Select number of articles", 1, 20, 5)

if st.button('Get News'):
    if query:
        with st.spinner('Fetching news and generating summary...'):
            summaries = get_summary(query, num_articles)
            response = llm_chain.run({'query': query, 'summaries': summaries})
        
        st.subheader('🧠 Summary:')
        st.write(response)

        # Timestamp
        timestamp = datetime.now().strftime("%B %d, %Y %I:%M %p")
        st.caption(f"🕒 Summary generated on {timestamp}")

        # Download button
        download_text = f"Query: {query}\n\nSummary:\n{response}\n\nGenerated on: {timestamp}"
        st.download_button(
            label="📄 Download Summary as TXT",
            data=download_text,
            file_name=f"{query.replace(' ', '_')}_summary.txt",
            mime="text/plain"
        )
    else:
        st.warning('⚠️ Please enter a query.')





