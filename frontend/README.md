Industrial Automation Dashboard (Frontend)

Overview
- React + Vite + TypeScript frontend for the Industrial Automation Dashboard exercise
- Connects to the provided FastAPI mock backend in api/
- Implements site selection, asset overview, real-time charts, storage alerts, and asset editing (PATCH)

Features mapped to the assignment
- Site selection: Home page and top-right selector on the dashboard
- Data visualization: Recharts time-series for
  - Heat production: actual vs planned per production asset
  - Storage: charge/discharge bars and state-of-charge area
  - Electricity prices: last 24h line chart
  - Network consumption: actual last 24h and forecast next 5 days
- Storage level alerts: visible on storage assets with thresholds (<=10% danger, >=90% warning)
- Asset management: edit asset name, capacity, efficiency, and cost_per_mwh via PATCH /assets/{id}. UI updates via React Query cache invalidation
- Best practices: React Query for async/data caching, loading/error states, modular hooks, simple responsive layout

Project structure
- src/
  - api/
    - client.ts: Axios instance with base URL
    - types.ts: TypeScript models aligning with API schemas
    - hooks.ts: React Query hooks for all endpoints
  - components/
    - AssetCard.tsx, AssetEditor.tsx, StorageAlert.tsx, SiteSelector.tsx
    - charts/TimeSeries.tsx: thin wrappers around Recharts charts
  - pages/
    - Home.tsx: site selection
    - SiteDashboard.tsx: the main dashboard per site
  - App.tsx: routes
  - main.tsx, index.css

Prerequisites
- Node.js 18+
- Running FastAPI backend from api/

Backend setup
Option A: Docker Compose
- cd api
- docker-compose up -d
- API: http://localhost:8000 (Swagger UI: /docs)

Option B: Local Python
- cd api
- python -m venv .venv && source .venv/bin/activate
- pip install -r requirements.txt
- python run.py
- API at http://localhost:8000

Frontend setup
- cd projects/home-assigment
- cp .env.example .env.local  # adjust VITE_API_BASE_URL if needed
- npm install
- npm run dev
- Open http://localhost:5173

Notes
- The FastAPI app already enables CORS for all origins, so no proxy is required
- If you change the API base URL, update VITE_API_BASE_URL in .env.local
- Current production and storage state are polled periodically (15–30s) to demonstrate "real-time" updates

Key endpoints used
- GET /sites, GET /sites/{site_id}
- GET /assets (with optional site_id)
- PATCH /assets/{asset_id}
- Production: GET /assets/{asset_id}/heat-production/{current|historical|planned}
- Storage: GET /assets/{asset_id}/storage/{charge-discharge|charge-discharge/planned|state|state/historical}
- Prices: GET /electricity-prices
- Consumption: GET /assets/{asset_id}/heat-consumption and /heat-consumption/forecast

Design choices
- React Query centralizes data fetching, caching and invalidation
- Recharts provides simple, responsive time-series charts
- Minimal CSS for a clean dark UI without a component library
- Type-safe models mirroring the API

Assumptions
- The simulated backend schemas are stable and served at localhost:8000 by default
- Asset PATCH supports partial updates as documented in api/models.py (name, capacity, efficiency, cost_per_mwh)

License
- For recruiting assignment use
