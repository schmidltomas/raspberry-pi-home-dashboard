#!/usr/bin/env python3
# coding=utf-8

import feedparser
import config
import logger
import json

"""Service for fetching news data from RSS feed."""


class RssServiceException(Exception):
	pass


def format_time(published_parsed):
	minutes = str(published_parsed.tm_min)
	if len(minutes) == 1:
		minutes = '0' + minutes
	return str(published_parsed.tm_hour) + ':' + minutes


class RSSService:
	url = config.rss_service['url']

	def fetch_data(self):
		logger.info("Fetching RSS news feed from=" + self.url)
		news_feed = feedparser.parse(self.url)

		if len(news_feed.entries) == 0:
			logger.error("Failed to fetch RSS new feed=" + news_feed.bozo_exception)
			raise RssServiceException(news_feed.bozo_exception)

		data = []
		for i in range(3):
			entry = news_feed.entries[i]
			data.append({
				"title": entry.title,
				"image_url": entry.media_content[0]['url'],
				"published": format_time(entry.published_parsed)
			})

		logger.info("Fetched RSSService data=" + json.dumps(data, ensure_ascii=False))
		return data
