import yaml


class PromptTemplateLoader:
    def __init__(self, path: str = "templates/llm.yaml"):
        self.path = path

    def load(self, template_name: str) -> str:
        with open(self.path, "r") as file:
            templates = yaml.safe_load(file)
        return templates.get(template_name, "")
