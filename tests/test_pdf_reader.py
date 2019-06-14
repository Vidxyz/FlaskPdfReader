import pytest
import unittest
import datetime
from flaskpdfreader.pdf_reader import *


EMPTY_TESTING_STATS = []

FIRST_TESTING_STATS = [(1, 'sample1.pdf', datetime.datetime(2019, 6, 13, 20, 13, 13), 9, 'banana'), 
                        (1, 'sample1.pdf', datetime.datetime(2019, 6, 13, 20, 13, 13), 7, 'potato'), 
                        (1, 'sample1.pdf', datetime.datetime(2019, 6, 13, 20, 13, 13), 4, 'onion'), 
                        (1, 'sample1.pdf', datetime.datetime(2019, 6, 13, 20, 13, 13), 2, 'hotdogs'), 
                        (1, 'sample1.pdf', datetime.datetime(2019, 6, 13, 20, 13, 13), 1, 'burgers'), ]
CLEANED_FIRST_STATS = [['sample1.pdf', datetime.datetime(2019, 6, 13, 20, 13, 13), 
                        [('banana', 9), ('potato',7), ('onion',4), ('hotdogs',2), ('burgers',1)]]]
JSON_FIRST_STATS = [
                    {'filename':'sample1.pdf',
                    'timestamp': datetime.datetime(2019, 6, 13, 20, 13, 13),
                    'most_common_words': [
                            {
                                'count': 9,
                                'word': 'banana'
                            },
                            {
                                'count': 7,
                                'word': 'potato'
                            },
                            {
                                'count': 4,
                                'word': 'onion'
                            },
                            {
                                'count': 2,
                                'word': 'hotdogs'
                            },
                            {
                                'count': 1,
                                'word': 'burgers'
                            },
                        ]
                    }
                    ]



SECOND_TESTING_STATS = [(1, 'sample1.pdf', datetime.datetime(2019, 6, 13, 20, 13, 13), 9, 'banana'), 
                        (1, 'sample1.pdf', datetime.datetime(2019, 6, 13, 20, 13, 13), 7, 'potato'), 
                        (1, 'sample1.pdf', datetime.datetime(2019, 6, 13, 20, 13, 13), 4, 'onion'), 
                        (1, 'sample1.pdf', datetime.datetime(2019, 6, 13, 20, 13, 13), 2, 'hotdogs'), 
                        (1, 'sample1.pdf', datetime.datetime(2019, 6, 13, 20, 13, 13), 1, 'burgers'), 

                        (2, 'sample2.pdf', datetime.datetime(2019, 6, 11, 20, 13, 13), 13, 'this'), 
                        (2, 'sample2.pdf', datetime.datetime(2019, 6, 11, 20, 13, 13), 11, 'is'), 
                        (2, 'sample2.pdf', datetime.datetime(2019, 6, 11, 20, 13, 13), 9, 'just'), 
                        (2, 'sample2.pdf', datetime.datetime(2019, 6, 11, 20, 13, 13), 4, 'another'), 
                        (2, 'sample2.pdf', datetime.datetime(2019, 6, 11, 20, 13, 13), 3, 'test'),
                        ]
CLEANED_SECOND_STATS = [['sample1.pdf', datetime.datetime(2019, 6, 13, 20, 13, 13), 
                        [('banana', 9), ('potato',7), ('onion',4), ('hotdogs',2), ('burgers',1)]],
                        ['sample2.pdf', datetime.datetime(2019, 6, 11, 20, 13, 13), 
                        [('this', 13), ('is',11), ('just',9), ('another',4), ('test',3)]]
                        ]
JSON_SECOND_STATS = [
                        {
                            'filename':'sample1.pdf',
                            'timestamp': datetime.datetime(2019, 6, 13, 20, 13, 13),
                            'most_common_words': [
                                    {
                                        'count': 9,
                                        'word': 'banana'
                                    },
                                    {
                                        'count': 7,
                                        'word': 'potato'
                                    },
                                    {
                                        'count': 4,
                                        'word': 'onion'
                                    },
                                    {
                                        'count': 2,
                                        'word': 'hotdogs'
                                    },
                                    {
                                        'count': 1,
                                        'word': 'burgers'
                                    },
                                ]
                        }, 
                        {
                            'filename':'sample2.pdf',
                            'timestamp': datetime.datetime(2019, 6, 11, 20, 13, 13),
                            'most_common_words': [
                                    {
                                        'count': 13,
                                        'word': 'this'
                                    },
                                    {
                                        'count': 11,
                                        'word': 'is'
                                    },
                                    {
                                        'count': 9,
                                        'word': 'just'
                                    },
                                    {
                                        'count': 4,
                                        'word': 'another'
                                    },
                                    {
                                        'count': 3,
                                        'word': 'test'
                                    },
                                ]
                        }, 
                    ]


def test_sanitize_stats():
    stats = EMPTY_TESTING_STATS
    cleaned_stats = sanitize_stats(stats)
    assert cleaned_stats == []

    stats = FIRST_TESTING_STATS
    cleaned_stats = sanitize_stats(stats)
    assert cleaned_stats == CLEANED_FIRST_STATS

    stats = SECOND_TESTING_STATS
    cleaned_stats = sanitize_stats(stats)
    assert cleaned_stats == CLEANED_SECOND_STATS


def test_make_json():
    stats = EMPTY_TESTING_STATS
    json_stats = make_json(stats)
    assert json_stats == []

    stats = CLEANED_FIRST_STATS
    json_stats = make_json(stats)
    assert json_stats == JSON_FIRST_STATS

    stats = CLEANED_SECOND_STATS
    json_stats = make_json(stats)
    assert json_stats == JSON_SECOND_STATS


def test_process_file(client):
    pass


def test_get_common_words(client):
    response = client.get('/get-common-words')
    assert response.status_code == 200