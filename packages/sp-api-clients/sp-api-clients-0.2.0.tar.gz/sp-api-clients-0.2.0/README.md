# sp-api-clients

This is a package generated from amazon selling partner open api models.

This package is for my personal usage, and may not be a good package,
but enough for myself.

## Features

* ready to use;
* provide code to generate clients, in case that amazon update models;
* type hint.

## Usage

For saving time, just paste my test code here.

For better understanding, all the fields are the same length of actual fields,
and some readable information are kept.

```python
def test_api():
    from datetime import datetime
    import sp_api_clients
    endpoint = "https://sellingpartnerapi-eu.amazon.com"
    marketplace_id = "A1F83G8C2ARO7P"

    refresh_token = "Atzr|xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
                    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
                    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
                    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    order_pk = 'xxx-xxxxxxx-xxxxxxx'
    role_arn = "arn:aws:iam::xxxxxxxxxxxx:role/sp_api_role"
    aws_access_key = 'xxxxxxxxxxxxxxxxxxxx'
    aws_secret_key = "xxxxx/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    client_config = dict(
        role_arn=role_arn,
        endpoint=endpoint,
        marketplace_id=marketplace_id,
        refresh_token=refresh_token,
        aws_access_key=aws_access_key,
        aws_secret_key=aws_secret_key,
    )
    order_client = sp_api_clients.orders.OrdersClient(**client_config)

    orders = order_client.getOrders(
        MarketplaceIds=[marketplace_id],
        CreatedAfter=datetime(2000, 1, 1).isoformat()).payload.Orders
    assert len(orders) > 0
    assert orders[0].AmazonOrderId == order_pk

```

## Configuration

The client configuration can be set both at the initiation and as environment variables.

* SP_API_ROLE_ARN
* SP_API_ENDPOINT
* SP_API_MARKETPLACE_ID
* SP_API_REFRESH_TOKEN
* SP_API_AWS_ACCESS_KEY
* SP_API_AWS_SECRET_KEY
* SP_API_LWA_CLIENT_KEY
* SP_API_LWA_CLIENT_SECRET

## Build

The client is generated in the following steps:

1. download amazon open api repository;
1. copy open api 2 json files from the amazon repository to a single directory;
1. convert open api 2 json files to open api 3 json files;
1. convert open api 3 json files to py clients.

The main script of generation is the `test_main` python file.

When convert open api to py clients,
I separated the process into 6 steps,
which are defined in the `swager_client_generator.stages` module.

If my build is not suitable for your demand,
or amazon api model updates but my build do not follow,
you can clone this repo, modify the `api.pyt` template and build it by yourself,
and please push a PR, thanks!
