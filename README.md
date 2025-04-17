# Fetch Take Home Exercise—SRE
This repository refines the original code in https://github.com/fetch-rewards/sre-take-home-exercise-python.

The Python script continuously determines the availability percentage of the endpoints in the provided YAML file.
The `Main-Thread` periodically launches a `Thread-Pool` for API requests.
The `Thread-Pool` launches `Threads` that reports the endpoints status (UP/DOWN).
Once the `Threads` completes or times out, the `Main-Thread` aggregate the results and prints the availability percentage of the overall endpoints and for each domain.

The `Main-Thread` continues to execute the `Thread-Pool` every 15 seconds, as long as the `Threads` doesn't encounter any exceptions.


## Requirements
* Python >= 3.8
* pip3 >= 23.2.1
* A valid YAML file, see the attached `sample.yaml`

## Installation

```bash
git clone https://github.com/NirAlon/sre-take-home-exercise-python.git
pip3 install requirements.txt
```

## Usage

```bash
python3 ./main.py <path/to/config.yaml>
```

## Refines

* `constants.py` - The original script contains hard-coded values. By defining constants, the script can be transformed into a generic concept and makes it easier to modify settings in the future.


* `utils.py` - Gathering together usable functions.
  * ```python
    def load_config(file_path):
        """
        Use the generator to load the config file and yield endpoint values one by one.
        """
    def string_to_json_parser(element):
        """
        Parses the body element to JSON, if body is missing return "None".
        """
    def url_to_domain_parser(url):
        """
        Extract from string url the domain
        """
    ```
* `main.py`
  * ```python
    def check_health(endpoint):
        """
        Function to perform health checks
        Returns the domain and state of the endpoint
    
        If 'method' value is missing set default to "GET"
        Parse body to JSON or set body to None
        Send the request with timeout=RESPONSE_TIMEOUT_SEC
        """
    def monitor_endpoints(endpoint):
        """
        Child-Thread function to monitor endpoints
        Returns the domain and it's endpoint state
    
        global stop_main_thread - Use the global flag to inform the Main-thread of an exception,
        domain = url_to_domain_parser - Extract the domain from the url.
        """
    def availability_cycles(file_path):
        """
        Main-Thread function uses ThreadPool to execute Child-Thread
        Aggregating and prints out the results
    
        Every monitor cycle is complete in CYCLE_TIMEOUT_SEC
        """
    
    if __name__ == "__main__":
        """
        Validates that the given config file ends with .yaml
        """
```