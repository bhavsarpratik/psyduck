import json
import os
from collections import Counter

import numpy as np
import pandas as pd
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, f1_score, fbeta_score)
from sklearn.model_selection import cross_val_score

np.set_printoptions(precision=2)


def get_clarity_matrix(y, y_pred):
    "Get clarity matrix dataframe."
    # y = np.squeeze(y)
    # y_pred = np.squeeze(y_pred)
    classifier_labels = sorted(list(set(y)))
    cm = confusion_matrix(y, y_pred, classifier_labels)
    index = [str(col) + "_actual" for col in classifier_labels]
    columms = [str(col) + "_pred" for col in classifier_labels]
    cm_df = pd.DataFrame(cm, columns=columms, index=index)
    actual_values = Counter(y)
    cm_df['Total'] = [(actual_values)[col] if col in (actual_values).keys() else 0 for col in classifier_labels]
    cm_df['Accuracy'] = [cm_df.iloc[:, i][row] / cm_df['Total'][row] for i, row in enumerate(cm_df.index.tolist())]
    cm_df = cm_df.fillna(0)
    cm_df.insert(0, 'Total', cm_df['Total'], allow_duplicates=True)
    cm_df.insert(1, 'Accuracy', cm_df['Accuracy'], allow_duplicates=True)
    return cm_df


def get_metrics(y, y_pred, beta=2, average_method='macro', y_encoder=None):
    if y_encoder:
        y = y_encoder.inverse_transform(y)
        y_pred = y_encoder.inverse_transform(y_pred)
    return {
        'accuracy': round(accuracy_score(y, y_pred), 4),
        'f1_score_macro': round(f1_score(y, y_pred, average=average_method), 4),
        'fbeta_score_macro': round(fbeta_score(y, y_pred, beta, average=average_method), 4),
        'report': classification_report(y, y_pred, output_dict=True),
        'report_csv': classification_report(y, y_pred, output_dict=False).replace('\n','\r\n')
    }


def save_metrics(metrics: dict, model_directory, file_name):
    path = os.path.join(model_directory, file_name + '_report.txt')
    classification_report_to_csv(metrics['report_csv'], path)
    metrics.pop('report_csv')
    path = os.path.join(model_directory, file_name + '_metrics.json')
    json.dump(metrics, open(path, 'w'), indent=4)


def df_swap_cols(df, columns):
    """Swaps the column by column name or index
    columns: Can be a tuple of column indexes or names
    ex. (2, -1) or ('a', 'b')
    """
    first, second = columns
    cols = list(df.columns)
    if type(first) is int:
        cols[first], cols[second] = cols[second], cols[first]
        df = df[cols]
    elif type(first) is str:
        df[first], df[second] = df[second], df[first]
    return df


def get_classification_report(y, y_pred, sortby='support', ascending=False, y_encoder=None, path=None):
    if y_encoder:
        y = y_encoder.inverse_transform(y)
        y_pred = y_encoder.inverse_transform(y_pred)
    class_report = classification_report(y, y_pred, output_dict=True)
    class_report = pd.DataFrame(class_report).transpose()
    class_report['support'] = class_report['support'].astype(int)
    class_report_metrics = class_report[-3:]
    class_report = class_report[:-3].sort_values(sortby, ascending=ascending)
    class_report['cum_sum'] = class_report.support.cumsum()/class_report.support.sum()
    class_report = pd.concat([class_report, class_report_metrics])
    class_report = df_swap_cols(class_report, columns=(-1, 4))
    class_report = class_report.fillna('')
    if path:
        class_report.to_csv(path)
    return class_report


def generate_cross_validation(model, x, y, k_folds=5, n_jobs=-1):
    """Does cross validation and saves the results in a csv."""
    score_column_names = ['accuracy_fold_' + str(i + 1) for i in range(k_folds)]
    cv_column_names = ['score_avg', *score_column_names]

    # Perform cross-validation
    print('Performing cross validation.')
    scores = cross_val_score(model, x, y, cv=k_folds, n_jobs=n_jobs)

    # Save cross-validation scores for later output
    cv_df = pd.DataFrame(data=[[scores.mean(), *scores]], columns=cv_column_names)
    print(cv_df)
    print('Average cross-validated accuracy: %.4f' % scores.mean())
    return cv_df


def get_top_k_pred(model, x, k=1):
    """Gives probabilities of top 3 predictions."""
    probs = model.predict_proba(x)
    return np.argsort(probs, axis=1)[:, -k:]


def top_k_accuracy(model, x, y, k=1):
    """Give accuracy for top k match."""
    best_k = get_top_k_pred(model, x, k)
    return sum([np.isin(y_, best_k_) for y_, best_k_ in zip(y, best_k)]) / len(y)
