import os
import json
from typing import List, Dict
from decouple import config
from langchain_openai import OpenAIEmbeddings

from app.services.base_service import BaseService
from app.services.pinecone_client import PineconeClient
from app.services.llm.langchain_service import LangChainService


class VehicleSearchService(BaseService):
    def __init__(self, data: str):
        super().__init__(data)
        self.query = data
        self.filters = {}
        self.results = []
        self.vector_query = None
        self.top_k = config("TOP_K", 10, cast=int)
        self.index = PineconeClient.get_index(config("PINECONE_INDEX_NAME", "car-index"))
        self.embeddings = OpenAIEmbeddings(api_key=config("OPENAI_API_KEY"))
        self.llm_service = LangChainService(template_name="buscar_carros")

    def receive_data(self, data: str):
        self.query = data

    def validate_or_prepare(self, force_llm: bool = False):
        """Obtém filtros estruturados via LangChain (somente se necessário)"""

        if not force_llm:
            # Se a resposta final já está no cache, a gente nem deveria estar aqui
            # print("validate_or_prepare chamado sem necessidade. Ignorando.")
            return

        llm_response = self.llm_service.invoke(self.query)
        self.was_cached = self.llm_service.was_cached

        try:
            self.filters = json.loads(llm_response)
        except json.JSONDecodeError:
            self.filters = {}
            # print("Erro ao decodificar JSON retornado pelo LLM em validate_or_prepare")

        text_description = self._build_query_text(self.filters)
        self.vector_query = self.embeddings.embed_query(text_description)

    def execute(self) -> Dict:
        """Executa a busca completa, com cache inteligente de resposta final"""

        response_cached = self.llm_service.lookup_final_response(self.query)
        if response_cached:
            self.was_cached = True
            # print("Resposta completa recuperada do cache final.")
            return {
                "cached": True,
                "mensagem": response_cached
            }

        llm_response = self.llm_service.invoke(self.query, use_cache=True)
        self.was_cached = self.llm_service.was_cached

        try:
            self.filters = json.loads(llm_response)
        except json.JSONDecodeError:
            self.filters = {}
            # print("Erro ao decodificar JSON retornado pelo LLM")

        text_description = self._build_query_text(self.filters)
        self.vector_query = self.embeddings.embed_query(text_description)

        response = self.index.query(
            vector=self.vector_query,
            top_k=self.top_k,
            include_metadata=True
        )
        self.results = [hit["metadata"] for hit in response.get("matches", [])]

        if not self.results:
            return {
                "cached": self.was_cached,
                "mensagem": "Nenhum veículo encontrado com esses critérios."
            }

        mensagem = self.llm_service.responder_resultado(self.query, self.results)
        self.llm_service.update_final_response(self.query, mensagem)

        return {
            "cached": self.was_cached,
            "mensagem": mensagem
        }

    def return_result(self, result: List[Dict]) -> Dict:
        if not result:
            return {
                "cached": self.was_cached,
                "mensagem": "Nenhum veículo encontrado com esses critérios."
            }

        mensagem = self.llm_service.responder_resultado(self.query, result)

        return {
            "cached": self.was_cached,
            "mensagem": mensagem
        }


    def _build_query_text(self, filters: dict) -> str:
        parts = []
        if marca := filters.get("marca"):
            parts.append(marca)
        if modelo := filters.get("modelo"):
            parts.append(modelo)
        if transmissao := filters.get("transmissao"):
            parts.append(transmissao)
        if preco := filters.get("preco_max"):
            parts.append(f"até R${preco}")
        if km := filters.get("quilometragem_max"):
            parts.append(f"menos de {km} km")
        return " ".join(parts) or self.query
