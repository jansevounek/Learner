import os
from supabase import create_client, Client

url: str = os.environ.get("VITE_SUPABASE_URL")
key: str = os.environ.get("VITE_SUPABASE_KEY")
supabase: Client = create_client(url, key)

__all__ = ['supabase']