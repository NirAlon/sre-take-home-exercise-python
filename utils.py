import json
from urllib.parse import urlparse
import yaml


def load_config(file_path):
    """
    Use the generator to load the config file and yield endpoint values one by one.
    """
    with open(file_path, 'r') as file:
        for endpoint in yaml.safe_load(file):
            yield endpoint


def string_to_json_parser(element):
    """
    Parses the body element to JSON, if body is missing return "None".
    """
    return json.loads(element) if element else None


def url_to_domain_parser(url):
    """
    Extract from string url the domain
    """
    return urlparse(url).hostname