import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import time
import re
import os
import PyPDF2

df = pd.DataFrame()
doc_splitter_pattern = re.compile(r'Página 1/\d+')
doc_type_pattern = re.compile(r'[De|Da|Do]+ ([A-Za-z]+)(?: para ([A-Za-z]+))? em (\d{2}/\d{2}/\d{4})')
doc_num_pattern = re.compile(r'Nr[.] (\d{5})')

stop_words = set(stopwords.words('portuguese'))

pdf_reader = PyPDF2.PdfFileReader(input('Enter the path of the file:\n'))

for page_num in range(pdf_reader.numPages):
    text = pdf_reader.getPage(page_num).extract_text()

    if doc_splitter_pattern.match(text): # início da mensagem
        pass

def extract_entry(text):
    # Determinar se mensagem for TEL, DET, ou CIT
    pass


