from pathlib import Path
Path("Procfile").write_text("web: uvicorn src.api.main:app --host 0.0.0.0 --port $PORT", encoding="utf-8")
print("Procfile created:")
print(Path("Procfile").read_text())