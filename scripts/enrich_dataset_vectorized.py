"""
Enrich doctor-patient dialogue dataset with UMLS concepts - vectorized approach for faster results
"""

import spacy
import pandas as pd

# model for medical entity recognition
nlp = spacy.load('en_core_sci_md')

# load UMLS data
aui_nodes_df = pd.read_csv('umls-graph/aui_nodes.csv')
# filter aui_nodes_df to include only 'SNOMEDCT_US' entries
aui_nodes_df = aui_nodes_df[aui_nodes_df['SAB'] == 'SNOMEDCT_US']
#case-insensitive string matching
aui_nodes_df['STR'] = aui_nodes_df['STR'].str.lower()

# dictionary mapping medical terms to UMLS CUIs
cui_dict = aui_nodes_df.groupby('STR')['CUI'].apply(list).to_dict()

# load dialogue dataset
dialogue_df = pd.read_csv('data/MTS-Dialog-TrainingSet.csv')

# extract medical terms from dialogue text using spacy
def extract_medical_terms(text, nlp_model):
    doc = nlp_model(text)
    return [ent.text for ent in doc.ents]

# map extracted medical terms to UMLS CUIs
def map_terms_to_cuis_vectorized(terms):
    return [(term, cui_dict.get(term.lower(), [])) for term in terms]

# apply extraction to 'section_text' column
dialogue_df['extracted_terms'] = dialogue_df['section_text'].apply(
    lambda text: extract_medical_terms(text, nlp)
    )

# apply vectorized mapping to extracted terms
dialogue_df['umls_cui_mappings'] = dialogue_df['extracted_terms'].apply(
    map_terms_to_cuis_vectorized
    )

# save enriched dataset
dialogue_df.to_csv('data/MTS-Dialog-TrainingSet-enriched-vectorized.csv', index=False)