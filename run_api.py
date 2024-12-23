import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.api.main:fast_app",
        host="localhost",
        port=8000,
        log_level="info",
        reload=True,
    )
