from decouple import config
from pinecone import Pinecone
from pinecone.core.client.exceptions import PineconeException


class PineconeClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            try:
                api_key = config("PINECONE_API_KEY")
                environment = config("PINECONE_ENVIRONMENT", default="us-east-1")
                
                if not api_key:
                    raise ValueError("Pinecone API key não encontrada. Verifique seu .env")
                cls._instance = Pinecone(api_key=api_key, environment=environment)

            except PineconeException as e:
                print(f"Erro ao inicializar Pinecone: {e}")
                raise
            except Exception as e:
                print(f"Erro de configuração Pinecone: {e}")
                raise

        return cls._instance

    @staticmethod
    def get_index(index_name: str):
        pinecone = PineconeClient()
        try:
            return pinecone.Index(index_name)
        except PineconeException as e:
            print(f"Erro ao acessar índice '{index_name}': {e}")
            raise
