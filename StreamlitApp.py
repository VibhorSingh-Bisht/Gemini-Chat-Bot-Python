import os
import streamlit as st
from data_ingestion import load_data
from embeddings import download_gemini_embedding
from main import load_model

def main():
    st.set_page_config(page_title="Recommendation System")

    st.header("Recommendation System using LLM-RAG")

    # Set the path to your document
    file_path = os.path.join(os.getcwd(), 'data', 'amazon_data.csv')

    # Check if the file exists
    if not os.path.isfile(file_path):
        st.error(f"The file {file_path} does not exist.")
        return

    user_question = st.text_input("Ask your question")

    if st.button("Submit & Process"):
        with st.spinner("Processing..."):
            document = load_data(file_path)
            model = load_model()
            query_engine = download_gemini_embedding(model, document)
                
            response = query_engine.query(user_question)
                
            st.write(response.response)
                
if __name__ == "__main__":
    main()
