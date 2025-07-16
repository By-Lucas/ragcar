# RAGCar — Agente Virtual com FastAPI, LangChain e Pinecone

Este projeto é um sistema inteligente com IA generativa (RAG) capaz de responder perguntas sobre veículos. Ele utiliza vetorização via **Pinecone**, raciocínio com **LangChain**, cache com **PostgreSQL** e interface via **FastAPI**.

![alt text](image.png)
---

## Tecnologias utilizadas

- OpenAI + LangChain
- Pinecone (busca vetorial)
- PostgreSQL + SQLAlchemy + Alembic
- FastAPI + Pydantic
- Upload de Excel com ingestão vetorial
- Cache em PostgreSQL
- Estrutura modular

---


## Como executar o projeto localmente

> Requisitos: Python 3.11+, PostgreSQL rodando em `http://127.0.0.1:8000/docs` com banco `test_db` criado

---

### 1. Clone o repositório
```bash
git clone git@github.com:By-Lucas/ragcar.git
cd ragcar
```

  -  Este projeto já vem com o arquivo `.env.zip` pronto para uso (com as credenciais e variáveis configuradas). Basta você descompactar ele e na raiz do projeto
  -  Ou se preferir crie um `.env`, as informacoes baixo, e depois cole as credencias de conexão com a OPENAI e PINECONE para que tenha sucesso na execução.
  ```bash
      # Ambiente de execução
      AMBIENT="local"

      # Número de resultados retornados nas buscas vetoriais
      TOP_K=20

      # Chave da OpenAI (substitua pela sua!)
      OPENAI_API_KEY=

      # Configurações do Pinecone
      PINECONE_API_KEY=
      PINECONE_ENVIRONMENT=us-east-1
      PINECONE_INDEX_NAME=car-index

      # Conexão com banco de dados (PostgreSQL)
      DATABASE_URL=postgresql+asyncpg://postgres:123@localhost:5432/test_db
  ```
    
### 2 Crie e ative o ambiente virtual
```bash
python -m venv venv
source venv/bin/activate

# Windows
# venv\Scripts\activate.bat
```

### 3 Instale as dependências
```bash
pip install -r requirements.txt
```

### 4 Execute as migrações com Alembic
```bash
alembic upgrade head
```

### 5 Inicie a aplicação FastAPI
```bash
uvicorn app.api.main:app --reload
```

### 6 Acesse a API via navegador
```bash
http://localhost:8000/docs
```


## Uso e engestor de dados local por terminal
- 1 Gere um Excel com os dados dos veículos
```bash
python scripts/generate_excel.py
```

- 2 Envie os dados para o Pinecone com o ingestor
```bash
PYTHONPATH=. python scripts/send_ingest_pinecone.py
# ou apenas
python scripts/send_ingest_pinecone.py
```

- 3 Envie uma perguinda do usuário e retorne
```bash
PYTHONPATH=. python scripts/ask_vehicle_query.py
# ou apenas
python scripts/ask_vehicle_query.py
```
