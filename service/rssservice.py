#!/usr/bin/env python3
# coding=utf-8

import feedparser

"""Service for fetching news data from RSS feed."""


def format_time(published_parsed):
	minutes = str(published_parsed.tm_min)
	if len(minutes) == 1:
		minutes = '0' + minutes
	return str(published_parsed.tm_hour) + ':' + minutes + ' | '


class RSSService:
	url = "http://feeds.bbci.co.uk/news/video_and_audio/news_front_page/rss.xml?edition=uk"

	def fetch_data(self):
		news_feed = feedparser.parse(self.url)

		data = ''
		for i in range(3):
			entry = news_feed.entries[i]
			entry_time = format_time(entry.published_parsed)
			data += entry_time + entry.title + '\n'

		return data
