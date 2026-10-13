import os
import tempfile
from langchain_core.documents import Document
from langchain_classic.document_loaders import WebBaseLoader


def load_text_file():
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as temp_file:
        temp_file.write(
            b"Hello, this is a sample text file.\nThis file is used to demonstrate the TextLoader."
        )
        temp_file_path = temp_file.name

    try:
        with open(temp_file_path, "r", encoding="utf-8") as f:
            file_content = f.read()

        documents = [
            Document(
              page_content=file_content, 
              metadata={"source": temp_file_path}
            )
        ]

        print(f"Loaded {len(documents)} document(s)")
        print(f"Content preview: {documents[0].page_content[:100]}...")
        print(f"Metadata: {documents[0].metadata}")

        #Print the loaded documents
        for doc in documents:
            print("Document Content:")
            print(doc)
            print(doc.page_content)
    finally:
        # Clean up the temporary file
        os.remove(temp_file_path)


def webBasedLoader():
    loader = WebBaseLoader("https://example.com")
    docs = loader.load()
    print(docs[0].page_content)
    print(docs[0].metadata)

webBasedLoader()