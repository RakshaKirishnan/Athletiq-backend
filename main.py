from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import athlete, metrics, training, analytics, comparison, auth
from app.routers.analytics import platform_router as analytics_platform_router

app = FastAPI(title="Athletiq API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(athlete.router)
app.include_router(metrics.router)
app.include_router(training.router)
app.include_router(analytics.router)
app.include_router(analytics_platform_router)
app.include_router(comparison.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
