import json
import os
import urllib.request


class LocalGranite:

    def __init__(self):
        self.base_url = os.getenv(
            "OLLAMA_BASE_URL",
            "http://127.0.0.1:11434"
        )

        self.model = os.getenv(
            "GRANITE_MODEL",
            "granite3.3:2b"
        )

    def chat(self, system_prompt, messages):

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                }
            ] + messages,
            "stream": False,
            "options": {
                "temperature": 0.35
            }
        }

        data = json.dumps(payload).encode("utf-8")

        request = urllib.request.Request(
            self.base_url + "/api/chat",
            data=data,
            headers={
                "Content-Type": "application/json"
            },
            method="POST"
        )

        try:

            with urllib.request.urlopen(
                request,
                timeout=120
            ) as response:

                result = json.loads(
                    response.read().decode("utf-8")
                )

                return result.get(
                    "message",
                    {}
                ).get(
                    "content",
                    ""
                ).strip()

        except Exception as error:

            print(
                "Local Granite unavailable:",
                error
            )

            return None