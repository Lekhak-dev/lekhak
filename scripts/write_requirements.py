from pathlib import Path

reqs = """fastapi==0.115.5
uvicorn==0.32.0
pydantic==2.10.3
transformers==4.46.3
torch==2.5.1
sentencepiece==0.2.0
requests==2.32.3
python-multipart==0.0.12
"""

Path("requirements.txt").write_text(reqs, encoding="utf-8")
print("requirements.txt written:")
print(reqs)