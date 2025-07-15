from decouple import config


def get_ambient_url() -> str:
    ambient = config("AMBIENT", default="local")

    urls = {
        "local": "http://localhost:8000"
    }

    return urls.get(ambient, "http://localhost:8000")
