import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.services.ingest_excel import ExcelPineconeIngestor

ingestor = ExcelPineconeIngestor(excel_path="base_veiculos.xlsx")
ingestor.run()
