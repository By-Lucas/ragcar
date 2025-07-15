import os
import uuid
import pandas as pd
from typing import List, Dict, Any
from decouple import config
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone, ServerlessSpec


class ExcelPineconeIngestor:
    def __init__(
        self,
        excel_path: str,
        openai_api_key: str | None = None,
        pinecone_api_key: str | None = None,
        pinecone_index_name: str = "car-index",
    ):
        self.excel_path = excel_path
        self.openai_api_key = openai_api_key or config("OPENAI_API_KEY")
        self.pinecone_api_key = pinecone_api_key or config("PINECONE_API_KEY")
        self.pinecone_index_name = pinecone_index_name

        self.embeddings = OpenAIEmbeddings(api_key=self.openai_api_key)
        self.pinecone = Pinecone(api_key=self.pinecone_api_key)
        self.index = self.pinecone.Index(self.pinecone_index_name)

    def run(self) -> None:
        data = self._load_excel()
        vectors = self._prepare_vectors(data)
        self._upload_to_pinecone(vectors)

    def _load_excel(self) -> pd.DataFrame:
        if not os.path.exists(self.excel_path):
            raise FileNotFoundError(f"Arquivo {self.excel_path} não encontrado.")
        df = pd.read_excel(self.excel_path)
        print(f"Excel carregado com {len(df)} linhas.")
        return df

    def _prepare_vectors(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        records = []
        for _, row in df.iterrows():
            metadata = row.to_dict()
            text = self._row_to_text(metadata)
            vector = self.embeddings.embed_query(text)
            records.append({
                "id": str(uuid.uuid4()),
                "values": vector,
                "metadata": metadata
            })
        print(f"Vetores preparados: {len(records)}")
        return records

    def _row_to_text(self, row: dict) -> str:
        return (
            f"{row.get('marca', '')} {row.get('modelo', '')} {row.get('ano', '')}, "
            f"motor {row.get('motorizacao', '')}, {row.get('combustivel', '')}, "
            f"transmissão {row.get('transmissao', '')}, {row.get('portas', '')} portas, "
            f"{row.get('cor', '')}, {row.get('quilometragem', '')} km, "
            f"R${row.get('preco', '')}"
        )

    def _upload_to_pinecone(self, vectors: List[Dict[str, Any]]) -> None:
        if not vectors:
            print("Nenhum vetor para subir.")
            return
        self.index.upsert(vectors)
        print(f"{len(vectors)} vetores enviados ao Pinecone com sucesso.")
