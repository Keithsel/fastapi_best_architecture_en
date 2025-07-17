#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re


def search_string(pattern: str, text: str) -> re.Match[str] | None:
    """
    Regex match anywhere in the string

    :param pattern: Regex pattern
    :param text: Text to match
    :return:
    """
    if not pattern or not text:
        return None

    result = re.search(pattern, text)
    return result


def match_string(pattern: str, text: str) -> re.Match[str] | None:
    """
    Regex match from the start of the string

    :param pattern: Regex pattern
    :param text: Text to match
    :return:
    """
    if not pattern or not text:
        return None

    result = re.match(pattern, text)
    return result


def is_phone(number: str) -> re.Match[str] | None:
    """
    Check mobile phone number format

    :param number: Phone number to check
    :return:
    """
    if not number:
        return None

    phone_pattern = r'^1[3-9]\d{9}$'
    return match_string(phone_pattern, number)


def is_git_url(url: str) -> re.Match[str] | None:
    """
    Check git URL format

    :param url: URL to check
    :return:
    """
    if not url:
        return None

    git_pattern = r'^(?!(git\+ssh|ssh)://|git@)(?P<scheme>git|https?|file)://(?P<host>[^/]*)(?P<path>(?:/[^/]*)*/)(?P<repo>[^/]+?)(?:\.git)?$'
    return match_string(git_pattern, url)
