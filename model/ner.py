#Entity Recognition
import spacy

nlp = spacy.load("en_core_web_sm")

def extract_entities(text: str):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents]
