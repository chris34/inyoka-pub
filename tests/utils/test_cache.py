#-*- coding: utf-8 -*-
"""
    tests.utils.test_cache
    ~~~~~~~~~~~~~~~~~~~~~~

    :copyright: (c) 2007-2015 by the Inyoka Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
from django.test import TestCase
from mock import MagicMock, patch, DEFAULT

from inyoka.utils.local import local
from inyoka.utils.cache import get_cache, RedisCache


class TestCache(TestCase):

    def setUp(self):
        local.cache = {}
        self.real = {}
        self.cache = get_cache('default')
        self.cache = get_cache('request')
        self.cache.cache = self.real

    def test_seperate(self):
        def _compare(key, value, exists=True):
            self.assertEqual(value, self.cache.get(key))
            self.assertEqual(value, self.cache.get(key))
            self.assertEqual(key in self.cache.cache, exists)

        self.cache.set('test', 'foo')
        self.cache.set('test', 'bar')
        self.cache.set('bar', 'foo')
        _compare('test', 'bar')
        _compare('blah', None, False)
        _compare('bar', 'foo')

    def test_many(self):
        def _compare_many(keys, value):
            self.assertEqual(value, self.cache.get_many(keys))
            self.assertEqual(value, self.cache.get_many(keys))

        def _compare(key, value, exists=True):
            self.assertEqual(value, self.cache.get(key))
            self.assertEqual(value, self.cache.get(key))
            self.assertEqual(key in self.cache.cache, exists)

        self.cache.set_many({
            'test': 'bar',
            'bar': 'foo'
        })

        _compare_many(('test', 'bar', 'blah'), {'test': 'bar', 'bar': 'foo'})
        _compare('test', 'bar')
        _compare('bar', 'foo')
        _compare('blah', None, False)

    def test_delete(self):
        self.cache.set('foo', 'bar')
        self.assertEqual(self.cache.get('foo'), 'bar')
        self.cache.delete('foo')
        self.assertEqual(self.cache.get('foo'), None)

    def test_short_key_exceeding_with_prefix_and_version(self):
        key = 'a' * 248
        keyhash = 'md5:6af3d61e2e3ef8e189cffbea802c7e69'

        self.cache.set(key, 1)
        self.assertEqual(self.cache.get(keyhash), 1)

        self.cache.delete(key)
        self.assertEqual(self.cache.get(keyhash), None)

        self.cache.set(keyhash, 2)
        self.assertEqual(self.cache.get(key), 2)

        self.cache.delete(keyhash)
        self.assertEqual(self.cache.get(keyhash), None)

    def test_long_key(self):
        key = 'a' * 251
        keyhash = 'md5:21f5b107cda33036590a19419afd7fb6'

        self.cache.set(key, 1)
        self.assertEqual(self.cache.get(keyhash), 1)

        self.cache.delete(key)
        self.assertEqual(self.cache.get(keyhash), None)

        self.cache.set(keyhash, 2)
        self.assertEqual(self.cache.get(key), 2)

        self.cache.delete(keyhash)
        self.assertEqual(self.cache.get(keyhash), None)

    def test_short_key_exceeding_with_prefix_and_version_many(self):
        keya = 'a' * 248
        keyahash = 'md5:6af3d61e2e3ef8e189cffbea802c7e69'
        keyb = 'b' * 248
        keybhash = 'md5:bc36adde631774af8fc8add2de9665b8'

        data = {
            'a': 'a',
            'b': 'b',
            keya: 'aaa',
            keyb: 'bbb',
        }

        datahash = {
            'a': 'a',
            'b': 'b',
            keyahash: 'aaa',
            keybhash: 'bbb',
        }

        self.cache.set_many(data)
        self.assertEqual(self.cache.get_many(data.keys()), data)

        for k in data:
            self.cache.delete(k)

        self.cache.set_many(data)
        # If we request by the hash, we cannot map to the original key
        self.assertEqual(self.cache.get_many(datahash.keys()), datahash)

        for k in data:
            self.cache.delete(k)

        self.cache.set_many(datahash)
        self.assertEqual(self.cache.get_many(data.keys()), data)

        for k in datahash:
            self.cache.delete(k)

        self.cache.set_many(datahash)
        # If we request by the hash, we cannot map to the original key
        self.assertEqual(self.cache.get_many(datahash.keys()), datahash)

        for k in datahash:
            self.cache.delete(k)

    def test_long_key_many(self):
        keya = 'a' * 251
        keyahash = 'md5:21f5b107cda33036590a19419afd7fb6'
        keyb = 'b' * 251
        keybhash = 'md5:7e1b07a8a48d8c53aa0d6144cd6b5dbb'

        data = {
            'a': 'a',
            'b': 'b',
            keya: 'aaa',
            keyb: 'bbb',
        }

        datahash = {
            'a': 'a',
            'b': 'b',
            keyahash: 'aaa',
            keybhash: 'bbb',
        }

        self.cache.set_many(data)
        self.assertEqual(self.cache.get_many(data.keys()), data)

        for k in data:
            self.cache.delete(k)

        self.cache.set_many(data)
        # If we request by the hash, we cannot map to the original key
        self.assertEqual(self.cache.get_many(datahash.keys()), datahash)

        for k in data:
            self.cache.delete(k)

        self.cache.set_many(datahash)
        self.assertEqual(self.cache.get_many(data.keys()), data)

        for k in datahash:
            self.cache.delete(k)

        self.cache.set_many(datahash)
        # If we request by the hash, we cannot map to the original key
        self.assertEqual(self.cache.get_many(datahash.keys()), datahash)

        for k in datahash:
            self.cache.delete(k)


class TestRedisCache(TestCase):
    """
    Tests the redis content cache.
    """

    @patch.multiple(
        RedisCache,
        __init__=lambda self: None,
        client=DEFAULT,
        make_key=lambda self, key: key,
    )
    def test_value_in_cache(self, client):
        """
        Simulate case in which there is a value in the cache.
        """
        client.decode.side_effect = lambda x: 'decoded %s' % x
        redis = MagicMock(name='redis')
        redis.get.return_value = 'cached value'  # Value in the cache
        client.get_client.return_value = redis
        redis_cache = RedisCache()

        value = redis_cache.get_or_set('test', lambda: 'test value', 30)

        self.assertEqual(
            value,
            'decoded cached value',
            "The value from the cache should be decoded and returned.",
        )
        self.assertFalse(
            redis.set.called,
            "redis.set() should not be called.",
        )
        self.assertEqual(
            redis.get.call_count,
            1,
            "redis.get() should only be called once.",
        )

    @patch.multiple(
        RedisCache,
        __init__=lambda self: None,
        client=DEFAULT,
        make_key=lambda self, key: key,
    )
    def test_value_not_in_cache(self, client):
        """
        Test case, where the value is not the redis cache.
        """
        client.decode.side_effect = lambda x: 'decoded %s' % x
        client.encode.side_effect = lambda x: 'encoded %s' % x
        redis = MagicMock(name='redis')
        redis.get.return_value = None  # No Value in the cache
        client.get_client.return_value = redis
        redis_cache = RedisCache()

        value = redis_cache.get_or_set('test', lambda: 'test value', 30)

        self.assertEqual(
            value,
            'decoded encoded test value',
            "The value from the callback argument should be encoded, decoded and returned.",
        )
        self.assertEqual(
            redis.set.call_count,
            2,
            "redis.set() should be called two times.",
        )
        self.assertEqual(
            redis.get.call_count,
            1,
            "redis.get() should only be called once.",
        )

    @patch('inyoka.utils.cache.sleep')
    @patch.multiple(
        RedisCache,
        __init__=lambda self: None,
        client=DEFAULT,
        make_key=lambda self, key: key,
    )
    def test_value_not_in_cache_two_parallel_clients(self, sleep, client):
        """
        Test case where there is no value in the cache and two clients access
        it at the same time. The test call simulates the second call.
        """
        client.decode.side_effect = lambda x: 'decoded %s' % x
        client.encode.side_effect = lambda x: 'encoded %s' % x
        redis = MagicMock(name='redis')
        redis.get.side_effect = (None, None, 'cached value')  # Value in cache after the third call
        redis.set.return_value = False  # The set call fails (value already in the cache)
        client.get_client.return_value = redis
        redis_cache = RedisCache()

        value = redis_cache.get_or_set('test', lambda: 'test value', 30)

        self.assertEqual(
            value,
            'decoded cached value',
            "The value from the callback argument should be decoded and returned.",
        )
        self.assertEqual(
            redis.set.call_count,
            2,
            "redis.set() should be called two times.",
        )
        self.assertEqual(
            redis.get.call_count,
            3,
            "redis.get() should be called three times.",
        )
        self.assertEqual(
            sleep.call_count,
            2,
            "sleep() should be called two times.",
        )
