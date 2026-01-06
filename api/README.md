# Industrial Automation Dashboard API

Mock REST API for the industrial automation dashboard frontend exercise. This API provides simulated data for industrial assets, heat production, electricity prices, and consumption forecasts.

## Overview

This FastAPI application serves as a backend simulation that provides:
- Industrial sites (collections of assets at one location)
- Industrial asset information (boilers, heat storage, district heating networks)
- Real-time and historical heat production data per asset
- Electricity prices in 15-minute resolution
- Simulated heat consumption data per asset
- Forecasted heat consumption per asset (5 days ahead)

## Prerequisites
- Python 3.8 or higher (for local development)
- pip (for local development)
- Docker and Docker Compose (for containerized deployment)

## Running the API

### Using Docker

**Docker Compose (from api directory):**
```bash
docker-compose up
# Or in detached mode:
docker-compose up -d
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive API Documentation (Swagger UI)**: http://localhost:8000/docs
- **Alternative API Documentation (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json
