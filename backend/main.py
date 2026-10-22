"""
FastAPI Backend Application
Kerala Urban Crime Hotspot Intelligence and Patrol Route Optimization System
"""

import os
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, Query, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import pandas as pd

from backend.config import CITIES_CONFIG, CRIME_CATEGORIES
from backend.data_discovery import (
    DATA_DISCOVERY_INVESTIGATION, AuthorizedFIRIngestor, get_or_create_city_dataset
)
from backend.spatial_mining import SpatialMiningEngine
from backend.routing_engine import PatrolOptimizer
from backend.pdf_generator import build_pdf_report
from backend.map_api import MapAPIService

app = FastAPI(
    title="Kerala Urban Crime Intelligence API",
    description="Micro-spatial crime hotspot mining and road-constrained patrol route optimization",
    version="1.0.0"
)

# Enable CORS for frontend Vite dev server (typically localhost:5173 or any port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cached engine instances per city
engines: Dict[str, SpatialMiningEngine] = {}
optimizers: Dict[str, PatrolOptimizer] = {}

def get_engine(city_id: str) -> SpatialMiningEngine:
    if city_id not in engines:
        engines[city_id] = SpatialMiningEngine(city_id)
    return engines[city_id]

def get_optimizer(city_id: str) -> PatrolOptimizer:
    if city_id not in optimizers:
        optimizers[city_id] = PatrolOptimizer(city_id)
    return optimizers[city_id]


# Pydantic models for request bodies
class OptimizeRequest(BaseModel):
    city_id: str = "kochi"
    start_station_id: str = "ekm_central"
    patrol_duration_minutes: int = 180
    num_vehicles: int = 1
    vehicle_type: str = "Patrol Car"
    priority_focus: str = "balanced"  # "balanced", "high_intensity_focused", "broad_coverage"
    dwell_time_minutes: int = 10
    return_to_start: bool = True


class FIRImportRecord(BaseModel):
    city_id: str = "kochi"
    police_station_id: str = "ekm_central"
    fir_number: Optional[str] = None
    crime_category: str = "THEFT_SNATCHING"
    registration_time: str
    occurrence_time: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    locality_name: Optional[str] = None
    raw_narrative: Optional[str] = None


# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------

@app.get("/api/cities")
def get_cities():
    """Returns list of configured Kerala urban centers."""
    result = []
    for cid, cdata in CITIES_CONFIG.items():
        result.append({
            "id": cid,
            "name": cdata["name"],
            "state": cdata["state"],
            "district": cdata["district"],
            "center": cdata["center"],
            "default_zoom": cdata["default_zoom"],
            "bounds": cdata["bounds"],
            "num_stations": len(cdata["police_stations"])
        })
    return result


@app.get("/api/stations")
def get_stations(city_id: str = Query("kochi")):
    """Returns police stations and jurisdiction details for a city."""
    city_cfg = CITIES_CONFIG.get(city_id)
    if not city_cfg:
        raise HTTPException(status_code=404, detail="City configuration not found")
    return {
        "city_id": city_id,
        "stations": city_cfg["police_stations"]
    }


@app.get("/api/categories")
def get_categories():
    """Returns crime classification taxonomy and IPC/BNS mappings."""
    return CRIME_CATEGORIES


def _filter_dataframe(
    df: pd.DataFrame,
    station_id: Optional[str] = None,
    category: Optional[str] = None,
    time_of_day: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> pd.DataFrame:
    """Applies operator filters to dataframe."""
    filtered = df.copy()
    if station_id and station_id != "all":
        filtered = filtered[filtered["police_station_id"] == station_id]
    if category and category != "all":
        filtered = filtered[filtered["crime_category"] == category]
    if time_of_day and time_of_day != "all":
        # Morning (06-12), Afternoon (12-17), Evening (17-22), Night (22-06)
        valid_h = filtered["hour_of_day"].dropna()
        if time_of_day == "morning":
            filtered = filtered[filtered["hour_of_day"].between(6, 11)]
        elif time_of_day == "afternoon":
            filtered = filtered[filtered["hour_of_day"].between(12, 16)]
        elif time_of_day == "evening":
            filtered = filtered[filtered["hour_of_day"].between(17, 21)]
        elif time_of_day == "night":
            filtered = filtered[(filtered["hour_of_day"] >= 22) | (filtered["hour_of_day"] <= 5)]
            
    if start_date:
        filtered = filtered[filtered["registration_time"] >= pd.to_datetime(start_date)]
    if end_date:
        filtered = filtered[filtered["registration_time"] <= pd.to_datetime(end_date)]
        
    return filtered


@app.get("/api/summary")
def get_summary(
    city_id: str = Query("kochi"),
    station_id: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    time_of_day: Optional[str] = Query(None),
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None)
):
    """Returns analytics summary statistics, diurnal trend, and category distributions."""
    engine = get_engine(city_id)
    df = engine.get_clean_data()
    filtered_df = _filter_dataframe(df, station_id, category, time_of_day, start_date, end_date)
    summary = engine.get_summary_statistics(filtered_df)
    return summary


@app.get("/api/mining/clusters")
def get_clusters(
    city_id: str = Query("kochi"),
    eps_km: float = Query(0.45),
    min_samples: int = Query(5),
    station_id: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    time_of_day: Optional[str] = Query(None)
):
    """Returns DBSCAN spatial clusters with persistence and density metrics."""
    engine = get_engine(city_id)
    df = engine.get_clean_data()
    filtered_df = _filter_dataframe(df, station_id, category, time_of_day)
    clusters = engine.compute_dbscan_clusters(eps_km, min_samples, filtered_df)
    return {
        "city_id": city_id,
        "num_clusters": len(clusters),
        "clusters": clusters
    }


@app.get("/api/mining/grid")
def get_grid(
    city_id: str = Query("kochi"),
    station_id: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    time_of_day: Optional[str] = Query(None)
):
    """Returns regular spatial grid cells with privacy-safe binned counts and statistics."""
    engine = get_engine(city_id)
    df = engine.get_clean_data()
    filtered_df = _filter_dataframe(df, station_id, category, time_of_day)
    cells = engine.build_spatial_grid(filtered_df)
    # Filter to non-empty cells to optimize payload
    active_cells = [c for c in cells if c["incident_count"] > 0]
    return {
        "city_id": city_id,
        "resolution_km": engine.res_km,
        "num_active_cells": len(active_cells),
        "cells": active_cells
    }


@app.get("/api/mining/forecast")
def get_forecast(city_id: str = Query("kochi")):
    """Returns predictive spatiotemporal forecast and chronological holdout evaluation metrics."""
    engine = get_engine(city_id)
    forecast = engine.run_spatiotemporal_forecast()
    return forecast


@app.post("/api/routing/optimize")
def optimize_patrol_route(req: OptimizeRequest):
    """Calculates road-network constrained patrol routes using Orienteering optimization."""
    optimizer = get_optimizer(req.city_id)
    result = optimizer.optimize_patrol(
        start_station_id=req.start_station_id,
        patrol_duration_minutes=req.patrol_duration_minutes,
        num_vehicles=req.num_vehicles,
        vehicle_type=req.vehicle_type,
        priority_focus=req.priority_focus,
        dwell_time_minutes=req.dwell_time_minutes,
        return_to_start=req.return_to_start
    )
    return result


@app.get("/api/provenance/audit")
def get_provenance_audit():
    """Returns statutory legal compliance declarations and empirical audit findings."""
    return DATA_DISCOVERY_INVESTIGATION


@app.post("/api/data/import")
def import_fir_record(record: FIRImportRecord):
    """
    Ingests an authorized FIR record, scrubs PII, enforces distinct occurrence vs
    registration timestamps, and integrates into the active dataset.
    """
    engine = get_engine(record.city_id)
    raw_dict = {
        "police_station_id": record.police_station_id,
        "fir_number": record.fir_number or "IMP-FIR-AUTHORIZED",
        "crime_category": record.crime_category,
        "registration_time": record.registration_time,
        "occurrence_time": record.occurrence_time,
        "latitude": record.latitude,
        "longitude": record.longitude,
        "locality_name": record.locality_name,
        "notes": record.raw_narrative
    }
    sanitized = AuthorizedFIRIngestor.process_imported_record(raw_dict, city_id=record.city_id)
    
    # Append to current dataset
    df = engine.get_clean_data()
    sanitized_row = {
        "record_id": sanitized["record_id"],
        "city_id": sanitized["city_id"],
        "fir_number": sanitized["fir_number"],
        "police_station_id": sanitized["police_station_id"],
        "police_station_name": sanitized["police_station_name"],
        "police_station_code": "IMP-CODE",
        "crime_category": sanitized["crime_category"],
        "crime_label": CRIME_CATEGORIES[sanitized["crime_category"]]["label"],
        "ipc_bns_section": sanitized["ipc_bns_section"],
        "severity_weight": sanitized["severity_weight"],
        "registration_time": sanitized["registration_time"],
        "occurrence_time": sanitized["occurrence_time"],
        "occurrence_time_unknown": sanitized["occurrence_time_unknown"],
        "hour_of_day": pd.to_datetime(sanitized["occurrence_time"]).hour if sanitized["occurrence_time"] else None,
        "day_of_week": pd.to_datetime(sanitized["registration_time"]).strftime("%A"),
        "month": pd.to_datetime(sanitized["registration_time"]).strftime("%B"),
        "latitude": sanitized["latitude"],
        "longitude": sanitized["longitude"],
        "locality_name": sanitized["locality_name"],
        "sanitized_notes": sanitized["sanitized_notes"],
        "provenance": sanitized["provenance"],
        "is_synthetic": False
    }
    
    new_df = pd.concat([df, pd.DataFrame([sanitized_row])], ignore_index=True)
    engine._df = new_df
    
    return {
        "status": "success",
        "message": "FIR Record ingested successfully. Personally identifiable information was scrubbed.",
        "sanitized_record": sanitized
    }


@app.get("/api/reports/download-pdf")
def download_pdf_report(city_id: str = Query("kochi")):
    """Generates and serves the publication-grade analytical PDF report."""
    try:
        pdf_path = build_pdf_report(city_id)
        if not os.path.exists(pdf_path):
            raise HTTPException(status_code=500, detail="PDF generation failed")
        
        return FileResponse(
            path=pdf_path,
            filename=f"Kerala_Urban_Crime_Intelligence_{city_id.upper()}.pdf",
            media_type="application/pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error compiling PDF: {str(e)}")


# ---------------------------------------------------------------------------
# Map API Endpoints (GeoJSON Layers, Geocoding, Basemaps)
# ---------------------------------------------------------------------------

@app.get("/api/map/basemaps")
def get_map_basemaps():
    """Returns available basemap tile styles."""
    return MapAPIService.get_basemaps()


@app.get("/api/map/geocode")
def geocode_map_location(q: str = Query(..., min_length=2), city_id: str = Query("kochi")):
    """Geocodes a street or landmark query with bounding box constraints."""
    return MapAPIService.geocode_location(q, city_id)


@app.get("/api/map/geojson/stations")
def get_stations_geojson_layer(city_id: str = Query("kochi")):
    """Returns police stations as a standardized GeoJSON FeatureCollection."""
    return MapAPIService.get_stations_geojson(city_id)


@app.get("/api/map/geojson/clusters")
def get_clusters_geojson_layer(city_id: str = Query("kochi")):
    """Returns DBSCAN hotspot clusters as a GeoJSON FeatureCollection."""
    return MapAPIService.get_clusters_geojson(city_id)


@app.get("/api/map/geojson/grid")
def get_grid_geojson_layer(city_id: str = Query("kochi")):
    """Returns spatial grid cells as GeoJSON Polygons with crime intensity."""
    return MapAPIService.get_grid_geojson(city_id)


@app.get("/api/map/geojson/jurisdictions")
def get_jurisdictions_geojson_layer(city_id: str = Query("kochi")):
    """Returns police station territorial jurisdiction boundary polygons."""
    return MapAPIService.get_jurisdictions_geojson(city_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
