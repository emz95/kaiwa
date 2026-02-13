from fastapi import APIRouter, HTTPException, status
from db.supabase import supabase
from models.scenario import ScenarioCreate, ScenarioUpdate, ScenarioResponse
from models.card import CardCreate, CardResponse
from uuid import UUID

router = APIRouter(
    prefix="/scenarios",
    tags=["scenarios"]
)

@router.get("", response_model=list[ScenarioResponse])
def get_scenarios():
    """Get all active scenarios, sorted by order_index"""
    try:
        response = supabase.table("scenarios").select("*").eq("is_active", True).order("order_index").execute()
        return response.data or []
    except Exception as e:
        print(f"Error fetching scenarios: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Failed to fetch scenarios. Please try again later."
        )

@router.get("/{scenario_id}", response_model=ScenarioResponse)
def get_scenario(scenario_id: UUID):
    """Get a specific scenario"""
    try:
        response = supabase.table("scenarios").select("*").eq("id", scenario_id).execute()
        if not response.data:
            raise HTTPException(
                status_code=404, 
                detail=f"Scenario {scenario_id} not found"
            )
        
        return response.data[0]
    except HTTPException:
        raise  
    except Exception as e:
        print(f"Error fetching scenario {scenario_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch scenario. Please try again later."
        )

@router.post("", status_code=status.HTTP_201_CREATED, response_model=ScenarioResponse)
def create_scenario(scenario: ScenarioCreate):
    """Create a new scenario"""
    try:
        response = supabase.table("scenarios").insert(scenario.model_dump()).execute()
        if not response.data:
            raise HTTPException(
                status_code=500,
                detail="Failed to create scenario"
            )
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating scenario: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to create scenario. Please try again later."
        )

@router.patch("/{scenario_id}", response_model=ScenarioResponse)
def update_scenario(scenario_id: UUID, scenario: ScenarioUpdate):
    """Update a specific scenario"""
    try:
        update_data = scenario.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="No fields provided to update"
            )
        response = supabase.table("scenarios").update(update_data).eq("id", scenario_id).execute()
        if not response.data:
            raise HTTPException(
                status_code=404,
                detail=f"Scenario {scenario_id} not found"
            )
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating scenario {scenario_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to update scenario. Please try again later."
        )
@router.delete("/{scenario_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_scenario(scenario_id: UUID):
    """Delete a specific scenario"""
    try:
        check_response = supabase.table("scenarios").select("id").eq("id", scenario_id).execute()
        if not check_response.data:
            raise HTTPException(
                status_code=404,
                detail=f"Scenario {scenario_id} not found"
            )
        
        supabase.table("scenarios").delete().eq("id", scenario_id).execute()
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting scenario {scenario_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to delete scenario. Please try again later."
        )

@router.get("/{scenario_id}/cards", response_model=list[CardResponse])
def get_scenario_cards(scenario_id: UUID):
    """Get all cards for a specific scenario"""
    try:
        scenario_check = supabase.table("scenarios").select("id").eq("id", scenario_id).execute()
        if not scenario_check.data:
            raise HTTPException(
                status_code=404,
                detail=f"Scenario {scenario_id} not found"
            )
        
        response = supabase.table("cards").select("*").eq("scenario_id", scenario_id).execute()
        return response.data or []
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching cards for scenario {scenario_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch cards. Please try again later."
        )

@router.post("/{scenario_id}/cards", status_code=status.HTTP_201_CREATED, response_model=CardResponse)
def create_scenario_card(scenario_id: UUID, card: CardCreate):
    """Create a new card for a specific scenario"""
    try:
        scenario_check = supabase.table("scenarios").select("id").eq("id", scenario_id).execute()
        if not scenario_check.data:
            raise HTTPException(
                status_code=404,
                detail=f"Scenario {scenario_id} not found"
            )
        
        card_data = card.model_dump()
        card_data["scenario_id"] = scenario_id
        
        response = supabase.table("cards").insert(card_data).execute()
        if not response.data:
            raise HTTPException(
                status_code=500,
                detail="Failed to create card"
            )
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating card for scenario {scenario_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to create card. Please try again later."
        ) 