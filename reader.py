import os
import PyPDF2
from gtts import gTTS

import data_func
import csv

def text_read(text):
    """text = ("Bregor realized there was only one thing to do. He left in search of answers to how to bring back that balance."
           " Too free the forces of nature. His mentor told him they were just stories. But Bregor knew better.")"""
    language = "en"
    speech = gTTS(text=text, lang=language, slow=False)
    speech.save("audio/text.mp3")
    os.system("start audio/text.mp3")

def read_stuff():
    reader = PyPDF2.PdfFileReader(
        'Complete_Works_Lovecraft.pdf')

    print(reader.documentInfo)

    num_of_pages = reader.numPages
    print('Number of pages: ' + str(num_of_pages))

    writer = PyPDF2.PdfFileWriter()

    for page in range(2, 4):
        writer.addPage(reader.getPage(page))

    output_filename = 'table_of_contents.pdf'

    with open(output_filename, 'wb') as output:
        writer.write(output)

    text = data_func.convert_pdf_to_string(
        'table_of_contents.pdf')

    text = text.replace('.', '')
    text = text.replace('\x0c', '')
    table_of_contents_raw = text.split('\n')

    title_list = []
    pagenum_list = []
    title_formatted_list = []
    for item in table_of_contents_raw:
        title, pagenum = \
            data_func.split_to_title_and_pagenum(item)
        if title != None:
            title_list.append(title)
            pagenum_list.append(pagenum)
            title_formatted_list.append(
                data_func.convert_title_to_filename(title))

    # for page_list, we need to add the last page as well
    pagenum_list.append(num_of_pages + 1)

    for i in range(1, len(title_formatted_list)):
        title_formatted = title_formatted_list[i]
        page_start = pagenum_list[i] - 1
        page_end = pagenum_list[i + 1] - 2

        writer = PyPDF2.PdfFileWriter()

        for page in range(page_start, page_end + 1):
            writer.addPage(reader.getPage(page))

        output_filename = './pdfs/' + title_formatted + '.pdf'

        with open(output_filename, 'wb') as output:
            writer.write(output)

    year_written = []
    # first element is Preface, where year is not applicable
    year_written.append('n/a')

    for title_formatted in title_formatted_list[1:]:

        text = data_func.convert_pdf_to_string(
            './pdfs/' + title_formatted + '.pdf')

        # exclude the year after the title, collect in a list
        i = 0
        while text[i] != '(':
            i += 1
        year = text[i + 1:i + 5]
        text = text[:i] + text[i + 6:]
        year_written.append(year)

        # replace 'Return to Table of Contents', which is not part of the text
        text = text.replace('Return to Table of Contents', '')

        # replace Fin from the end of the last title
        if title_formatted == 'the_haunter_of_the_dark':
            text = text[:-15]

        # save in a txt file
        text_file = open('./txts/' + title_formatted + '.txt', 'w')
        n = text_file.write(text)
        text_file.close()

        with open('table_of_contents.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerows(zip(
                title_list, pagenum_list, title_formatted_list, year_written))

def just_reader():
    text = data_func.convert_pdf_to_string("pdfs/Bregor Freyason and Pan(demonium) Backstories.pdf")
    print(text)
    return text


if __name__ == '__main__':
    text = just_reader()
    text_read(text)


