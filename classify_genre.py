import logging
import os
from utils import *
import pandas as pd

def classify(dataset_list, classifer_list, featureignore_list=None):
    extract_data(dataset_list)
    extract_csv(dataset_list)

if __name__ == "__main__":
    parser = ArgumentParser(description="""

    """)
    parser.add_argument('-d', '--dataset', nargs='+', help='Specify the dataset you want to use', required=True)
    parser.add_argument('-i', '--ignore', nargs='+', help='Specify features to ignore', required=False)
    parser.add_argument('-c', '--classifier', nargs='+', help='Classifiers to be used', required=True)
    args = parser.parse_args()
    logging.basicConfig(filename='./logs/results.log', level=logging.DEBUG)
    classify(args.dataset, args.classifier, args.ignore)

