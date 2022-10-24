from google.cloud import storage

def create_new_bucket_google_cloud(name_client, blob_name):
    """

    Create new databases for Google cloud.

    Args:
        name:
            Name of Storage Bucket identified.

        blob_name:
            Name the Blob Storage.

    Returns:
            Bucket Client created with success.

    """

    """ Creating credentials for Google Cloud Storage. """

    client = storage.Client()
    blob_entity = storage.bucket.Bucket(client, name_client)
    blob_created = blob_entity.blob(blob_name)

    """ Check if necessary commands """

    if blob_created.exists(client):
        print("Bucket created with success, please check it in google cloud platforms.")
    else:
        print("Failed to creating Bucket. Please check it.")

    if not blob_created:
        print("Try in Retry failed.")
    else:
        pass

    return client
