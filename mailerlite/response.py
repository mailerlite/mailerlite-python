from __future__ import absolute_import


class ApiResponse(dict):
    """
    The decoded JSON body of a response

    It is a dict, so you use it like the dicts that the other methods return.
    It also has the status code and the headers of the response.
    """

    def __init__(self, response):
        super().__init__(response.json())
        self.status_code = response.status_code
        self.headers = response.headers

    @property
    def is_idempotent_replay(self):
        """
        True if the API returned the stored response of an earlier request
        with the same idempotency key
        """

        return self.headers.get("Idempotent-Replayed") == "true"
