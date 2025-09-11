from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda

load_dotenv()

def build_chain(transcript: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 200,
        chunk_overlap = 100
    )

    docs = splitter.create_documents([transcript])

    vector_store = FAISS.from_documents(
        documents=docs,
        embedding=OpenAIEmbeddings()
    )

    retriever = vector_store.as_retriever(
        search_type = "similarity",
        search_kwargs = {"k":4}
    )

    model = ChatOpenAI(model_name="gpt-4", temperature=0.2)

    prompt = PromptTemplate(
        template="""
        You are a reliable and intelligent assistant. 
        Your task is to answer the user’s question using the provided transcript as your primary source of truth.

        Guidelines:
        1. Use only the facts that are explicitly present in the transcript whenever possible.
        2. If the transcript does not directly mention the answer, clearly state this by saying:
        "The transcript does not directly mention this, but based on my understanding and the transcript provided, here is my answer:"
        — then give your best possible answer.
        3. Never invent details that contradict the transcript.
        4. Keep answers clear, concise, and directly relevant to the question.
        5. If the transcript suggests multiple interpretations, present them fairly.

        Transcript Context:
        -------------------
        {context}

        User Question:
        --------------
        {question}

        Your Answer:
        """,
        input_variables=["context", "question"]
    )

    def format_docs(retrieved_data):
        return "\n\n".join(doc.page_content for doc in retrieved_data)

    parallel_chain = RunnableParallel(
        {
            "question" : RunnablePassthrough(),
            "context" : retriever | RunnableLambda(format_docs)
        }
    )

    parser = StrOutputParser()
    final_chain = parallel_chain | prompt | model | parser

    return final_chain
