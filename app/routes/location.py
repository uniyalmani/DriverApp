from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from fastapi.encoders import jsonable_encoder
from app.utilities.helpers import Location
from app.services import driver
from app.utilities.dependencies import is_valid_token
import time

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


@router.websocket("/ws/updatelocation")
async def updatelocation(websocket: WebSocket, driver: object = Depends(driver.Driver_Methods)):

    await websocket.accept()
    try:
        token = websocket.headers["token"]
        user_data = is_valid_token(token)
        # # if not data:
        # #     raise WebSocketDisconnect

        # email = data["email"]

        while True:
            print(websocket.query_params, "----------------------------")
            data = await websocket.receive_json()
            longitude = websocket.query_params["longitude"]
            latitude = websocket.query_params["latitude"]
            user_data["longitude"] = longitude
            user_data["latitude"] = latitude
            ret = driver.update_location(user_data)

            await websocket.send_json({"loc":[longitude, latitude], "data": user_data, "ret":user_data})
    except Exception as e:
        await websocket.send_json({"data":[], "error": e, "message": "failed"})
            

