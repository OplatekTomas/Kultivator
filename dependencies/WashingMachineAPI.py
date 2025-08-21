from BaseDependencies import SingletonDependency, TransientDependency
import threading
import requests
import time


class WashingMachineAPI(SingletonDependency):

    url = "http://192.168.10.16:5000/WashingMachine/"
    _is_running_status = None

    def __init__(self):
        # Start background thread to check the machine status
        self._start_background_task()

    def _start_background_task(self):
        def fetch_status():
            while True:
                try:
                    # Make a GET request to the /isrunning endpoint
                    response = requests.get(self.url + "isrunning")
                    response.raise_for_status()
                    # Update the running status
                    self._is_running_status = response.text.lower() == "true"
                except requests.RequestException as e:
                    # Handle exceptions (e.g., log them if required)
                    self._is_running_status = None
                # Wait 5 seconds before the next request
                time.sleep(5)

        threading.Thread(target=fetch_status, daemon=True).start()

    # request to get the status of the washing machine
    def is_running(self):
        return self._is_running_status


