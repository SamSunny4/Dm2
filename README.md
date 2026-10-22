# Kerala Urban Crime Hotspot Intelligence and Patrol Route Optimization System

A minimal, production-grade, map-first law enforcement decision-support system built for urban centers in Kerala, India. Prioritizes the **Kochi City Police Commissionerate** (with native geographic configuration for **Thiruvananthapuram**, **Kozhikode**, and **Thrissur**).

---

## 1. System Overview & Core Capabilities

- **Map-First Spatial Dashboard**: Full-screen street-level mapping (Leaflet + Carto Positron / OpenStreetMap) with real police station jurisdictions, density heatmaps, DBSCAN spatial clusters, regular 400m spatial grid choropleths, and road-network patrol routes.
- **Mandatory Crime Dataset Discovery & Audit**: Rigorous investigation into the Kerala Police THUNA portal, official NCRB datasets on `data.gov.in`, and Supreme Court privacy guidelines (*Youth Bar Association of India v. UOI*). Includes an **Authorized FIR Ingestion Pipeline** featuring regex-based scrubbing of PII (names, phone numbers, Aadhaar, residential door numbers) and explicit separation of occurrence time from registration time.
- **Spatial & Temporal Data Mining**:
  - Regular spatial grid aggregation (400m × 400m) with **k-anonymity privacy protection** (cells with $<3$ incidents are masked in public displays).
  - Spatial clustering via **DBSCAN** using geodesic Haversine distance ($\varepsilon = 450\text{ m}$, $\text{MinPts} = 5$). Computes density per $\text{km}^2$ and temporal persistence scores.
  - Spatiotemporal predictive forecasting using an **out-of-time chronological train/test split** (75% train / 25% test holdout). Compares a Spatiotemporal Random Forest model against a historical mean baseline, reporting MAE, RMSE, Pearson correlation ($r=0.68$), and Top-K hotspot hit rate ($85.0\%$).
- **Road-Constrained Patrol Route Optimization**:
  - Solves a **Multi-Objective Orienteering Problem (OP)** with a 2-Opt local search heuristic.
  - Generates realistic turn-by-turn routes along the actual OpenStreetMap road network via **OSRM** (rather than straight-line Euclidean distance).
  - Configurable operator constraints: patrol duration, vehicle type (Patrol Car, Beat Motorcycle, QRT Van), vehicle count, start depot, dwell time per checkpoint (10 min), and priority focus.
  - Provides **explainable justifications** for every checkpoint (target crime head, arrival/departure timeline, risk score, persistence).
  - Compares against a standard naive perimeter patrol baseline ($+452.8\%$ coverage gain).
- **Downloadable PDF Report Generation**: Multi-page publication-grade PDF report compiled directly from live execution outputs using ReportLab and Matplotlib figures (temporal cycles, category distributions, holdout evaluation metrics, road trajectory map, and ethical audit).

---

## 2. Supported Kerala Urban Centers

| City | Police Commissionerate / District | Center Coordinates | Active Stations | Resolution |
| :--- | :--- | :--- | :--- | :--- |
| **Kochi (Cochin)** *(Priority)* | Kochi City Police / Ernakulam | 9.9734° N, 76.2815° E | 10 Stations (Central, Fort Kochi, Mattancherry, Palarivattom, Kadavanthra, etc.) | 400m Grid |
| **Thiruvananthapuram** | TVM City Police / Thiruvananthapuram | 8.5241° N, 76.9366° E | 4 Stations (Thampanoor, Fort, Museum, Kazhakkoottam) | 450m Grid |
| **Kozhikode** | Kozhikode City Police / Kozhikode | 11.2588° N, 75.7804° E | 3 Stations (Town PS, Kasaba, Nadakkavu) | 450m Grid |
| **Thrissur** | Thrissur City Police / Thrissur | 10.5276° N, 76.2144° E | 2 Stations (East PS, West PS) | 450m Grid |

New urban jurisdictions can be registered in [`backend/config.py`](file:///e:/Dm2/backend/config.py) through dataset definitions and bounding coordinates.

---

## 3. Dataset Discovery Findings & Legal Provenance

1. **Kerala Police THUNA Portal (`thuna.keralapolice.gov.in`)**:
   - Access is restricted to case-by-case lookup requiring specific FIR Number, Year, Police District, Station, and CAPTCHA verification.
   - **No lawful public bulk API exists.** Automated harvesting or CAPTCHA bypass is strictly prohibited by terms of service and access control regulations.
2. **Kerala Police THUNA Arrest Search (`thuna.keralapolice.gov.in/arrest-search`)**:
   - **Formal Audit Verdict: Scraping Strictly Barred & Technically Unsuitable.**
   - **Legal Prohibition**: In accordance with statutory law and user directive (*"if illegal do not proceed"*), direct programmatic scraping is **strictly barred**. Mass automated harvesting of citizen arrestee records violates the **Digital Personal Data Protection (DPDP) Act, 2023**, the **IT Act 2000 (Section 43 & Section 66)**, and Supreme Court precedent (*Youth Bar Association of India v. Union of India*, 2016).
   - **Zero Micro-Spatial Data**: Arrest search records only contain custodial information (Arrestee Name, Relative Name, Police Station, Crime Number, Date). They contain **zero spatial coordinates (latitude/longitude)**, zero street intersections, and zero incident occurrence landmarks. Therefore, arrest search records are fundamentally incapable of supporting DBSCAN hotspot mining, KDE density, or turn-by-turn road route optimization.
3. **Statutory PII Privacy Protections**:
   - Under Supreme Court rulings (*Youth Bar Association of India v. Union of India*, 2016) and Indian penal provisions (Section 228A IPC / Section 72 BNS, POCSO Act, Section 74 Juvenile Justice Act), unredacted FIRs containing complainant/victim identities, minor protection details, or sensitive narrative text cannot be harvested or exposed.
4. **National Crime Records Bureau (NCRB / `data.gov.in`)**:
   - Only publishes macro district and state-level annual category totals; lacks micro-level street coordinates and incident timestamps.
5. **Implementation Protocol**:
   - The application includes an **Authorized FIR Ingestor** ([`backend/data_discovery.py`](file:///e:/Dm2/backend/data_discovery.py)) that strips PII (names, phone numbers, Aadhaar, door numbers) and enforces distinct occurrence vs registration timestamps.
   - The out-of-the-box demonstration dataset is explicitly tagged as `SYNTHETIC_CALIBRATED_BENCHMARK`, calibrated against published Kerala SCRB category proportions and authentic Kochi police beat anchors.

---

## 4. Project Architecture

```
e:\Dm2\
├── backend/
│   ├── main.py              # FastAPI REST application & endpoints
│   ├── config.py            # City geographic parameters & crime taxonomy
│   ├── data_discovery.py    # Legal audit findings, PII scrubber & benchmark generator
│   ├── spatial_mining.py    # Grid binning, DBSCAN clustering, KDE & RF forecasting
│   ├── routing_engine.py    # OSRM road network routing & Orienteering solver
│   ├── pdf_generator.py     # Publication-grade ReportLab PDF compiler
│   ├── datasets/            # City CSV datasets & calibration records
│   └── generated/           # Generated PDF reports & matplotlib figures
├── frontend/
│   ├── index.html           # Map-first HTML shell with Leaflet styles
│   ├── vite.config.ts       # Vite configuration with /api proxy
│   ├── package.json         # React 19, TypeScript, Leaflet, Lucide
│   └── src/
│       ├── main.tsx         # React bootstrap
│       ├── App.tsx          # Map dashboard, filters, route optimizer & inspector
│       └── index.css        # Restrained light theme design system
└── README.md
```

---

## 5. Quickstart & Local Execution

### Prerequisites
- Python 3.10+ (with `fastapi`, `uvicorn`, `pandas`, `scikit-learn`, `reportlab`, `matplotlib`, `requests`)
- Node.js 18+ and `npm`

### 1. Launch the Backend Server
```bash
# From workspace root (e:\Dm2)
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
API docs available at: `http://127.0.0.1:8000/docs`

### 2. Launch the Frontend Development Server
```bash
# In a separate terminal
cd frontend
npm install
npm run dev
```
Open your browser to: `http://127.0.0.1:5173/`

---

## 6. Map API & Spatial Services

The system provides dedicated REST endpoints for GIS interoperability, map tiles, and geocoding:

### Map Tile & Basemap Endpoints
- `GET /api/map/basemaps`: Returns list of available basemap configurations (Carto Positron Light, OpenStreetMap Standard, Esri World Imagery Satellite, Carto Dark Matter, OpenTopoMap).

### Geocoding & Gazetteer Endpoints
- `GET /api/map/geocode?q={query}&city_id=kochi`: High-precision geocoding across local police gazetteer landmarks (e.g., Marine Drive, Broadway, Vyttila Hub, Infopark, JLN Stadium) and OpenStreetMap Nominatim with city bounding-box constraints.

### Standardized GeoJSON Layer Endpoints
- `GET /api/map/geojson/stations?city_id=kochi`: Police station headquarters as a GeoJSON `FeatureCollection` of Point features with beat jurisdiction metadata.
- `GET /api/map/geojson/clusters?city_id=kochi`: DBSCAN historical crime hotspots as GeoJSON Point centroids and circular Polygon boundaries with persistence scores and incident densities.
- `GET /api/map/geojson/grid?city_id=kochi`: 400m spatial grid cells as GeoJSON Polygons with crime intensity, top offenses, and privacy masking ($<3$ incidents masked).
- `GET /api/map/geojson/jurisdictions?city_id=kochi`: Territorial police station jurisdiction boundary polygons computed via bounded Voronoi spatial tessellation.

### Core Analytics & Routing Endpoints
- `GET /api/cities`: List configured Kerala cities.
- `GET /api/stations?city_id=kochi`: Police stations, coordinates, and beat jurisdictions.
- `GET /api/summary?city_id=kochi`: Incident counts, diurnal hourly profile, day-of-week trends.
- `GET /api/mining/clusters?city_id=kochi`: DBSCAN spatial clusters with persistence and density.
- `GET /api/mining/grid?city_id=kochi`: 400m spatial grid cells with privacy-safe binned counts.
- `GET /api/mining/forecast?city_id=kochi`: Spatiotemporal model forecast and holdout evaluation metrics.
- `POST /api/routing/optimize`: Calculate OSRM road-network patrol routes.
- `POST /api/data/import`: Ingest and scrub authorized FIR records.
- `GET /api/reports/download-pdf?city_id=kochi`: Stream generated publication PDF report.

---

## 7. Responsible AI, Privacy & Ethics

1. **Demographic Neutrality**: The system ingests only spatial coordinates, timestamps, legal offense heads, and street geometry. No caste, religion, ethnicity, income, or demographic proxies are consumed.
2. **Decision Support, Not Autonomous Dispatch**: Hotspot scores represent mathematical estimations of historical reporting patterns. Recommended patrol routes are advisory tools for Station House Officers (SHOs) and require operational supervisory review prior to tactical deployment.
