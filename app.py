import streamlit as st
from langchain_config import llm_chain, get_summary

st.title('📰 Equity Research News Tool')
st.write('Enter your query to get the latest news articles summarized.')

query = st.text_input('Query')

if st.button('Get News'):
    if query:
        with st.spinner('Fetching news and generating summary...'):
            summaries = get_summary(query)
            response = llm_chain.run({'query': query, 'summaries': summaries})
        st.subheader('🧠 Summary:')
        st.write(response)
    else:
        st.warning('⚠️ Please enter a query.')



