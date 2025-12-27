import os
import requests

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_KEY")
SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET", "resumes")


def upload_file_to_supabase(file_bytes: bytes, file_path: str, content_type: str):
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        raise RuntimeError("Supabase env vars missing")

    url = f"{SUPABASE_URL}/storage/v1/object/{SUPABASE_BUCKET}/{file_path}"

    headers = {
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": content_type,
    }

    response = requests.post(url, headers=headers, data=file_bytes)

    if response.status_code not in (200, 201):
        raise RuntimeError(f"Upload failed: {response.text}")


def generate_signed_url(path: str, expires_in: int = 300) -> str:
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        raise RuntimeError("Supabase environment variables are missing")

    path = path.lstrip("/")

    url = f"{SUPABASE_URL}/storage/v1/object/sign/{SUPABASE_BUCKET}/{path}"

    headers = {
        "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
        "Content-Type": "application/json",
    }

    payload = {"expiresIn": expires_in}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code != 200:
        raise RuntimeError(f"Signed URL failed: {response.text}")

    signed_path = response.json()["signedURL"]

    # ✅ CRITICAL FIX: return FULL URL
    return f"{SUPABASE_URL}/storage/v1{signed_path}"