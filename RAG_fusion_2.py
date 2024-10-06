import os
from itertools import chain
from operator import itemgetter
import pathlib
from langchain.load import dumps, loads
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Cohere
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents.base import Document
from langchain_cohere import CohereEmbeddings  # Update this line
from langchain_community.vectorstores import Qdrant
from langchain_core.runnables import RunnableLambda
from qdrant_client import models, QdrantClient
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings

# Constants
TOP_K = 5
MAX_DOCS_FOR_CONTEXT = 5
QDRANT_URL = "https://b47815b9-2834-49ae-8cbf-165d4126cfbe.europe-west3-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "FNKyGP8L9j3U3vkWCwhda5nrB3cuPflwfnSWoNwVfMNE7kuTA0s8xg")  # Use your Qdrant API key
QDRANT_COLLECTION_NAME = "ACTRESS_PROFILES"

# Set the Cohere API key as an environment variable
os.environ["COHERE_API_KEY"] = "cqzA1AZDRH3DgEzAWhXw3qYo6x4gqNvUdh8ARyCp"  # Use your Cohere API key
embedding_model = CohereEmbeddings(model="embed-english-v3.0", cohere_api_key=os.getenv("COHERE_API_KEY"))
semantic_chunker_embed_model = FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")

# Initialize Qdrant client
qdrant_client = QdrantClient(QDRANT_URL, prefer_grpc=True, api_key=QDRANT_API_KEY)

def read_txt_files(directory: str) -> list[Document]:
    """Reads all .txt files in a given directory and returns a list of Document objects.

    Args:
        directory (str): The path to the directory containing .txt files.

    Returns:
        list[Document]: A list of Document objects containing the content of the .txt files.
    """
    documents = []
    for txt_file in pathlib.Path(directory).glob('*.txt'):
        with open(txt_file, 'r') as file:
            content = file.read()
            metadata = {"filename": txt_file.stem}
            documents.append(Document(page_content=content, metadata=metadata))
    return documents

def reciprocal_rank_fusion(results: list[list], k=60) -> list[Document]:
    """Rerank docs (Reciprocal Rank Fusion)

    Args:
        results (list[list]): Retrieved documents
        k (int, optional): Parameter k for RRF. Defaults to 60.

    Returns:
        ranked_results: List of documents reranked by RRF
    """
    fused_scores = {}
    for docs in results:
        for rank, doc in enumerate(docs):
            doc_str = dumps(doc)
            if doc_str not in fused_scores:
                fused_scores[doc_str] = 0
            fused_scores[doc_str] += 1 / (rank + k)

    reranked_results = [
        (loads(doc), score)
        for doc, score in sorted(fused_scores.items(), key=lambda x: x[1], reverse=True)
    ]

    return [x[0] for x in reranked_results[:MAX_DOCS_FOR_CONTEXT]]

def query_generator(original_query: dict) -> list[str]:
    """Generate queries from original query

    Args:
        original_query (dict): Original query

    Returns:
        list[str]: List of generated queries
    """
    query = original_query.get("query")

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a helpful assistant that generates multiple search queries based on a single input query.",
            ),
            (
                "user",
                "Generate multiple search queries related to: {original_query}. When creating queries, please refine or add closely related contextual information, without significantly altering the original query's meaning.",
            ),
            ("user", "OUTPUT (3 queries):"),
        ]
    )

    model = Cohere()
    query_generator_chain = (
        prompt | model | StrOutputParser() | (lambda x: x.split("\n"))
    )

    queries = query_generator_chain.invoke({"original_query": query})
    queries.insert(0, "0. " + query)

    return queries

def create_QDrant_collection():
    """Create Qdrant collection."""
    embeddings = CohereEmbeddings(model="embed-english-v3.0", cohere_api_key=os.getenv("COHERE_API_KEY"))
    qdrant_client.recreate_collection(
        collection_name=QDRANT_COLLECTION_NAME,
        vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE),
    )
'''
def upload_chunks_to_QDrant(documents):
    """Upload document chunks to Qdrant."""
    records_to_upload = []
    for idx, chunk in enumerate(documents):
        content = chunk.page_content
        vector = embedding_model.encode(content).tolist()

        record = models.PointStruct(
            id=idx,
            vector=vector,
            payload={"page_content": content}
        )
        records_to_upload.append(record)

    qdrant_client.upload_points(
        collection_name=QDRANT_COLLECTION_NAME,
        points=records_to_upload
    )
    return
'''
def upload_chunks_to_QDrant(documents):
    records_to_upload = []
    for idx, chunk in enumerate(documents):
        content = chunk.page_content
        # Change how you call to get the embedding
        vector = embedding_model.embed_documents([content])[0]  # Check if this is the correct call

        record = models.PointStruct(
            id=idx,
            vector=vector,
            payload={"page_content": content}
        )
        records_to_upload.append(record)

    qdrant_client.upload_points(
        collection_name=QDRANT_COLLECTION_NAME,
        points=records_to_upload
    )
    return

def rrf_retriever(query: str) -> list[Document]:
    """RRF retriever

    Args:
        query (str): Query string
        directory (str): Directory containing the .txt files

    Returns:
        list[Document]: Retrieved documents
    """
    # Read documents from the directory

    # Initialize Qdrant vector store
    qdrant = Qdrant(
        client=qdrant_client,
        collection_name=QDRANT_COLLECTION_NAME,
        embeddings=embedding_model,
    )

    # Set up the retriever with search kwargs
    retriever = qdrant.as_retriever(search_kwargs={"k": TOP_K})

    # RRF chain setup
    chain = (
        {"query": itemgetter("query")}
        | RunnableLambda(query_generator)
        | retriever.map()  # Use the Qdrant retriever
        | reciprocal_rank_fusion
    )

    # Invoke the chain with the query
    result = chain.invoke({"query": query})

    # Print the top K matched documents
    print("Top K Matched Documents:")
    for idx, document in enumerate(result[:TOP_K]):
        print(f"Document {idx + 1}:\nFilename: {document.metadata.get('filename', 'N/A')}, Content: {document.page_content[:100]}...\n")

    return result