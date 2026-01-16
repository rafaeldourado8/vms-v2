"""MinIO initialization script - Create buckets."""
import boto3
import os
import sys
from botocore.exceptions import ClientError

# MinIO configuration from environment
MINIO_ENDPOINT = os.getenv("STORAGE_ENDPOINT", "http://localhost:9000")
MINIO_ACCESS_KEY = os.getenv("STORAGE_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("STORAGE_SECRET_KEY", "minioadmin")

# Buckets to create
BUCKETS = [
    os.getenv("STORAGE_BUCKET_RECORDINGS", "recordings"),
    os.getenv("STORAGE_BUCKET_CLIPS", "clips"),
    os.getenv("STORAGE_BUCKET_LPR", "lpr-images"),
    os.getenv("STORAGE_BUCKET_THUMBNAILS", "thumbnails"),
]


def init_minio():
    """Initialize MinIO buckets."""
    print("🚀 Initializing MinIO...")
    print(f"Endpoint: {MINIO_ENDPOINT}")
    
    try:
        # Create S3 client
        s3_client = boto3.client(
            "s3",
            endpoint_url=MINIO_ENDPOINT,
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
        )
        
        # Create buckets
        for bucket in BUCKETS:
            try:
                s3_client.head_bucket(Bucket=bucket)
                print(f"✅ Bucket '{bucket}' already exists")
            except ClientError:
                s3_client.create_bucket(Bucket=bucket)
                print(f"✅ Bucket '{bucket}' created")
        
        print("✅ MinIO initialized successfully!")
        return 0
        
    except Exception as e:
        print(f"❌ Error initializing MinIO: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(init_minio())
