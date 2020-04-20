from gql import gql, Client
import os
from gql.transport.requests import RequestsHTTPTransport


def get_client():
    token = os.getenv("GITHUB_PERSONAL_TOKEN")
    transport=RequestsHTTPTransport(
        url='https://api.github.com/graphql',
        use_json=True,
        headers={
            "Content-type": "application/json",
            "Authorization": f"bearer {token}",
        },
        verify=True
    )

    return Client(
        retries=3,
        transport=transport,
        fetch_schema_from_transport=True
    )
