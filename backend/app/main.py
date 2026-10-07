import time
from collections import defaultdict, deque
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import Base, engine
from app.api import auth, campaigns, dashboard, admin

Base.metadata.create_all(bind=engine)
app=FastAPI(title="PhishLens 2.0 API",version=settings.version,description="Defensive security-awareness simulation and behavioral risk intelligence API")
app.add_middleware(CORSMiddleware,allow_origins=list(settings.cors_origins),allow_credentials=True,allow_methods=["*"],allow_headers=["*"])

# Lightweight development rate limiter. Production deployments should use a shared store at the reverse-proxy/API-gateway layer.
_rate_windows = defaultdict(deque)
_RATE_LIMIT = 120
_RATE_PERIOD = 60

@app.middleware("http")
async def rate_limit(request: Request, call_next):
    if request.url.path in {"/health", "/docs", "/openapi.json"}:
        return await call_next(request)
    ip = request.client.host if request.client else "unknown"
    now = time.time()
    q = _rate_windows[ip]
    while q and now - q[0] > _RATE_PERIOD:
        q.popleft()
    if len(q) >= _RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Rate limit exceeded; try again later")
    q.append(now)
    return await call_next(request)
app.include_router(auth.router); app.include_router(campaigns.router); app.include_router(dashboard.router); app.include_router(admin.router)

@app.get("/health")
def health(): return {"status":"ok","service":settings.app_name,"version":settings.version}
