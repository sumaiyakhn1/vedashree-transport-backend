from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sheets import get_routes, update_count

app = FastAPI()


class UpdateRequest(BaseModel):
    route: str
    type: str   # student | employee
    change: int # +1 or -1


@app.get("/transport/routes")
def routes():
    return get_routes()


@app.post("/transport/update")
def update(req: UpdateRequest):
    try:
        update_count(req.route, req.type, req.change)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
