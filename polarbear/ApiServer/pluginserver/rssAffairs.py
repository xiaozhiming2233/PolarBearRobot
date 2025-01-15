#!/usr/bin/env python
# Coding: utf-8
# Author: Samsepi0l

import time
import json
import requests
import feedparser

# 定义网络安全相关的RSS源
rss_feeds = [
    "https://threatpost.com/feed/",
    "https://krebsonsecurity.com/feed/",
    "https://feeds.feedburner.com/securityweek",
    "https://www.darkreading.com/rss_simple.asp",
    "https://www.bleepingcomputer.com/feed/"
]

def fetch_rss_feed(feed_url):
    """获取并解析RSS源"""
    feed = feedparser.parse(feed_url)
    return feed

def print_feed_entries(feed):
    """打印RSS源中的条目"""
    for entry in feed.entries:
        print(f"Title: {entry.title}")
        print(f"Link: {entry.link}")
        print(f"Published: {entry.published}")
        print(f"Summary: {entry.summary}")
        print("-" * 80)

def main():
    for feed_url in rss_feeds:
        print(f"Fetching feed from: {feed_url}")
        feed = fetch_rss_feed(feed_url)
        import pdb;pdb.set_trace()
        print_feed_entries(feed)
        print("\n" + "=" * 80 + "\n")

if __name__ == "__main__":
    main()