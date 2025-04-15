# Fetch Take Home Exercise—SRE
This repository refines the original code in https://github.com/fetch-rewards/sre-take-home-exercise-python.

The Python script continuously determines the availability percentage of the endpoints in the provided YAML file.
The `Main-Thread` periodically launches a `Child-Thread` for API requests.
The `Child-Thread` reports the endpoints status (UP/DOWN) and counts number of successes.
Once the `Child-Thread` completes or times out, the `Main-Thread` calculates and prints the availability percentage for each domain.

The `Main-Thread` continues to execute the `Child-Thread` every 15 seconds, as long as the `Child-Thread` doesn't encounter any exceptions.


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
* `main.py`
  * ```python
    def load_config(file_path):
        """
        Use the generator to load the config file and yield endpoint values one by one.
        """
    def string_to_json_parser(element):
        """
        Parses the body element to JSON, if body is missing return "None".
        """
    def check_health(endpoint):
        """
        If 'method' value is missing, set default to "GET"
        Parse body to JSON or set body to "None"
        Send the request with timeout=RESPONSE_TIMEOUT_SEC
        """
    def monitor_endpoints(yaml_endpoint_gen, domain_stats):
        """
        global stop_main_thread - Use the global flag to inform the Main-thread of an exception
        (time.perf_counter() - start_time) < CYCLE_TIMEOUT_SEC - Limit the monitoring to CYCLE_TIMEOUT_SEC
        (endpoint := next(yaml_endpoint_gen, None)) is not None - Assignment operator to return the next endpoint or "None"
        domain = urlparse(endpoint[URL]).hostname - returns the domain without port
        """
    def availability_cycles(file_path):
        """
        Main-Thread function launches Child-Thread and prints out the results
        Executes Child-Thread every CYCLE_TIMEOUT_SEC
        """
    
    if __name__ == "__main__":
        """
        Validates that the given config file ends with .yaml
        """
```