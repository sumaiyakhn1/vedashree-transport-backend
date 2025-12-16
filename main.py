from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sheets import get_routes, update_count

app = FastAPI(title="Transport Backend")

# 🔓 Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------
# Health check
# --------------------
@app.get("/")
def health():
    return {"status": "ok"}


# --------------------
# Request model
# --------------------
class UpdateRequest(BaseModel):
    route: str        # Route name
    type: str         # "student" or "employee"
    change: int       # +1 or -1


# --------------------
# Fetch routes
# --------------------
@app.get("/transport/routes")
def fetch_routes():
    try:
        return get_routes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# --------------------
# Update seat count
# --------------------
@app.post("/transport/update")
def update_seat(req: UpdateRequest):
    try:
        update_count(req.route, req.type, req.change)
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
