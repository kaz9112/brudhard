import sys
from langchain_text_splitters import RecursiveCharacterTextSplitter

# loader = PyPDFLoader("pdf_test.pdf")
# raw_docs = loader.load()

def split_text(full_text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=700, separators=["\n", " ", ""])
    chunks = splitter.split_text(full_text)
    return chunks