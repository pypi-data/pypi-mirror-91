#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .common import _find_raw_content


def _similar_single(p, media_name):
	return media_name.lower() in p.lower() and (len(p) - len(media_name)) < 10


def _similar(p, media_names):
	return any([_similar_single(p, m) for m in media_names])


def _cleanup_raw_title(raw):
	raw = ''.join(raw.split('BBC Learning English - '))
	media_names = ['nyt', 'new york times', 'stackoverflow', 'bbc', 'opinion']
	index = raw.rfind('- ')
	if index != -1:
		raw = raw[:index]
	raw = raw.strip()
	parts = raw.split('|')
	parts = [p for p in parts if not _similar(p, media_names)]
	return ('|'.join(parts)).strip()


def _yield_possible_title_item(soup):
	yield soup.find("meta", {"property": "twitter:title"})
	yield soup.find("meta", {"name": "twitter:title"})
	yield soup.find("h1", class_='single-post-title')
	yield soup.find("h1", class_='news_title')
	yield soup.find("h1", class_='entry-title')
	yield soup.find('table', class_='infobox')
	yield soup.find('meta', property='og:title')
	yield soup.find("h1", class_='title')
	yield soup.find("h1", class_='story_art_title')
	yield soup.find("h1", class_='post-head')
	yield soup.find("h2", class_='question-title')
	yield soup.find("title")
	yield soup.find("h1")
	yield soup.find("h2")

	for item in soup.find_all('meta'):
		if 'title' in str(item.attrs):
			yield item


def _find_title_from_item(item):
	raw = _find_raw_content(item)
	return _cleanup_raw_title(raw)


def _find_title(soup, doc):
	for item in _yield_possible_title_item(soup):
		if not item:
			continue
		result = _find_title_from_item(item)
		if result and len(result) < 200:
			return result
	return _cleanup_raw_title(doc.title())
