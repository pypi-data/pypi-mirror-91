class InvalidApiKeyError(Exception):
    def __init__(self, message='Unauthorized 401 returned. Maybe due to an Invalid API Key?'):
        self.message = message
        super().__init__(message)


class ConfiglyRequestError(Exception):
    def __init__(self, response):
        self.response = response
        status_code = str(response.status_code)
        text = str(response.text)

        self.message = (
            f'Something went wrong. An HTTP status of {status_code} was'
            f"returned with text: '{text}'. Have you upgraded the library?"
        )

        super().__init__(self.message)


class ConfiglyConnectionError(Exception):
    def __init__(self, message, error):
        self.message = message
        self.original_error = error
