import time
import requests
from collections import defaultdict
from constants import *
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from utils import string_to_json_parser, load_config, url_to_domain_parser

stop_main_thread = False


def check_health(endpoint):
    """
    Function to perform health checks
    Returns the domain and state of the endpoint

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


def monitor_endpoints(endpoint):
    """
    Child-Thread function to monitor endpoints
    Returns the domain and it's endpoint state

    global stop_main_thread - Use the global flag to inform the Main-thread of an exception,
    domain = url_to_domain_parser - Extract the domain from the url.
    """
    global stop_main_thread
    try:
        domain = url_to_domain_parser(endpoint[URL])
        result = check_health(endpoint)
        return domain , 1 if result == SERVER_UP else 0
    except Exception as e:
        stop_main_thread = True
        raise e

def availability_cycles(file_path):
    """
    Main-Thread function uses ThreadPool to execute Child-Thread
    Aggregating and prints out the results

    Every monitor cycle is complete in CYCLE_TIMEOUT_SEC
    """
    while not stop_main_thread:
        domain_stats = defaultdict(lambda: {SERVER_UP: 0, TOTAL: 0})
        start = time.perf_counter()
        with ThreadPoolExecutor() as executor:
            try:
                results = executor.map(monitor_endpoints, load_config(file_path), timeout=CYCLE_TIMEOUT_SEC)
                for domain, state in results:
                    domain_stats[OVERALL_ENDPOINTS][SERVER_UP] += state
                    domain_stats[OVERALL_ENDPOINTS][TOTAL] += 1
                    domain_stats[domain][SERVER_UP] += state
                    domain_stats[domain][TOTAL] += 1
            except TimeoutError:
                print(THREAD_POOL_TIMEOUT_MSG)
            for domain, stats in domain_stats.items():
                availability = round(100 * stats[SERVER_UP] / stats[TOTAL])
                print(LOG_AVAILABILITY_RESULTS.format(domain, availability, stats[TOTAL]))
            print(PRINT_SEPARATOR)
            executor.shutdown()
        if (time.perf_counter()-start)<CYCLE_TIMEOUT_SEC:
            time.sleep(CYCLE_TIMEOUT_SEC-(time.perf_counter()-start))

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