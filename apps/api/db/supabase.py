import os
from pathlib import Path
from dotenv import load_dotenv
from supabase import create_client, Client


env_path = Path(__file__).parent.parent.parent.parent / ".env"

loaded = load_dotenv(env_path)

SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")


supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_SERVICE_ROLE_KEY,
)