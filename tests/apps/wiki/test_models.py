# -*- coding: utf-8 -*-
from django.core.cache import cache, caches

from inyoka.utils.test import TestCase
from inyoka.wiki.models import Page
from inyoka.wiki.exceptions import CaseSensitiveException


class TestPageManager(TestCase):
    def test_get_by_name_case_sensitive(self):
        """
        Tests that get_by_name does not ignore case.
        """
        Page.objects.create('test', 'test content')

        with self.assertRaises(CaseSensitiveException):
            Page.objects.get_by_name('Test', cached=False)

    def test_get_by_name_cache_case_sensitive_set(self):
        """
        Tests that get_by_name creates the correct cache.
        """
        Page.objects.create('Test', 'test content')

        Page.objects.get_by_name('Test')

        self.assertIsNone(cache.get('wiki/page/Test'))
        self.assertIsNotNone(cache.get('wiki/page/test'))

    def test_get_missing(self):
        """
        Tests, that get_missing returns a dict with the correct conent.
        """
        Page.objects.create('test1', 'test content')
        Page.objects.create('test2', '[:test1:] content')
        test3 = Page.objects.create('test3', '[:missing:] content')

        missing_pages = Page.objects.get_missing()

        self.assertEqual(dict(missing_pages), {'missing': [test3]})

    def test_render_all_pages(self):
        """
        Test, that a rendered page will be put into the cache.
        """
        page = Page.objects.create('test1', '[:test1:] content')

        _field = page.rev.text._meta.get_field('value')
        cache_key = _field.get_redis_key(page.rev.text.__class__, page.rev.text, _field.name)

        content_cache = caches['content']
        self.assertFalse(content_cache.has_key(cache_key))

        Page.objects.render_all_pages()

        self.assertTrue(content_cache.has_key(cache_key))

    def test_render_all_pages__two_pages(self):
        """
        Test, that two rendered pages will be put into the cache.
        """
        page = Page.objects.create('test1', '[:test1:] content')
        page2 = Page.objects.create('test2', 'test content')

        _field = page.rev.text._meta.get_field('value')
        cache_key = _field.get_redis_key(page.rev.text.__class__, page.rev.text, _field.name)
        cache_key2 = _field.get_redis_key(page2.rev.text.__class__, page2.rev.text, _field.name)

        content_cache = caches['content']
        self.assertFalse(content_cache.has_key(cache_key))
        self.assertFalse(content_cache.has_key(cache_key2))

        Page.objects.render_all_pages()

        self.assertTrue(content_cache.has_key(cache_key))
        self.assertTrue(content_cache.has_key(cache_key2))
