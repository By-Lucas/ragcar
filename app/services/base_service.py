from abc import ABC, abstractmethod
from typing import Any


class BaseService(ABC):
    """
    Contrato padrão para serviços reutilizáveis e estruturados.
    Segue o ciclo:
    1. receber dados
    2. validar/preparar dados
    3. executar lógica
    4. retornar resultado
    """

    def __init__(self, data: Any = None):
        self.data = data

    def run(self, *args, **kwargs) -> Any:
        """
        Método principal que orquestra a execução do serviço.
        """
        self.receive_data(self.data)
        self.validate_or_prepare()
        result = self.execute()
        return self.return_result(result)

    @abstractmethod
    def receive_data(self, data: Any) -> None:
        """Recebe e armazena os dados de entrada."""
        pass

    @abstractmethod
    def validate_or_prepare(self) -> None:
        """Trata, valida ou transforma os dados para uso interno."""
        pass

    @abstractmethod
    def execute(self) -> Any:
        """Executa a lógica principal do serviço."""
        pass

    @abstractmethod
    def return_result(self, result: Any) -> Any:
        """Formata ou retorna o resultado final para o chamador."""
        pass
