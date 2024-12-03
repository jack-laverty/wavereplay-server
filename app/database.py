from supabase import create_client
from typing import Optional


class SupabaseClient:
    def __init__(self, url: str, key: str):
        self.client = create_client(url, key)

    def get_client(self, token: Optional[str] = None):
        """Returns a Supabase client with the JWT token if provided"""
        if token:
            self.client.auth.set_session(token)
        return self.client
