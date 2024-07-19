import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import time
import os
import PyPDF2

def split_pdf_by_keyword(pdf_path, keyword):
    pdf_reader = PyPDF2.PdfFileReader(pdf_path)

    # Iterate through each page in the PDF
    for page_num in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_num)
        text = page.extract_text()

        # Check if the keyword exists in the text of the current page
        if keyword in text:
            pdf_writer = PyPDF2.PdfFileWriter()
            pdf_writer.addPage(page)

            # Add pages from current position till the next occurrence of the keyword
            for page_num_inner in range(page_num+1, pdf_reader.numPages):
                page_inner = pdf_reader.getPage(page_num_inner)
                
                # Check for the next occurrence of the keyword
                if keyword in page_inner.extract_text():
                    break
                else:
                    pdf_writer.addPage(page_inner)

            # Output PDF file name based on page number
            output_filename = f"telegramas_{page_num + 1}.pdf"

            # Write the extracted pages to a new PDF
            with open(f'./split_pdfs/{output_filename}', "wb") as output_pdf:
                pdf_writer.write(output_pdf)
            print(f"PDF split at page {page_num + 1}. Saved as '{output_filename}'.")

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

split_pdf_by_keyword('./input/telegramas_1-5_jan.pdf', 'Página 1')
pdfs_list = [file for file in os.listdir('./split_pdfs/') if file.endswith('.pdf')]

for pdf in pdfs_list:
    path = f'./split_pdfs/{pdf}'
    wnl = WordNetLemmatizer()

    created_time = time.ctime(os.path.getctime(path))
    created_time_obj = time.strptime(created_time)
    time_stamp = time.strftime('%Y-%m-%d %H:%M:%S', created_time_obj)

    tokenized_text = word_tokenize(' '.join(extract_text_from_pdf(path)), language='portuguese')
    extracted_text = ' '.join([wnl.lemmatize(str.lower(word)) for word in tokenized_text if word not in stop_words])

    df1.loc[len(df1)] = {'Date Created': created_time, 'Name': pdf, 'Text': extracted_text}

print(df1)
df1.to_excel("telegramas.xlsx")