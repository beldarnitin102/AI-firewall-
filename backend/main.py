from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
import hashlib
import jwt

from config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_MINUTES
from logger import logger

from ml import (
    model,
    generate_packets,
    detect,
    evaluate_and_respond,
    enforce_policy
)

# ================= APP =================
app = FastAPI(title="AI Firewall Backend", version="1.1")

# ================= CORS =================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= AUTH =================
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# ================= USERS =================
users_db = {
    "admin": {
        "username": "admin",
        "password": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "admin"
    },
    "user": {
        "username": "user",
        "password": hashlib.sha256("user123".encode()).hexdigest(),
        "role": "user"
    }
}

# ================= HELPERS =================
def create_token(data: dict):
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except:
        logger.warning("Invalid or expired token")
        raise HTTPException(status_code=401, detail="Invalid token")

# ================= MIDDLEWARE =================
@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logger.info(
        f"{request.method} {request.url.path} "
        f"Status={response.status_code}"
    )
    return response

# ================= ROUTES =================

@app.get("/")
def root():
    return {
        "status": "running",
        "engine": "AI Firewall",
        "day": 21
    }

@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow()}

# ---------- LOGIN ----------
@app.post("/login")
def login(data: dict):
    user = users_db.get(data.get("username"))
    if not user:
        logger.warning("Login failed: user not found")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    hashed = hashlib.sha256(data.get("password").encode()).hexdigest()
    if hashed != user["password"]:
        logger.warning("Login failed: wrong password")
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({
        "sub": user["username"],
        "role": user["role"]
    })

    logger.info(f"Login success: {user['username']}")
    return {
        "access_token": token,
        "token_type": "bearer"
    }

# ---------- CURRENT USER ----------
@app.get("/me")
def current_user(user=Depends(verify_token)):
    return {
        "username": user["sub"],
        "role": user["role"]
    }

# ---------- DETECT ----------
@app.get("/detect")
def detect_threats(user=Depends(verify_token)):
    packets = generate_packets()
    predictions = detect(model, packets)
    responses = evaluate_and_respond(packets, predictions)

    results = []

    for i in range(len(responses)):
        policy_action = enforce_policy(user["role"], packets[i])

        results.append({
            "packet": responses[i]["packet"],
            "prediction": responses[i]["prediction"],
            "action": responses[i]["action"],
            "policy": policy_action
        })

    logger.info(
        f"Detection run by {user['sub']} | "
        f"Role={user['role']} | Packets={len(results)}"
    )

    return {
        "count": len(results),
        "results": results,
        "timestamp": datetime.utcnow()
    }
