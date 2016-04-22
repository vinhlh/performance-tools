#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# Author Vinh Le <vinh.le@zalora.com>
# (c) April 2016

from bs4 import BeautifulSoup
import requests
from urlparse import urlparse

valid_domains = [
    'googleads.g.doubleclick.net',
    'webtrekk-asia.net',
    'a.akamaihd.net',
    'data:image/png;base64'
]

def parse_html(html):
    return BeautifulSoup(html, 'html.parser')

def get_links(soup, attribute, tag = None):
    elements = soup.find_all(tag, attrs={attribute: True})
    links = []
    for element in elements:
        link = element.get(attribute)
        if link:
            links.append(link)

    return links

def get_invalid_domains(links):
    invalid_domains = {}
    for link in links:
        uri    = urlparse(link)
        domain = uri.netloc
        if domain and all(valid_domain not in domain for valid_domain in valid_domains):
            if domain not in invalid_domains:
                invalid_domains[domain] = []
            invalid_domains[domain].append(link)
    return invalid_domains

def print_results(url, invalid_domains):
    print '[{0}] Check {1}:'.format('✓' if not invalid_domains else 'x', url)

    for domain, links in invalid_domains.iteritems():
        print '{0:30} {1}'.format(domain, links[0])
        for link in links[1:]:
            print '{0:30} {1}'.format('', link)

def validate_country(url):
    response = requests.get(url)
    soup     = parse_html(response.text)

    print_results(url, get_invalid_domains(get_links(soup, 'data-bg') + get_links(soup, 'data-src') + get_links(soup, 'src', 'img')))

# run
countries = [
    'http://zalora.com.my',
    'http://zalora.co.id',
    'http://zalora.co.th',
    'http://zalora.com.ph',
    'http://zalora.vn',
    'http://zalora.sg',
    'http://zalora.com.hk',
    'http://zalora.com.tw'
]
for country in countries:
    validate_country(country)