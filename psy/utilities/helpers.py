import datetime
import glob
import json
import multiprocessing
import os
import pickle
import shutil
import time
from collections import defaultdict
from functools import wraps

import pandas as pd
import requests
from dateutil.relativedelta import relativedelta
from pytz import timezone


def delete_contents(path, delete_files=True, delete_folders=True, delete_itself=False):
    '''Delete contents in a directory'''
    print('Cleaning', path)
    if os.path.isdir(path):
        if delete_itself:
            shutil.rmtree(path)
        else:
            if delete_files:
                files = glob.glob('%s/*.*' % path)
                for f in files:
                    os.remove(f)
            if delete_folders:
                folders = glob.glob('%s/*' % path)
                for f in folders:
                    os.rmdir(f)


def create_folder(directory, delete_old=False):
    if delete_old:
        delete_contents(directory, delete_itself=delete_old)
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print('Directory created.' + directory)
    except OSError:
        print('Directory exists.' + directory)


def copy_folder(src, dest, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dest, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def get_command_output(cmd):
    return os.popen(cmd).read()


def run_command(cmd):
    return os.system(cmd)


def shutdown(seconds=0, os='linux'):
    """Shutdown system after seconds given. Useful for shutting EC2 to save costs."""
    if os == 'linux':
        run_command('sudo shutdown -h -t sec %s' % seconds)
    elif os == 'windows':
        run_command('shutdown -s -t %s' % seconds)


def timing(f):
    """Decorator for timing functions
    Usage:
    @timing
    def function(a):
        pass
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print('function:%r took: %2.2f sec' % (f.__name__,  end - start))
        return result
    return wrapper


def track_start_end(f):
    """Decorator for printing start and end of function
    Usage:
    @track_start_end
    def function(a):
        pass
    """

    @wraps(f)
    def wrapper(*args, **kwargs):
        print('Started:%r' % (f.__name__))
        result = f(*args, **kwargs)
        print('Ended:%r' % (f.__name__))
        return result
    return wrapper


def get_dict_by_list_of_keys(dictionary, keys):
    if type(keys) == type([]):
        for key in keys:
            dictionary = dictionary.get(key, {})
        return dictionary
    else:
        return {}


def add_params_to_object_from_dict(object, dictionary, key=None):
    if key:
        dictionary = dictionary[key]

    for param, param_value in dictionary.items():
        setattr(object, param, param_value)

    return object


def add_params_to_object_from_dict_path(object, dictionary_path, key=None):
    """ Add objects to a class from a dictionary file path.
    Useful for adding params to a global class from a json.
    """
    dictionary = json.load(open(dictionary_path))
    return add_params_to_object_from_dict(object, dictionary, key=key)

        
def call(method, url, payload=None, headers={'Content-Type': 'application/json'}):
    """ Use for calling APIs.
    Usage
    call('delete', 'http://localhost:8888/delete')
    """
    return getattr(getattr(requests, method)(url, data=json.dumps(payload), headers=headers), 'json')()


def get_cpu_count():
    """Useful for getting cores to be used in n_jobs in scikit or other multi-threading tasks."""
    return multiprocessing.cpu_count()


def load_json(file):
    with open(file) as json_file:
        return json.load(json_file)


def save_json(json_data, file, indent=4):
    with open(file, 'w') as outfile:
        json.dump(json_data, outfile, indent=indent)


def save_pickle(object, path):
    pickle.dump(object, open(path, 'wb'), protocol=pickle.HIGHEST_PROTOCOL)


def load_pickle(path):
    return pickle.load(open(path, 'rb'))


def get_datetime(zone='UTC', format='%Y-%m-%d-%H:%M:%S'):
    tz = timezone(zone)
    time = datetime.datetime.now(tz)
    return time.strftime(format)


def get_relative_date(zone='Asia/Kolkata', format='%Y-%m-%d', **kwargs): 
    """
    zone: Asia/Kolkata for India
    **kwargs: years, months, days, leapdays, weeks, hours, minutes, seconds, microseconds
    """
    tz = timezone(zone)
    time = datetime.datetime.now(tz)
    time_relative = time + relativedelta(**kwargs)
    return time_relative.strftime(format)


def get_timestamp(zone='UTC'):
    """Timestamp for databases."""
    tz = timezone(zone)
    time = datetime.datetime.now(tz)
    return time.strftime('%Y-%m-%d %H:%M:%S')


def get_epoch_num(file_path):
    """For keras saved model with file_name format"""
    x = file_path.split('-')
    return int(x[x.index('epoch') + 1].replace('.h5', ''))


def get_all_filepaths_with_extension(directory, extension='h5'):
    """For keras saved model with file_name format"""
    return glob.glob(os.path.join(directory, '*.%s' % extension))


def delete_files_with_extension(directory, extension='h5'):
    for p in get_all_filepaths_with_extension(directory, extension='h5'):
        print('Deleting %s' % p)
        os.remove(p)


def get_best_model_path(directory, extension='h5'):
    """For keras saved model with file_name format"""
    return sorted(get_all_filepaths_with_extension(directory, extension='h5'), reverse=True)[0]



def get_environment(env_variable='api_environment'):
    """Useful for detecting environment if we have set environment variable containing env name."""
    environment = os.environ.get(env_variable, 'local')
    print("Running.. We are in " + str(environment) + " environment")
    return environment


def get_nested_defaultdict():
    return defaultdict(get_nested_defaultdict)


def swap_df_columns(df, columns):
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
