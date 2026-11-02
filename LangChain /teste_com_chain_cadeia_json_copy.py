
from dotenv import load_dotenv
from langchain_core.globals import set_debug
from langchain_core.output_parsers import (
    JsonOutputParser,
    StrOutputParser,
)
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

class Restaurantes(BaseModel):
    cidade:str = Field("A cidade recomendada para visitar")
    restaurantes:str = Field("Restaurantes recomendados na cidade")


promptTemplate = PromptTemplate(input_variables=['interesses']
    ,template=
    """
Sugira uma cidade dado o meu interesse em 
{interesses}
{formato_saida}
    """,
    partial_variables={"formato_saida" : parser.get_format_instructions()}
)
resdtaurenteparse = JsonOutputParser(pydantic_object=Restaurantes)


promptTemplateRestaurante = PromptTemplate(input_variables=['cidade']
    ,template=
    """Sugira um restaurante na cidade de {cidade}
{formato_saida}""",
    partial_variables={"formato_saida" : resdtaurenteparse.get_format_instructions()}
)

promptRotasRecomendadas = PromptTemplate(input_variables=['cidade','restaurantes']
    ,template=
    """Sugira rotas recomendadas para visitar a cidade de {cidade} e o restaurante {restaurantes}
"""
)

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.6,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

cadeia = promptTemplate | llm | parser
cadeiaRestaurante = promptTemplateRestaurante | llm | resdtaurenteparse
cadeiaRotasRecomendadas = promptRotasRecomendadas | llm | StrOutputParser()

cadeias = cadeia | cadeiaRestaurante | cadeiaRotasRecomendadas



# 3. Fazendo uma pergunta para o modelo (Invocando)
resposta = cadeias.invoke({'interesses':'praia'})

# 4. Exibindo o resultado
print(resposta)