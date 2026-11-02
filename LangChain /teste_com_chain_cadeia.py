
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

# Carrega as variáveis do arquivo .env para o sistema
load_dotenv()
promptTemplate = PromptTemplate(input_variables=['interesses']
    ,template=
    """
Sugira uma cidade dado o meu interesse em 
{interesses}
    """
)




llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.6,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

cadeia = promptTemplate | llm | StrOutputParser()

# 3. Fazendo uma pergunta para o modelo (Invocando)
resposta = cadeia.invoke({'interesses':'praia'})

# 4. Exibindo o resultado
print(resposta)