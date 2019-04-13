import http.client
import urllib.parse
import json
import time
import numpy as np
import re
import requests
import nltk
from flair.data import Sentence
from flair.embeddings import WordEmbeddings, DocumentPoolEmbeddings
from sklearn.metrics.pairwise import cosine_similarity


def is_difference_large(text1: str, text2: str) -> bool:
    text1_preprocessed = Sentence(text1)
    text2_preprocessed = Sentence(text2)

    glove_embedding = WordEmbeddings('glove')
    document_embedding = DocumentPoolEmbeddings([glove_embedding])
    document_embedding.embed(text1_preprocessed)
    document_embedding.embed(text2_preprocessed)

    text1_embedding = text1_preprocessed.get_embedding()
    text2_embedding = text2_preprocessed.get_embedding()
    text1_embedding = np.reshape(text1_embedding, (-1, 1))
    text2_embedding = np.reshape(text2_embedding, (-1, 1))
    similarity = cosine_similarity(text1_embedding, text2_embedding)
    # Some example treshold
    # TODO: Determine a good threshold for example in pitch
    if np.mean(similarity) > 0.06:
        return False
    else:
        return True


def which_paragraph_changed(text: str) -> list:
    list_of_paragraphs = re.findall(r"[^#]+", text)
    has_changes = [_check_if_has_diff(paragraph) for paragraph in list_of_paragraphs]
    return has_changes


def _check_if_has_diff(text: str) -> bool:
    diff_tokens = ["<ins>", "<del>"]
    return any(diff_token in text for diff_token in diff_tokens)


def keyphrase_extraction(text: str) -> list:
    key_phrase_api_url = "https://westeurope.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases"
    documents = {'documents': [
        {'id': '1', 'language': 'en',
         'text': text},
    ]}
    headers = {'Ocp-Apim-Subscription-Key': "d20c819104a04b1083286a8a15e93f16"}
    response = requests.post(key_phrase_api_url, headers=headers, json=documents)
    key_phrases = response.json()
    return key_phrases['documents'][0]['keyPhrases']


def count_changes(difference):
    # Takes difference from wdiffhtml as input
    # Returns total number of changes in words
    dif = difference.splitlines()
    num_changes = 0
    for line in dif:
        if '<ins>' in line:
            word_list = nltk.word_tokenize(
                line[re.search('<ins>', line).end():re.search('</ins>', line).start()])
            num_changes += len(word_list)
        if '<del>' in line:
            word_list = nltk.word_tokenize(
                line[re.search('<del>', line).end():re.search('</del>', line).start()])
            num_changes += len(word_list)
    return num_changes


if __name__ == "__main__":
    with open('text1.txt', 'r') as f:
        text1_ = f.read()
    with open('text3.txt', 'r') as f:
        text2_ = f.read()
    print(is_difference_large(text1_, text2_))

    with open('example.md', 'r') as f:
        example_md = f.read()
    print(which_paragraph_changed(example_md))
    # print(keyphrase_extraction("I really hate Azure because it is a bad documented service."))
#     print(keyphrase_extraction('''The First Picture Of A Black Hole
# Katie Bouman led development of a computer program that made the breakthrough image possible.
# The remarkable photo, showing a halo of dust and gas 500 million trillion km from Earth, was released on Wednesday. For Dr Bouman, its creation was the realization of an endeavor previously thought impossible.'''))
    print(keyphrase_extraction('''Katie Bouman led development of a computer program that made the breakthrough image possible.
The remarkable photo, showing a halo of dust and gas 500 million trillion km from Earth, was released on Wednesday.'''))
    print(keyphrase_extraction('''Kip Thorne  made some cool but wrong visual effects.'''))