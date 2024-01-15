import requests
from bs4 import BeautifulSoup
import os
import pathlib
from urllib.parse import urljoin
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
import openai
import tiktoken
import chromadb


def get_links(url):
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a')

    links = [link.get('href') for link in links if link.get('href') is not None and not link.get('href').startswith('#') and '/' in link.get('href') and 'github' not in link.get('href')]
    raw_links = links.copy()

    cleaned_links = []
    for link in links:
        link = link.split('/')[-1]
        if link.endswith('.html'):
            link = link[:-5]
        if link.endswith('_Cheat_Sheet'):
            link = link[:-12]
        cleaned_links.append(link)

    return cleaned_links, raw_links

def fetch_and_store_content(raw_links, cleaned_links, base_url):
    # If the directory doesn't exist, create it
    os.makedirs("CheatSheets", exist_ok=True)
    condition = 0

    for raw, cleaned in zip(raw_links, cleaned_links):
        # Construct a safe filename by replacing spaces with underscores and appending .txt
        filename = pathlib.Path("CheatSheets", cleaned.replace(' ', '_') + ".txt")

        # If the file already exists, skip it
        if filename.exists():
            continue

        # Get the full URL by using urljoin
        full_url = urljoin(base_url, raw)
        condition = 1

        try:
            # Fetch the content of the link
            response = requests.get(full_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the specific tag that contains the content
            content_tag = soup.find('div', {'class': 'wiki-content'})

            # If the tag is not found, use the entire soup
            if content_tag is None:
                content_tag = soup

            # Write the text content to a file
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content_tag.get_text())
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch {full_url}: {e}")
    return condition

url = 'https://cheatsheetseries.owasp.org/Glossary.html'
cleaned_links, raw_links = get_links(url)

condition = fetch_and_store_content(raw_links, cleaned_links, base_url='https://cheatsheetseries.owasp.org')


# ... other parts of your code


os.environ['OPENAI_API_KEY'] = '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'

persist_directory = 'db'
loader = DirectoryLoader('./CheatSheets', glob= "./*txt", loader_cls=TextLoader)

if condition == 1:
    # create the directory if it doesn't exist
    os.makedirs(persist_directory)
    print("API COST GOES UP")

vectordb_file = os.path.join(persist_directory, "vectordb_file")

if condition == 1:
    # create the database if the file doesn't exist
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
    texts = text_splitter.split_documents(documents)

    embedding = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(documents=texts, embedding=embedding, persist_directory=persist_directory)
    vectordb.persist()
    vectordb = None
    print("API COST GOES UP SLIGHTLY")
    #print(texts[5])

# 9:56 is probably the correct time stamp to fix this issue

condition2 = 0

while condition2 == 0:

    condition3 = 0

    while condition3 == 0:
        print("Do you want to ask a question y/n: ", end='')
        UserInput = input()

        if(UserInput == 'y'):
            condition3 = 1

        if(UserInput == 'n'):
            exit()

    print()

    ## HERE WE GO AGAIN WITH THIS SCHTUFF

    persist_directory = 'db'
    embedding = OpenAIEmbeddings()

    vectordb2 = Chroma(persist_directory = persist_directory, embedding_function = embedding)

    retriever = vectordb2.as_retriever(search_kwargs = {'k': 4})

    # TURBO LLM GOES HERE
    turbo_llm = ChatOpenAI(
        temperature = 0, model_name = 'gpt-3.5-turbo'
    )

    # Make the chain to answer somem questions
    qa_chain = RetrievalQA.from_chain_type(llm = turbo_llm, chain_type = "stuff", retriever = retriever, return_source_documents = True)

    def process_llm_response(llm_response):
        print(llm_response['result'])
        print('\n\nSources:')
        for source in llm_response['source_documents']:
            print(source.metadata['source'])

    # Full Example

    print("Please input your question: ", end="")
    query = "If you don't know the answer, just say that you don't know, don't try to make up an answer.\n----------------\n{" + input() + "}"
    print()
    print("Prompt loading ....")
    #print(query + '\n\n\n')
    llm_response = qa_chain(query) #This actually does register
                        #Even though it's out of order due to recursion
    process_llm_response(llm_response)
    
    print()
    print()

    # Ok all of the retriever code goes here

    # $1.15
