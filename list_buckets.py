import os
from google.cloud import storage

# Set the credentials explicitly
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\takaw\OneDrive\Desktop\hotel_reservation\config\service_account_key.json"

# Initialize the client
client = storage.Client()

# List buckets
buckets = list(client.list_buckets())

print("Buckets:")
for bucket in buckets:
    print(bucket.name)
