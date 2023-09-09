from dotenv import load_dotenv
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

load_dotenv()

from llama_index.llms import ChatMessage, MessageRole
from llama_index.prompts import ChatPromptTemplate

# Text QA Prompt
chat_text_qa_msgs = [
    ChatMessage(
        role=MessageRole.SYSTEM,
        content="As an DIY expert in a big hardware retail chain, you are supposed to answer customers' DIY questiones base on product information.",
    ),
    ChatMessage(
        role=MessageRole.USER,
        content=(
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the context information and not prior knowledge, "
            "answer the question: {query_str}\n"
        ),
    ),
]
text_qa_template = ChatPromptTemplate(chat_text_qa_msgs)

# Refine Prompt
chat_refine_msgs = [
    ChatMessage(
        role=MessageRole.SYSTEM,
        content="Always answer the question, even if the context isn't helpful.",
    ),
    ChatMessage(
        role=MessageRole.USER,
        content=(
            "We have the opportunity to refine the original answer "
            "(only if needed) with some more context below.\n"
            "------------\n"
            "{context_msg}\n"
            "------------\n"
            "Given the new context, refine the original answer to better "
            "answer the question: {query_str}. "
            "If the context isn't useful, output the original answer again.\n"
            "Original Answer: {existing_answer}"
        ),
    ),
]
refine_template = ChatPromptTemplate(chat_refine_msgs)

# def load_index_with_multiStepQueryEngine():
#     from llama_index import StorageContext, load_index_from_storage
#     storage_context = StorageContext.from_defaults(persist_dir="./storage")
#     index = load_index_from_storage(storage_context=storage_context)

#     from llama_index.query_engine.multistep_query_engine import MultiStepQueryEngine
#     from llama_index.indices.query.query_transform.base import StepDecomposeQueryTransform
#     step_decompose_transform = StepDecomposeQueryTransform()

#     index_summary = "As an expert on DIY project and hardware tools, please answer the following customer questions."

#     query_engine = MultiStepQueryEngine(
#         query_engine=index.as_chat_engine(),
#         query_transform=step_decompose_transform,
#         index_summary = index_summary
#     )
#     return query_engine

def load_index():
    from llama_index import StorageContext, load_index_from_storage
    storage_context = StorageContext.from_defaults(persist_dir="./storage")
    index = load_index_from_storage(storage_context=storage_context)
    # query_engine = index.as_query_engine()

    query_engine = index.as_chat_engine(text_qa_template=text_qa_template, refine_template=refine_template)
    return query_engine

def create_index():
    from pathlib import Path
    from llama_index import download_loader
    SimpleCSVReader = download_loader("SimpleCSVReader")
    loader = SimpleCSVReader()
    documents = loader.load_data(file=Path('./data'))

    from llama_index import GPTVectorStoreIndex
    index = GPTVectorStoreIndex.from_documents(documents)
    index.storage_context.persist()

if __name__ == "__main__":
    query_engine = load_index()
    response = query_engine.chat("I would like to clean up my deck, what product should I buy?") 
    print(response.response)
    response = query_engine.chat("which one is the cheapest?") 
    print(response.response)
