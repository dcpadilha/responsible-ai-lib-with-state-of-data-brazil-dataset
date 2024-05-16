# How To Efficiently Download Any Dataset from Kaggle
# https://ravi-chan.medium.com/how-to-download-any-data-set-from-kaggle-7e2adc152d7f

import os
import json

import numpy as np
import pandas as pd
import opendatasets as od

from utils.attributes import TARGET_COLUMN, SENSITIVE_ATTRIBUTES, NOT_FEATURES


DATASET_URL = 'https://www.kaggle.com/datasets/datahackers/state-of-data-2022/data'


def main():
    if not os.path.exists('state-of-data-2022'):
        download_dataset_from_kaggle(DATASET_URL)
    else:
        pass
    
    df = pd.read_csv('state-of-data-2022/State_of_data_2022.csv')

    column_mapping = get_column_mapping(df.columns)
    df = df.rename(columns=column_mapping)

    df = treat_sensitive_attributes(df)
    print(f'Full dataset shape: {df.shape}')

    columns_to_drop = [TARGET_COLUMN] + list(SENSITIVE_ATTRIBUTES.values()) + list(NOT_FEATURES.keys())    
    print(f'Dataset shape after drop columns and nan target: {df.drop(columns=columns_to_drop).shape}')

    df = df.dropna(subset=[TARGET_COLUMN]) 
    
    X = df.drop(columns_to_drop, axis=1)
    y = df[TARGET_COLUMN]

    df[TARGET_COLUMN] = df[TARGET_COLUMN].apply(lambda x: 1 if x == 'Sim' else 0)

    return X, y



def download_dataset_from_kaggle(url):
    od.download(url)


def get_column_mapping(columns):
    column_dict = {}
    column_mapping = {}

    for column in columns:
        column_stripped = column.strip("(')")
        column_splitted = column_stripped.replace("'", "").split(', ')

        column_dict[column_splitted[0].strip()] = ', '.join(column_splitted[1:])
        column_mapping[column] = column_splitted[0].strip()

    write_dictionary_on_json_file('data/column_mapping.json', column_dict)

    return column_mapping


def write_dictionary_on_json_file(file_path, dict):
    with open(file_path, 'w', encoding='utf-8') as json_file:
        sorted_dict = {k: dict[k] for k in sorted(dict)}
        json.dump(sorted_dict, json_file, ensure_ascii=False, indent=4)


def treat_sensitive_attributes(df):
    df[SENSITIVE_ATTRIBUTES['age']] = df[SENSITIVE_ATTRIBUTES['age']].apply(categorize_age)
    df[SENSITIVE_ATTRIBUTES['gender']] = df[SENSITIVE_ATTRIBUTES['gender']].apply(categorize_gender)
    df[SENSITIVE_ATTRIBUTES['race_color']] = df[SENSITIVE_ATTRIBUTES['race_color']].apply(categorize_race_color)
    df[SENSITIVE_ATTRIBUTES['pwd']] = df[SENSITIVE_ATTRIBUTES['pwd']].apply(categorize_pwd)

    return df


def categorize_age(age):
    if age <= 40:
        return '18-40'
    elif age > 40:
        return '40+'
    else:
        return np.nan
    

def categorize_gender(gender):
    if gender in ['Masculino', 'Feminino']:
        return gender
    else:
        return None
    

def categorize_race_color(race_color):
    if race_color == 'Branca':
        return race_color
    elif race_color in ['Parda', 'Preta', 'Amarela', 'Indígena', 'Outra']:
        return 'Não Branca'
    else:
        return None
    

def categorize_pwd(pwd):
    if pwd in ['Sim', 'Não']:
        return pwd
    else:
        return None


if __name__ == '__main__':
    main()
