"""Miscellaneous helper functions."""

import os
import pickle
import pickletools
import gzip

from collections import Counter

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    classification_report,
)


def print_evaluation(y_true, y_pred):
    """Prints some classification reports."""
    print(f"accuracy = {accuracy_score(y_true, y_pred)}")
    print(f"precision = {precision_score(y_true, y_pred)}")
    print(f"recall = {recall_score(y_true, y_pred)}")
    print()
    print(classification_report(y_true, y_pred))


def word_counts(headlines, preproc, tokenize, n=None):
    """Makes a DataFrame with the most common words.
    Arguments:
    headlines - Headlines to look.
    n - Number of most common words to extract (None for all of the words).

    Returns:
    A DataFrame with the columns "word" and "count".
    """
    counter = Counter(word for hl in headlines for word in tokenize(preproc(hl)) )
    return pd.DataFrame(counter.most_common(n), columns=("word", "count"))


def plot_freq(headlines, preproc, tokenize, n=40, title="Word Frequency"):
    """Plots the frequency of the n words."""

    counts = word_counts(headlines, preproc, tokenize, n)

    plt.figure(figsize=(20, 8))
    plt.title(title)
    plt.xticks(rotation=-45)
    plt.bar(counts["word"], counts["count"])


def ensure_dir(filename):
    """Create the directory of filename if it does not already exist."""
    dir = os.path.dirname(filename)
    if not os.path.exists(dir):
        os.makedirs(dir)


def pickle_gzip(obj, filename):
    p = pickletools.optimize(pickle.dumps(obj))
    ensure_dir(filename)
    with gzip.open(filename, 'wb') as f:
        f.write(p)


def unpickle_gzip(filename):
    with gzip.open(filename) as f:
        return pickle.load(f)
