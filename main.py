from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from sheets import get_routes, update_count

app = FastAPI(title="Transport Dashboard Backend")

# ✅ CORS (so React can call this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # later you can restrict this
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------
# Health check
# ---------------------------
@app.get("/")
def health():
    return {"status": "ok"}


# ---------------------------
# Models
# ---------------------------
class UpdateRequest(BaseModel):
    route: str
    type: str       # "student" or "employee"
    change: int     # +1 or -1 (or any integer)


# ---------------------------
# Routes
# ---------------------------
@app.get("/transport/routes")
def fetch_routes():
    """
    Fetch all transport routes with seat info
    """
    try:
        return get_routes()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/transport/update")
def update_transport(req: UpdateRequest):
    """
    Update student/employee count for a route
    """
    try:
        update_count(req.route, req.type, req.change)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
