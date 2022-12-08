from fastapi import APIRouter, Depends
from app.helpers import Location

router = APIRouter()

@router.get("/distance", 
            tags=["Common Routes"])
def get_distance(source_longitude: float = 0.0, source_latitude: float = 0.0, 
                    destination_longitude: float = 0.0, destination_latitude: float = 0.0):
    
    source = (source_longitude, source_latitude)
    destination = (destination_longitude, destination_latitude)
    
    print(source, destination)
    location = Location(source, destination)
   
    return location.distance_time()
