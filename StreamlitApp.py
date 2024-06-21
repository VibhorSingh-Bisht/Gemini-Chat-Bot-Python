import os
import streamlit as st
import traceback
from data_ingestion import load_data
from embeddings import download_gemini_embedding
from main import load_model

def main():
    st.set_page_config(page_title="Recommendation System")

    st.header("Recommendation System")

    # Set the path to your document
    file_path = os.path.join(os.getcwd(), 'data', 'amazon_data.csv')

    # Check if the file exists
    if not os.path.isfile(file_path):
        st.error(f"The file {file_path} does not exist.")
        return

    user_question = st.text_input("Ask your question")

    if st.button("Submit & Process"):
        with st.spinner("Processing..."):
            try:
                # Load the document data
                document = load_data(file_path)

                # Load the language model
                model = load_model()

                # Download Gemini embeddings and create query engine
                query_engine = download_gemini_embedding(model, document)

                # Perform the query
                response = query_engine.query(user_question)

                # Display the response
                st.write(response.response)
            except Exception as e:
                st.error("An error occurred during processing.")
                st.error(str(e))
                st.error(traceback.format_exc())

if __name__ == "__main__":
    main()
