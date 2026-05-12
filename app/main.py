from fastapi import FastAPI
from app.config import APP_NAME, ENVIRONMENT

app = FastAPI(title = APP_NAME)

@app.get("/")
def root():
	return {
	"message":"Backend Running",
	"environment":ENVIRONMENT
	}

@app.get("/health")
def health_check():
	return {
	"status":"healthy"
	}