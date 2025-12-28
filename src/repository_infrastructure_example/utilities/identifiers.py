import uuid

from slugify import slugify


def create_slug(text: str) -> str:
    """
    Create a slug from the given text.

    :param text: The text to create a slug from.
    :return: The slug.
    """
    return slugify(text, max_length=50)


def generate_uuid() -> uuid.UUID:
    """
    Generate a random UUID.

    :return: A UUID.
    """
    return uuid.uuid4()
