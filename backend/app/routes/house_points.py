"""
REST API endpoints for managing house points.
"""
from typing import List, Optional
from enum import Enum
from fastapi import APIRouter, HTTPException, Path, Query, Body, Depends
from pydantic import BaseModel, Field
from datetime import datetime

# Router for house points
router = APIRouter(
    prefix="/api/house-points",
    tags=["House Points"],
    responses={404: {"description": "Not found"}},
)

# Pydantic models for request/response validation and Swagger documentation
class HouseEnum(str, Enum):
    GRYFFINDOR = "Gryffindor"
    HUFFLEPUFF = "Hufflepuff"
    RAVENCLAW = "Ravenclaw"
    SLYTHERIN = "Slytherin"

class PointTransaction(BaseModel):
    id: Optional[int] = Field(None, description="Unique identifier for the transaction")
    house: HouseEnum = Field(..., description="House name (Gryffindor, Hufflepuff, Ravenclaw, Slytherin)")
    points: int = Field(..., description="Number of points (positive for addition, negative for deduction)")
    reason: str = Field(..., description="Reason for awarding or deducting points")
    awarded_by: str = Field(..., description="Name of the staff member who awarded points")
    timestamp: Optional[datetime] = Field(None, description="When the points were awarded")
    student_name: Optional[str] = Field(None, description="Name of the student who earned the points (optional)")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "house": "Gryffindor",
                "points": 10,
                "reason": "Excellent work in Transfiguration class",
                "awarded_by": "Minerva McGonagall",
                "student_name": "Harry Potter"
            }
        }
    }

class PointTransactionResponse(PointTransaction):
    id: int
    timestamp: datetime
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "house": "Gryffindor",
                "points": 10,
                "reason": "Excellent work in Transfiguration class",
                "awarded_by": "Minerva McGonagall",
                "timestamp": "2023-09-01T14:30:45.123Z",
                "student_name": "Harry Potter"
            }
        }
    }

class HouseStanding(BaseModel):
    house: str = Field(..., description="House name")
    points: int = Field(..., description="Total points")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "house": "Gryffindor",
                "points": 450
            }
        }
    }

# Mock data for demonstration
mock_transactions = [
    PointTransactionResponse(
        id=1,
        house="Gryffindor",
        points=50,
        reason="Saving the Philosopher's Stone",
        awarded_by="Albus Dumbledore",
        timestamp=datetime.now(),
        student_name="Harry Potter"
    ),
    PointTransactionResponse(
        id=2,
        house="Slytherin",
        points=20,
        reason="Excellence in Potions",
        awarded_by="Severus Snape",
        timestamp=datetime.now(),
        student_name="Draco Malfoy"
    ),
    PointTransactionResponse(
        id=3,
        house="Gryffindor",
        points=10,
        reason="Answering questions correctly in class",
        awarded_by="Minerva McGonagall",
        timestamp=datetime.now(),
        student_name="Hermione Granger"
    ),
    PointTransactionResponse(
        id=4,
        house="Hufflepuff",
        points=15,
        reason="House unity demonstration",
        awarded_by="Pomona Sprout",
        timestamp=datetime.now(),
        student_name=None  # Example of points awarded to the entire house
    )
]

# Routes with detailed Swagger documentation
@router.get(
    "/",
    response_model=List[PointTransactionResponse],
    summary="Get All Points Transactions",
    description="Retrieve a list of all house point transactions with optional filtering",
    response_description="List of point transactions"
)
async def get_all_points_transactions(
    house: Optional[str] = Query(None, description="Filter by house name"),
    min_points: Optional[int] = Query(None, description="Minimum points value"),
    awarded_by: Optional[str] = Query(None, description="Filter by who awarded the points"),
    student: Optional[str] = Query(None, description="Filter by student who earned the points")
):
    """
    Get all house point transactions with optional filtering.
    
    - **house**: Filter by house name
    - **min_points**: Filter by minimum points value
    - **awarded_by**: Filter by who awarded the points
    - **student**: Filter by student who earned the points
    """
    # In a real application, this would query the database
    filtered = mock_transactions
    
    if house:
        filtered = [t for t in filtered if t.house.lower() == house.lower()]
    if min_points is not None:
        filtered = [t for t in filtered if t.points >= min_points]
    if awarded_by:
        filtered = [t for t in filtered if awarded_by.lower() in t.awarded_by.lower()]
    if student:
        filtered = [t for t in filtered if t.student_name and student.lower() in t.student_name.lower()]
        
    return filtered

@router.get(
    "/{transaction_id}",
    response_model=PointTransactionResponse,
    summary="Get Point Transaction",
    description="Retrieve a specific point transaction by ID",
    responses={
        200: {"description": "Successful response"},
        404: {"description": "Transaction not found"}
    }
)
async def get_point_transaction(
    transaction_id: int = Path(..., description="The ID of the transaction to retrieve", gt=0)
):
    """
    Get a specific point transaction by ID.
    
    - **transaction_id**: The unique identifier of the transaction
    """
    for transaction in mock_transactions:
        if transaction.id == transaction_id:
            return transaction
    raise HTTPException(status_code=404, detail="Transaction not found")

@router.post(
    "/",
    response_model=PointTransactionResponse,
    status_code=201,
    summary="Create Point Transaction",
    description="Record a new house point transaction",
    response_description="The created point transaction"
)
async def create_point_transaction(
    transaction: PointTransaction = Body(..., description="The point transaction to create")
):
    """
    Create a new point transaction.
    
    - Request body: PointTransaction object
    """
    # In a real application, this would save to the database
    new_id = max([t.id for t in mock_transactions]) + 1 if mock_transactions else 1
    new_transaction = PointTransactionResponse(
        id=new_id,
        house=transaction.house,
        points=transaction.points,
        reason=transaction.reason,
        awarded_by=transaction.awarded_by,
        student_name=transaction.student_name,
        timestamp=datetime.now()
    )
    mock_transactions.append(new_transaction)
    return new_transaction

@router.get(
    "/standings",
    response_model=List[HouseStanding],
    summary="Get House Standings",
    description="Get the current total points for each house",
    response_description="List of houses with their total points"
)
async def get_house_standings():
    """
    Get the current standings (total points) for each house.
    """
    # In a real application, this would be calculated from the database
    standings = {}
    for t in mock_transactions:
        if t.house not in standings:
            standings[t.house] = 0
        standings[t.house] += t.points
    
    return [HouseStanding(house=house, points=points) for house, points in standings.items()] 