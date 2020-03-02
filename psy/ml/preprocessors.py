from os.path import join as joinpath

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

from psy.utilities import helpers


def train_test_splitter(x, y, test_size=0.1, method='random'):
    '''Returns splitted data as train_x, test_x, train_y, test_y
    method
    random: Splits randomly in stratifies manner
    first_n: Splits by first n rows. Needed when we want to use first n rows for train and rest for test.
    '''
    if method == 'random':
        return train_test_split(x, y, test_size=test_size, stratify=y, random_state=0)
    elif method == 'first_n':
        train_length = int(len(x) * (1 - test_size))
        train_x, test_x = x[:train_length], x[train_length:]
        train_y, test_y = y[:train_length], y[train_length:]
        return train_x, test_x, train_y, test_y


def train_test_splitter_df(df, x_col_names, y_col_name, test_size=0.1):
    '''Returns splitted data as train_x, test_x, train_y, test_y'''
    return train_test_split(df[x_col_names], df[y_col_name], test_size=test_size, stratify=df[y_col_name], random_state=0)


def split_save_df(df, x_col_names, y_col_name, output_directory, test_size=0.1, method='random', output_format='csv', train_name='train.csv', test_name='test.csv'):
    '''
    method
    random: Splits randomly in stratifies manner
    first_n: Splits by first n rows. Needed when we want to use first n rows for train and rest for test.
    '''
    if method == 'random':
        df_train, df_test = train_test_split(df, stratify=df[[y_col_name]], test_size=test_size, random_state=0)
    elif method == 'first_n':
        train_length = int(len(df) * (1 - test_size))
        df_train, df_test = df[:train_length], df[train_length:]
    if output_format == 'csv':
        df_train.to_csv(joinpath(output_directory, train_name), index=False)
        df_test.to_csv(joinpath(output_directory, test_name), index=False)
    elif output_format == 'tsv':
        df_train.to_csv(joinpath(output_directory, train_name), sep='\t', index=False)
        df_test.to_csv(joinpath(output_directory, test_name), sep='\t', index=False)


def flag_by_value_count(df, col_name, freq_threshold=2, drop=False, replace_by='minority'):
    value_counts = df[col_name].value_counts()
    to_remove = value_counts[value_counts < freq_threshold].index
    df[col_name].replace(to_remove, replace_by, inplace=True)
    if drop:
        df = df[df[col_name] != replace_by]
    return df


def normalize_inputs_groupwise(df, scale_cols, groupby, save_dir='data', filename='normalizer.json', should_skipna=True, mode='train', save_dict=True):
    """Takes a dataframe and normalizes scale_cols columns groupwise.
    mode:
    train - saves normalizer dictionary
    predict - loads normalizer dictionary
    """
    dict_path = joinpath(save_dir, filename)
    helpers.create_folder(save_dir, delete_old=False)

    non_scale_cols = [col for col in df.columns if col not in scale_cols]
    df_scale_cols = df[scale_cols]
    groups = set(df[groupby])

    for group in groups:
        if mode == 'train':
            normalizer = helpers.get_nested_defaultdict()
        elif mode == 'predict':
            normalizer = helpers.load_json(dict_path)

        df_group = df_scale_cols[getattr(df, groupby) == group]
        for c in scale_cols:
            print(c)
            df_group_col = df_group[c]
            if mode == 'train':
                maxv = df_group_col.max(axis=0, skipna=should_skipna)
                minv = df_group_col.min(axis=0, skipna=should_skipna)
                meanv = df_group_col.mean(axis=0, skipna=should_skipna)
                sdv = df_group_col.std(axis=0, skipna=should_skipna)
                # Filling dictionary
                normalizer[c]['maxv'] = float(maxv)
                normalizer[c]['minv'] = float(minv)
                normalizer[c]['meanv'] = float(meanv)
                normalizer[c]['sdv'] = float(sdv)
            elif mode == 'predict':
                # Loading values from dictionary
                maxv = normalizer[c]['maxv']
                minv = normalizer[c]['minv']
                meanv = normalizer[c]['meanv']
                sdv = normalizer[c]['sdv']
            if maxv != minv and sdv != 0 and not np.isnan(sdv):
                df_group[c] = (df_group_col - meanv) / sdv
            else:
                logger.warning('Problem col:%s for %s:%s' % (c, groupby, group))
                df_group[c] = np.nan  # np.nan is actually None

        if mode == 'train' and save_dict:
            # Saving dictionary
            helpers.save_json(normalizer, dict_path)

        df_scale_cols.loc[getattr(df, groupby) == group] = df_group

    print('Scaling complete.')

    return pd.concat([df[non_scale_cols], df_scale_cols], axis=1)


def smooth_labels(y, smooth_factor=0.1):
    '''Convert a matrix of one-hot row-vector labels into smoothed versions.

    # Arguments
        y: matrix of one-hot row-vector labels to be smoothed
        smooth_factor: label smoothing factor (between 0 and 1)

    # Returns
        A matrix of smoothed labels.
    '''
    assert len(y.shape) == 2
    if 0 <= smooth_factor <= 1:
        # label smoothing ref: https://www.robots.ox.ac.uk/~vgg/rg/papers/reinception.pdf
        y *= 1 - smooth_factor
        y += smooth_factor / y.shape[1]
    else:
        raise Exception(
            'Invalid label smoothing factor: ' + str(smooth_factor))
    return y
