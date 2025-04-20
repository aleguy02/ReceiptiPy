import secrets
import string
import base64

from src.config.config import Config


# credit to https://www.reddit.com/r/pythontips/comments/1fzxjv3/how_to_generate_random_strings_in_python/
def generate_random_string(length: int) -> str:
    """
    Generate a random alphanumeric string of the specified length.
    This function creates a string consisting of randomly selected
    uppercase letters, lowercase letters, and digits.
    Args:
        length (int): The length of the random string to generate.
    Returns:
        str: A randomly generated alphanumeric string of the specified length.
    """
    return "".join(
        secrets.choice(string.ascii_letters + string.digits) for _ in range(length)
    )


def generate_auth_header() -> str:
    """
    Generate a Base 64 encoded string that contains the client ID and client secret key.
    Returns:
        str: A base64 encoded string
    """
    # this article was helpful: https://ioflood.com/blog/python-base64-encode/
    return base64.b64encode(
        (Config.CLIENT_ID + ":" + Config.CLIENT_SECRET).encode("utf-8")
    ).decode()
