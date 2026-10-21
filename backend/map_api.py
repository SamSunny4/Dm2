"""
Map API & Geospatial Service Layer
Provides:
- Standardized GeoJSON endpoints (Stations, Hotspots, Spatial Grid Cells, Station Jurisdictions)
- High-precision local gazetteer and OSM Nominatim geocoding API
- Multi-basemap registry (Carto Light, OSM, Esri Satellite, Carto Dark, OpenTopoMap)
- Custom Mapbox / Google Maps / MapTiler API configuration integration
"""

import math
import requests
from typing import Dict, List, Any, Optional
import numpy as np
from scipy.spatial import Voronoi

from backend.config import CITIES_CONFIG, CRIME_CATEGORIES
from backend.spatial_mining import SpatialMiningEngine

BASEMAP_PROVIDERS = [
    {
        "id": "osm_standard",
        "name": "OpenStreetMap Standard",
        "type": "raster",
        "url": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        "attribution": "&copy; <a href='https://openstreetmap.org/copyright'>OpenStreetMap</a> contributors",
        "max_zoom": 19,
        "is_default": True
    },
    {
        "id": "carto_light",
        "name": "Carto Positron (Light)",
        "type": "raster",
        "url": "https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        "attribution": "&copy; <a href='https://openstreetmap.org'>OpenStreetMap</a> &copy; <a href='https://carto.com/'>CARTO</a>",
        "max_zoom": 19,
        "is_default": False
    },
    {
        "id": "esri_satellite",
        "name": "Esri World Imagery (Satellite)",
        "type": "raster",
        "url": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        "attribution": "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community",
        "max_zoom": 18,
        "is_default": False
    },
    {
        "id": "carto_dark",
        "name": "Carto Dark Matter (Night)",
        "type": "raster",
        "url": "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        "attribution": "&copy; <a href='https://openstreetmap.org'>OpenStreetMap</a> &copy; <a href='https://carto.com/'>CARTO</a>",
        "max_zoom": 19,
        "is_default": False
    },
    {
        "id": "opentopomap",
        "name": "OpenTopoMap (Topographic)",
        "type": "raster",
        "url": "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
        "attribution": "Kartendaten: &copy; <a href='https://openstreetmap.org/copyright'>OpenStreetMap</a>-Mitwirkende, SRTM | Kartendarstellung: &copy; <a href='http://opentopomap.org'>OpenTopoMap</a>",
        "max_zoom": 17,
        "is_default": False
    }
]

# Local gazetteer anchors for instant offline geocoding
LOCAL_GAZETTEER = {
    "kochi": [
        {"name": "Broadway Commercial Strip", "category": "Commercial Hub", "lat": 9.9760, "lon": 76.2805, "station": "Central PS"},
        {"name": "Marine Drive Promenade", "category": "Public Walkway", "lat": 9.9805, "lon": 76.2755, "station": "Central PS"},
        {"name": "MG Road Shenoys Junction", "category": "Transit / Commercial", "lat": 9.9720, "lon": 76.2825, "station": "Central PS"},
        {"name": "High Court of Kerala", "category": "Judicial Complex", "lat": 9.9830, "lon": 76.2770, "station": "Central PS"},
        {"name": "Ernakulam South Railway Station (Junction)", "category": "Railway Terminal", "lat": 9.9675, "lon": 76.2890, "station": "Town South PS"},
        {"name": "Ernakulam North Railway Station (Town)", "category": "Railway Terminal", "lat": 9.9920, "lon": 76.2885, "station": "Central PS"},
        {"name": "Vyttila Mobility Hub", "category": "Multi-Modal Transit Terminal", "lat": 9.9670, "lon": 76.3210, "station": "Kadavanthra PS"},
        {"name": "Jawaharlal Nehru International Stadium (Kaloor)", "category": "Sports & Public Events", "lat": 9.9985, "lon": 76.3010, "station": "Palarivattom PS"},
        {"name": "Palarivattom Bypass Junction", "category": "Highway Interchange", "lat": 10.0045, "lon": 76.3080, "station": "Palarivattom PS"},
        {"name": "Fort Kochi Chinese Fishing Nets & Beach", "category": "Tourism & Coastal Precinct", "lat": 9.9680, "lon": 76.2415, "station": "Fort Kochi PS"},
        {"name": "Mattancherry Jew Town & Synagogue", "category": "Heritage Zone", "lat": 9.9575, "lon": 76.2595, "station": "Mattancherry PS"},
        {"name": "Infopark Phase 1 & 2 (Kakkanad)", "category": "IT / Technology Park", "lat": 10.0125, "lon": 76.3620, "station": "Infopark PS"},
        {"name": "SmartCity Kochi", "category": "Technology Park", "lat": 10.0070, "lon": 76.3690, "station": "Infopark PS"},
        {"name": "Ernakulam District Collectorate (Civil Station)", "category": "Government Center", "lat": 10.0345, "lon": 76.3360, "station": "Thrikkakara PS"},
        {"name": "Cochin University of Science and Technology (CUSAT)", "category": "University Campus", "lat": 10.0410, "lon": 76.3265, "station": "Kalamassery PS"},
        {"name": "Kalamassery Premier Junction (NH 66)", "category": "Industrial Highway Corridor", "lat": 10.0530, "lon": 76.3210, "station": "Kalamassery PS"},
        {"name": "Kadavanthra Junction & Metro Station", "category": "Metro Station & Junction", "lat": 9.9685, "lon": 76.2990, "station": "Kadavanthra PS"},
        {"name": "Nettoor Vegetable Market (Panangad)", "category": "Wholesale Market", "lat": 9.9140, "lon": 76.3120, "station": "Panangad PS"},
        {"name": "Hill Palace Museum (Tripunithura)", "category": "Heritage / Royal Precinct", "lat": 9.9525, "lon": 76.3533, "station": "Hill Palace PS"}
    ],
    "thiruvananthapuram": [
        {"name": "Thampanoor Central Bus Station & Railway Terminal", "category": "Transit Hub", "lat": 8.4892, "lon": 76.9504, "station": "Thampanoor PS"},
        {"name": "East Fort & Sree Padmanabhaswamy Temple", "category": "Heritage Precinct", "lat": 8.4825, "lon": 76.9442, "station": "Fort PS"},
        {"name": "Technopark Campus (Kazhakkoottam)", "category": "IT Corridor", "lat": 8.5684, "lon": 76.8722, "station": "Kazhakkoottam PS"},
        {"name": "Museum & Zoo Compound", "category": "Public Park", "lat": 8.5133, "lon": 76.9567, "station": "Museum PS"}
    ],
    "kozhikode": [
        {"name": "SM Street (Sweet Meat Street)", "category": "Commercial Pedestrian Strip", "lat": 11.2562, "lon": 75.7767, "station": "Town PS"},
        {"name": "Mananchira Square", "category": "Public Park / Historic Pond", "lat": 11.2520, "lon": 75.7795, "station": "Town PS"},
        {"name": "Moffusil Bus Stand (Rajaji Road)", "category": "Transit Hub", "lat": 11.2514, "lon": 75.7925, "station": "Kasaba PS"},
        {"name": "Kozhikode Beach Promenade", "category": "Coastal Public Promenade", "lat": 11.2610, "lon": 75.7680, "station": "Nadakkavu PS"}
    ],
    "thrissur": [
        {"name": "Thekkinkadu Maidan & Swaraj Round", "category": "Civic Round & Temple Grounds", "lat": 10.5244, "lon": 76.2144, "station": "East PS"},
        {"name": "Shakthan Thampuran Bus Stand", "category": "Bus Terminal", "lat": 10.5180, "lon": 76.2195, "station": "East PS"},
        {"name": "Thrissur Railway Station", "category": "Railway Station", "lat": 10.5175, "lon": 76.2085, "station": "West PS"}
    ]
}


class MapAPIService:
    """Provides GeoJSON layers, geocoding, and map metadata services."""
    
    @staticmethod
    def get_basemaps() -> List[Dict[str, Any]]:
        """Returns supported basemap tile layer configurations."""
        return BASEMAP_PROVIDERS

    @staticmethod
    def geocode_location(query: str, city_id: str = "kochi") -> List[Dict[str, Any]]:
        """
        Geocodes a street or landmark query. Checks local gazetteer first,
        then queries OpenStreetMap Nominatim with bounding box constraint.
        """
        query_norm = query.strip().lower()
        if not query_norm:
            return []

        results = []
        # 1. Match local gazetteer
        gaz = LOCAL_GAZETTEER.get(city_id, [])
        for item in gaz:
            if query_norm in item["name"].lower() or any(w in item["name"].lower() for w in query_norm.split()):
                results.append({
                    "name": item["name"],
                    "display_name": f"{item['name']} ({item['category']}), {item['station']}",
                    "latitude": item["lat"],
                    "longitude": item["lon"],
                    "type": item["category"],
                    "source": "Local Police Gazetteer",
                    "police_station": item["station"]
                })

        # 2. Query OSM Nominatim if query is longer and local matches are few
        if len(results) < 3:
            city_cfg = CITIES_CONFIG.get(city_id, CITIES_CONFIG["kochi"])
            b = city_cfg["bounds"]
            # Nominatim viewbox format: min_lon,max_lat,max_lon,min_lat (left,top,right,bottom)
            viewbox_str = f"{b['min_lon']},{b['max_lat']},{b['max_lon']},{b['min_lat']}"
            
            try:
                headers = {"User-Agent": "KeralaPoliceUrbanHotspotSystem/1.0 (internal-demo)"}
                params = {
                    "q": f"{query}, {city_cfg['name']}, Kerala",
                    "format": "json",
                    "limit": 5,
                    "viewbox": viewbox_str,
                    "bounded": 1
                }
                resp = requests.get("https://nominatim.openstreetmap.org/search", params=params, headers=headers, timeout=3.0)
                if resp.status_code == 200:
                    data = resp.json()
                    for d in data:
                        lat = float(d["lat"])
                        lon = float(d["lon"])
                        # ensure within city bounds
                        if b["min_lat"] <= lat <= b["max_lat"] and b["min_lon"] <= lon <= b["max_lon"]:
                            # Avoid duplicates
                            if not any(abs(r["latitude"] - lat) < 0.001 and abs(r["longitude"] - lon) < 0.001 for r in results):
                                results.append({
                                    "name": d.get("name") or d.get("display_name", "").split(",")[0],
                                    "display_name": d.get("display_name"),
                                    "latitude": lat,
                                    "longitude": lon,
                                    "type": d.get("type", "osm_feature"),
                                    "source": "OpenStreetMap Nominatim",
                                    "police_station": "City Jurisdiction"
                                })
            except Exception:
                pass  # Fall back to gazetteer results

        return results[:8]

    @staticmethod
    def get_stations_geojson(city_id: str = "kochi") -> Dict[str, Any]:
        """Returns police stations as a GeoJSON FeatureCollection."""
        city_cfg = CITIES_CONFIG.get(city_id, CITIES_CONFIG["kochi"])
        features = []
        for s in city_cfg["police_stations"]:
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [s["lon"], s["lat"]]
                },
                "properties": {
                    "id": s["id"],
                    "name": s["name"],
                    "short_name": s["short_name"],
                    "code": s["code"],
                    "jurisdiction": s["jurisdiction"],
                    "patrol_vehicles": s["patrol_vehicles"],
                    "city_id": city_id
                }
            })
        return {
            "type": "FeatureCollection",
            "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
            "features": features
        }

    @staticmethod
    def get_clusters_geojson(city_id: str = "kochi") -> Dict[str, Any]:
        """Returns DBSCAN clusters as a GeoJSON FeatureCollection."""
        mining = SpatialMiningEngine(city_id)
        clusters = mining.compute_dbscan_clusters()
        features = []
        
        for cl in clusters:
            # 1. Centroid point
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [cl["centroid"][1], cl["centroid"][0]]
                },
                "properties": {
                    "cluster_id": cl["cluster_id"],
                    "locality_name": cl["locality_name"],
                    "incident_count": cl["incident_count"],
                    "density_per_sqkm": cl["density_incidents_per_sqkm"],
                    "persistence_score": cl["persistence_score"],
                    "primary_crime": cl["primary_category"],
                    "police_station": cl["police_station"],
                    "radius_meters": cl["radius_meters"],
                    "feature_type": "hotspot_centroid"
                }
            })
            
            # 2. Circular polygon boundary approximation (32 vertices)
            radius_deg = cl["radius_meters"] / 111000.0
            lon_radius_deg = radius_deg / math.cos(math.radians(cl["centroid"][0]))
            coords = []
            for angle in np.linspace(0, 2 * math.pi, 33):
                pt_lon = cl["centroid"][1] + lon_radius_deg * math.cos(angle)
                pt_lat = cl["centroid"][0] + radius_deg * math.sin(angle)
                coords.append([round(float(pt_lon), 6), round(float(pt_lat), 6)])
                
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [coords]
                },
                "properties": {
                    "cluster_id": cl["cluster_id"],
                    "locality_name": cl["locality_name"],
                    "incident_count": cl["incident_count"],
                    "persistence_score": cl["persistence_score"],
                    "feature_type": "hotspot_perimeter"
                }
            })
            
        return {
            "type": "FeatureCollection",
            "features": features
        }

    @staticmethod
    def get_grid_geojson(city_id: str = "kochi") -> Dict[str, Any]:
        """Returns spatial grid cells as GeoJSON Polygons with crime intensity and privacy masking."""
        mining = SpatialMiningEngine(city_id)
        cells = mining.build_spatial_grid()
        forecast = mining.run_spatiotemporal_forecast()
        pred_map = {p["cell_id"]: p for p in forecast.get("cell_forecasts", [])}
        
        features = []
        for c in cells:
            if c["incident_count"] == 0:
                continue
                
            b = c["bounds"]
            poly_coords = [
                [b["west"], b["south"]],
                [b["east"], b["south"]],
                [b["east"], b["north"]],
                [b["west"], b["north"]],
                [b["west"], b["south"]]
            ]
            
            p_data = pred_map.get(c["cell_id"], {})
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [poly_coords]
                },
                "properties": {
                    "cell_id": c["cell_id"],
                    "incident_count": c["incident_count"],
                    "display_count": c["display_count"],
                    "is_privacy_suppressed": c["is_privacy_suppressed"],
                    "severity_score": c["severity_score"],
                    "top_category": c["top_category"],
                    "top_station": c["top_station"],
                    "peak_hour": c["peak_hour"],
                    "predicted_count_7d": p_data.get("predicted_incidents_next_7d", 0.0),
                    "forecast_intensity": p_data.get("forecast_intensity_index", 0.0)
                }
            })
            
        return {
            "type": "FeatureCollection",
            "features": features
        }

    @staticmethod
    def get_jurisdictions_geojson(city_id: str = "kochi") -> Dict[str, Any]:
        """
        Generates territorial police station jurisdiction boundary polygons
        using bounded Voronoi spatial tessellation around station headquarters.
        """
        city_cfg = CITIES_CONFIG.get(city_id, CITIES_CONFIG["kochi"])
        stations = city_cfg["police_stations"]
        bounds = city_cfg["bounds"]
        
        pts = np.array([[s["lon"], s["lat"]] for s in stations])
        
        # Bounding box limits
        min_lon, max_lon = bounds["min_lon"], bounds["max_lon"]
        min_lat, max_lat = bounds["min_lat"], bounds["max_lat"]
        
        # Add perimeter boundary anchors to bound Voronoi diagram
        anchors = np.array([
            [min_lon - 0.1, min_lat - 0.1],
            [min_lon - 0.1, max_lat + 0.1],
            [max_lon + 0.1, min_lat - 0.1],
            [max_lon + 0.1, max_lat + 0.1],
            [min_lon - 0.1, (min_lat + max_lat) / 2],
            [max_lon + 0.1, (min_lat + max_lat) / 2],
            [(min_lon + max_lon) / 2, min_lat - 0.1],
            [(min_lon + max_lon) / 2, max_lat + 0.1]
        ])
        all_pts = np.vstack([pts, anchors])
        vor = Voronoi(all_pts)
        
        features = []
        for i, station in enumerate(stations):
            region_idx = vor.point_region[i]
            region = vor.regions[region_idx]
            if not region or -1 in region:
                continue
                
            poly = [vor.vertices[v] for v in region]
            # Clip poly to city bounds
            clipped_poly = []
            for pt in poly:
                c_lon = max(min_lon, min(max_lon, float(pt[0])))
                c_lat = max(min_lat, min(max_lat, float(pt[1])))
                clipped_poly.append([round(c_lon, 6), round(c_lat, 6)])
            clipped_poly.append(clipped_poly[0])  # close ring
            
            features.append({
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [clipped_poly]
                },
                "properties": {
                    "station_id": station["id"],
                    "station_name": station["name"],
                    "short_name": station["short_name"],
                    "code": station["code"],
                    "jurisdiction_description": station["jurisdiction"],
                    "patrol_units": station["patrol_vehicles"]
                }
            })
            
        return {
            "type": "FeatureCollection",
            "features": features
        }
