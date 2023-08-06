class WebDriverError(Exception):
    """
    Base class for more specific WebDriverErrors
    """

    pass


class TabNotOpenException(WebDriverError):
    """
    Throw this when a tab is expected to be open(ed), but it does not
    """

    pass
