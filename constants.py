# Response constants
LOWER_STATUS_CODE = 200
UPPER_STATUS_CODE = 300
RESPONSE_TIMEOUT_SEC = 0.5 # 500 ms

# Response return status
SERVER_UP = "UP"
SERVER_DOWN = "DOWN"

# Monitoring cycle in seconds
CYCLE_TIMEOUT_SEC = 15

# Requests methods
GET = "GET"

# Configuration file keys
METHOD = "method"
URL = "url"
HEADERS = "headers"
BODY = "body"

# Domains states keys
TOTAL = "total"
OVERALL_ENDPOINTS = "overall_endpoints"


# Informative messages
DOT_YAML = ".yaml"
FILE_IS_NOT_YAML_MSG = f"File type: Config file must ends with {DOT_YAML}"
USAGE_MSG = "Usage: python monitor.py <config_file_path>"
KEYBOARD_INTERRUPT_MSG = "\nMonitoring stopped by user."
LOG_AVAILABILITY_RESULTS = "{} has {}% availability percentage, counted {} endpoints."
THREAD_POOL_TIMEOUT_MSG = "ThreadPool executor has reached the timeout"
PRINT_SEPARATOR = "---"

