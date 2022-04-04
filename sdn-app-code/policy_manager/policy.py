import requests 
import logging

class Trigger:

    status = False
    def compute_status(self, avg, threshold):

        if avg > threshold:
            self.status = True


class Policy:

    triggered = False

    #def __init__(self):


class RateLimitPolicy(Policy):

    samples = []
    threshold = 0

    trigger = Trigger()

    def probe(self):
        
        logging.warning("beginning probe")
        if len(self.samples) == 6:
            self.samples.pop(0)
        
        flowresponse = requests.get(self.url, auth=("onos", "rocks"))
        print(flowresponse.json())
        packets = flowresponse.json()["flows"][0]["packets"]
        self.samples.append(int(packets) - self.baseline)

        avg = (self.samples[-1] - self.samples[0]) / (len(self.samples) or 1) * 10

        logging.warning(f"avg: {avg} calculated from: {self.samples}")
        self.trigger.compute_status(avg, self.threshold)

    def __init__(self, url, threshold):
        
        self.threshold = threshold
        self.url = url
        logging.warning("policy debug output")
        logging.warning(url)
        logging.warning(requests.get(url, auth=("onos", "rocks")))
        logging.warning(requests.get(url, auth=("onos", "rocks")).json())

        self.baseline = requests.get(url, auth=("onos", "rocks")).json()["flows"][0]["packets"]