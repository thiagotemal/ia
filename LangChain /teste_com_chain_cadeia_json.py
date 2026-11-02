
from dotenv import load_dotenv
from langchain_core.globals import set_debug
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field

# Carrega as variáveis do arquivo .env para o sistema
load_dotenv()
set_debug(True)


class CidadeSugerida(BaseModel):
    cidade: str = Field(..., description="Cidade sugerida para o interesse fornecido")
    descricao: str = Field(..., description="Descrição da cidade sugerida")

parser = JsonOutputParser(pydantic_object=CidadeSugerida)

promptTemplate = PromptTemplate(input_variables=['interesses']
    ,template=
    """
Sugira uma cidade dado o meu interesse em 
{interesses}
{formato_saida}
    """,
    partial_variables={"formato_saida" : parser.get_format_instructions()}
)


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.6,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

cadeia = promptTemplate | llm | parser

# 3. Fazendo uma pergunta para o modelo (Invocando)
resposta = cadeia.invoke({'interesses':'praia'})

# 4. Exibindo o resultado
print(resposta)