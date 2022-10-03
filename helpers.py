# Import libraries needed for keyword extraction
import spacy
from string import punctuation

# Load library needed for keyword extraction
nlp = spacy.load("en_core_web_lg")

def keywords(text):
    """Extracts keywords from a text"""

    result = []
    # Only check for adjectives, nouns, and verbs
    pos_tag = ['ADJ', 'NOUN', 'VERB']

    # Lowercase the document to make it case-insensitive
    loweredText = nlp(text.lower())

    # For each word in the lowered text (lemmatized):
    for token in loweredText:
        
        # Ignore punctuation, etc.
        if(token.lemma_ in nlp.Defaults.stop_words or token.lemma_ in punctuation):
            continue
        
        # Lemmatize each token and add to result
        if(token.pos_ in pos_tag):
            result.append(token.lemma_)
    return result