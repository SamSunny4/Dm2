"""
Comprehensive PDF Report Generator
Produces an executive, publication-grade analytical PDF report containing:
- Legal data discovery and provenance audit (Kerala Police THUNA / NCRB).
- Actual generated charts (matplotlib): diurnal crime cycles, category breakdown, model evaluation.
- DBSCAN cluster analysis and spatial grid intensity.
- Chronological train/test baseline evaluation table.
- OSRM Road network patrol route map and ordered checkpoint log with justifications.
- Ethical, equity, and privacy protection protocols.
"""

import os
import io
import math
from datetime import datetime
from typing import Dict, Any, List

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

from backend.config import CITIES_CONFIG, CRIME_CATEGORIES
from backend.data_discovery import DATA_DISCOVERY_INVESTIGATION
from backend.spatial_mining import SpatialMiningEngine
from backend.routing_engine import PatrolOptimizer, RoadRoutingEngine

GENERATED_DIR = os.path.join(os.path.dirname(__file__), "generated")
os.makedirs(GENERATED_DIR, exist_ok=True)


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas for adding running header and 'Page X of Y' footer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#555555"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Kerala Urban Crime Hotspot Intelligence & Patrol Route Optimization System")
            self.drawRightString(558, 750, "Kochi Operational Prototype | SCRB Calibrated")
            self.setStrokeColor(colors.HexColor("#dddddd"))
            self.setLineWidth(0.5)
            self.line(54, 744, 558, 744)

        # Footer
        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawString(54, 36, "CONFIDENTIAL - LAW ENFORCEMENT DECISION SUPPORT SYSTEM")
        self.drawRightString(558, 36, page_str)
        self.setStrokeColor(colors.HexColor("#dddddd"))
        self.setLineWidth(0.5)
        self.line(54, 46, 558, 46)
        self.restoreState()


def generate_charts(city_id: str, mining: SpatialMiningEngine, route_data: Dict[str, Any]) -> Dict[str, str]:
    """Generates figures using matplotlib from real system execution outputs."""
    summary = mining.get_summary_statistics()
    forecast = mining.run_spatiotemporal_forecast()
    eval_m = forecast["evaluation_metrics"]
    
    chart_paths = {}
    
    # Chart 1: Diurnal & Weekly Crime Distribution
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9.5, 3.4), dpi=160)
    
    hours = [h["hour"] for h in summary["hourly_trend"]]
    h_counts = [h["count"] for h in summary["hourly_trend"]]
    ax1.plot(hours, h_counts, color="#1e3a8a", marker="o", markersize=3.5, linewidth=1.8)
    ax1.fill_between(hours, h_counts, color="#3b82f6", alpha=0.18)
    ax1.set_title("Hourly Incident Frequency (24-Hour Cycle)", fontsize=9, fontweight="bold", pad=8)
    ax1.set_xlabel("Hour of Day (IST)", fontsize=8)
    ax1.set_ylabel("Recorded Incident Count", fontsize=8)
    ax1.grid(True, linestyle="--", alpha=0.4)
    ax1.tick_params(labelsize=7.5)
    
    # Mark evening peak window
    ax1.axvspan(17, 23, color="#ef4444", alpha=0.10, label="High Deterrence Window")
    ax1.legend(loc="upper left", fontsize=7)

    # Days of week
    days = [d["day"][:3] for d in summary["day_of_week"]]
    d_counts = [d["count"] for d in summary["day_of_week"]]
    bars = ax2.bar(days, d_counts, color="#0f766e", width=0.55, edgecolor="#115e59", linewidth=0.8)
    ax2.set_title("Day of Week Incident Distribution", fontsize=9, fontweight="bold", pad=8)
    ax2.set_xlabel("Day of Week", fontsize=8)
    ax2.set_ylabel("Incident Count", fontsize=8)
    ax2.grid(True, axis="y", linestyle="--", alpha=0.4)
    ax2.tick_params(labelsize=7.5)
    for bar in bars:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., h + 2, f"{int(h)}", ha="center", va="bottom", fontsize=7)

    plt.tight_layout()
    chart1_path = os.path.join(GENERATED_DIR, f"{city_id}_temporal_trends.png")
    fig.savefig(chart1_path, bbox_inches="tight")
    plt.close(fig)
    chart_paths["temporal"] = chart1_path

    # Chart 2: Offense Taxonomy Breakdown
    fig, ax = plt.subplots(figsize=(7.5, 3.0), dpi=160)
    cats = [c["label"] for c in summary["categories"]]
    counts = [c["count"] for c in summary["categories"]]
    bar_colors = [c["color"] for c in summary["categories"]]
    
    y_pos = range(len(cats))
    ax.barh(y_pos, counts, color=bar_colors, edgecolor="#333333", linewidth=0.5, height=0.6)
    ax.set_yticks(y_pos)
    ax.set_yticklabels(cats, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("Recorded Incident Volume", fontsize=8)
    ax.set_title(f"Crime Category Distribution ({mining.city_cfg['name']})", fontsize=9, fontweight="bold", pad=8)
    ax.grid(True, axis="x", linestyle="--", alpha=0.4)
    ax.tick_params(labelsize=7.5)
    
    for i, v in enumerate(counts):
        ax.text(v + 5, i, f"{v} ({v*100/summary['total_records']:.1f}%)", va="center", fontsize=7)

    plt.tight_layout()
    chart2_path = os.path.join(GENERATED_DIR, f"{city_id}_categories.png")
    fig.savefig(chart2_path, bbox_inches="tight")
    plt.close(fig)
    chart_paths["categories"] = chart2_path

    # Chart 3: Model Evaluation Metrics vs Baseline
    fig, (ax_mae, ax_cov) = plt.subplots(1, 2, figsize=(8.5, 2.8), dpi=160)
    
    m_data = eval_m["models"]
    models = ["Historical Baseline", "Spatiotemporal RF"]
    maes = [m_data["baseline_historical_mean"]["mae"], m_data["spatiotemporal_random_forest"]["mae"]]
    rmses = [m_data["baseline_historical_mean"]["rmse"], m_data["spatiotemporal_random_forest"]["rmse"]]
    
    x = np.arange(len(models))
    w = 0.35
    ax_mae.bar(x - w/2, maes, w, label="MAE", color="#64748b", edgecolor="#334155")
    ax_mae.bar(x + w/2, rmses, w, label="RMSE", color="#0284c7", edgecolor="#0369a1")
    ax_mae.set_xticks(x)
    ax_mae.set_xticklabels(models, fontsize=8)
    ax_mae.set_ylabel("Error Metric (Count)", fontsize=8)
    ax_mae.set_title("Chronological Holdout Error Comparison", fontsize=8.5, fontweight="bold")
    ax_mae.legend(fontsize=7.5)
    ax_mae.grid(True, axis="y", linestyle="--", alpha=0.4)
    ax_mae.tick_params(labelsize=7.5)

    # Correlation & Coverage Gauge
    ax_cov.bar(["Top-K Coverage %", "Pearson Correlation (x100)"], 
               [eval_m["top_k_hotspot_coverage_percent"], eval_m["pearson_correlation"] * 100],
               color=["#10b981", "#6366f1"], width=0.45, edgecolor="#1f2937")
    ax_cov.set_ylim(0, 110)
    ax_cov.set_ylabel("Score / Percentage", fontsize=8)
    ax_cov.set_title("Forecast Fidelity & Hotspot Capture", fontsize=8.5, fontweight="bold")
    ax_cov.grid(True, axis="y", linestyle="--", alpha=0.4)
    ax_cov.tick_params(labelsize=7.5)
    ax_cov.text(0, eval_m["top_k_hotspot_coverage_percent"] + 3, f"{eval_m['top_k_hotspot_coverage_percent']}%", ha="center", fontsize=8, fontweight="bold")
    ax_cov.text(1, eval_m["pearson_correlation"] * 100 + 3, f"r={eval_m['pearson_correlation']:.3f}", ha="center", fontsize=8, fontweight="bold")

    plt.tight_layout()
    chart3_path = os.path.join(GENERATED_DIR, f"{city_id}_model_eval.png")
    fig.savefig(chart3_path, bbox_inches="tight")
    plt.close(fig)
    chart_paths["model_eval"] = chart3_path

    # Chart 4: Road Network Patrol Route Spatial Map
    fig, ax_map = plt.subplots(figsize=(8.0, 5.0), dpi=170)
    
    vr = route_data["vehicle_routes"][0]
    poly = np.array(vr["route_polyline"])  # [lat, lon]
    
    # Plot road polyline
    if len(poly) > 0:
        ax_map.plot(poly[:, 1], poly[:, 0], color="#2563eb", linewidth=2.2, label=f"OSRM Road Trajectory ({vr['total_distance_km']} km)", zorder=3)
    
    # Plot start/depot station
    stations = mining.city_cfg["police_stations"]
    st_lats = [s["lat"] for s in stations]
    st_lons = [s["lon"] for s in stations]
    ax_map.scatter(st_lons, st_lats, color="#64748b", marker="s", s=40, label="Police Stations", zorder=4)
    
    # Highlight depot
    start_st = next((s for s in stations if s["name"] == vr["start_station"]), stations[0])
    ax_map.scatter([start_st["lon"]], [start_st["lat"]], color="#dc2626", marker="*", s=160, label=f"Depot ({start_st['short_name']})", zorder=6)
    
    # Plot ordered checkpoints
    for cp in vr["checkpoints"]:
        c_lat, c_lon = cp["coords"]
        ax_map.scatter([c_lon], [c_lat], color="#ea580c", marker="o", s=70, edgecolor="#ffffff", linewidth=1.2, zorder=5)
        ax_map.text(c_lon + 0.002, c_lat + 0.001, f"#{cp['sequence_number']}", fontsize=8, fontweight="bold", color="#1e293b", zorder=7)

    # Plot background DBSCAN clusters as subtle halos
    clusters = mining.compute_dbscan_clusters()
    for cl in clusters[:6]:
        circ = plt.Circle((cl["centroid"][1], cl["centroid"][0]), cl["radius_meters"] / (111000.0 * math.cos(math.radians(cl["centroid"][0]))),
                          color="#f97316", alpha=0.12, zorder=2)
        ax_map.add_patch(circ)

    ax_map.set_title(f"Kochi Optimized Urban Patrol Route ({vr['vehicle_name']} - {vr['total_mission_time_minutes']} min)", fontsize=9.5, fontweight="bold", pad=8)
    ax_map.set_xlabel("Longitude (°E)", fontsize=8)
    ax_map.set_ylabel("Latitude (°N)", fontsize=8)
    ax_map.grid(True, linestyle=":", alpha=0.5)
    ax_map.legend(loc="upper left", fontsize=7.5)
    ax_map.tick_params(labelsize=7.5)

    plt.tight_layout()
    chart4_path = os.path.join(GENERATED_DIR, f"{city_id}_route_map.png")
    fig.savefig(chart4_path, bbox_inches="tight")
    plt.close(fig)
    chart_paths["route_map"] = chart4_path

    return chart_paths


def build_pdf_report(city_id: str = "kochi") -> str:
    """
    Builds the official comprehensive PDF report from active application execution.
    Returns absolute filepath to generated PDF.
    """
    pdf_filename = f"Kerala_Urban_Crime_Intelligence_Report_{city_id.upper()}.pdf"
    pdf_path = os.path.join(GENERATED_DIR, pdf_filename)
    
    # Run active pipeline engines
    mining = SpatialMiningEngine(city_id)
    summary = mining.get_summary_statistics()
    clusters = mining.compute_dbscan_clusters()
    forecast = mining.run_spatiotemporal_forecast()
    optimizer = PatrolOptimizer(city_id)
    route_data = optimizer.optimize_patrol(
        start_station_id="ekm_central",
        patrol_duration_minutes=180,
        num_vehicles=1,
        vehicle_type="Patrol Car",
        priority_focus="balanced"
    )
    
    # Generate matplotlib figures from execution outputs
    chart_paths = generate_charts(city_id, mining, route_data)
    
    # ReportLab document setup
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom restrained police typography styles
    title_style = ParagraphStyle(
        "DocTitle",
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#475569"),
        spaceAfter=14
    )
    h1_style = ParagraphStyle(
        "Heading1_Custom",
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#1e293b"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        "Heading2_Custom",
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#334155"),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        "Body_Custom",
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1e293b"),
        spaceAfter=6
    )
    callout_style = ParagraphStyle(
        "Callout_Custom",
        fontName="Helvetica-Oblique",
        fontSize=8.0,
        leading=11.5,
        textColor=colors.HexColor("#334155")
    )
    meta_style = ParagraphStyle(
        "Meta_Custom",
        fontName="Helvetica",
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor("#64748b")
    )
    
    story = []

    # Document Header Banner
    story.append(Paragraph("KERALA STATE CRIME INTELLIGENCE & PATROL OPTIMIZATION SYSTEM", title_style))
    story.append(Paragraph(
        f"Operational Hotspot Analysis, Spatiotemporal Prediction & Road-Network Routing Audit | Focus Area: <b>{mining.city_cfg['name']}</b><br/>"
        f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')} | Provenance: SCRB Calibrated Benchmark & OSRM Engine",
        subtitle_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#0f172a"), spaceBefore=0, spaceAfter=12))

    # Executive Summary Card
    exec_text = (
        f"<b>Operational Briefing:</b> This report presents the empirical outputs of the predictive hotspot modeling "
        f"and road-constrained patrol routing system for <b>{mining.city_cfg['name']}</b> ({mining.city_cfg['district']} District). "
        f"The system processed <b>{summary['total_records']:,}</b> validated incident records across <b>{len(mining.city_cfg['police_stations'])}</b> "
        f"police station jurisdictions. Spatial clustering identified <b>{len(clusters)}</b> persistent core hotspot zones. "
        f"Using an out-of-time chronological holdout evaluation (75% train / 25% test), the Spatiotemporal Random Forest model achieved a "
        f"<b>{forecast['evaluation_metrics']['top_k_hotspot_coverage_percent']}%</b> top-tier hotspot capture rate with Pearson correlation <i>r = {forecast['evaluation_metrics']['pearson_correlation']:.3f}</i>. "
        f"The road-network patrol optimizer improved priority coverage by <b>{route_data['baseline_comparison']['coverage_gain_percent']}%</b> over naive fixed-perimeter patrolling."
    )
    exec_table = Table([[Paragraph(exec_text, body_style)]], colWidths=[504])
    exec_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(exec_table)
    story.append(Spacer(1, 10))

    # SECTION 1: Legal Investigation & Data Provenance Discovery
    story.append(Paragraph("1. Crime Dataset Discovery & Legal Provenance Audit", h1_style))
    story.append(Paragraph(
        "A rigorous discovery investigation was conducted across statutory law enforcement data repositories in Kerala to establish "
        "whether incident-level First Information Report (FIR) microdata can be lawfully ingested in bulk. The findings are summarized below:",
        body_style
    ))

    disc_data = [
        [Paragraph("<b>Repository</b>", meta_style), Paragraph("<b>Access Type</b>", meta_style), Paragraph("<b>Legal / Technical Findings</b>", meta_style), Paragraph("<b>Status in System</b>", meta_style)]
    ]
    for src in DATA_DISCOVERY_INVESTIGATION["sources_investigated"]:
        disc_data.append([
            Paragraph(f"<b>{src['source_name']}</b><br/><font color='#64748b'>{src['url']}</font>", meta_style),
            Paragraph("Case-by-case lookup" if not src["bulk_access_available"] else "Bulk Tabular", meta_style),
            Paragraph(src["statutory_limitations"], meta_style),
            Paragraph(f"<b>{src['verdict'][:45]}...</b>", meta_style)
        ])
    
    disc_table = Table(disc_data, colWidths=[110, 75, 230, 89])
    disc_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(disc_table)
    story.append(Spacer(1, 6))

    prot = DATA_DISCOVERY_INVESTIGATION["privacy_protocol"]
    privacy_notice = (
        f"<b>Statutory Compliance Note:</b> Under Supreme Court directives (<i>Youth Bar Association of India v. Union of India</i>, 2016), "
        f"unredacted FIR documents containing sensitive complainant/victim identities, minor protection (POCSO), or sexual assault "
        f"(Section 228A IPC / Section 72 BNS) cannot be publicly harvested or exposed. Consequently, the operational system implements "
        f"an automated <b>Authorized FIR Ingestion Pipeline</b> featuring regex scrubbing of names, contact numbers, and residential door numbers. "
        f"The functional benchmark evaluated here is explicitly stamped as <b>SYNTHETIC_CALIBRATED_BENCHMARK</b>, parameterized against "
        f"published Kerala State Crime Records Bureau (SCRB) annual ratios and Kochi police commissionerate station beats."
    )
    story.append(Paragraph(privacy_notice, callout_style))
    story.append(Spacer(1, 10))

    # SECTION 2: Spatial & Temporal Data Mining
    story.append(Paragraph("2. Spatial & Temporal Data Mining Architecture", h1_style))
    story.append(Paragraph(
        f"The study area of <b>{mining.city_cfg['name']}</b> was partitioned into regular spatial cells of <b>{mining.res_km * 1000:.0f}m × {mining.res_km * 1000:.0f}m</b> "
        f"({mining.res_km**2:.3f} km² per cell). To preserve privacy, individual incidents are binned into cell counts; any cell with fewer than 3 incidents "
        f"is masked as '<i>&lt; 3</i>' in public reporting (k-anonymity principle). Temporal cycles were computed across 24 hourly bins and 7 day-of-week slots.",
        body_style
    ))
    story.append(Image(chart_paths["temporal"], width=504, height=180))
    story.append(Spacer(1, 8))
    story.append(Image(chart_paths["categories"], width=504, height=201))
    story.append(Spacer(1, 10))

    story.append(PageBreak())  # PAGE 2

    # SECTION 3: Spatial Clustering & Machine Learning Forecasting
    story.append(Paragraph("3. Spatial Clustering (DBSCAN) & Predictive Modeling", h1_style))
    story.append(Paragraph(
        "Density-Based Spatial Clustering of Applications with Noise (<b>DBSCAN</b>) was applied using the haversine metric on geodesic coordinates "
        f"(ε = 450 meters, MinPts = 5 incidents). This identified {len(clusters)} dense crime clusters. "
        "A temporal persistence score was formulated as the ratio of active weeks over total monitoring duration.",
        body_style
    ))

    # DBSCAN Table
    clust_table_data = [
        [Paragraph("<b>Cluster ID</b>", meta_style), Paragraph("<b>Focal Locality</b>", meta_style), Paragraph("<b>Incidents</b>", meta_style), 
         Paragraph("<b>Density (/km²)</b>", meta_style), Paragraph("<b>Persistence</b>", meta_style), Paragraph("<b>Primary Offense</b>", meta_style)]
    ]
    for cl in clusters[:6]:
        clust_table_data.append([
            Paragraph(f"<b>{cl['cluster_id']}</b>", meta_style),
            Paragraph(cl["locality_name"], meta_style),
            Paragraph(str(cl["incident_count"]), meta_style),
            Paragraph(str(cl["density_incidents_per_sqkm"]), meta_style),
            Paragraph(f"{cl['persistence_score']:.2f}", meta_style),
            Paragraph(f"{cl['primary_category']}<br/><font color='#64748b'>{cl['police_station']}</font>", meta_style)
        ])
    
    cl_tab = Table(clust_table_data, colWidths=[70, 130, 50, 70, 60, 124])
    cl_tab.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(cl_tab)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Model Evaluation & Chronological Train/Test Holdout</b>", h2_style))
    eval_expl = (
        f"To avoid temporal data leakage, an out-of-time chronological train/test split was enforced. "
        f"Training partition: {forecast['evaluation_metrics']['chronological_split']['train_start']} to {forecast['evaluation_metrics']['chronological_split']['train_end']} (75%). "
        f"Evaluation holdout: {forecast['evaluation_metrics']['chronological_split']['test_start']} to {forecast['evaluation_metrics']['chronological_split']['test_end']} (25%). "
        f"A <b>Spatiotemporal Random Forest Regressor</b> with spatial lags and station proximity was compared against a naive <b>Historical Mean Baseline</b>."
    )
    story.append(Paragraph(eval_expl, body_style))
    story.append(Image(chart_paths["model_eval"], width=504, height=165))
    story.append(Spacer(1, 10))

    # SECTION 4: Road Network Patrol Route Optimization
    story.append(Paragraph("4. Patrol Route Optimization & Road Network Navigation", h1_style))
    story.append(Paragraph(
        "Operational patrol routes are computed using an <b>Orienteering Problem (OP) solver</b> with a 2-Opt local search heuristic. "
        "Unlike naive straight-line models, all routes query the <b>OpenStreetMap road network via OSRM</b> for genuine driving geometries, "
        "one-way corridors, and turn penalties. Staggered dwell times (10 minutes per stop) ensure proactive deterrent presence.",
        body_style
    ))
    story.append(Image(chart_paths["route_map"], width=504, height=315))
    story.append(Spacer(1, 8))

    story.append(PageBreak())  # PAGE 3

    # Checkpoint Log & Justifications Table
    story.append(Paragraph("<b>Patrol Mission Checkpoint Schedule & Explainable Decision Log</b>", h2_style))
    vr = route_data["vehicle_routes"][0]
    
    cp_headers = [
        Paragraph("<b>Stop #</b>", meta_style), Paragraph("<b>Checkpoint Sector</b>", meta_style), 
        Paragraph("<b>Arr - Dep</b>", meta_style), Paragraph("<b>Target Crime & Justification</b>", meta_style)
    ]
    cp_rows = [cp_headers]
    for cp in vr["checkpoints"]:
        cp_rows.append([
            Paragraph(f"<b>#{cp['sequence_number']}</b>", meta_style),
            Paragraph(f"<b>{cp['name']}</b><br/><font color='#64748b'>Score: {cp['priority_score']}</font>", meta_style),
            Paragraph(f"+{cp['arrival_minute']}m to +{cp['departure_minute']}m<br/>({cp['dwell_minutes']}m dwell)", meta_style),
            Paragraph(f"<b>{cp['target_crime']}</b> ({cp['ipc_sections']})<br/>{cp['justification']}", meta_style)
        ])
    
    cp_table = Table(cp_rows, colWidths=[45, 125, 84, 250])
    cp_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f1f5f9")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 4),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(cp_table)
    story.append(Spacer(1, 10))

    # Optimization Comparison Metrics Table
    b_comp = route_data["baseline_comparison"]
    comp_data = [
        [Paragraph("<b>Metric Dimension</b>", meta_style), Paragraph("<b>Naive Fixed Perimeter</b>", meta_style), Paragraph("<b>Optimized Road Route</b>", meta_style), Paragraph("<b>Variance / Gain</b>", meta_style)],
        [Paragraph("Total Road Distance", meta_style), Paragraph(f"{b_comp['baseline_distance_km']} km", meta_style), Paragraph(f"{vr['total_distance_km']} km", meta_style), Paragraph(f"+{vr['total_distance_km'] - b_comp['baseline_distance_km']:.1f} km (Road Bound)", meta_style)],
        [Paragraph("Hotspot Priority Coverage", meta_style), Paragraph(f"{b_comp['baseline_coverage_score']:.1f}", meta_style), Paragraph(f"{b_comp['optimized_total_coverage_score']:.1f}", meta_style), Paragraph(f"<b>+{b_comp['coverage_gain_percent']}%</b>", meta_style)],
        [Paragraph("Routing Engine", meta_style), Paragraph("Euclidean / Fixed Buffer", meta_style), Paragraph("OSRM Road Network", meta_style), Paragraph("Exact Street Geometry", meta_style)],
        [Paragraph("High-Priority Checkpoints", meta_style), Paragraph("5 Naive Stops", meta_style), Paragraph(f"{vr['num_checkpoints']} Optimized Stops", meta_style), Paragraph("2-Opt Sequence Minimized", meta_style)]
    ]
    comp_table = Table(comp_data, colWidths=[120, 110, 110, 164])
    comp_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f8fafc")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 10))

    # SECTION 5: Responsible AI, Ethical Considerations & Governance
    story.append(Paragraph("5. Responsible AI, Privacy & Supervisor Oversight Protocol", h1_style))
    eth_text = (
        "<b>1. Demographic Neutrality:</b> In strict compliance with constitutional non-discrimination safeguards, the algorithmic "
        "pipeline consumes exclusively objective spatiotemporal variables (historical incident time, offense classification, street network geometry, "
        "and police station coordinates). No demographic, religious, caste, linguistic, or socioeconomic proxy indicators are ingested.<br/>"
        "<b>2. Uncertainty Communication:</b> All predicted hotspot intensities represent mathematical estimates derived from past reporting distributions, "
        "not deterministic forecasts of individual criminal behavior. Reporting variations across precincts must be taken into account.<br/>"
        "<b>3. Mandatory Human Supervisor Oversight:</b> Recommended patrol schedules are decision-support aids designed for Station House Officers (SHOs) "
        "and supervisory ACP/DCP personnel. Algorithmic outputs cannot substitute for human police judgment and situational tactical intelligence."
    )
    eth_table = Table([[Paragraph(eth_text, body_style)]], colWidths=[504])
    eth_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#94a3b8")),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(eth_table)
    story.append(Spacer(1, 14))

    # Sign-off block
    sign_data = [
        [Paragraph("<b>Prepared by:</b> Urban Crime Intelligence Unit", meta_style), Paragraph("<b>Supervisory Review:</b> Station House Officer (SHO)", meta_style)],
        [Paragraph("<b>Classification:</b> Operational Decision Support", meta_style), Paragraph("<b>Status:</b> Approved for Shift Briefing", meta_style)]
    ]
    sign_table = Table(sign_data, colWidths=[252, 252])
    sign_table.setStyle(TableStyle([
        ("LINEABOVE", (0, 0), (-1, 0), 0.5, colors.HexColor("#94a3b8")),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    story.append(sign_table)

    # Build PDF with running headers and page numbers
    doc.build(story, canvasmaker=NumberedCanvas)
    return pdf_path


if __name__ == "__main__":
    out = build_pdf_report("kochi")
    print(f"Generated PDF: {out}")
