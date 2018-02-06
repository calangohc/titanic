# -*- coding: utf-8 -*-

import os
from six.moves import urllib

# Initializes paths according to links below:
# https://www.kaggle.com/c/titanic/download/train.csv
# https://www.kaggle.com/c/titanic/download/test.csv
# https://www.kaggle.com/c/titanic/download/gender_submission.csv

TITANIC_ROOT = "https://www.kaggle.com/c/titanic/download/"
TRAIN = 'train.csv'
TEST = 'test.csv'
GENDER_SUB = 'gender_submission.csv'


def fetch_raw_data(root_url, filename, path='data/raw/'):
    """
    Fetches raw daw from server and save to disk.

    :param root_url: URL from which the File will be download
    :param filename: File Name (Both in Server and Local)
    :param path: Local path to save file, cookie cutter standard is 'data/raw' for this case
    """

    # Check if path dir exists and if not creates new dir
    if not os.path.isdir(path):
        os.makedirs(path)

    # Create URL and file_path
    url = root_url + filename
    file_path = path + filename

    # Download file from 'url' and save to disk on 'file_path'
    urllib.request.urlretrieve(url, file_path)


def fetch_data_kaggle_titanic(path='data/raw/'):
    """
    Downloads all relevant raw data from Titanic dataset from Kaggle.

    """
    fetch_raw_data(TITANIC_ROOT, TRAIN, path)
    fetch_raw_data(TITANIC_ROOT, TEST, path)
    fetch_raw_data(TITANIC_ROOT, GENDER_SUB, path)


if __name__ == '__main__':
    # TODO find a better way to find the absolute path for 'data/raw'
    # Get absolute path for 'data/raw/'
    absolute_path = os.getcwd()
    parent_path = os.path.split(absolute_path)[0]
    greatparent_path = os.path.split(parent_path)[0]
    final_path = os.path.join(greatparent_path, 'data/raw/')

    # Fetch Titanic Data
    fetch_data_kaggle_titanic(final_path)
