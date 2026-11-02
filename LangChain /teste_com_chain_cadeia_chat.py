
from dotenv import load_dotenv
from langchain_core.globals import set_debug
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import (
  ChatPromptTemplate,
  MessagesPlaceholder,
)
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import MessagesState, StateGraph

# Carrega as variáveis do arquivo .env para o sistema
load_dotenv()
set_debug(False)


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.6,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# 1. Defina o grafo com o estado de mensagens padrão
builder = StateGraph(MessagesState)

lista_perguntas = [
    "Sugira algum investimento de renda fixa para o mês de junho",
    "porque das escolhas?",
]



chat_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "HAja como consultor de investimentos. Se apresente como Jarvas",
        ),
        MessagesPlaceholder(variable_name="history"),
    ]
)

memoria = {}
sessao = "sessao1"
cadeia = chat_prompt | llm | StrOutputParser()

def call_model(state: MessagesState):
  response = cadeia.invoke({"history": state["messages"]})

  # Retornamos a resposta dentro de um dicionário na chave "messages"
  # O LangGraph vai anexar automaticamente essa resposta ao histórico existente
  return {"messages": response}



    

builder.add_node("model", call_model)
builder.set_entry_point("model")
builder.set_finish_point("model")

# 4. Compile o grafo com o checkpointer (memória ativa)
checkpointer = MemorySaver()
app = builder.compile(checkpointer=checkpointer)

# 5. Testando a memória da conversa usando o 'thread_id'
config = {"configurable": {"thread_id": "usuario-999"}}




print("--- Turno 1 ---")
output1 = app.invoke({"messages": [("user", lista_perguntas[0])]}, config)
print(output1["messages"][-1].content)  # Resposta do modelo

print("--- Turno 2 ---")
output1 = app.invoke({"messages": [("user", lista_perguntas[1])]}, config)
print(output1["messages"][-1].content)  # Resposta do modelo


