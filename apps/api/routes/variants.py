from fastapi import APIRouter, HTTPException, status
from db.supabase import supabase
from models.variant import VariantCreate, VariantUpdate, VariantResponse
from uuid import UUID

router = APIRouter(
    prefix="/variants",
    tags=["variants"]
)

@router.get("", response_model=list[VariantResponse])
def get_variants():
    """Get all variants"""
    try:
        response = supabase.table("variants").select("*").execute()
        return response.data or []
    except Exception as e:
        print(f"Error fetching variants: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail="Failed to fetch variants. Please try again later."
        )

@router.get("/{variant_id}", response_model=VariantResponse)
def get_variant(variant_id: UUID):
    """Get a specific variant"""
    try:
        response = supabase.table("variants").select("*").eq("id", variant_id).execute()
        if not response.data:
            raise HTTPException(
                status_code=404,
                detail=f"Variant {variant_id} not found"
            )
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching variant {variant_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch variant. Please try again later."
        )


@router.post("", status_code=status.HTTP_201_CREATED, response_model=VariantResponse)
def create_variant(variant: VariantCreate):
    """Create a new variant"""
    try:
        response = supabase.table("variants").insert(variant.model_dump()).execute()
        if not response.data:
            raise HTTPException(
                status_code=500,
                detail="Failed to create variant"
            )
        return response.data[0]
    except HTTPException: 
        raise
    except Exception as e:
        print(f"Error creating variant: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to create variant. Please try again later."
        )

@router.delete("/{variant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_variant(variant_id: UUID):
    """Delete a specific variant"""
    try:
        check_response = supabase.table("variants").select("id").eq("id", variant_id).execute() 
        if not check_response.data:
            raise HTTPException(
                status_code=404,
                detail=f"Variant {variant_id} not found"
            )
        supabase.table("variants").delete().eq("id", variant_id).execute()
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting variant {variant_id}: {str(e)}")
        raise HTTPException(
            status_code=500,    
            detail="Failed to delete variant. Please try again later."
        )

@router.patch("/{variant_id}", response_model=VariantResponse)
def update_variant(variant_id: UUID, variant: VariantUpdate):
    """Update a specific variant"""
    try:
        update_data = variant.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=400,
                detail="No fields provided to update"
            )
        response = supabase.table("variants").update(update_data).eq("id", variant_id).execute()
        if not response.data:
            raise HTTPException(
                status_code=404,
                detail=f"Variant {variant_id} not found"
            )
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error updating variant {variant_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Failed to update variant. Please try again later."
        )