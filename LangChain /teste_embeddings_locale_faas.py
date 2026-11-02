from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

# O modelo será baixado automaticamente na primeira execução e rodará localmente
embeddings = HuggingFaceEmbeddings(
    model_name="tardellirs/embeddinggemma-pt-br",
        model_kwargs={"device": "cpu"},  # Muda para "cuda" se tiver placa de vídeo Nvidia
    encode_kwargs={"normalize_embeddings": True},
)

documento = TextLoader("documentos/GTB_gold_Nov23.txt",
                       encoding="utf-8"
                       ).load() 

pedacos = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=100
).split_documents(documento)


print(f"Quantidade de pedaços: {len(pedacos)}") 


dados_recuperados = FAISS.from_documents(
    pedacos, embeddings
).as_retriever(search_kwargs={"k":2})

prompt_consulta_seguro = ChatPromptTemplate.from_messages([
    ("system", "Responda usando exclusivamente o conteúdo fornecido"),
    ("human", "{query}\n\nContexto: \n{contexto}\n\nResposta:")
])





def responder(pergunta:str):
    trechos = dados_recuperados.invoke(pergunta)
    contexto = "\n\n".join(um_trecho.page_content for um_trecho in trechos)
    return contexto

print(responder("Como devo proceder caso tenha um item roubado?"))