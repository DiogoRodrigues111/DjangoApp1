from google.cloud import storage
import os

""" CONSTANTS """

# TODO:
#   Maybe put this constant in settings.py

# Top-level of the environments set.
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "djangoapp-366400-27c6c0b72706.json"


def create_new_bucket_google_cloud(bucket_name):
    """

    Create new databases for Google cloud.

    Args:
        bucket_name:
            Name of Storage Bucket identified.

    Returns:
            Bucket Client created with success.

    """

    """ Creating credentials for Google Cloud Storage. """

    client = storage.Client()
    bucket_entity = client.bucket(bucket_name=bucket_name)
    created_if_not_exists = client.create_bucket(bucket_entity, location="US")

    """ Check if necessary commands """

    return created_if_not_exists