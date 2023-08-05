
RESPONSE_OK = 200


class Response:

    def __new__(self, *args, **kwargs):
        response = args[0]
        if response.status_code == 200:
            return "success", response.json()
        else:
            return "failure", response.text
