import numpy as np
import re
import os
import itertools
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD, LatentDirichletAllocation
from malaya.text.jarowinkler import JaroWinkler
from sklearn.metrics.pairwise import cosine_similarity
from malaya.text.function import (
    summary_textcleaning,
    split_into_sentences,
    simple_textcleaning,
    STOPWORDS,
)
from malaya.graph.pagerank import pagerank
from malaya.stem import sastrawi
from malaya.model import skip_thought
from malaya.cluster import cluster_words
from malaya.text.vectorizer import SkipGramVectorizer
from herpetologist import check_type
from typing import List, Tuple


class DEEP_SKIPTHOUGHT:
    def __init__(
        self, sess, x, logits, attention, dictionary, maxlen, model = None
    ):
        self._sess = sess
        self._X = x
        self._logits = logits
        self._attention = attention
        self.dictionary = dictionary
        self._maxlen = maxlen
        self._rev_dictionary = {v: k for k, v in self.dictionary.items()}
        self._model = model

    def vectorize(self, strings):

        """
        Vectorize string inputs using bert attention.

        Parameters
        ----------
        strings : str / list of str

        Returns
        -------
        array: vectorized strings
        """

        if isinstance(strings, list):
            if not isinstance(strings[0], str):
                raise ValueError('input must be a list of strings or a string')
        else:
            if not isinstance(strings, str):
                raise ValueError('input must be a list of strings or a string')
        if isinstance(strings, str):
            strings = [strings]

        splitted_fullstop = [summary_textcleaning(i) for i in strings]
        original_strings = [i[0] for i in splitted_fullstop]
        cleaned_strings = [i[1] for i in splitted_fullstop]
        sequences = skip_thought.batch_sequence(
            cleaned_strings, self.dictionary, maxlen = self._maxlen
        )
        return self._sess.run(
            self._logits, feed_dict = {self._X: np.array(sequences)}
        )


class DEEP_SUMMARIZER:
    def __init__(self, vectorizer):
        self._vectorizer = vectorizer

    @check_type
    def summarize(
        self, corpus, top_k: int = 3, important_words: int = 3, **kwargs
    ):
        """
        Summarize list of strings / corpus

        Parameters
        ----------
        corpus: str, list

        top_k: int, (default=3)
            number of summarized strings.
        important_words: int, (default=3)
            number of important words.

        Returns
        -------
        string: summarized string
        """
        if not isinstance(corpus, list) and not isinstance(corpus, str):
            raise ValueError('corpus must be a list')
        if isinstance(corpus, list):
            if not isinstance(corpus[0], str):
                raise ValueError('corpus must be list of strings')

        if isinstance(corpus, str):
            corpus = split_into_sentences(corpus)
        else:
            corpus = '. '.join(corpus)
            corpus = split_into_sentences(corpus)

        splitted_fullstop = [summary_textcleaning(i) for i in corpus]
        original_strings = [i[0] for i in splitted_fullstop]
        cleaned_strings = [i[1] for i in splitted_fullstop]

        if 'DEEP_SKIPTHOUGHT' in str(self._vectorizer):

            sequences = skip_thought.batch_sequence(
                cleaned_strings,
                self._vectorizer.dictionary,
                maxlen = self._vectorizer._maxlen,
            )
            vectors, attention = self._vectorizer._sess.run(
                [self._vectorizer._logits, self._vectorizer._attention],
                feed_dict = {self._vectorizer._X: np.array(sequences)},
            )
            attention = attention.sum(axis = 0)
            indices = np.argsort(attention)[::-1]
            top_words = [
                self._vectorizer._rev_dictionary[i]
                for i in indices
                if self._vectorizer._rev_dictionary[i] not in STOPWORDS
            ][:important_words]

        else:
            vectors = self._vectorizer.vectorize(corpus)
            attentions = self._vectorizer.attention(corpus, **kwargs)
            flatten = list(itertools.chain(*attentions))
            r = {}
            for f in flatten:
                c = simple_textcleaning(f[0])
                if c in STOPWORDS:
                    continue
                if c not in r:
                    r[c] = f[1]
                else:
                    r[c] += f[1]
            top_words = sorted(r, key = r.get, reverse = True)[:important_words]

        similar = cosine_similarity(vectors, vectors)
        similar[similar >= 0.99999] = 0
        scores = pagerank(similar)
        ranked_sentences = sorted(
            ((scores[i], s) for i, s in enumerate(original_strings)),
            reverse = True,
        )
        summary = [r[1] for r in ranked_sentences[:top_k]]

        return {
            'summary': ' '.join(summary),
            'top-words': top_words,
            'cluster-top-words': cluster_words(top_words),
        }


_skipthought_availability = {
    'lstm': {
        'Description': 'LSTM skip-thought deep learning model trained on news dataset.'
    },
    'residual-network': {
        'Description': 'residual network with Bahdanau Attention skip-thought deep learning model trained on wikipedia dataset.'
    },
}

_vectorizer_availability = {
    'tfidf': {'Description': 'TFIDF Vectorizer'},
    'bow': {'Description': 'Bag-Of-Word Vectorizer'},
    'skip-gram': {'Description': 'Bag-Of-Word with Gram-Skipping Vectorizer'},
}


def available_skipthought():
    """
    List available deep skip-thought models.
    """
    from malaya.function import describe_availability

    return describe_availability(_skipthought_availability)


def available_vectorizer():
    """
    List available vectorizer for malaya.summarization.extractive.lda and malaya.summarization.extractive.lsa .
    """
    from malaya.function import describe_availability

    return describe_availability(_vectorizer_availability)


@check_type
def deep_skipthought(model: str = 'lstm'):
    """
    Load deep learning skipthought model.

    Parameters
    ----------
    model : str, optional (default='skip-thought')
        Model architecture supported. Allowed values:

        * ``'lstm'`` - LSTM skip-thought deep learning model trained on news dataset.
        * ``'residual-network'`` - residual network with Bahdanau Attention skip-thought deep learning model trained on wikipedia dataset.

    Returns
    -------
    DEEP_SKIPTHOUGHT: malaya.summarize.DEEP_SKIPTHOUGHT class
    """
    model = model.lower()
    mapping = {
        'lstm': skip_thought.news_load_model,
        'residual-network': skip_thought.wiki_load_model,
    }
    model = mapping.get(model)
    if not model:
        raise ValueError(
            'model is not supported, please check supported models from malaya.summarization.extractive.available_skipthought()'
        )
    sess, x, logits, attention, dictionary, maxlen = model()
    return DEEP_SKIPTHOUGHT(sess, x, logits, attention, dictionary, maxlen)


@check_type
def _base_summarizer(
    corpus,
    decomposition,
    top_k: int = 3,
    max_df: float = 0.95,
    min_df: int = 2,
    ngram: Tuple[int, int] = (1, 3),
    vectorizer: str = 'bow',
    important_words: int = 10,
    retry: int = 5,
    **kwargs,
):

    vectorizer = vectorizer.lower()
    if not vectorizer in ['tfidf', 'bow', 'skip-gram']:
        raise ValueError("vectorizer must be in  ['tfidf', 'bow', 'skip-gram']")

    if min_df < 1:
        raise ValueError('min_df must be bigger than 0')
    if not (max_df <= 1 and max_df > 0):
        raise ValueError(
            'max_df must be bigger than 0, less than or equal to 1'
        )
    if not isinstance(corpus, list) and not isinstance(corpus, str):
        raise ValueError('corpus must be a list')
    if isinstance(corpus, list):
        if not isinstance(corpus[0], str):
            raise ValueError('corpus must be list of strings')
    if isinstance(corpus, str):
        corpus = split_into_sentences(corpus)
    else:
        corpus = '. '.join(corpus)
        corpus = split_into_sentences(corpus)

    splitted_fullstop = [summary_textcleaning(i) for i in corpus]
    original_strings = [i[0] for i in splitted_fullstop]
    cleaned_strings = [i[1] for i in splitted_fullstop]
    stemmed = [sastrawi(i) for i in cleaned_strings]

    mapping = {
        'tfidf': TfidfVectorizer,
        'bow': CountVectorizer,
        'skip-gram': SkipGramVectorizer,
    }
    Vectorizer = mapping.get(vectorizer)
    if not Vectorizer:
        raise ValueError(
            'vectorizer is not supported, please check supported vectorizers from malaya.summarization.extractive.available_vectorizer()'
        )

    tf_vectorizer = Vectorizer(
        max_df = max_df,
        min_df = min_df,
        ngram_range = ngram,
        stop_words = STOPWORDS,
        **kwargs,
    )
    tf = tf_vectorizer.fit_transform(stemmed)
    if hasattr(tf_vectorizer, 'idf_'):
        indices = np.argsort(tf_vectorizer.idf_)[::-1]
    else:
        indices = np.argsort(np.asarray(tf.sum(axis = 0))[0])[::-1]

    features = tf_vectorizer.get_feature_names()
    top_words = [features[i] for i in indices[:important_words]]
    vectors = decomposition(tf.shape[1] // 2).fit_transform(tf)
    similar = cosine_similarity(vectors, vectors)
    similar[similar >= 0.999] = 0
    scores = pagerank(similar, retry)
    ranked_sentences = sorted(
        ((scores[i], s) for i, s in enumerate(original_strings)), reverse = True
    )
    summary = [r[1] for r in ranked_sentences[:top_k]]
    return {
        'summary': ' '.join(summary),
        'top-words': top_words,
        'cluster-top-words': cluster_words(top_words),
    }


def lda(
    corpus,
    top_k = 3,
    important_words = 10,
    max_df = 0.95,
    min_df = 2,
    ngram = (1, 3),
    vectorizer = 'bow',
    **kwargs,
):
    """
    summarize a list of strings using LDA, scoring using TextRank.

    Parameters
    ----------
    corpus: list
    top_k: int, (default=3)
        number of summarized strings.
    important_words: int, (default=10)
        number of important words.
    max_df: float, (default=0.95)
        maximum of a word selected based on document frequency.
    min_df: int, (default=2)
        minimum of a word selected on based on document frequency.
    ngram: tuple, (default=(1,3))
        n-grams size to train a corpus.
    vectorizer: str, (default='bow')
        vectorizer technique. Allowed values:

        * ``'bow'`` - Bag of Word.
        * ``'tfidf'`` - Term frequency inverse Document Frequency.
        * ``'skip-gram'`` - Bag of Word with skipping certain n-grams.

    Returns
    -------
    dict: result
    """
    return _base_summarizer(
        corpus,
        LatentDirichletAllocation,
        top_k = top_k,
        max_df = max_df,
        min_df = min_df,
        ngram = ngram,
        vectorizer = vectorizer,
        important_words = important_words,
        **kwargs,
    )


def lsa(
    corpus,
    top_k = 3,
    important_words = 10,
    max_df = 0.95,
    min_df = 2,
    ngram = (1, 3),
    vectorizer = 'bow',
    **kwargs,
):
    """
    summarize a list of strings using LSA, scoring using TextRank.

    Parameters
    ----------
    corpus: list
    top_k: int, (default=3)
        number of summarized strings.
    important_words: int, (default=10)
        number of important words.
    max_df: float, (default=0.95)
        maximum of a word selected based on document frequency.
    min_df: int, (default=2)
        minimum of a word selected on based on document frequency.
    ngram: tuple, (default=(1,3))
        n-grams size to train a corpus.
    vectorizer: str, (default='bow')
        vectorizer technique. Allowed values:

        * ``'bow'`` - Bag of Word.
        * ``'tfidf'`` - Term frequency inverse Document Frequency.
        * ``'skip-gram'`` - Bag of Word with skipping certain n-grams.

    Returns
    -------
    dict: result
    """
    return _base_summarizer(
        corpus,
        TruncatedSVD,
        top_k = top_k,
        max_df = max_df,
        min_df = min_df,
        ngram = ngram,
        vectorizer = vectorizer,
        important_words = important_words,
        **kwargs,
    )


@check_type
def doc2vec(
    vectorizer,
    corpus,
    top_k: int = 3,
    aggregation: int = 'mean',
    soft: bool = True,
):
    """
    summarize a list of strings using doc2vec, scoring using TextRank.

    Parameters
    ----------
    vectorizer : object
        fast-text or word2vec interface object.
    corpus: list
    top_k: int, (default=3)
        number of summarized strings.
    aggregation : str, optional (default='mean')
        Aggregation supported. Allowed values:

        * ``'mean'`` - mean.
        * ``'min'`` - min.
        * ``'max'`` - max.
        * ``'sum'`` - sum.
        * ``'sqrt'`` - square root.
    soft: bool, optional (default=True)
        word not inside vectorizer will replace with nearest word if True, else, will skip.

    Returns
    -------
    dictionary: result
    """
    if not hasattr(vectorizer, 'get_vector_by_name'):
        raise ValueError('vectorizer must has `get_vector_by_name` method')
    if not isinstance(corpus, list) and not isinstance(corpus, str):
        raise ValueError('corpus must be a list')
    if isinstance(corpus, list):
        if not isinstance(corpus[0], str):
            raise ValueError('corpus must be list of strings')
    if isinstance(corpus, str):
        corpus = split_into_sentences(corpus)
    else:
        corpus = '. '.join(corpus)
        corpus = split_into_sentences(corpus)
    splitted_fullstop = [summary_textcleaning(i) for i in corpus]
    original_strings = [i[0] for i in splitted_fullstop]
    cleaned_strings = [i[1] for i in splitted_fullstop]

    aggregation = aggregation.lower()
    if aggregation == 'mean':
        aggregation_function = np.mean
    elif aggregation == 'min':
        aggregation_function = np.min
    elif aggregation == 'max':
        aggregation_function = np.max
    elif aggregation == 'sum':
        aggregation_function = np.sum
    elif aggregation == 'sqrt':
        aggregation_function = np.sqrt
    else:
        raise ValueError(
            'aggregation only supports `mean`, `min`, `max`, `sum` and `sqrt`'
        )

    vectors = []
    for string in cleaned_strings:
        inside = []
        for token in string.split():
            try:
                inside.append(vectorizer.get_vector_by_name(token))
            except:
                if not soft:
                    pass
                else:
                    arr = np.array(
                        [
                            self._jarowinkler.similarity(token, k)
                            for k in vectorizer.words
                        ]
                    )
                    idx = (-arr).argsort()[0]
                    inside.append(
                        vectorizer.get_vector_by_name(vectorizer.words[idx])
                    )
        vectors.append(aggregation_function(inside, axis = 0))
    similar = cosine_similarity(vectors, vectors)
    similar[similar >= 0.999] = 0
    scores = pagerank(similar)
    ranked_sentences = sorted(
        ((scores[i], s) for i, s in enumerate(original_strings)), reverse = True
    )
    summary = [r[1] for r in ranked_sentences[:top_k]]
    return ' '.join(summary)


def encoder(vectorizer):
    """
    Encoder interface for summarization.

    Parameters
    ----------
    vectorizer : object
        encoder interface object, eg, BERT, skip-thought, XLNET, ALBERT, ALXLNET.

    Returns
    -------
    result: malaya.summarization.extractive.DEEP_SUMMARIZER
    """

    if not hasattr(vectorizer, 'vectorize'):
        raise ValueError('vectorizer must has `vectorize` method')
    return DEEP_SUMMARIZER(vectorizer)
