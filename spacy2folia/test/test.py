#!/usr/bin/env python

text = """Hello world. This is a test.
Let's see how this works. This sentence
spans two lines.

The capital of The Netherlands is Amsterdam. The government, however, always convenes in The Hague.
"""

import spacy
from spacy2folia import spacy2folia

nlp = spacy.load("en_core_web_sm")
doc = nlp(text)
foliadoc = spacy2folia.convert(doc, "untitled", paragraphs=True)
print(foliadoc.xmlstring())


