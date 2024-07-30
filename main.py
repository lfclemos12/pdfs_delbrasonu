import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import time
import string
import re
import os
import PyPDF2

def extract_entry(text: str):
    # Buscar por padrões
    doc_type_match = re.search(doc_type_pattern, text)
    doc_num_match = re.search(doc_num_pattern, text)

    # Validação de formato documento, ref. linha 76
    if not (doc_type_match and doc_num_match):
        return None

    # Extrair dados
    msg_type = None
    sender, receiver, date = doc_type_match.group(1, 2, 3)
    year = date[-4:]
    msg_number = doc_num_match.group(1)

    # Determinar se mensagem for TEL, DET, ou CIT
    if sender == 'SERE' and not receiver:
        msg_type = 'CIT'
    elif sender == 'SERE' and receiver:
        msg_type = 'DET'
    else:
        msg_type = 'TEL'

    doc_name = f'{msg_type}_{year}_{msg_number}'

    # Extrair corpo da mensagem
    body_text = None

    if msg_type == 'CIT' or msg_type == 'DET':
        body_text = text[text.index('//'): text.index('EXTERIORES')]
    else:
        body_text = text[text.index('//'): text.index('Sérgio')]

    return doc_name, msg_type, sender, receiver, date, body_text


def text_pipeline(s: str):
    s = str.lower(s) # Converter em letras minúsculas
    s = str.translate(s, str.maketrans('','', string.punctuation)) # Remover puntuação
    s = str.join(' ', [word for word in str.split(s) if word not in stop_words_pt]) # Remover stopwords
    return s

data = []
doc_splitter_pattern = re.compile(r'Página 1/\d+')
doc_type_pattern = re.compile(r'[De|Da|Do]+ ([A-Za-z]+)(?: para ([A-Za-z]+))? em (\d{2}/\d{2}/\d{4})')
doc_num_pattern = re.compile(r'Nr[.] (\d{5})')

stop_words_pt = set(stopwords.words('portuguese'))

palavra_chave = input('Por favor, escolha a palavra chave:\n')

for file in [path for path in os.listdir('./input/') if path.endswith('.pdf')]:
    pdf_reader = PyPDF2.PdfFileReader(f'./input/{file}')

    for page_num in range(pdf_reader.numPages):
        text = pdf_reader.getPage(page_num).extract_text()

        if doc_splitter_pattern.match(text): # início da mensagem
            for page_num_inner in range(page_num+1, pdf_reader.numPages):
                inner_text = pdf_reader.getPage(page_num_inner).extract_text()

                if not doc_splitter_pattern.match(inner_text):
                    text += inner_text
                else:
                    break
            
            # Validação de formato documento
            extracted_entry = extract_entry(text)

            if not extracted_entry:
                continue # se não for uma página valida, pula para próxima
            else:
                (documt, tipo, remit, dest, dat, texto) = extract_entry(text)
            
            data.append(
                {'documento':documt, 
                'tipo':tipo, 
                'remitente':remit, 
                'destinatário':dest, 
                'data':dat, 
                'texto':texto})

df = pd.DataFrame(data)

text_series = df['texto'].copy(deep=True)

nos_palavra_chave = [] 

for entry in text_series:
    nos_palavra_chave.append(entry.count(palavra_chave))

df[f'no_palavra_chave_{palavra_chave}'] = pd.Series(nos_palavra_chave)

df.to_excel('telegramas.xlsx')