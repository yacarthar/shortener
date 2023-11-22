class TokenMissingError(Exception):
    def __init__(self, token, message="Token Missing."):
        self.token = token
        self.message = message
        super().__init__(self.message)


class TokenDecodeError(Exception):
    def __init__(self, token, message="Token Decoded Error."):
        self.token = token
        self.message = message
        super().__init__(self.message)


class TokenTypeError(Exception):
    """Exception raised for token error

    Attributes:
        token -- input token which caused the error
        message -- explanation of the error
    """

    def __init__(self, token, ttype):
        self.token = token
        self.message = f"Invalid Token Type: {ttype.capitalize()} Token."
        super().__init__(self.message)


class TokenRevokedError(Exception):
    def __init__(self, token, message="Invalid Token: Revoked Token."):
        self.token = token
        self.message = message
        super().__init__(self.message)


class TokenExpiredError(Exception):
    def __init__(self, token, message="Token Expired."):
        self.token = token
        self.message = message
        super().__init__(self.message)
