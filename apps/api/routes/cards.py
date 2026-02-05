from fastapi import APIRouter, HTTPException, status
from db.supabase import supabase
from models.card import CardCreate, CardUpdate, CardResponse
from uuid import UUID

router = APIRouter(
    prefix="/cards",
    tags=["cards"]
)

@router.get("/{card_id}", response_model=CardResponse)
def get_card(card_id: UUID):
    """Get a specific card"""
    try:
        response = supabase.table("cards").select("*").eq("id", card_id).execute()
        if not response.data:
            raise HTTPException(
                status_code=404, 
                detail=f"Card {card_id} not found"
            )
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching card {card_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch card. Please try again later."
        )

@router.post("", status_code=status.HTTP_201_CREATED, response_model=CardResponse)
def create_card(card: CardCreate):
    """Create a new card"""
    try:
        response = supabase.table("cards").insert(card.model_dump()).execute()
        if not response.data:
            raise HTTPException(
                status_code=500,
                detail="Failed to create card"
            )
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creating card: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to create card. Please try again later."
        )

@router.patch("/{card_id}", response_model=CardResponse)
def update_card(card_id: UUID, card: CardUpdate):
    """Update a specific card"""
    try:
        update_data = card.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="No fields provided to update"
            )
        response = supabase.table("cards").update(update_data).eq("id", card_id).execute()
        if not response.data:
            raise HTTPException(
                status_code=404,
                detail=f"Card {card_id} not found"
            )
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating card {card_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to update card. Please try again later."
        )

@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(card_id: UUID):
    """Delete a specific card"""
    try:
        check_response = supabase.table("cards").select("id").eq("id", card_id).execute()
        if not check_response.data:
            raise HTTPException(
                status_code=404,
                detail=f"Card {card_id} not found"
            )
        
        supabase.table("cards").delete().eq("id", card_id).execute()
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting card {card_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to delete card. Please try again later."
        )
