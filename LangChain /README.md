# Estudos de LangChain e IA generativa

## Objetivo

Este projeto reúne scripts independentes para estudar integrações de modelos de linguagem com LangChain e Groq. Os exemplos cobrem prompts, composição de chains, saída estruturada, histórico e roteamento com LangGraph, além de RAG (busca em documentos seguida de geração de resposta) com embeddings locais e FAISS.

O repositório é didático: cada script demonstra um fluxo específico e pode ser executado separadamente. Não é uma aplicação única nem um serviço de produção.

A Groq foi escolhida como provedora dos modelos por oferecer uma opção de uso gratuito adequada para testes e aprendizado. A disponibilidade, as cotas e os limites gratuitos podem variar conforme as condições atuais do serviço.

## Requisitos

- Linux ou outro ambiente compatível com as dependências Python do projeto.
- Python compatível com as versões listadas em `requirements.txt`.
- Chave de API da Groq para os exemplos que chamam um modelo remoto.
- Acesso à internet na primeira execução do RAG, para baixar o modelo de embeddings Hugging Face.

## Configuração

Na raiz do projeto, crie ou atualize o arquivo `.env`:

```env
GROQ_API_KEY=sua_chave_da_groq
```

Não compartilhe nem versione esse arquivo. A maioria dos scripts carrega as variáveis com `python-dotenv`.

Crie e ative o ambiente virtual e instale as dependências:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Se `.venv` já existir, basta ativá-lo e instalar as dependências. Execute os comandos a partir da raiz do projeto, pois os caminhos para arquivos em `documentos/` são relativos ao diretório atual.

## Executar exemplos

Execute um script por vez, com o ambiente virtual ativado. Por exemplo:

```bash
python teste_com_chain.py
python teste_com_chain_cadeia.py
python teste_com_chain_rag.py
python teste_com_chain_rag_pdf.py
```

## Scripts

- `teste_com_chain.py`: cria um prompt parametrizado e chama o modelo Groq diretamente.
- `teste_com_chain_cadeia.py`: compõe prompt, modelo e parser de texto com LCEL (`|`).
- `teste_com_chain_simples.py`: chama a API Groq usando o SDK oficial, sem a abstração de chat do LangChain.
- `teste_com_chain_cadeia_json.py` e `teste_com_chain_cadeia_json_copy.py`: experimentos de saída estruturada em JSON com Pydantic e parsers do LangChain.
- `teste_com_chain_cadeia_chat.py`: experimenta estado de mensagens e memória em processo com LangGraph.
- `teste_com_chain_cadeia_chat_copy.py`: experimenta roteamento assíncrono para fluxos especializados em praia ou montanha com LangGraph.
- `teste_com_chain_rag.py`: carrega o documento TXT `documentos/GTB_gold_Nov23.txt`, divide o conteúdo em trechos, indexa-o com FAISS e responde perguntas usando recuperação e Groq.
- `teste_com_chain_rag_pdf.py`: aplica um fluxo semelhante ao PDF `documentos/estrategia_app_casas_veraneio.pdf`.
- `teste_embeddings_locale_faas.py`: demonstra embeddings locais e recuperação de trechos do documento TXT com FAISS.

## Observações

- Os exemplos de RAG usam `tardellirs/embeddinggemma-pt-br` localmente e configuram `device="cpu"`. O download inicial pode demorar e requer conexão com a internet.
- O índice FAISS é criado em memória durante a execução dos scripts; os exemplos não persistem o índice em disco.
- A memória baseada em `MemorySaver` também existe apenas durante a execução do processo.
- `teste_com_chain_simples.py` atualmente lê `GROK_API_KEY` (com `K` antes do `Q`). Para usar o `.env` descrito acima, altere essa referência no script para `GROQ_API_KEY`.
- `requirements.txt` registra as versões das dependências instaladas no ambiente do projeto.
