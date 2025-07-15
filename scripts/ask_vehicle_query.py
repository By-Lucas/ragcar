import os
import sys
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.vehicle_search import VehicleSearchService


async def main():
    print("Digite sua pergunta (ex: Quero ver carros azuis):")
    user_query = input("> ")

    service = VehicleSearchService(user_query)
    service.receive_data(user_query)

    service.validate_or_prepare()
    result = service.execute()
    resposta = service.return_result(result)

    print("\nResposta da IA:")
    print(resposta["mensagem"])
    print("\nCache usado:", resposta["cached"])


if __name__ == "__main__":
    asyncio.run(main())
