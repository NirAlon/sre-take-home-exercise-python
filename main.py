import time
import yaml
import requests
from collections import defaultdict
import json
from urllib.parse import urlparse
import threading
from constants import *

stop_main_thread = False

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


def check_health(endpoint):
    """
    Function to perform health checks
    If 'method' value is missing set default to "GET"
    Parse body to JSON or set body to None
    Send the request with timeout=RESPONSE_TIMEOUT_SEC
    """
    url = endpoint[URL]
    method = endpoint.get(METHOD, GET)
    headers = endpoint.get(HEADERS)
    body = string_to_json_parser(endpoint.get(BODY, None))

    try:
        response = requests.request(method, url, headers=headers, json=body, timeout=RESPONSE_TIMEOUT_SEC)
        return SERVER_UP if LOWER_STATUS_CODE <= response.status_code < UPPER_STATUS_CODE else SERVER_DOWN
    except requests.RequestException:
        return SERVER_DOWN


def monitor_endpoints(yaml_endpoint_gen, domain_stats):
    """
    Child-Thread function to monitor endpoints

    global stop_main_thread - Use the global flag to inform the Main-thread of an exception
    (time.perf_counter() - start_time) < CYCLE_TIMEOUT_SEC - Limit the monitoring to CYCLE_TIMEOUT_SEC
    (endpoint := next(yaml_endpoint_gen, None)) is not None - Assignment operator to return the next endpoint or None
    domain = urlparse(endpoint[URL]).hostname - returns the domain without port
    """
    global stop_main_thread
    try:
        start_time = time.perf_counter()
        while (endpoint := next(yaml_endpoint_gen, None)) is not None and (time.perf_counter() - start_time) < CYCLE_TIMEOUT_SEC:
            domain = urlparse(endpoint[URL]).hostname
            result = check_health(endpoint)
            domain_stats[TOTAL_ENDPOINTS][TOTAL] += 1
            domain_stats[domain][TOTAL] += 1
            if result == SERVER_UP:
                domain_stats[domain][SERVER_UP] += 1
                domain_stats[TOTAL_ENDPOINTS][SERVER_UP] += 1
    except Exception as e:
        stop_main_thread = True
        raise e

def availability_cycles(file_path):
    """
    Main-Thread function launches Child-Thread and prints out the results
    Executes Child-Thread every CYCLE_TIMEOUT_SEC
    """
    while not stop_main_thread:
        yaml_endpoint_gen = load_config(file_path)
        domain_stats = defaultdict(lambda: {SERVER_UP: 0, TOTAL: 0})
        t = threading.Thread(target=monitor_endpoints, args=(yaml_endpoint_gen, domain_stats,), daemon=True)
        t.start()
        t.join(CYCLE_TIMEOUT_SEC)
        for domain, stats in domain_stats.items():
            availability = round(100 * stats[SERVER_UP] / stats[TOTAL])
            print(LOG_AVAILABILITY_RESULTS.format(domain, availability, stats[TOTAL]))
        print(PRINT_SEPARATOR)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print(USAGE_MSG)
        sys.exit(1)
    elif not sys.argv[1].lower().endswith(DOT_YAML):
        print(FILE_IS_NOT_YAML_MSG)
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        availability_cycles(config_file)
    except KeyboardInterrupt:
        print(KEYBOARD_INTERRUPT_MSG)