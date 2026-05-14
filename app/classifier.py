from app.bert_trainer import VillaMessageClassifier

# Load once at module level — not on every call

from pathlib import Path

# change "villa_bert_model" to whatever you decided to name your model's folder

MODEL_DIR = Path(__file__).parent / "villa_bert_model"
_classifier = VillaMessageClassifier(model_dir=str(MODEL_DIR))

# DeBERTa-based intent classification layer
# returns operational query category
def classify_query(message: str) -> str:
    result = _classifier.predict(message)
    return result["category"]