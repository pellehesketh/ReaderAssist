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


def just_reader():
    text = data_func.convert_pdf_to_string("pdfs/Bregor Freyason and Pan(demonium) Backstories.pdf")
    print(text)
    return text


if __name__ == '__main__':
    text = just_reader()
    text_read(text)


