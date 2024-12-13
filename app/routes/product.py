from fastapi import APIRouter, HTTPException, Query
from app.services.product_service import get_products_paginated

router = APIRouter()

@router.get("/")
async def get_all_products(page: int = Query(1, ge=1), limit: int = Query(10, ge=1)):
    try:
        products = await get_products_paginated(page, limit)
        return {"products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
