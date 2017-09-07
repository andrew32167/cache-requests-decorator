#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import os
import hashlib
import json
import pickle
from helper import local_to_rfc3339, rfc3339_to_local
import functools

_DEFAULT_CACHE_AGE = timedelta(minutes=42)


class CacheDecorator(object):
    """cache_decorator - Class for caching requests result JSONs
    WARNING works only with STATIC functions

    Caches requests to /tmp/cache_decorator/ folder

    """

    def __init__(self, cache_age=_DEFAULT_CACHE_AGE):
        """ init function that also creates cache directory and/or clean it """

        self._cache_dir = '/tmp/cache_decorator/'
        self._hash_template = '{request_type}_{params}'
        self._cache_file_template = '{hash}_{date}.cache'
        self._cache_max_age = cache_age

        if not os.path.isdir(self._cache_dir):
            os.mkdir(self._cache_dir)

        self._clear_cache_dir()

    def __call__(self, fn):
        """
        Decorator callable function

        :param args: *args of function that being decorated
        :param kwargs: *kwargs of function that being decorated
        :return: result of passed function if cache not found, if found read from cache file
        """

        self.func = fn

        @functools.wraps(fn)
        def _decorated(*args, **kwargs):
            hash_seed, filename = self._prepare_filename(*args, **kwargs)

            cache = self._check_cache(hash_seed)
            if cache is not False:
                try:
                    return self._pickle_read(cache)
                except ValueError:
                    os.remove('{}{}'.format(self._cache_dir, cache))
                    res = self.func(*args, **kwargs)
                    self._pickle_write(filename, res)
                    return res
            else:
                res = self.func(*args, **kwargs)
                self._pickle_write(filename, res)
                return res

        return _decorated

    def _prepare_filename(self, *args, **kwargs):
        """
        Function to prepare filename according to self._hash_template and self._cache_file_template

        :param args:
        :param kwargs:
        :return: hash_seed, date
        """

        sorted_kwargs = sorted(dict(kwargs).items())

        seed = self._hash_template.format(request_type=self.func.__name__,
                                          params=str(sorted_kwargs) + str(args))

        hash_seed = hashlib.md5(seed).hexdigest()
        filename = self._cache_file_template.format(hash=hash_seed,
                                                    date=local_to_rfc3339(datetime.now()))
        return hash_seed, filename

    def _parse_filename(self, file_name):
        """
        Function to parse cached filename into hash_seed and datetime

        :param file_name:
        :return: hash_seed, date
        """

        res = file_name.split('_')
        if len(res) == 2:
            cache_hash_seed, raw_date = res
            date = rfc3339_to_local(raw_date.split('.cache')[0])

            return cache_hash_seed, date
        else:
            print('Failed to read filename for {}'.format(file_name))
            os.remove('{}{}'.format(self._cache_dir, file_name))
            return None, None

    def _clear_cache_dir(self):
        """ Clearing caching directory by removing [`#*#`, `*~`, `.#*`] files"""

        for (dirpath, dirnames, filenames) in os.walk(self._cache_dir):
            for filename in filenames:
                if filename.startswith('#') and filename.endswith('#') or \
                        filename.endswith('~') or \
                        filename.startswith('.#'):
                    os.remove(''.join([dirpath, filename]))

    def _write_to_file(self, filename, content):
        """
        Function for writing to cache file

        :param filename: filename
        :param content: json object to serialize
        :return:
        """

        with open('{}{}'.format(self._cache_dir, filename), 'w+') as f:
            f.write(json.dumps(content))

    def _pickle_write(self, filename, content):
        with open('{}{}'.format(self._cache_dir, filename), 'wb') as f:
            pickle.dump(content, f)

    def _pickle_read(self, filename):
        with open('{}{}'.format(self._cache_dir, filename), 'r') as f:
            return pickle.load(f)

    def _read_from_file(self, filename):
        """
        Function for reading from cache file

        :param filename: filename
        :return: parsed json from a file
        """

        with open('{}{}'.format(self._cache_dir, filename), 'r') as f:
            content = f.read()
            return json.loads(content)

    def _check_cache(self, hash_seed):
        """
        Function for checking if there are cached files for hashed function seed

        :param hash_seed: md5 seed that is formed as it stated in self._hash_template
        :return: filename if cached is found, if not False
        """

        if os.path.isdir(self._cache_dir):
            for (dirpath, dirnames, filenames) in os.walk(self._cache_dir):
                for filename in filenames:
                    if filename.endswith('.cache'):
                        cached_hash_seed, date = self._parse_filename(filename)
                        if datetime.now() - self._cache_max_age >= date:
                            os.remove('{}{}'.format(self._cache_dir, filename))
                            continue
                        else:
                            if cached_hash_seed == hash_seed:
                                return filename
            return False
        else:
            os.mkdir(self._cache_dir)
            return False
