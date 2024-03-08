# How To Efficiently Download Any Dataset from Kaggle
# https://ravi-chan.medium.com/how-to-download-any-data-set-from-kaggle-7e2adc152d7f

import os
import pandas as pd
import opendatasets as od

DATASET_URL = 'https://www.kaggle.com/datasets/datahackers/state-of-data-2022/data'


def main():
    if not os.path.exists('state-of-data-2022'):
        download_dataset_from_kaggle(DATASET_URL)
    else:
        pass
    
    df = pd.read_csv('state-of-data-2022/State_of_data_2022.csv')

    print(df.shape)

def download_dataset_from_kaggle(url):
    od.download(url)

if __name__ == '__main__':
    main()
