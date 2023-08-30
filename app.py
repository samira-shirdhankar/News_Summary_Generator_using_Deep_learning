import streamlit as st
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
#!pip install -U spacy
#!python -m spacy download en_core_web_sm

st.set_page_config(
    page_title="News Article Summarization App",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.title(':blue[_News Article Summary Generator_]') ##this is heading 

## get user input
form = st.form(key='my-form')
text = form.text_input(label='Enter an News Article')
submit_button = form.form_submit_button(label='Generate Summary')
#text = form.text_area('Enter an article whose summary is to be generated',height=300)

if submit_button:
    stopwords = list(STOP_WORDS)

    nlp = spacy.load('en_core_web_sm')

    doc = nlp(text)

    tokens = [token.text for token in doc]

    punctuation = punctuation + '\n'


    ##Frequency Table

    word_frequencies = {}
    for word in doc:
        if word.text.lower() not in stopwords:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies:
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1



    max_frequency = max(word_frequencies.values())


    ##Frequency normalization
    ##dividing every value with the max_frequency i.e 11

    for word in word_frequencies.keys():
        word_frequencies[word] = word_frequencies[word]/max_frequency


    ##Sentence Tokenization
    #o/p --> list of sentences

    sentence_tokens = [sent for sent in doc.sents]


    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent] += word_frequencies[word.text.lower()]



    ##selecting only 30% of sentences.

    select_length = int(len(sentence_tokens)*0.3)
    #select_length

    summary = nlargest(select_length, sentence_scores, key = sentence_scores.get)

    #summary

    final_summary = [word.text for word in summary]
    summary = ''.join(final_summary)


    st.text_area('Text summary is: ',summary,height=300)
else:
    pass



