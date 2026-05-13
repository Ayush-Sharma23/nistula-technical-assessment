from app.bert_trainer import VillaMessageClassifier

# Load once at module level — not on every call
# After
from pathlib import Path

MODEL_DIR = Path(__file__).parent / "villa_bert_model"
_classifier = VillaMessageClassifier(model_dir=str(MODEL_DIR))

def classify_query(message: str) -> str:
    result = _classifier.predict(message)
    return result["category"]