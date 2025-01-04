import requests

API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
headers = {"Authorization": "Bearer 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"}


class Falcon7BFewShotLogInference:
    def __init__(self):
        return

    def initialise(self):
        return

    def get_prompt(self, log: str) -> str:
        return """
        Classify the given log line into faulty or normal.
        Following are some of the normal state logs. Refer to them when deciding whether the given log template contains a failure indicator or normal.
        Normal state logs:
        br0: port entered state,
        device promiscuous mode,
        delete user,
        Failed for invalid user from port ssh2,
        Could not find device,
        waiting for device initialization: No such device",
        uid= euid=,
        Failed password for from port  ssh2,
        Received disconnect from port :: disconnected by user,
        tap1: Gained,
        Lost carrier,
        Stopped target,
        Disconnected from user port ,
        Stopped target Host and Network Name Lookups.,
        Finished Exit the Session.,
        Stopped User Manager for UID .,
        FAILED LOGIN () on '/dev/tty1' FOR 'UNKNOWN', Authentication failure,
        Stopping System Logging Service...

        Command: Classify the given log line as faulty or normal, referring to above normal log lines, and give a short reason in 4-5 words why the given log line would lead to a VM failure. 
        The faulty log lines should contain a valid reason for VM failure due to hardware fault or critical software issue, otherwise VMs would not fail. 
        The response should only contain the result and the reason.

        Log line: {log_line}
        Result: """.format(
            log_line=log
        )

    def query(self, payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    def infer(self, log: str) -> bool:
        prompt = self.get_prompt(log)
        payload = {
            "inputs": prompt,
            "parameters": {"max_new_tokens": 20},
            "options": {"use_cache": True, "wait_for_model": True},
        }
        response = self.query(payload)
        result_start_idx = response[0]["generated_text"].find("Result")
        generated_text = response[0]["generated_text"][result_start_idx + 6 : -1]
        print("Generated text:", generated_text)
        return (
            generated_text.lower().find("fault") >= 0
            or generated_text.lower().find("failure") >= 0
        )
