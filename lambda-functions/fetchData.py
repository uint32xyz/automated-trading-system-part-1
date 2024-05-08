import json
import requests
import boto3
import botocore
import csv
import io
from datetime import datetime


def lambda_handler(event, context):
    bucket_name = "ADD_YOUR_S3_BUCKET_NAME"
    current_date = datetime.now().strftime("%Y/%m/%d/%H")
    file_key = f"cmc/latest/{current_date}/cmcdata.csv"
    s3_client = boto3.client("s3")

    url = (
        "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?limit=1250"
    )
    headers = {
        "X-CMC_PRO_API_KEY": "ADD_YOUR_API_KEY_HERE",
        "Accept": "application/json",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()

        # Process new data
        flattened_quotes = [
            {
                # Dimensions
                "name": coin["name"],
                "symbol": coin["symbol"],
                "circulating_supply": coin["circulating_supply"],
                "total_supply": coin["total_supply"],
                "max_supply": coin["max_supply"],
                "date_added": coin["date_added"],
                "num_market_pairs": coin["num_market_pairs"],
                "cmc_rank": coin["cmc_rank"],
                # Metrics
                "price": coin["quote"]["USD"]["price"],
                "volume_24h": coin["quote"]["USD"]["volume_24h"],
                "volume_change_24h": coin["quote"]["USD"]["volume_change_24h"],
                "percent_change_1h": coin["quote"]["USD"]["percent_change_1h"],
                "percent_change_24h": coin["quote"]["USD"]["percent_change_24h"],
                "percent_change_7d": coin["quote"]["USD"]["percent_change_7d"],
                "percent_change_30d": coin["quote"]["USD"]["percent_change_30d"],
                "percent_change_60d": coin["quote"]["USD"]["percent_change_60d"],
                "percent_change_90d": coin["quote"]["USD"]["percent_change_90d"],
                "market_cap": coin["quote"]["USD"]["market_cap"],
                "market_cap_dominance": coin["quote"]["USD"]["market_cap_dominance"],
                "fully_diluted_market_cap": coin["quote"]["USD"][
                    "fully_diluted_market_cap"
                ],
                "last_updated": coin["quote"]["USD"]["last_updated"],
                "timestamp": datetime.utcnow()
                .replace(minute=0, second=0, microsecond=0, tzinfo=None)
                .isoformat(),
            }
            for coin in data["data"]
        ]

        # Convert new data to CSV format
        csv_file = io.StringIO()
        writer = csv.DictWriter(csv_file, fieldnames=flattened_quotes[0].keys())
        writer.writeheader()
        writer.writerows(flattened_quotes)

        # Upload to S3
        try:
            s3_client.put_object(
                Bucket=bucket_name, Key=file_key, Body=csv_file.getvalue()
            )
            print(f"Successfully uploaded file to {bucket_name}/{file_key}")
        except botocore.exceptions.ClientError as e:
            print(f"Error uploading file to S3: {e}")
            return {
                "statusCode": 500,
                "body": json.dumps("Error uploading file to S3."),
            }

        return {
            "statusCode": 200,
            "body": json.dumps("CSV file created and uploaded to S3 successfully."),
        }

    except requests.RequestException as e:
        print(f"Request error: {e}")
        return {"statusCode": 500, "body": json.dumps("Error fetching data from API.")}

