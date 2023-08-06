from datahub.Manager import Manager


def connection(client_id=None, client_secret=None):
    if client_id is None:
        raise Exception("No Client ID Provided")
    if client_secret is None:
        raise Exception("No Client Secret Provided")
    return Manager(client_id=client_id, client_secret=client_secret)
