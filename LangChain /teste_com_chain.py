
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

# Carrega as variáveis do arquivo .env para o sistema
load_dotenv()
promptTemplate = PromptTemplate(input_variables=['dias','numero_criancas','atividade']
    ,template=
    """
Crie um roteiro de viagem de {dias} dias,
para uma familia com {numero_criancas} criancas,
que gostam de {atividade}
    """
)

prompt = promptTemplate.invoke( input={
    "dias" : 10,
    "numero_criancas" : 1,
    "atividade" :"pescar"
}    )


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.6,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

# 3. Fazendo uma pergunta para o modelo (Invocando)
resposta = llm.invoke(prompt)

# 4. Exibindo o resultado
print(resposta.content)