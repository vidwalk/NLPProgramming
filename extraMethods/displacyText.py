import spacy
from spacy import displacy

nlp = spacy.load("en_core_web_sm")
text = """Due to thz`e highly volatile and competitive nature of the industries in which the Company competes, the Company must continually introduce new products, services and technologies, enhance existing products and services, and effectively stimulate customer demand for new and upgraded products."""
doc = nlp(text)
sentence_spans = list(doc.sents)
displacy.serve(sentence_spans, style="dep")
