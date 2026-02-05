import sys
from pathlib import Path

script_dir = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(script_dir))

from db.supabase import supabase


scenarios = [
    {
        "slug": "restaurant",
        "name": "Restaurant",
        "description": "Ordering food and interacting with restaurant staff",
        "order_index": 0,
        "is_active": True,
    },
    {
        "slug": "grocery-store",
        "name": "Grocery Store",
        "description": "Shopping at a grocery store and interacting with staff",
        "order_index": 1,
        "is_active": True,
    }
]

scenario_ids = {}

for s in scenarios:
    # Check if scenario exists by slug
    existing = supabase.table("scenarios").select("id").eq("slug", s["slug"]).execute()
    
    if existing.data:
        # Update existing scenario
        res = supabase.table("scenarios").update(s).eq("slug", s["slug"]).execute()
        scenario_ids[s["slug"]] = existing.data[0]["id"]
    else:
        # Insert new scenario
        res = supabase.table("scenarios").insert(s).execute()
        scenario_ids[s["slug"]] = res.data[0]["id"]

print("Seeded scenarios")


cards = [
    {
        "scenario_slug": "restaurant",
        "npc": "Have you decided on your order?",
        "intent": "Say you're ready and order ramen politely.",
    },
    {
        "scenario_slug": "restaurant",
        "npc": "Would you like something to drink?",
        "intent": "Order water politely.",
    },
    {
        "scenario_slug": "restaurant",
        "npc": "Will that be all?",
        "intent": "Confirm that's all.",
    },
    {
        "scenario_slug": "restaurant",
        "npc": "Will you be paying together?",
        "intent": "Say you will pay separately.",
    },
]

for card in cards:
    # Check if card already exists (by scenario_id, npc, and intent)
    existing_card = supabase.table("cards").select("id").eq("scenario_id", scenario_ids[card["scenario_slug"]]).eq("npc", card["npc"]).eq("intent", card["intent"]).execute()
    
    if not existing_card.data:
        # Only insert if it doesn't exist
        supabase.table("cards").insert({
            "scenario_id": scenario_ids[card["scenario_slug"]],
            "npc": card["npc"],
            "intent": card["intent"],
        }).execute()

print("Seeded cards")