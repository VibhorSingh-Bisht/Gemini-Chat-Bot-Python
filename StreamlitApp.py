import streamlit as st
from data_ingestion import load_data
from embeddings import download_gemini_embedding
from main import load_model

    
def main():
    # file_path = f'{os.getcwd()}\\data\\amazon_data.csv'
    # if not os.path.isfile(file_path):
    #     amazon_scrape_final.main()
    st.set_page_config("Recommendation System")
    
    doc=st.file_uploader("upload your document")
    
    st.header("Recommendation System using LLM-RAG")
    
    user_question= st.text_input("Ask your question")
    
    if st.button("submit & process"):
        with st.spinner("Processing..."):
            document=load_data(doc)
            model=load_model()
            query_engine=download_gemini_embedding(model,document)
                
            response = query_engine.query(user_question)
                
            st.write(response.response)
                
                
if __name__=="__main__":
    main()          
                