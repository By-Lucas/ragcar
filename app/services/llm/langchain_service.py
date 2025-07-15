import json
import psycopg2
from decouple import config
from typing import Dict, List

from langchain_openai import OpenAI
from langchain.globals import set_llm_cache

from app.services.llm.postgres_cache import PostgresCache
from app.services.llm.prompt_template import PromptTemplateLoader


class LangChainService:
    def __init__(self, template_name="buscar_carros"):
        self.model = OpenAI(
            model_name=config("OPENAI_MODEL", default="gpt-3.5-turbo-instruct"),
            temperature=0.2,
            openai_api_key=config("OPENAI_API_KEY")
        )
        self.prompt_loader = PromptTemplateLoader()
        self.template_name = template_name
        self.was_cached = False

        self.conn = psycopg2.connect(
            dbname=config("POSTGRES_DB", default="postgres"),
            user=config("POSTGRES_USER", default="postgres"),
            password=config("POSTGRES_PASSWORD", default="123"),
            host=config("POSTGRES_HOST", default="localhost"),
            port=config("POSTGRES_PORT", default=5432, cast=int),
        )

        self.cache = PostgresCache(self.conn)
        set_llm_cache(self.cache)

    def invoke(self, user_query: str, use_cache: bool = True) -> str:
        template = self.prompt_loader.load(self.template_name)
        prompt = template.format(query=user_query)

        self.was_cached = False

        if use_cache:
            cached = self.cache.lookup(prompt, llm_string="")
            if cached:
                self.was_cached = True
                return cached[0]["text"]

        response = self.model.invoke(prompt)
        text = getattr(response, "text", str(response))
        self.cache.update(prompt, llm_string="", return_val=[response])
        return text

    
    def responder_resultado(self, query: str, carros: List[Dict]) -> str:
        template = self.prompt_loader.load("responder_carros")
        prompt = template.format(query=query, carros=json.dumps(carros, ensure_ascii=False))
        response = self.model.invoke(prompt)
        return getattr(response, "text", str(response))

    def lookup_final_response(self, query: str) -> str | None:
        key = f"resposta_final::{query}"
        cached = self.cache.lookup(key, llm_string="responder_carros")
        if cached:
            return cached[0]["text"]
        return None

    def update_final_response(self, query: str, texto: str):
        key = f"resposta_final::{query}"
        self.cache.update(
            prompt=key,
            llm_string="responder_carros",
            return_val=[{"text": texto}]
        )

