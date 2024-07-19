import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import time
import os
import PyPDF2

def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as pdf:
        reader = PyPDF2.PdfFileReader(pdf, strict=False)
        pdf_text = []

        for page in reader.pages:
            content = page.extract_text()
            pdf_text.append(content)

        return pdf_text

stop_words = set(stopwords.words('portuguese'))

df1 = pd.DataFrame({'Date Created': [], 'Name': [], 'Text': []})

pdfs_list = [file for file in os.listdir('./') if file.endswith('.pdf')]

for pdf in pdfs_list:
    created_time = time.ctime(os.path.getctime(pdf))
    created_time_obj = time.strptime(created_time)
    time_stamp = time.strftime('%Y-%m-%d %H:%M:%S', created_time_obj)

    tokenized_text = word_tokenize(' '.join(extract_text_from_pdf(pdf)), language='portuguese')
    extracted_text = ' '.join([str.lower(word) for word in tokenized_text if word not in stop_words])

    df1.loc[len(df1)] = {'Date Created': created_time, 'Name': pdf, 'Text': extracted_text}

print(df1)
df1.to_excel("telegramas.xlsx")