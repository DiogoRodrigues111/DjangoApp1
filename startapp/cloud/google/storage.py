from google.cloud import storage

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
    bucket_entity = client.bucket(bucket_name)
    bucket_entity.location = "PT-BR"
    bucket_entity = client.create_bucket(bucket_entity)

    """ Check if necessary commands """

    if bucket_entity.exists(client):
        print("Bucket created with success, please check it in google cloud platforms.")
    else:
        print("Failed to creating Bucket. Please check it.")

    if not bucket_entity:
        print("Try in Retry failed.")
    else:
        pass

    return bucket_entity
