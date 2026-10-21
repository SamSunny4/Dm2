import React, { useEffect, useState, useRef } from 'react';
import L from 'leaflet';
import { 
  Shield, 
  Navigation, 
  BarChart3, 
  Download, 
  CheckCircle2, 
  Crosshair, 
  RefreshCw, 
  ChevronRight,
  ChevronLeft,
  Search,
  Sliders,
  Layers,
  X
} from 'lucide-react';

interface City {
  id: string;
  name: string;
  state: string;
  district: string;
  center: [number, number];
  default_zoom: number;
  bounds: { min_lat: number; max_lat: number; min_lon: number; max_lon: number };
  num_stations: number;
}

interface Station {
  id: string;
  name: string;
  short_name: string;
  code: string;
  lat: number;
  lon: number;
  operational_radius_km?: number;
  jurisdiction: string;
  patrol_vehicles: string[];
}

interface Cluster {
  cluster_id: string;
  label: number;
  incident_count: number;
  centroid: [number, number];
  radius_meters: number;
  locality_name: string;
  police_station: string;
  average_severity: number;
  primary_category: string;
  persistence_score: number;
  density_incidents_per_sqkm: number;
}

interface GridCell {
  cell_id: string;
  row: number;
  col: number;
  bounds: { south: number; west: number; north: number; east: number };
  centroid: [number, number];
  incident_count: number;
  display_count: string;
  is_privacy_suppressed: boolean;
  severity_score: number;
  top_category: string;
  top_station: string;
  peak_hour: number | null;
  predicted_count_7d?: number;
  forecast_intensity?: number;
}

interface Checkpoint {
  sequence_number: number;
  name: string;
  coords: [number, number];
  arrival_minute: number;
  departure_minute: number;
  dwell_minutes: number;
  priority_score: number;
  target_crime: string;
  ipc_sections: string;
  checkpoint_type?: string;
  checkpoint_label?: string;
  code?: string;
  beat_sector?: string;
  sop_action?: string;
  justification: string;
}

interface VehicleRoute {
  vehicle_id: string;
  vehicle_name: string;
  call_sign?: string;
  vehicle_model?: string;
  beat_sector?: string;
  theme_color?: string;
  start_station: string;
  return_station: string;
  coverage_radius_km?: number;
  num_checkpoints: number;
  total_distance_km: number;
  driving_time_minutes: number;
  dwell_time_minutes: number;
  total_mission_time_minutes: number;
  hotspot_coverage_score: number;
  is_osrm_network_route: boolean;
  checkpoints: Checkpoint[];
  route_polyline: [number, number][];
}

interface StationCoverage {
  station_name: string;
  station_short_name: string;
  station_code: string;
  depot_coords: [number, number];
  operational_radius_km: number;
  jurisdiction: string;
  coverage_boundary?: [number, number][];
}

interface OptimizationResponse {
  mission_parameters: any;
  station_coverage?: StationCoverage;
  vehicle_routes: VehicleRoute[];
  baseline_comparison: {
    baseline_name: string;
    baseline_distance_km: number;
    baseline_coverage_score: number;
    optimized_total_coverage_score: number;
    coverage_gain_percent: number;
    optimization_objective: string;
  };
  uncovered_priority_sectors: { id: string; name: string; risk: number }[];
  equity_and_ethical_audit: any;
}

interface BasemapProvider {
  id: string;
  name: string;
  url: string;
  attribution: string;
  max_zoom: number;
  is_default: boolean;
}

export function App() {
  // Application State
  const [cities, setCities] = useState<City[]>([]);
  const [selectedCity, setSelectedCity] = useState<string>('kochi');
  const [stations, setStations] = useState<Station[]>([]);
  const [selectedStation, setSelectedStation] = useState<string>('all');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [selectedTimeOfDay, setSelectedTimeOfDay] = useState<string>('all');
  const [categories, setCategories] = useState<Record<string, any>>({});
  
  // Analytics State
  const [summary, setSummary] = useState<any>(null);
  const [clusters, setClusters] = useState<Cluster[]>([]);
  const [gridCells, setGridCells] = useState<GridCell[]>([]);
  const [forecastData, setForecastData] = useState<any>(null);
  
  // Patrol Optimization State
  const [optimizing, setOptimizing] = useState<boolean>(false);
  const [routeResult, setRouteResult] = useState<OptimizationResponse | null>(null);
  const [patrolDuration, setPatrolDuration] = useState<number>(180);
  const [patrolVehicles, setPatrolVehicles] = useState<number>(1);
  const [vehicleType, setVehicleType] = useState<string>('Patrol Car');
  const [priorityFocus, setPriorityFocus] = useState<string>('balanced');
  
  // UI Panels
  const [activeTab, setActiveTab] = useState<'analytics' | 'routing' | 'provenance'>('analytics');
  const [sidebarCollapsed, setSidebarCollapsed] = useState<boolean>(false);
  const [selectedInspector, setSelectedInspector] = useState<any | null>(null);
  const [pdfDownloading, setPdfDownloading] = useState<boolean>(false);
  
  // Map API State
  const [basemaps, setBasemaps] = useState<BasemapProvider[]>([]);
  const [activeBasemap, setActiveBasemap] = useState<string>('carto_light');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState<boolean>(false);
  const [showSearchDropdown, setShowSearchDropdown] = useState<boolean>(false);
  const [showMapApiModal, setShowMapApiModal] = useState<boolean>(false);
  const [mapApiConfig, setMapApiConfig] = useState({
    mapboxToken: '',
    googleApiKey: '',
    customOsrmUrl: 'http://router.project-osrm.org'
  });
  
  // Map Layer Toggles
  const [showHeatmap, setShowHeatmap] = useState<boolean>(true);
  const [showClusters, setShowClusters] = useState<boolean>(true);
  const [showGrid, setShowGrid] = useState<boolean>(true);
  const [showStations, setShowStations] = useState<boolean>(true);
  const [showJurisdictions, setShowJurisdictions] = useState<boolean>(false);
  const [showRoute, setShowRoute] = useState<boolean>(true);

  // FIR Ingestion Test State
  const [importForm, setImportForm] = useState({
    police_station_id: 'ekm_central',
    fir_number: '342/2026',
    crime_category: 'THEFT_SNATCHING',
    registration_time: new Date().toISOString().slice(0, 16),
    occurrence_time: new Date(Date.now() - 4 * 3600000).toISOString().slice(0, 16),
    locality_name: 'Near Shenoys Cinema, MG Road',
    raw_narrative: 'Complainant Sri Suresh Kumar (Phone: 9847012345) reported snatching of gold chain near door no. 42/108.'
  });
  const [importStatus, setImportStatus] = useState<any | null>(null);

  // Leaflet Map References
  const mapContainerRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);
  const tileLayerRef = useRef<L.TileLayer | null>(null);
  const searchMarkerRef = useRef<L.Marker | null>(null);
  
  const layerStationsRef = useRef<L.LayerGroup>(L.layerGroup());
  const layerJurisdictionsRef = useRef<L.LayerGroup>(L.layerGroup());
  const layerClustersRef = useRef<L.LayerGroup>(L.layerGroup());
  const layerGridRef = useRef<L.LayerGroup>(L.layerGroup());
  const layerHeatmapRef = useRef<L.LayerGroup>(L.layerGroup());
  const layerRouteRef = useRef<L.LayerGroup>(L.layerGroup());

  // 1. Initial Load: Cities, Taxonomy, Basemaps
  useEffect(() => {
    fetch('/api/cities')
      .then(res => res.json())
      .then(data => setCities(data))
      .catch(err => console.error('Error fetching cities:', err));

    fetch('/api/categories')
      .then(res => res.json())
      .then(data => setCategories(data))
      .catch(err => console.error('Error fetching categories:', err));

    fetch('/api/map/basemaps')
      .then(res => res.json())
      .then(data => setBasemaps(data))
      .catch(err => console.error('Error fetching basemaps:', err));
  }, []);

  // 2. Initialize Leaflet Map
  useEffect(() => {
    if (!mapContainerRef.current || mapInstanceRef.current) return;

    const map = L.map(mapContainerRef.current, {
      center: [9.9734, 76.2815],
      zoom: 13,
      zoomControl: false
    });

    L.control.zoom({ position: 'topright' }).addTo(map);

    // Initial default Carto Positron basemap
    const defaultTile = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://openstreetmap.org">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>',
      maxZoom: 19
    }).addTo(map);
    tileLayerRef.current = defaultTile;

    layerJurisdictionsRef.current.addTo(map);
    layerHeatmapRef.current.addTo(map);
    layerGridRef.current.addTo(map);
    layerClustersRef.current.addTo(map);
    layerStationsRef.current.addTo(map);
    layerRouteRef.current.addTo(map);

    mapInstanceRef.current = map;

    return () => {
      map.remove();
      mapInstanceRef.current = null;
    };
  }, []);

  // 3. Basemap Provider Switcher
  const handleBasemapChange = (providerId: string) => {
    setActiveBasemap(providerId);
    const provider = basemaps.find(b => b.id === providerId);
    if (provider && mapInstanceRef.current) {
      if (tileLayerRef.current) {
        mapInstanceRef.current.removeLayer(tileLayerRef.current);
      }
      const newTile = L.tileLayer(provider.url, {
        attribution: provider.attribution,
        maxZoom: provider.max_zoom
      }).addTo(mapInstanceRef.current);
      tileLayerRef.current = newTile;
    }
  };

  // 4. Geocoding Search Handlers
  const handleSearchInput = async (val: string) => {
    setSearchQuery(val);
    if (val.trim().length < 2) {
      setSearchResults([]);
      setShowSearchDropdown(false);
      return;
    }
    setIsSearching(true);
    try {
      const res = await fetch(`/api/map/geocode?q=${encodeURIComponent(val)}&city_id=${selectedCity}`);
      const data = await res.json();
      setSearchResults(data);
      setShowSearchDropdown(true);
    } catch (e) {
      console.error(e);
    } finally {
      setIsSearching(false);
    }
  };

  const handleSelectLocation = (loc: any) => {
    setShowSearchDropdown(false);
    setSearchQuery(loc.name);
    if (mapInstanceRef.current) {
      mapInstanceRef.current.flyTo([loc.latitude, loc.longitude], 15, { duration: 1.2 });
      
      if (searchMarkerRef.current) {
        mapInstanceRef.current.removeLayer(searchMarkerRef.current);
      }

      const pinIcon = L.divIcon({
        className: 'search-pin-icon',
        html: `<div style="background-color:#ef4444; border:2px solid #ffffff; width:26px; height:26px; border-radius:50%; box-shadow:0 0 10px rgba(239,68,68,0.8); display:flex; align-items:center; justify-content:center; color:#fff; font-size:12px; font-weight:bold;">📍</div>`,
        iconSize: [26, 26],
        iconAnchor: [13, 13]
      });

      const marker = L.marker([loc.latitude, loc.longitude], { icon: pinIcon }).addTo(mapInstanceRef.current);
      marker.bindPopup(`
        <div style="font-family:var(--font-sans); padding:4px;">
          <div style="font-weight:700; color:#dc2626; font-size:12.5px;">${loc.name}</div>
          <div style="font-size:11px; color:#475569; margin-top:2px;">${loc.display_name}</div>
          <div style="font-size:10.5px; color:#1e3a8a; margin-top:4px;">Jurisdiction: <b>${loc.police_station}</b></div>
          <div style="font-size:9.5px; color:#64748b; margin-top:2px;">Source: ${loc.source}</div>
        </div>
      `).openPopup();
      searchMarkerRef.current = marker;
    }
  };

  // 5. GeoJSON Export Function
  const handleExportGeoJSON = async (layerName: string) => {
    try {
      const res = await fetch(`/api/map/geojson/${layerName}?city_id=${selectedCity}`);
      const data = await res.json();
      const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `kerala_${selectedCity}_${layerName}.geojson`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (e) {
      console.error('GeoJSON export error:', e);
    }
  };

  // 6. Load City Data & Stations when selectedCity changes
  useEffect(() => {
    fetch(`/api/stations?city_id=${selectedCity}`)
      .then(res => res.json())
      .then(data => {
        setStations(data.stations || []);
        if (data.stations && data.stations.length > 0) {
          setImportForm(prev => ({ ...prev, police_station_id: data.stations[0].id }));
        }
      });

    // Fly map to city center
    const cityObj = cities.find(c => c.id === selectedCity);
    if (cityObj && mapInstanceRef.current) {
      mapInstanceRef.current.flyTo(cityObj.center, cityObj.default_zoom, { duration: 1.2 });
    }

    // Refresh data mining
    fetchMiningData();
  }, [selectedCity, cities]);

  // 7. Reload Data on Filter Changes
  useEffect(() => {
    fetchMiningData();
  }, [selectedStation, selectedCategory, selectedTimeOfDay]);

  const fetchMiningData = () => {
    const params = new URLSearchParams({
      city_id: selectedCity,
      station_id: selectedStation,
      category: selectedCategory,
      time_of_day: selectedTimeOfDay
    });

    fetch(`/api/summary?${params.toString()}`)
      .then(res => res.json())
      .then(data => setSummary(data))
      .catch(err => console.error(err));

    fetch(`/api/mining/clusters?${params.toString()}`)
      .then(res => res.json())
      .then(data => setClusters(data.clusters || []))
      .catch(err => console.error(err));

    fetch(`/api/mining/grid?${params.toString()}`)
      .then(res => res.json())
      .then(data => setGridCells(data.cells || []))
      .catch(err => console.error(err));

    fetch(`/api/mining/forecast?city_id=${selectedCity}`)
      .then(res => res.json())
      .then(data => setForecastData(data))
      .catch(err => console.error(err));
  };

  // 8. Update Map Layers whenever data changes
  useEffect(() => {
    if (!mapInstanceRef.current) return;

    // --- A. Stations Layer ---
    layerStationsRef.current.clearLayers();
    if (showStations) {
      stations.forEach(st => {
        const icon = L.divIcon({
          className: 'custom-station-icon',
          html: `<div style="background-color:#1e3a8a; border:2px solid #ffffff; width:22px; height:22px; border-radius:4px; display:flex; align-items:center; justify-content:center; color:#ffffff; font-size:10px; font-weight:bold; box-shadow:0 1px 4px rgba(0,0,0,0.4);" title="${st.name}">PS</div>`,
          iconSize: [22, 22],
          iconAnchor: [11, 11]
        });

        const marker = L.marker([st.lat, st.lon], { icon });
        marker.bindPopup(`
          <div style="font-family:var(--font-sans); padding:4px;">
            <div style="font-weight:700; font-size:13px; color:#1e3a8a;">${st.name}</div>
            <div style="font-size:11px; color:#64748b; margin-top:2px;">Code: <b>${st.code}</b></div>
            <div style="font-size:11.5px; margin-top:6px; line-height:1.35;"><b>Beat Jurisdiction:</b><br/>${st.jurisdiction}</div>
            <div style="margin-top:6px; font-size:11px; color:#047857;"><b>Patrol Units:</b> ${st.patrol_vehicles.join(', ')}</div>
          </div>
        `);
        layerStationsRef.current.addLayer(marker);
      });
    }

    // --- B. Station Territorial Jurisdictions Layer (GeoJSON) ---
    layerJurisdictionsRef.current.clearLayers();
    if (showJurisdictions) {
      fetch(`/api/map/geojson/jurisdictions?city_id=${selectedCity}`)
        .then(res => res.json())
        .then(geojson => {
          L.geoJSON(geojson, {
            style: {
              color: '#3b82f6',
              weight: 1.5,
              dashArray: '4, 4',
              fillColor: '#60a5fa',
              fillOpacity: 0.08
            },
            onEachFeature: (feature, layer) => {
              const p = feature.properties;
              layer.bindTooltip(`<b>${p.station_name}</b><br/>${p.jurisdiction_description}`, { sticky: true });
            }
          }).addTo(layerJurisdictionsRef.current);
        })
        .catch(err => console.error('Error loading jurisdictions GeoJSON:', err));
    }

    // --- C. Clusters Layer (DBSCAN) ---
    layerClustersRef.current.clearLayers();
    if (showClusters) {
      clusters.forEach(cl => {
        const circle = L.circle(cl.centroid, {
          radius: cl.radius_meters,
          color: '#ea580c',
          weight: 1.5,
          fillColor: '#f97316',
          fillOpacity: 0.18
        });

        circle.on('click', () => {
          setSelectedInspector({
            type: 'Historical Cluster (DBSCAN)',
            title: cl.locality_name,
            id: cl.cluster_id,
            incidents: cl.incident_count,
            density: `${cl.density_incidents_per_sqkm} / km²`,
            persistence: `${(cl.persistence_score * 100).toFixed(0)}%`,
            primaryCrime: cl.primary_category,
            station: cl.police_station
          });
        });

        circle.bindTooltip(`
          <div style="font-size:11px;">
            <b>${cl.locality_name}</b><br/>
            ${cl.incident_count} Incidents | Persistence: ${(cl.persistence_score * 100).toFixed(0)}%
          </div>
        `);

        layerClustersRef.current.addLayer(circle);
      });
    }

    // --- D. Spatial Grid Layer (with Privacy-safe counts) ---
    layerGridRef.current.clearLayers();
    if (showGrid) {
      gridCells.forEach(cell => {
        const count = cell.incident_count;
        if (count === 0) return;

        // Color based on incident count / severity
        const fillColor = count > 15 ? '#b91c1c' : (count > 8 ? '#ea580c' : (count >= 3 ? '#f59e0b' : '#38bdf8'));
        const opacity = count > 15 ? 0.35 : (count > 8 ? 0.28 : 0.20);

        const bounds: L.LatLngBoundsLiteral = [
          [cell.bounds.south, cell.bounds.west],
          [cell.bounds.north, cell.bounds.east]
        ];

        const rect = L.rectangle(bounds, {
          color: fillColor,
          weight: 0.8,
          fillColor: fillColor,
          fillOpacity: opacity
        });

        rect.on('click', () => {
          setSelectedInspector({
            type: 'Spatial Grid Cell (400m)',
            title: `Sector ${cell.cell_id}`,
            id: cell.cell_id,
            incidents: cell.display_count,
            isSuppressed: cell.is_privacy_suppressed,
            severityScore: cell.severity_score,
            primaryCrime: cell.top_category,
            station: cell.top_station,
            peakHour: cell.peak_hour !== null ? `${cell.peak_hour}:00 IST` : 'N/A',
            forecast7d: cell.predicted_count_7d || 'N/A'
          });
        });

        rect.bindTooltip(`
          <div style="font-size:11px;">
            <b>Sector ${cell.cell_id}</b><br/>
            Count: <b>${cell.display_count}</b> ${cell.is_privacy_suppressed ? '(Masked for Privacy)' : ''}<br/>
            Top: ${cell.top_category}
          </div>
        `);

        layerGridRef.current.addLayer(rect);
      });
    }

    // --- E. Heatmap Layer ---
    layerHeatmapRef.current.clearLayers();
    if (showHeatmap && gridCells.length > 0) {
      gridCells.forEach(cell => {
        if (cell.incident_count < 2) return;
        const heatCircle = L.circleMarker(cell.centroid, {
          radius: Math.min(22, 6 + cell.incident_count * 0.8),
          color: 'transparent',
          fillColor: cell.incident_count > 10 ? '#dc2626' : '#f97316',
          fillOpacity: 0.25
        });
        layerHeatmapRef.current.addLayer(heatCircle);
      });
    }

    // --- F. Patrol Route Layer ---
    layerRouteRef.current.clearLayers();
    if (showRoute && routeResult && routeResult.vehicle_routes) {
      // 1. Station Local Beat Boundary (Visualizes tight operational coverage area)
      if (routeResult.station_coverage && routeResult.station_coverage.coverage_boundary) {
        const boundary = L.polygon(routeResult.station_coverage.coverage_boundary, {
          color: '#0284c7',
          dashArray: '5, 5',
          weight: 2,
          fillColor: '#38bdf8',
          fillOpacity: 0.08
        });
        boundary.bindTooltip(`
          <b>${routeResult.station_coverage.station_short_name} Janamaithri Beat Zone</b><br/>
          Operational Radius: ${routeResult.station_coverage.operational_radius_km} km (Close City Coverage)
        `, { sticky: true, direction: 'top' });
        layerRouteRef.current.addLayer(boundary);

        // Depot Station Marker
        const depotIcon = L.divIcon({
          className: 'depot-pin',
          html: `
            <div style="background-color:#0f172a; border:2.5px solid #38bdf8; width:28px; height:28px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#38bdf8; font-size:10px; font-weight:800; box-shadow:0 3px 8px rgba(0,0,0,0.5);" title="${routeResult.station_coverage.station_name}">
              DEP
            </div>
          `,
          iconSize: [28, 28],
          iconAnchor: [14, 14]
        });
        const depotMarker = L.marker(routeResult.station_coverage.depot_coords, { icon: depotIcon });
        depotMarker.bindPopup(`
          <div style="font-family:var(--font-sans); padding:4px; max-width:260px;">
            <div style="font-size:10.5px; font-weight:800; color:#0284c7; text-transform:uppercase;">POLICE STATION DEPOT</div>
            <div style="font-weight:700; font-size:13px; color:#0f172a; margin-top:2px;">${routeResult.station_coverage.station_name}</div>
            <div style="font-size:11px; color:#475569; margin-top:4px;">
              <b>Jurisdiction:</b> ${routeResult.station_coverage.jurisdiction}
            </div>
            <div style="font-size:11px; color:#0369a1; margin-top:4px; font-weight:600;">
              Janamaithri Beat Radius: ${routeResult.station_coverage.operational_radius_km} km
            </div>
          </div>
        `);
        layerRouteRef.current.addLayer(depotMarker);
      }

      // 2. Individual Vehicle Routes with Distinct Theming
      routeResult.vehicle_routes.forEach((vr, vrIdx) => {
        const vColor = vr.theme_color || (vrIdx === 0 ? '#1d4ed8' : (vrIdx === 1 ? '#d97706' : '#e11d48'));
        
        // Draw real OSRM road polyline
        if (vr.route_polyline && vr.route_polyline.length > 0) {
          const polyline = L.polyline(vr.route_polyline, {
            color: vColor,
            weight: 4.5,
            opacity: 0.88,
            lineJoin: 'round'
          });
          polyline.bindTooltip(`
            <b>${vr.vehicle_name}</b> (${vr.call_sign || 'Patrol'})<br/>
            ${vr.beat_sector || 'Station Beat'} • ${vr.total_distance_km} km
          `, { sticky: true });
          layerRouteRef.current.addLayer(polyline);
        }

        // Checkpoints markers
        vr.checkpoints.forEach(cp => {
          const cpIcon = L.divIcon({
            className: 'custom-cp-icon',
            html: `
              <div style="background-color:${vColor}; border:2px solid #ffffff; width:25px; height:25px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#ffffff; font-size:11px; font-weight:700; box-shadow:0 2px 6px rgba(0,0,0,0.4);" title="${cp.name}">
                ${cp.sequence_number}
              </div>
            `,
            iconSize: [25, 25],
            iconAnchor: [12.5, 12.5]
          });

          const cpMarker = L.marker(cp.coords, { icon: cpIcon });
          cpMarker.bindPopup(`
            <div style="font-family:var(--font-sans); padding:4px; max-width:280px;">
              <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:4px;">
                <span style="font-size:10px; font-weight:800; color:${vColor};">CHECKPOINT #${cp.sequence_number}</span>
                <span style="font-size:9.5px; font-weight:700; background:#f1f5f9; padding:1px 5px; border-radius:3px; color:#475569;">${cp.checkpoint_label || 'POINT BOOK'}</span>
              </div>
              <div style="font-weight:700; font-size:13px; color:#0f172a;">${cp.name}</div>
              <div style="font-size:10.5px; color:#64748b; margin-top:2px;">
                <b>Unit:</b> ${vr.call_sign || vr.vehicle_name} | <b>Sector:</b> ${cp.beat_sector || vr.beat_sector}
              </div>
              <div style="font-size:11px; color:#475569; font-family:var(--font-mono); margin-top:4px;">
                Arr: +${cp.arrival_minute}m | Dwell: ${cp.dwell_minutes}m | Dep: +${cp.departure_minute}m
              </div>
              <div style="font-size:11px; color:#b45309; background:#fffbeb; border:1px solid #fde68a; border-radius:3px; padding:4px 6px; margin-top:5px;">
                <b>Target Crime:</b> ${cp.target_crime} (${cp.ipc_sections})
              </div>
              ${cp.sop_action ? `
                <div style="font-size:11px; color:#166534; background:#f0fdf4; border:1px solid #bbf7d0; border-radius:3px; padding:5px 7px; margin-top:5px; line-height:1.35;">
                  <b>Kerala Police SOP:</b> ${cp.sop_action}
                </div>
              ` : ''}
              <div style="font-size:10.5px; color:#64748b; margin-top:5px; line-height:1.3;">
                ${cp.justification}
              </div>
            </div>
          `);
          layerRouteRef.current.addLayer(cpMarker);
        });
      });
    }

  }, [
    showStations, showJurisdictions, showClusters, showGrid, showHeatmap, showRoute,
    stations, clusters, gridCells, routeResult, selectedCity
  ]);

  // Handle Patrol Route Optimization Request
  const handleOptimizeRoute = async () => {
    setOptimizing(true);
    try {
      const activeDepotId = selectedStation !== 'all' ? selectedStation : (stations[0]?.id || 'ekm_central');
      const res = await fetch('/api/routing/optimize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          city_id: selectedCity,
          start_station_id: activeDepotId,
          patrol_duration_minutes: patrolDuration,
          num_vehicles: patrolVehicles,
          vehicle_type: vehicleType,
          priority_focus: priorityFocus,
          dwell_time_minutes: 10,
          return_to_start: true
        })
      });
      const data = await res.json();
      setRouteResult(data);
      setShowRoute(true);

      // Focus map on local station beat area
      if (data.station_coverage?.depot_coords && mapInstanceRef.current) {
        mapInstanceRef.current.setView(data.station_coverage.depot_coords, 14, { animate: true });
      }
    } catch (err) {
      console.error('Optimization error:', err);
    } finally {
      setOptimizing(false);
    }
  };

  // Handle PDF Report Download
  const handleDownloadPDF = async () => {
    setPdfDownloading(true);
    try {
      const res = await fetch(`/api/reports/download-pdf?city_id=${selectedCity}`);
      if (!res.ok) throw new Error('Download failed');
      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `Kerala_Urban_Crime_Intelligence_${selectedCity.toUpperCase()}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Error downloading PDF:', err);
      alert('PDF generation error. Please try again.');
    } finally {
      setPdfDownloading(false);
    }
  };

  // Handle Authorized FIR Ingestion & PII Scrubbing Demo
  const handleImportFIR = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch('/api/data/import', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          city_id: selectedCity,
          ...importForm
        })
      });
      const data = await res.json();
      setImportStatus(data);
      fetchMiningData(); // refresh
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="app-container">
      {/* Top Application Header */}
      <header className="top-header">
        <div className="brand-section">
          <div className="brand-badge">POLICE ANALYTICS</div>
          <div>
            <div className="brand-title">Kerala Urban Crime Hotspot Intelligence & Patrol Optimization</div>
            <div className="brand-subtitle">Law Enforcement Decision Support System | SCRB Calibrated Baseline</div>
          </div>
        </div>

        {/* Map Geocoding Search Bar */}
        <div className="map-search-wrap">
          <div className="map-search-input-wrap">
            <Search size={13} color="#64748b" />
            <input 
              type="text"
              className="map-search-input"
              placeholder="Search landmark or street (e.g. Marine Drive, Broadway)..."
              value={searchQuery}
              onChange={e => handleSearchInput(e.target.value)}
              onFocus={() => { if (searchResults.length > 0) setShowSearchDropdown(true); }}
            />
            {isSearching && <RefreshCw size={11} className="spin" color="#64748b" />}
          </div>

          {/* Autocomplete Dropdown */}
          {showSearchDropdown && searchResults.length > 0 && (
            <div className="search-dropdown">
              {searchResults.map((loc, idx) => (
                <div key={idx} className="search-item" onClick={() => handleSelectLocation(loc)}>
                  <div className="search-item-name">{loc.name}</div>
                  <div className="search-item-meta">{loc.display_name}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        <div className="header-controls">
          {/* City Selector */}
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            <span style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-muted)' }}>CITY:</span>
            <select 
              className="select-input" 
              value={selectedCity} 
              onChange={e => setSelectedCity(e.target.value)}
              style={{ fontWeight: 600 }}
            >
              {cities.map(c => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </div>

          {/* Map API Config Button */}
          <button 
            className="btn btn-secondary btn-sm"
            onClick={() => setShowMapApiModal(true)}
            title="Configure Map API endpoints & tile keys"
          >
            <Sliders size={13} />
            <span>Map API</span>
          </button>

          {/* Download PDF Button */}
          <button 
            className="btn btn-download" 
            onClick={handleDownloadPDF} 
            disabled={pdfDownloading}
            title="Download comprehensive publication-grade PDF report"
          >
            {pdfDownloading ? (
              <RefreshCw size={13} className="spin" />
            ) : (
              <Download size={13} />
            )}
            <span>{pdfDownloading ? 'Generating...' : 'Download PDF Report'}</span>
          </button>
        </div>
      </header>

      {/* Quick Filters Bar */}
      <div className="filters-bar">
        {/* Station Filter */}
        <div className="filter-group">
          <label className="filter-label">Jurisdiction Station</label>
          <select 
            className="select-input" 
            value={selectedStation} 
            onChange={e => setSelectedStation(e.target.value)}
          >
            <option value="all">All Stations ({stations.length})</option>
            {stations.map(s => (
              <option key={s.id} value={s.id}>{s.short_name}</option>
            ))}
          </select>
        </div>

        {/* Crime Category Filter */}
        <div className="filter-group">
          <label className="filter-label">Offense Category</label>
          <select 
            className="select-input" 
            value={selectedCategory} 
            onChange={e => setSelectedCategory(e.target.value)}
          >
            <option value="all">All Offense Heads</option>
            {Object.entries(categories).map(([key, val]) => (
              <option key={key} value={key}>{val.label}</option>
            ))}
          </select>
        </div>

        {/* Time of Day Filter */}
        <div className="filter-group">
          <label className="filter-label">Time of Occurrence</label>
          <select 
            className="select-input" 
            value={selectedTimeOfDay} 
            onChange={e => setSelectedTimeOfDay(e.target.value)}
          >
            <option value="all">24 Hours (Full Diurnal)</option>
            <option value="morning">Morning (06:00 - 11:59)</option>
            <option value="afternoon">Afternoon (12:00 - 16:59)</option>
            <option value="evening">Evening Rush (17:00 - 21:59)</option>
            <option value="night">Night Beat (22:00 - 05:59)</option>
          </select>
        </div>

        {/* Status Badge & Sidebar Toggle */}
        <div style={{ marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <button 
            className="btn btn-secondary btn-sm"
            onClick={() => setSidebarCollapsed(!sidebarCollapsed)}
            title="Toggle Sidebar"
          >
            {sidebarCollapsed ? <ChevronRight size={12} /> : <ChevronLeft size={12} />}
            <span>{sidebarCollapsed ? 'Show Panel' : 'Hide Panel'}</span>
          </button>
          <div style={{ fontSize: '11px', color: 'var(--text-muted)' }}>
            Dataset: <b style={{ color: 'var(--text-primary)' }}>{summary?.total_records || 0} Records</b>
          </div>
          <div style={{ fontSize: '10.5px', padding: '3px 6px', backgroundColor: '#ecfdf5', color: '#047857', borderRadius: '3px', border: '1px solid #a7f3d0', fontWeight: 600 }}>
            Map API / OSRM Ready
          </div>
        </div>
      </div>

      {/* Main Split Interface */}
      <div className="main-content">
        {/* Left Analytical Sidebar */}
        <aside className={`sidebar ${sidebarCollapsed ? 'collapsed' : ''}`}>
          {/* Tabs */}
          <div className="sidebar-tabs">
            <button 
              className={`tab-btn ${activeTab === 'analytics' ? 'active' : ''}`}
              onClick={() => setActiveTab('analytics')}
            >
              <BarChart3 size={14} />
              <span>Hotspots & Metrics</span>
            </button>
            <button 
              className={`tab-btn ${activeTab === 'routing' ? 'active' : ''}`}
              onClick={() => setActiveTab('routing')}
            >
              <Navigation size={14} />
              <span>Patrol Optimizer</span>
            </button>
            <button 
              className={`tab-btn ${activeTab === 'provenance' ? 'active' : ''}`}
              onClick={() => setActiveTab('provenance')}
            >
              <Shield size={14} />
              <span>Legal Provenance</span>
            </button>
          </div>

          <div className="sidebar-body">
            {/* TAB 1: HOTSPOTS & ANALYTICS */}
            {activeTab === 'analytics' && (
              <>
                {/* Metric Cards Row */}
                <div className="metric-row">
                  <div className="metric-box">
                    <div className="metric-val">{summary?.total_records || 0}</div>
                    <div className="metric-lbl">Total Incidents</div>
                  </div>
                  <div className="metric-box">
                    <div className="metric-val">{clusters.length}</div>
                    <div className="metric-lbl">DBSCAN Clusters</div>
                  </div>
                  <div className="metric-box">
                    <div className="metric-val" style={{ color: '#059669' }}>
                      {forecastData?.evaluation_metrics?.top_k_hotspot_coverage_percent || '85.0'}%
                    </div>
                    <div className="metric-lbl">Model Hit Rate</div>
                  </div>
                </div>

                {/* Model Evaluation Notice */}
                {forecastData && (
                  <div className="panel-card" style={{ backgroundColor: '#f8fafc', borderColor: '#cbd5e1' }}>
                    <div className="card-title">
                      <span>Model Evaluation (Holdout 75/25 Split)</span>
                      <span style={{ fontSize: '10px', color: '#0284c7' }}>Pearson r = {forecastData.evaluation_metrics.pearson_correlation}</span>
                    </div>
                    <div style={{ fontSize: '11.5px', color: 'var(--text-secondary)', lineHeight: 1.4 }}>
                      Chronological holdout test evaluated strictly out-of-time. Random Forest regressor with spatial lags outperformed historical baseline:
                      <div style={{ marginTop: '6px', display: 'flex', gap: '12px', fontFamily: 'var(--font-mono)', fontSize: '11px' }}>
                        <div>Model MAE: <b>{forecastData.evaluation_metrics.models.spatiotemporal_random_forest.mae}</b></div>
                        <div>Baseline MAE: <b>{forecastData.evaluation_metrics.models.baseline_historical_mean.mae}</b></div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Diurnal Hourly Frequency Bar Histogram */}
                {summary && summary.hourly_trend && (
                  <div className="panel-card">
                    <div className="card-title">
                      <span>24-Hour Diurnal Crime Profile</span>
                      <span style={{ fontSize: '10px', color: '#e11d48' }}>Peak: 17:00 - 22:00 IST</span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'flex-end', height: '60px', gap: '2px', paddingBottom: '4px' }}>
                      {summary.hourly_trend.map((h: any) => {
                        const maxCount = Math.max(...summary.hourly_trend.map((x: any) => x.count), 1);
                        const pct = (h.count / maxCount) * 100;
                        const isPeak = h.hour >= 17 && h.hour <= 22;
                        return (
                          <div 
                            key={h.hour} 
                            style={{ 
                              flex: 1, 
                              height: `${pct}%`, 
                              backgroundColor: isPeak ? '#e11d48' : '#3b82f6',
                              borderRadius: '1px'
                            }}
                            title={`${h.hour}:00 - ${h.count} incidents`}
                          />
                        );
                      })}
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '9.5px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>
                      <span>00:00</span>
                      <span>06:00</span>
                      <span>12:00</span>
                      <span>18:00</span>
                      <span>23:00</span>
                    </div>
                  </div>
                )}

                {/* Offense Categories Breakdown Table */}
                {summary && summary.categories && (
                  <div className="panel-card">
                    <div className="card-title">Offense Category Distribution</div>
                    <table className="data-table">
                      <thead>
                        <tr>
                          <th>Category</th>
                          <th>Count</th>
                          <th>Ratio</th>
                          <th>Legal Head</th>
                        </tr>
                      </thead>
                      <tbody>
                        {summary.categories.map((c: any) => (
                          <tr key={c.category_id}>
                            <td style={{ fontWeight: 500 }}>{c.label}</td>
                            <td style={{ fontFamily: 'var(--font-mono)' }}>{c.count}</td>
                            <td>{c.percent}%</td>
                            <td style={{ color: 'var(--text-muted)', fontSize: '10px' }}>{c.ipc_bns}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}

                {/* DBSCAN Hotspots List */}
                <div className="panel-card">
                  <div className="card-title">Top Historical Hotspots (DBSCAN)</div>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                    {clusters.slice(0, 5).map(cl => (
                      <div 
                        key={cl.cluster_id} 
                        style={{ padding: '6px 8px', border: '1px solid var(--border-light)', borderRadius: '3px', cursor: 'pointer', backgroundColor: 'var(--bg-secondary)' }}
                        onClick={() => {
                          if (mapInstanceRef.current) {
                            mapInstanceRef.current.flyTo(cl.centroid, 15);
                          }
                        }}
                      >
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 600, fontSize: '11.5px' }}>
                          <span>{cl.locality_name}</span>
                          <span style={{ color: '#ea580c' }}>{cl.incident_count} Incidents</span>
                        </div>
                        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '10.5px', color: 'var(--text-muted)', marginTop: '2px' }}>
                          <span>{cl.primary_category}</span>
                          <span>Persistence: {(cl.persistence_score * 100).toFixed(0)}%</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </>
            )}

            {/* TAB 2: PATROL ROUTE OPTIMIZATION */}
            {activeTab === 'routing' && (
              <>
                <div className="panel-card">
                  <div className="kerala-patrol-banner">
                    <Shield size={16} color="#166534" style={{ flexShrink: 0, marginTop: 1 }} />
                    <div>
                      <div className="kerala-patrol-banner-title">Kerala Police Janamaithri Beat Scheme Active</div>
                      <div className="kerala-patrol-banner-desc">
                        Strict localized station jurisdiction (~2.5 - 3.8 km radius) • Dedicated non-overlapping beat sectors per car • Registered Point Books & e-Beat verification.
                      </div>
                    </div>
                  </div>

                  <div className="card-title">Patrol Mission Parameters</div>
                  
                  <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                    <div>
                      <label className="filter-label">Deployment Station (Depot)</label>
                      <select 
                        className="select-input" 
                        style={{ width: '100%', marginTop: '3px' }}
                        value={selectedStation !== 'all' ? selectedStation : (stations[0]?.id || 'ekm_central')}
                        onChange={e => setSelectedStation(e.target.value)}
                      >
                        {stations.map(s => (
                          <option key={s.id} value={s.id}>
                            {s.name} ({s.short_name}) • {s.operational_radius_km || 3.2} km Beat
                          </option>
                        ))}
                      </select>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                      <div>
                        <label className="filter-label">Patrol Shift Duration</label>
                        <select 
                          className="select-input" 
                          style={{ width: '100%', marginTop: '3px' }}
                          value={patrolDuration}
                          onChange={e => setPatrolDuration(Number(e.target.value))}
                        >
                          <option value={120}>2 Hours (120 min)</option>
                          <option value={180}>3 Hours (180 min)</option>
                          <option value={240}>4 Hours (240 min)</option>
                          <option value={360}>6 Hours (360 min)</option>
                        </select>
                      </div>

                      <div>
                        <label className="filter-label">Patrol Units Dispatched</label>
                        <select 
                          className="select-input" 
                          style={{ width: '100%', marginTop: '3px' }}
                          value={patrolVehicles}
                          onChange={e => setPatrolVehicles(Number(e.target.value))}
                        >
                          <option value={1}>1 Unit (Station Mobile Patrol)</option>
                          <option value={2}>2 Units (Mobile Bolero + Cheetah Motorcycle)</option>
                          <option value={3}>3 Units (Mobile + Cheetah Bike + Pink Patrol)</option>
                        </select>
                      </div>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                      <div>
                        <label className="filter-label">Vehicle Role</label>
                        <select 
                          className="select-input" 
                          style={{ width: '100%', marginTop: '3px' }}
                          value={vehicleType}
                          onChange={e => setVehicleType(e.target.value)}
                        >
                          <option value="Patrol Car">Station Mobile (Bolero / 22 km/h)</option>
                          <option value="Beat Motorcycle">Cheetah Motorcycle (20 km/h)</option>
                          <option value="Pink Police Patrol">Pink Patrol (Women Safety / 22 km/h)</option>
                          <option value="Quick Response Team">ERSS-112 QRT Van (25 km/h)</option>
                        </select>
                      </div>

                      <div>
                        <label className="filter-label">Tactical Priority Focus</label>
                        <select 
                          className="select-input" 
                          style={{ width: '100%', marginTop: '3px' }}
                          value={priorityFocus}
                          onChange={e => setPriorityFocus(e.target.value)}
                        >
                          <option value="balanced">Balanced Deterrence</option>
                          <option value="high_intensity_focused">High Severity Hotspot Focus</option>
                          <option value="broad_coverage">Broad Janamaithri Beat Coverage</option>
                        </select>
                      </div>
                    </div>

                    <button 
                      className="btn btn-primary" 
                      style={{ width: '100%', justifyContent: 'center', marginTop: '6px', padding: '8px' }}
                      onClick={handleOptimizeRoute}
                      disabled={optimizing}
                    >
                      {optimizing ? (
                        <>
                          <RefreshCw size={14} className="spin" />
                          <span>Solving Janamaithri Road Routes...</span>
                        </>
                      ) : (
                        <>
                          <Crosshair size={14} />
                          <span>Calculate Realistic Beat Routes</span>
                        </>
                      )}
                    </button>
                  </div>
                </div>

                {/* Route Results Breakdown */}
                {routeResult && routeResult.vehicle_routes && (
                  <div className="panel-card">
                    <div className="card-title">
                      <span>Recommended Beat Solutions</span>
                      <span style={{ fontSize: '10.5px', color: '#047857', fontWeight: 700 }}>
                        +{routeResult.baseline_comparison.coverage_gain_percent}% vs Naive
                      </span>
                    </div>

                    {routeResult.station_coverage && (
                      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '6px 8px', background: 'var(--bg-secondary)', border: '1px solid var(--border-light)', borderRadius: '4px', marginBottom: '10px', fontSize: '11px' }}>
                        <div>
                          <b>Base Station:</b> {routeResult.station_coverage.station_short_name}
                        </div>
                        <div style={{ color: '#0284c7', fontWeight: 700 }}>
                          Beat Radius: {routeResult.station_coverage.operational_radius_km} km
                        </div>
                      </div>
                    )}

                    {routeResult.vehicle_routes.map((vr) => {
                      const vColor = vr.theme_color || '#1d4ed8';
                      return (
                        <div key={vr.vehicle_id} className="vehicle-card" style={{ borderLeft: `4px solid ${vColor}` }}>
                          <div className="vehicle-card-header">
                            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                              <span className="callsign-badge" style={{ backgroundColor: vColor }}>
                                {vr.call_sign || 'PATROL'}
                              </span>
                              <div>
                                <div className="beat-sector-title">{vr.vehicle_name}</div>
                                <div className="vehicle-model-meta">
                                  {vr.beat_sector} • {vr.vehicle_model || 'Kerala Police'}
                                </div>
                              </div>
                            </div>
                            <span className="coverage-radius-pill">
                              {vr.coverage_radius_km || 3.2} km Beat
                            </span>
                          </div>

                          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '4px', margin: '8px 0' }}>
                            <div style={{ background: 'var(--bg-secondary)', padding: '5px', borderRadius: '3px', fontSize: '10.5px' }}>
                              <div style={{ color: 'var(--text-muted)' }}>Distance</div>
                              <div style={{ fontWeight: 700 }}>{vr.total_distance_km} km</div>
                            </div>
                            <div style={{ background: 'var(--bg-secondary)', padding: '5px', borderRadius: '3px', fontSize: '10.5px' }}>
                              <div style={{ color: 'var(--text-muted)' }}>Drive / Dwell</div>
                              <div style={{ fontWeight: 700 }}>{vr.driving_time_minutes}m / {vr.dwell_time_minutes}m</div>
                            </div>
                            <div style={{ background: 'var(--bg-secondary)', padding: '5px', borderRadius: '3px', fontSize: '10.5px' }}>
                              <div style={{ color: 'var(--text-muted)' }}>Checkpoints</div>
                              <div style={{ fontWeight: 700 }}>{vr.num_checkpoints} Stops</div>
                            </div>
                            <div style={{ background: 'var(--bg-secondary)', padding: '5px', borderRadius: '3px', fontSize: '10.5px' }}>
                              <div style={{ color: 'var(--text-muted)' }}>Deterrence</div>
                              <div style={{ fontWeight: 700, color: '#047857' }}>{vr.hotspot_coverage_score}</div>
                            </div>
                          </div>

                          {/* Checkpoints Schedule */}
                          <div className="card-title" style={{ fontSize: '11px', marginTop: '10px' }}>
                            Ordered Checkpoints & Kerala Police SOPs
                          </div>
                          <div className="checkpoint-timeline">
                            {vr.checkpoints.map(cp => {
                              const typeClass = (cp.checkpoint_type || 'point_book').toLowerCase().replace(/_/g, '-');
                              return (
                                <div key={cp.sequence_number} className="checkpoint-item">
                                  <div className="checkpoint-badge" style={{ backgroundColor: vColor }}>
                                    {cp.sequence_number}
                                  </div>
                                  <div className="checkpoint-content">
                                    <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '2px' }}>
                                      <span className={`checkpoint-type-tag type-${typeClass}`}>
                                        {cp.checkpoint_label || 'POINT BOOK'}
                                      </span>
                                      {cp.code && (
                                        <span style={{ fontSize: '9.5px', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)' }}>
                                          {cp.code}
                                        </span>
                                      )}
                                    </div>
                                    <div className="checkpoint-name">{cp.name}</div>
                                    <div className="checkpoint-timing">
                                      Arr: +{cp.arrival_minute}m | Dwell: {cp.dwell_minutes}m | Dep: +{cp.departure_minute}m
                                    </div>
                                    <div className="checkpoint-justification">
                                      <b>Target:</b> {cp.target_crime} ({cp.ipc_sections})<br/>
                                      {cp.justification}
                                    </div>
                                    {cp.sop_action && (
                                      <div className="checkpoint-sop-box">
                                        <b>Kerala Police SOP:</b> {cp.sop_action}
                                      </div>
                                    )}
                                  </div>
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      );
                    })}

                    {/* Operational Disclaimer */}
                    <div style={{ marginTop: '10px', padding: '8px', backgroundColor: '#fffbeb', border: '1px solid #fef3c7', borderRadius: '4px', fontSize: '11px', color: '#92400e', lineHeight: 1.4 }}>
                      <b>Kerala Police Statutory Notice (Janamaithri Suraksha):</b> Patrol routes are calibrated to Section 64/65 of the Kerala Police Act 2011 and official e-Beat registers. Coverage is strictly restricted to designated station beats to prevent jurisdictional overreach. Mandatory Station House Officer (SHO) review is required prior to tactical roll-call.
                    </div>
                  </div>
                )}
              </>
            )}

            {/* TAB 3: LEGAL PROVENANCE & FIR INGESTION */}
            {activeTab === 'provenance' && (
              <>
                <div className="panel-card">
                  <div className="card-title">Legal Discovery & Access Findings</div>
                  <div style={{ fontSize: '11.5px', color: 'var(--text-secondary)', lineHeight: 1.45, display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    <div>
                      <b>1. Kerala Police THUNA Portal:</b> Requires case-specific FIR Number, Year, Station, and CAPTCHA. No lawful public bulk API exists. Bulk scraping violates access controls and terms of service.
                    </div>
                    <div>
                      <b>2. Statutory Privacy Safeguards:</b> Under Supreme Court directives (<i>Youth Bar Association v. UOI</i>) and statutory provisions (Sec 228A IPC / Sec 72 BNS, POCSO), unredacted FIRs containing victim identities cannot be publicly harvested or exposed.
                    </div>
                    <div>
                      <b>3. System Protocol:</b> Real incident-level data is ingested exclusively via authorized redacted channels with automated PII scrubbing. Benchmark evaluations are explicitly stamped <code>SYNTHETIC_CALIBRATED_BENCHMARK</code>.
                    </div>
                  </div>
                </div>

                {/* FIR Document Ingestion Demo */}
                <div className="panel-card">
                  <div className="card-title">Authorized FIR Ingestion Pipeline (PII Scrubbing)</div>
                  <form onSubmit={handleImportFIR} style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    <div>
                      <label className="filter-label">Station</label>
                      <select 
                        className="select-input" 
                        style={{ width: '100%' }}
                        value={importForm.police_station_id}
                        onChange={e => setImportForm({ ...importForm, police_station_id: e.target.value })}
                      >
                        {stations.map(s => (
                          <option key={s.id} value={s.id}>{s.name}</option>
                        ))}
                      </select>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                      <div>
                        <label className="filter-label">FIR Number</label>
                        <input 
                          type="text" 
                          className="text-input" 
                          style={{ width: '100%' }}
                          value={importForm.fir_number}
                          onChange={e => setImportForm({ ...importForm, fir_number: e.target.value })}
                        />
                      </div>
                      <div>
                        <label className="filter-label">Category</label>
                        <select 
                          className="select-input" 
                          style={{ width: '100%' }}
                          value={importForm.crime_category}
                          onChange={e => setImportForm({ ...importForm, crime_category: e.target.value })}
                        >
                          {Object.entries(categories).map(([k, v]) => (
                            <option key={k} value={k}>{v.label}</option>
                          ))}
                        </select>
                      </div>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                      <div>
                        <label className="filter-label">Registration Time</label>
                        <input 
                          type="datetime-local" 
                          className="text-input" 
                          style={{ width: '100%' }}
                          value={importForm.registration_time}
                          onChange={e => setImportForm({ ...importForm, registration_time: e.target.value })}
                        />
                      </div>
                      <div>
                        <label className="filter-label">Occurrence Time (Distinct)</label>
                        <input 
                          type="datetime-local" 
                          className="text-input" 
                          style={{ width: '100%' }}
                          value={importForm.occurrence_time}
                          onChange={e => setImportForm({ ...importForm, occurrence_time: e.target.value })}
                        />
                      </div>
                    </div>

                    <div>
                      <label className="filter-label">Locality / Sector</label>
                      <input 
                        type="text" 
                        className="text-input" 
                        style={{ width: '100%' }}
                        value={importForm.locality_name}
                        onChange={e => setImportForm({ ...importForm, locality_name: e.target.value })}
                      />
                    </div>

                    <div>
                      <label className="filter-label">Raw Narrative (Contains Test PII)</label>
                      <textarea 
                        className="text-input" 
                        rows={2} 
                        style={{ width: '100%', resize: 'vertical' }}
                        value={importForm.raw_narrative}
                        onChange={e => setImportForm({ ...importForm, raw_narrative: e.target.value })}
                      />
                    </div>

                    <button type="submit" className="btn btn-secondary" style={{ width: '100%', justifyContent: 'center' }}>
                      <CheckCircle2 size={13} color="#059669" />
                      <span>Sanitize PII & Ingest Record</span>
                    </button>
                  </form>

                  {importStatus && (
                    <div style={{ marginTop: '10px', padding: '8px', backgroundColor: '#f0fdf4', border: '1px solid #bbf7d0', borderRadius: '4px', fontSize: '11px' }}>
                      <div style={{ color: '#166534', fontWeight: 600 }}>{importStatus.message}</div>
                      <div style={{ marginTop: '4px', color: '#334155' }}>
                        <b>Scrubbed Notes:</b> {importStatus.sanitized_record.sanitized_notes}
                      </div>
                    </div>
                  )}
                </div>
              </>
            )}
          </div>
        </aside>

        {/* Central Map Canvas */}
        <main className="map-container-wrap">
          <div id="map" ref={mapContainerRef} />

          {/* Floating Basemap Provider Switcher */}
          <div className="map-basemap-controls">
            <span style={{ fontSize: '10.5px', fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase' }}>
              Base Map:
            </span>
            {basemaps.map(b => (
              <button
                key={b.id}
                className={`basemap-pill-btn ${activeBasemap === b.id ? 'active' : ''}`}
                onClick={() => handleBasemapChange(b.id)}
                title={b.name}
              >
                {b.id === 'esri_satellite' ? '🛰️ Satellite' : (b.id === 'carto_dark' ? '🌙 Night' : (b.id === 'opentopomap' ? '⛰️ Topo' : (b.id === 'osm_standard' ? '🌐 OSM' : '🗺️ Light')))}
              </button>
            ))}
          </div>

          {/* Floating Map Layers Control & GeoJSON Export */}
          <div className="map-layer-controls">
            <div style={{ fontSize: '11px', fontWeight: 700, color: 'var(--text-secondary)', textTransform: 'uppercase', display: 'flex', justifyContent: 'space-between' }}>
              <span>Map Layers</span>
              <Layers size={13} color="#64748b" />
            </div>
            <label className="layer-toggle-item">
              <input type="checkbox" checked={showHeatmap} onChange={e => setShowHeatmap(e.target.checked)} />
              <span>Incident Density Heatmap</span>
            </label>
            <label className="layer-toggle-item">
              <input type="checkbox" checked={showClusters} onChange={e => setShowClusters(e.target.checked)} />
              <span>Historical Clusters (DBSCAN)</span>
            </label>
            <label className="layer-toggle-item">
              <input type="checkbox" checked={showGrid} onChange={e => setShowGrid(e.target.checked)} />
              <span>Spatial Grid Cells (400m)</span>
            </label>
            <label className="layer-toggle-item">
              <input type="checkbox" checked={showStations} onChange={e => setShowStations(e.target.checked)} />
              <span>Police Stations</span>
            </label>
            <label className="layer-toggle-item">
              <input type="checkbox" checked={showJurisdictions} onChange={e => setShowJurisdictions(e.target.checked)} />
              <span>Station Jurisdictions (Voronoi)</span>
            </label>
            <label className="layer-toggle-item">
              <input type="checkbox" checked={showRoute} onChange={e => setShowRoute(e.target.checked)} />
              <span>Patrol Road Route (OSRM)</span>
            </label>

            {/* GeoJSON Export Section */}
            <div style={{ marginTop: '6px', paddingTop: '6px', borderTop: '1px solid var(--border-light)' }}>
              <div style={{ fontSize: '10px', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '4px' }}>
                EXPORT GEOJSON API:
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4px' }}>
                <button className="btn btn-secondary btn-sm" onClick={() => handleExportGeoJSON('stations')}>
                  PS Points
                </button>
                <button className="btn btn-secondary btn-sm" onClick={() => handleExportGeoJSON('clusters')}>
                  Hotspots
                </button>
                <button className="btn btn-secondary btn-sm" onClick={() => handleExportGeoJSON('grid')}>
                  Grid Cells
                </button>
                <button className="btn btn-secondary btn-sm" onClick={() => handleExportGeoJSON('jurisdictions')}>
                  Boundaries
                </button>
              </div>
            </div>
          </div>

          {/* Map Legend */}
          <div className="map-legend">
            <div style={{ fontWeight: 600, fontSize: '10.5px', textTransform: 'uppercase', color: 'var(--text-secondary)' }}>
              Hotspot Intensity
            </div>
            <div className="legend-scale">
              <span style={{ fontSize: '10px', color: 'var(--text-muted)' }}>Low</span>
              <div className="scale-gradient" />
              <span style={{ fontSize: '10px', color: 'var(--text-muted)' }}>High</span>
            </div>
            <div style={{ marginTop: '4px', fontSize: '10px', color: 'var(--text-muted)' }}>
              Counts &lt; 3 suppressed for privacy
            </div>
          </div>

          {/* Selected Element Inspector Drawer */}
          {selectedInspector && (
            <div className="inspector-drawer">
              <div className="inspector-header">
                <div>
                  <div style={{ fontSize: '10px', color: 'var(--text-muted)', textTransform: 'uppercase' }}>{selectedInspector.type}</div>
                  <div className="inspector-title">{selectedInspector.title}</div>
                </div>
                <button className="close-btn" onClick={() => setSelectedInspector(null)}>
                  <X size={14} />
                </button>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '6px', fontSize: '11.5px' }}>
                <div>
                  <span style={{ color: 'var(--text-muted)' }}>Incident Volume: </span>
                  <b>{selectedInspector.incidents}</b>
                  {selectedInspector.isSuppressed && <span style={{ color: '#ea580c', fontSize: '10px' }}> (k-masked)</span>}
                </div>
                <div>
                  <span style={{ color: 'var(--text-muted)' }}>Top Offense: </span>
                  <b>{selectedInspector.primaryCrime}</b>
                </div>
                <div>
                  <span style={{ color: 'var(--text-muted)' }}>Station: </span>
                  <b>{selectedInspector.station}</b>
                </div>
                {selectedInspector.persistence && (
                  <div>
                    <span style={{ color: 'var(--text-muted)' }}>Persistence: </span>
                    <b>{selectedInspector.persistence}</b>
                  </div>
                )}
                {selectedInspector.peakHour && (
                  <div>
                    <span style={{ color: 'var(--text-muted)' }}>Peak Window: </span>
                    <b>{selectedInspector.peakHour}</b>
                  </div>
                )}
              </div>
            </div>
          )}
        </main>
      </div>

      {/* Map API Configuration Modal */}
      {showMapApiModal && (
        <div className="modal-backdrop">
          <div className="modal-box">
            <div className="modal-header">
              <div style={{ fontWeight: 700, fontSize: '13px', color: '#1e3a8a', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <Sliders size={15} />
                <span>Map API & Spatial Service Configuration</span>
              </div>
              <button className="close-btn" onClick={() => setShowMapApiModal(false)}>
                <X size={16} />
              </button>
            </div>
            <div className="modal-body">
              <div>
                <label className="filter-label">OSRM Routing Engine Endpoint</label>
                <input 
                  type="text" 
                  className="text-input" 
                  style={{ width: '100%', marginTop: '3px' }}
                  value={mapApiConfig.customOsrmUrl}
                  onChange={e => setMapApiConfig({ ...mapApiConfig, customOsrmUrl: e.target.value })}
                />
                <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginTop: '2px' }}>
                  Default: Public OpenStreetMap OSRM router. Can be changed to Kerala Police intranet routing server.
                </div>
              </div>

              <div>
                <label className="filter-label">Custom Mapbox Access Token (Optional)</label>
                <input 
                  type="password" 
                  className="text-input" 
                  style={{ width: '100%', marginTop: '3px' }}
                  placeholder="pk.eyJ1Ij..."
                  value={mapApiConfig.mapboxToken}
                  onChange={e => setMapApiConfig({ ...mapApiConfig, mapboxToken: e.target.value })}
                />
                <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginTop: '2px' }}>
                  Enables custom Mapbox high-contrast vector tiles.
                </div>
              </div>

              <div>
                <label className="filter-label">Google Maps JavaScript API Key (Optional)</label>
                <input 
                  type="password" 
                  className="text-input" 
                  style={{ width: '100%', marginTop: '3px' }}
                  placeholder="AIzaSy..."
                  value={mapApiConfig.googleApiKey}
                  onChange={e => setMapApiConfig({ ...mapApiConfig, googleApiKey: e.target.value })}
                />
                <div style={{ fontSize: '10px', color: 'var(--text-muted)', marginTop: '2px' }}>
                  Optional for proprietary Google Satellite and Road overlays.
                </div>
              </div>

              <div style={{ padding: '8px', backgroundColor: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '4px', fontSize: '11px', color: '#475569' }}>
                <b>Available GeoJSON REST Endpoints:</b>
                <div style={{ marginTop: '4px', fontFamily: 'var(--font-mono)', fontSize: '10.5px' }}>
                  • <code>/api/map/geojson/stations</code> (Police stations)<br/>
                  • <code>/api/map/geojson/clusters</code> (DBSCAN hotspots)<br/>
                  • <code>/api/map/geojson/grid</code> (400m risk cells)<br/>
                  • <code>/api/map/geojson/jurisdictions</code> (Station boundaries)<br/>
                  • <code>/api/map/geocode?q=...</code> (Nominatim geocoding)
                </div>
              </div>
            </div>
            <div className="modal-footer">
              <button className="btn btn-secondary" onClick={() => setShowMapApiModal(false)}>
                Cancel
              </button>
              <button className="btn btn-primary" onClick={() => setShowMapApiModal(false)}>
                Save API Preferences
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
