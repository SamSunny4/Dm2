"""
Kerala Urban Crime Hotspot Intelligence and Patrol Route Optimization System
Configuration & City Geographical Registries
Calibrated to authentic Kerala Police Janamaithri Suraksha beats, registered Point Books,
and statutory police station jurisdictions.
"""

from typing import Dict, List, Any

CITIES_CONFIG: Dict[str, Dict[str, Any]] = {
    "kochi": {
        "id": "kochi",
        "name": "Kochi (Cochin)",
        "state": "Kerala",
        "district": "Ernakulam",
        "center": [9.9734, 76.2815],
        "default_zoom": 13,
        "bounds": {
            "min_lat": 9.9050,
            "max_lat": 10.0850,
            "min_lon": 76.2200,
            "max_lon": 76.3850
        },
        "grid_resolution_km": 0.40,  # ~400m cell size
        "police_stations": [
            {
                "id": "ekm_central",
                "name": "Ernakulam Central Police Station",
                "short_name": "Central PS",
                "code": "EKM-CEN-01",
                "lat": 9.9734,
                "lon": 76.2815,
                "operational_radius_km": 3.2,
                "jurisdiction": "MG Road, Broadway Commercial Strip, Shenoys, Marine Drive Walkway, High Court Precinct",
                "patrol_vehicles": ["Patrol Car 101", "Beat Motorcycle 12", "Quick Response QRT-1"],
                "janamaithri_beats": [
                    {
                        "beat_id": "ekm_central_b1",
                        "name": "Janamaithri Beat 1 (Marine Drive & Commercial Core)",
                        "sector": "Waterfront / Broadway Market Strip",
                        "call_sign": "ALPHA-1",
                        "vehicle_type": "Station Mobile Patrol (Mahindra Bolero)",
                        "point_books": [
                            {
                                "id": "PB-CEN-01",
                                "name": "Menaka Junction & Shanmugham Road",
                                "coords": [9.9785, 76.2778],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #01",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Sign physical register at merchant kiosk; inspect pedestrian crowds and night bus shelters; maintain high-visibility vigil.",
                                "peak_hour": 19
                            },
                            {
                                "id": "PB-CEN-02",
                                "name": "Broadway Wholesale Market North Entrance",
                                "coords": [9.9808, 76.2812],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #02",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Inspect closed shutter padlocks, foot-patrol narrow merchant alleys, verify night security watchmen.",
                                "peak_hour": 2
                            },
                            {
                                "id": "PB-CEN-03",
                                "name": "Marine Drive Rainbow Walkway & Promenade",
                                "coords": [9.9830, 76.2765],
                                "checkpoint_type": "WOMEN_SAFETY_ZONE",
                                "checkpoint_label": "Promenade Vigil Post (Pink Patrol)",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "Foot patrol along public walkway, eve-teasing deterrence, anti-nuisance inspection near boat jetties.",
                                "peak_hour": 20
                            },
                            {
                                "id": "PB-CEN-04",
                                "name": "High Court / Menaka Ferry Terminal Link",
                                "coords": [9.9852, 76.2785],
                                "checkpoint_type": "TRANSIT_HUB",
                                "checkpoint_label": "Jetty Transit Security Post",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Surveillance of passenger disembarkation, check suspicious baggage, verify auto-rickshaw queue discipline.",
                                "peak_hour": 18
                            }
                        ]
                    },
                    {
                        "beat_id": "ekm_central_b2",
                        "name": "Janamaithri Beat 2 (MG Road & South Arteries)",
                        "sector": "Commercial Arterial & College Zone",
                        "call_sign": "BRAVO-2",
                        "vehicle_type": "Cheetah Beat Motorcycle (Royal Enfield)",
                        "point_books": [
                            {
                                "id": "PB-CEN-05",
                                "name": "Shenoys Junction Commercial Strip",
                                "coords": [9.9708, 76.2828],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #03",
                                "priority_crime": "ASSAULT_AFFRAY",
                                "sop_action": "Retail corridor foot patrol, check closing retail outlets, inspect bank ATM anterooms.",
                                "peak_hour": 21
                            },
                            {
                                "id": "PB-CEN-06",
                                "name": "Jos Junction & Station Approach Road",
                                "coords": [9.9678, 76.2842],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Kavala Checking Point",
                                "priority_crime": "VEHICLE_THEFT",
                                "sop_action": "Vehicle checking naka, check two-wheeler registrations, deter drunken driving and speeding.",
                                "peak_hour": 22
                            },
                            {
                                "id": "PB-CEN-07",
                                "name": "Maharajas College Ground Perimeter",
                                "coords": [9.9722, 76.2858],
                                "checkpoint_type": "WOMEN_SAFETY_ZONE",
                                "checkpoint_label": "Campus Suraksha Post",
                                "priority_crime": "NARCOTICS_NDPS",
                                "sop_action": "Anti-narcotics surveillance around stadium perimeter and hostel gates; student safety check.",
                                "peak_hour": 17
                            },
                            {
                                "id": "PB-CEN-08",
                                "name": "St. Teresa's / Park Avenue Corridor",
                                "coords": [9.9760, 76.2801],
                                "checkpoint_type": "WOMEN_SAFETY_ZONE",
                                "checkpoint_label": "Women Safety Corridor",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "Pink Police surveillance during college dispersal and evening rush; bus waiting shed monitoring.",
                                "peak_hour": 16
                            }
                        ]
                    }
                ]
            },
            {
                "id": "fort_kochi",
                "name": "Fort Kochi Police Station",
                "short_name": "Fort Kochi PS",
                "code": "EKM-FTK-02",
                "lat": 9.9658,
                "lon": 76.2427,
                "operational_radius_km": 2.8,
                "jurisdiction": "Fort Kochi Beach, Vypin Ro-Ro Ferry, Princess St, Heritage Tourism Zone",
                "patrol_vehicles": ["Tourist Police Cruiser", "Coastal Beat 04"],
                "janamaithri_beats": [
                    {
                        "beat_id": "fort_kochi_b1",
                        "name": "Janamaithri Beat 1 (Heritage & Tourist Beach)",
                        "sector": "Coastal & Heritage Tourism",
                        "call_sign": "ALPHA-1",
                        "vehicle_type": "Tourist Police Cruiser (Maruti Ertiga)",
                        "point_books": [
                            {
                                "id": "PB-FTK-01",
                                "name": "Fort Kochi Beach & Chinese Fishing Nets",
                                "coords": [9.9675, 76.2410],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #01",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Tourist assistance and vigilance against bag snatching; beach walkway foot patrol.",
                                "peak_hour": 18
                            },
                            {
                                "id": "PB-FTK-02",
                                "name": "Princess Street Cafe & Homestay Strip",
                                "coords": [9.9648, 76.2435],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #02",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Homestay and foreign tourist safety check; night shutter and guest log inspection.",
                                "peak_hour": 23
                            },
                            {
                                "id": "PB-FTK-03",
                                "name": "Parade Ground & St. Francis Church",
                                "coords": [9.9655, 76.2405],
                                "checkpoint_type": "WOMEN_SAFETY_ZONE",
                                "checkpoint_label": "Heritage Open Ground Post",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "Night surveillance of open grounds; deter antisocial gathering and illegal alcohol consumption.",
                                "peak_hour": 21
                            }
                        ]
                    },
                    {
                        "beat_id": "fort_kochi_b2",
                        "name": "Janamaithri Beat 2 (Ro-Ro Ferry & Coastal Border)",
                        "sector": "Ferry Terminal & Inner Pockets",
                        "call_sign": "BRAVO-2",
                        "vehicle_type": "Coastal Beat Motorcycle (TVS Apache)",
                        "point_books": [
                            {
                                "id": "PB-FTK-04",
                                "name": "Vypin Ro-Ro Ferry Vehicle Terminal",
                                "coords": [9.9705, 76.2442],
                                "checkpoint_type": "TRANSIT_HUB",
                                "checkpoint_label": "Ro-Ro Ferry Naka",
                                "priority_crime": "VEHICLE_THEFT",
                                "sop_action": "Ferry queue vehicle check; verify suspicious vehicles embarking/disembarking from Vypin.",
                                "peak_hour": 19
                            },
                            {
                                "id": "PB-FTK-05",
                                "name": "Calvathy Canal Bridge & Border Link",
                                "coords": [9.9620, 76.2490],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Canal Border Checking Post",
                                "priority_crime": "ASSAULT_AFFRAY",
                                "sop_action": "Border junction checking; verify motorcycle riders; deter gang disputes across canal.",
                                "peak_hour": 22
                            },
                            {
                                "id": "PB-FTK-06",
                                "name": "Amaravathi & Bishop House Enclave",
                                "coords": [9.9605, 76.2420],
                                "checkpoint_type": "LOCKED_HOUSE_CHECK",
                                "checkpoint_label": "Residential Suraksha Point",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Locked house surveillance check for registered holidaying residents; residential pocket vigil.",
                                "peak_hour": 3
                            }
                        ]
                    }
                ]
            },
            {
                "id": "mattancherry",
                "name": "Mattancherry Police Station",
                "short_name": "Mattancherry PS",
                "code": "EKM-MAT-03",
                "lat": 9.9572,
                "lon": 76.2589,
                "operational_radius_km": 2.5,
                "jurisdiction": "Jew Town, Mattancherry Palace, Bazaar Road, Kochangadi Wholesale Market",
                "patrol_vehicles": ["Beat Motorcycle 08", "Station Patrol 2"],
                "janamaithri_beats": [
                    {
                        "beat_id": "mattancherry_b1",
                        "name": "Janamaithri Beat 1 (Jew Town & Spice Godowns)",
                        "sector": "Wholesale Market & Heritage Antique Strip",
                        "call_sign": "ALPHA-1",
                        "vehicle_type": "Station Mobile Patrol (Mahindra Bolero)",
                        "point_books": [
                            {
                                "id": "PB-MAT-01",
                                "name": "Jew Town Synagogue Lane",
                                "coords": [9.9578, 76.2595],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #01",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Antique jewelry and heritage shop security verification; night padlock checking.",
                                "peak_hour": 1
                            },
                            {
                                "id": "PB-MAT-02",
                                "name": "Bazaar Road Spice Godowns",
                                "coords": [9.9625, 76.2530],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #02",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Spice warehouse corridor foot patrol; verify goods carrier loading at night.",
                                "peak_hour": 20
                            },
                            {
                                "id": "PB-MAT-03",
                                "name": "Mattancherry Dutch Palace Gate",
                                "coords": [9.9585, 76.2580],
                                "checkpoint_type": "TRANSIT_HUB",
                                "checkpoint_label": "Palace Tourist Vigil Post",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "Monument perimeter patrol; disperse unauthorized crowds after closing hours.",
                                "peak_hour": 18
                            }
                        ]
                    },
                    {
                        "beat_id": "mattancherry_b2",
                        "name": "Janamaithri Beat 2 (Kochangadi & Chullikkal)",
                        "sector": "Market Junction & Commercial Crossings",
                        "call_sign": "BRAVO-2",
                        "vehicle_type": "Cheetah Beat Motorcycle (Bajaj Pulsar)",
                        "point_books": [
                            {
                                "id": "PB-MAT-04",
                                "name": "Kochangadi Wholesale Market Junction",
                                "coords": [9.9535, 76.2575],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Market Kavala Naka",
                                "priority_crime": "ASSAULT_AFFRAY",
                                "sop_action": "Wholesale market junction naka; resolve night loading disputes; check suspicious individuals.",
                                "peak_hour": 22
                            },
                            {
                                "id": "PB-MAT-05",
                                "name": "Chullikkal Junction & Commercial Strip",
                                "coords": [9.9495, 76.2560],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #03",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Bank branch and ATM kiosk physical check; verify security guard presence.",
                                "peak_hour": 3
                            },
                            {
                                "id": "PB-MAT-06",
                                "name": "Kappalandimukku Community Point",
                                "coords": [9.9550, 76.2540],
                                "checkpoint_type": "LOCKED_HOUSE_CHECK",
                                "checkpoint_label": "Residential Suraksha Point",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Dense residential lane patrol; locked house verification; interaction with community beat volunteers.",
                                "peak_hour": 19
                            }
                        ]
                    }
                ]
            },
            {
                "id": "kadavanthra",
                "name": "Kadavanthra Police Station",
                "short_name": "Kadavanthra PS",
                "code": "EKM-KAD-04",
                "lat": 9.9687,
                "lon": 76.2995,
                "operational_radius_km": 3.0,
                "jurisdiction": "Sahodaran Ayyappan (SA) Road, Kadavanthra Junction, Gandhinagar, Elamkulam",
                "patrol_vehicles": ["Patrol Car 104", "Beat Motorcycle 15"],
                "janamaithri_beats": [
                    {
                        "beat_id": "kadavanthra_b1",
                        "name": "Janamaithri Beat 1 (SA Road & Metro Hub)",
                        "sector": "Metro Corridor & Commercial Strip",
                        "call_sign": "ALPHA-1",
                        "vehicle_type": "Station Mobile Patrol (Mahindra Bolero)",
                        "point_books": [
                            {
                                "id": "PB-KAD-01",
                                "name": "Kadavanthra Junction & Metro Station",
                                "coords": [9.9685, 76.2990],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #01",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Metro passenger feeder surveillance; jewelry showroom night vigil; sign physical register.",
                                "peak_hour": 19
                            },
                            {
                                "id": "PB-KAD-02",
                                "name": "Rajiv Gandhi Indoor Stadium Outer Ring",
                                "coords": [9.9660, 76.2980],
                                "checkpoint_type": "WOMEN_SAFETY_ZONE",
                                "checkpoint_label": "Stadium Vigil Post",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "Sports complex perimeter check; prevent unauthorized gatherings; check dimly lit parking lots.",
                                "peak_hour": 21
                            },
                            {
                                "id": "PB-KAD-03",
                                "name": "Elamkulam Metro Station Feeder",
                                "coords": [9.9710, 76.3040],
                                "checkpoint_type": "TRANSIT_HUB",
                                "checkpoint_label": "Metro Feeder Security Post",
                                "priority_crime": "VEHICLE_THEFT",
                                "sop_action": "Two-wheeler parking lot surveillance; verify parked vehicles; deter snatching at transit stops.",
                                "peak_hour": 18
                            }
                        ]
                    },
                    {
                        "beat_id": "kadavanthra_b2",
                        "name": "Janamaithri Beat 2 (Gandhinagar Residential & Kaloor Link)",
                        "sector": "Residential Enclaves & Sub-Arteries",
                        "call_sign": "BRAVO-2",
                        "vehicle_type": "Cheetah Beat Motorcycle (Royal Enfield)",
                        "point_books": [
                            {
                                "id": "PB-KAD-04",
                                "name": "Gandhinagar Housing Colony Main Gate",
                                "coords": [9.9725, 76.2960],
                                "checkpoint_type": "LOCKED_HOUSE_CHECK",
                                "checkpoint_label": "Locked House Suraksha Point",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Check registered locked houses in residential colony; inspect rear service lanes.",
                                "peak_hour": 2
                            },
                            {
                                "id": "PB-KAD-05",
                                "name": "Kaloor-Kadavanthra Link Road Pockets",
                                "coords": [9.9750, 76.3015],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Link Road Checking Point",
                                "priority_crime": "ASSAULT_AFFRAY",
                                "sop_action": "Intercept speeding motorcycles on link road; verify rider documents; check dark stretches.",
                                "peak_hour": 22
                            },
                            {
                                "id": "PB-KAD-06",
                                "name": "Kumaranasan Junction & Market Road",
                                "coords": [9.9645, 76.3025],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #02",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Local neighborhood junction check; verify ATM anteroom lock integrity.",
                                "peak_hour": 20
                            }
                        ]
                    }
                ]
            },
            {
                "id": "palarivattom",
                "name": "Palarivattom Police Station",
                "short_name": "Palarivattom PS",
                "code": "EKM-PAL-05",
                "lat": 10.0039,
                "lon": 76.3078,
                "operational_radius_km": 3.2,
                "jurisdiction": "Palarivattom Junction, JLN International Stadium, Pipeline Rd, Thammanam",
                "patrol_vehicles": ["Patrol Car 105", "Traffic Enforcement Team"],
                "janamaithri_beats": [
                    {
                        "beat_id": "palarivattom_b1",
                        "name": "Janamaithri Beat 1 (Bypass & Stadium Zone)",
                        "sector": "Major Junction & Stadium Perimeter",
                        "call_sign": "ALPHA-1",
                        "vehicle_type": "Station Mobile Patrol (Mahindra Bolero)",
                        "point_books": [
                            {
                                "id": "PB-PAL-01",
                                "name": "Palarivattom Bypass Flyover Junction",
                                "coords": [10.0055, 76.3115],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Bypass Major Naka",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "Major highway intersection vehicle check; intercept reckless drivers; ensure smooth traffic flow.",
                                "peak_hour": 21
                            },
                            {
                                "id": "PB-PAL-02",
                                "name": "JLN International Stadium Parking & Grounds",
                                "coords": [9.9985, 76.3035],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #01",
                                "priority_crime": "ASSAULT_AFFRAY",
                                "sop_action": "Patrol vast stadium parking grounds; deter alcohol consumption and night affrays; verify point book.",
                                "peak_hour": 22
                            },
                            {
                                "id": "PB-PAL-03",
                                "name": "Kaloor Stadium Metro Station Gate",
                                "coords": [9.9970, 76.3015],
                                "checkpoint_type": "TRANSIT_HUB",
                                "checkpoint_label": "Metro Hub Post",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Passenger protection during last metro train arrivals; auto fare enforcement.",
                                "peak_hour": 22
                            }
                        ]
                    },
                    {
                        "beat_id": "palarivattom_b2",
                        "name": "Janamaithri Beat 2 (Thammanam & Pipeline Beat)",
                        "sector": "Commercial Hub & Residential Corridors",
                        "call_sign": "BRAVO-2",
                        "vehicle_type": "Cheetah Beat Motorcycle (TVS Apache)",
                        "point_books": [
                            {
                                "id": "PB-PAL-04",
                                "name": "Thammanam Road Commercial Junction",
                                "coords": [9.9935, 76.3125],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #02",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Gold loan offices and commercial establishment shutter security inspection.",
                                "peak_hour": 2
                            },
                            {
                                "id": "PB-PAL-05",
                                "name": "Pipeline Road Residential Enclaves",
                                "coords": [10.0080, 76.3060],
                                "checkpoint_type": "LOCKED_HOUSE_CHECK",
                                "checkpoint_label": "Locked House Suraksha Point",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Foot patrol in residential lanes; verify gate locks; contact Janamaithri colony reps.",
                                "peak_hour": 3
                            },
                            {
                                "id": "PB-PAL-06",
                                "name": "Chakkaraparambu NH Service Road",
                                "coords": [9.9995, 76.3180],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Service Road Naka",
                                "priority_crime": "VEHICLE_THEFT",
                                "sop_action": "Highway service road surveillance; inspect parked commercial vehicles and trailers.",
                                "peak_hour": 23
                            }
                        ]
                    }
                ]
            },
            {
                "id": "thrikkakara",
                "name": "Thrikkakara Police Station",
                "short_name": "Thrikkakara PS",
                "code": "EKM-THK-06",
                "lat": 10.0354,
                "lon": 76.3357,
                "operational_radius_km": 3.4,
                "jurisdiction": "Ernakulam District Collectorate, NGO Quarters, CUSAT University Gate, Toll Gate",
                "patrol_vehicles": ["Patrol Car 106", "Beat Motorcycle 19"],
                "janamaithri_beats": [
                    {
                        "beat_id": "thrikkakara_b1",
                        "name": "Janamaithri Beat 1 (Civil Station & Collectorate)",
                        "sector": "Administrative Complex & Quarters",
                        "call_sign": "ALPHA-1",
                        "vehicle_type": "Station Mobile Patrol (Mahindra Bolero)",
                        "point_books": [
                            {
                                "id": "PB-THK-01",
                                "name": "Ernakulam District Collectorate & Civil Station",
                                "coords": [10.0350, 76.3345],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #01",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "District administrative complex security check; verify night watch post; inspect gate register.",
                                "peak_hour": 18
                            },
                            {
                                "id": "PB-THK-02",
                                "name": "NGO Quarters Residential Enclave",
                                "coords": [10.0380, 76.3385],
                                "checkpoint_type": "LOCKED_HOUSE_CHECK",
                                "checkpoint_label": "Quarters Suraksha Point",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Government quarters locked house patrol; check boundary walls and dimly lit pathways.",
                                "peak_hour": 2
                            },
                            {
                                "id": "PB-THK-03",
                                "name": "Thrikkakara Temple Junction",
                                "coords": [10.0325, 76.3315],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Temple Junction Naka",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Pilgrim and community transit vigil; vehicle checking at junction; deter chain snatching.",
                                "peak_hour": 19
                            }
                        ]
                    },
                    {
                        "beat_id": "thrikkakara_b2",
                        "name": "Janamaithri Beat 2 (CUSAT Campus & Toll Gate)",
                        "sector": "University Corridor & Transit Link",
                        "call_sign": "BRAVO-2",
                        "vehicle_type": "Cheetah Beat Motorcycle (Royal Enfield)",
                        "point_books": [
                            {
                                "id": "PB-THK-04",
                                "name": "CUSAT University South Gate & Student Hub",
                                "coords": [10.0425, 76.3265],
                                "checkpoint_type": "WOMEN_SAFETY_ZONE",
                                "checkpoint_label": "Campus Anti-Narcotics Post",
                                "priority_crime": "NARCOTICS_NDPS",
                                "sop_action": "Anti-narcotics surveillance near university cafes; student safety patrol; verify point book.",
                                "peak_hour": 21
                            },
                            {
                                "id": "PB-THK-05",
                                "name": "Toll Gate & Pipeline Junction",
                                "coords": [10.0255, 76.3225],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Toll Gate Naka",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "Transit vehicle checking; enforce helmet and seatbelt compliance; inspect commercial auto stands.",
                                "peak_hour": 20
                            },
                            {
                                "id": "PB-THK-06",
                                "name": "University South Hostel Access Road",
                                "coords": [10.0390, 76.3235],
                                "checkpoint_type": "WOMEN_SAFETY_ZONE",
                                "checkpoint_label": "Hostel Security Link",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Night escort and surveillance near women's hostels; check suspicious parked vehicles.",
                                "peak_hour": 22
                            }
                        ]
                    }
                ]
            },
            {
                "id": "infopark",
                "name": "Infopark Police Station (Kakkanad)",
                "short_name": "Infopark PS",
                "code": "EKM-INF-07",
                "lat": 10.0112,
                "lon": 76.3638,
                "operational_radius_km": 3.6,
                "jurisdiction": "Infopark Phase 1 & 2, SmartCity Kochi, Edachira, Chittethukara Tech Corridor",
                "patrol_vehicles": ["IT Corridor Patrol 01", "Night Beat Car 107"],
                "janamaithri_beats": [
                    {
                        "beat_id": "infopark_b1",
                        "name": "Janamaithri Beat 1 (IT Expressways & Tech Parks)",
                        "sector": "Tech Corridor & Night Shift Route",
                        "call_sign": "ALPHA-1",
                        "vehicle_type": "IT Corridor Patrol Cruiser (Mahindra Bolero)",
                        "point_books": [
                            {
                                "id": "PB-INF-01",
                                "name": "Infopark Phase 1 Main Expressway Gate",
                                "coords": [10.0125, 76.3620],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #01",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "Night-shift IT employee cab escort monitoring; verify driver IDs; maintain high-visibility road presence.",
                                "peak_hour": 23
                            },
                            {
                                "id": "PB-INF-02",
                                "name": "SmartCity Kochi Access Bridge",
                                "coords": [10.0080, 76.3675],
                                "checkpoint_type": "TRANSIT_HUB",
                                "checkpoint_label": "SmartCity Security Post",
                                "priority_crime": "VEHICLE_THEFT",
                                "sop_action": "Tech campus perimeter check; surveillance of employee parking zones; intercept rash driving.",
                                "peak_hour": 20
                            },
                            {
                                "id": "PB-INF-03",
                                "name": "Infopark Phase 2 Cyber Campus Gate",
                                "coords": [10.0035, 76.3710],
                                "checkpoint_type": "WOMEN_SAFETY_ZONE",
                                "checkpoint_label": "Cyber Campus Women Vigil Post",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Pink patrol vigil for late-night female tech professionals; bus shelter security check.",
                                "peak_hour": 22
                            }
                        ]
                    },
                    {
                        "beat_id": "infopark_b2",
                        "name": "Janamaithri Beat 2 (Edachira Commercial & Chittethukara)",
                        "sector": "Commercial Hub & Paying Guest Belt",
                        "call_sign": "BRAVO-2",
                        "vehicle_type": "Cheetah Beat Motorcycle (TVS Apache)",
                        "point_books": [
                            {
                                "id": "PB-INF-04",
                                "name": "Edachira Junction Commercial Hub",
                                "coords": [10.0145, 76.3575],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Edachira Market Naka",
                                "priority_crime": "ASSAULT_AFFRAY",
                                "sop_action": "Evening foot patrol in commercial market; check closing restaurants and tea stalls; resolve traffic snarls.",
                                "peak_hour": 21
                            },
                            {
                                "id": "PB-INF-05",
                                "name": "Chittethukara Hostel & Residential Belt",
                                "coords": [10.0175, 76.3540],
                                "checkpoint_type": "LOCKED_HOUSE_CHECK",
                                "checkpoint_label": "Hostel Suraksha Point",
                                "priority_crime": "BURGLARY",
                                "sop_action": "PG accommodations and apartment perimeter patrol; check door security and night watchmen.",
                                "peak_hour": 2
                            },
                            {
                                "id": "PB-INF-06",
                                "name": "Kusumagiri Hospital Link Road",
                                "coords": [10.0210, 76.3590],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #02",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Emergency corridor access check; verify hospital visitor parking security.",
                                "peak_hour": 19
                            }
                        ]
                    }
                ]
            },
            {
                "id": "kalamassery",
                "name": "Kalamassery Police Station",
                "short_name": "Kalamassery PS",
                "code": "EKM-KLM-08",
                "lat": 10.0542,
                "lon": 76.3198,
                "operational_radius_km": 3.6,
                "jurisdiction": "Premier Junction, HMT Industrial Colony, NUALS, Container Road Flyover",
                "patrol_vehicles": ["Highway Patrol 03", "Beat Motorcycle 21"],
                "janamaithri_beats": [
                    {
                        "beat_id": "kalamassery_b1",
                        "name": "Janamaithri Beat 1 (Premier Junction & Industrial Belt)",
                        "sector": "Highway Naka & Industrial Enclave",
                        "call_sign": "ALPHA-1",
                        "vehicle_type": "Highway Patrol Cruiser (Mahindra Bolero)",
                        "point_books": [
                            {
                                "id": "PB-KLM-01",
                                "name": "Premier Junction & NH Flyover Underpass",
                                "coords": [10.0535, 76.3205],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Premier Major Naka",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "National Highway intersection naka; check long-distance trucks and drunken drivers; sign register.",
                                "peak_hour": 22
                            },
                            {
                                "id": "PB-KLM-02",
                                "name": "HMT Colony & Industrial Gates",
                                "coords": [10.0610, 76.3340],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #01",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Industrial unit perimeter check; inspect warehouse padlocks; verify security guards.",
                                "peak_hour": 2
                            },
                            {
                                "id": "PB-KLM-03",
                                "name": "Apollo Tyres Junction",
                                "coords": [10.0650, 76.3275],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #02",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Factory shift change vigil; safeguard workers carrying wages or cash; foot patrol.",
                                "peak_hour": 18
                            }
                        ]
                    },
                    {
                        "beat_id": "kalamassery_b2",
                        "name": "Janamaithri Beat 2 (Container Road & Educational Zone)",
                        "sector": "Expressway & Academic Institutions",
                        "call_sign": "BRAVO-2",
                        "vehicle_type": "Cheetah Beat Motorcycle (Bajaj Pulsar)",
                        "point_books": [
                            {
                                "id": "PB-KLM-04",
                                "name": "Container Road Flyover Junction",
                                "coords": [10.0485, 76.3110],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Container Road Expressway Post",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "Anti-speeding and illegal bike race deterrence on four-lane container expressway.",
                                "peak_hour": 23
                            },
                            {
                                "id": "PB-KLM-05",
                                "name": "NUALS Law University Perimeter",
                                "coords": [10.0560, 76.3270],
                                "checkpoint_type": "WOMEN_SAFETY_ZONE",
                                "checkpoint_label": "University Suraksha Post",
                                "priority_crime": "NARCOTICS_NDPS",
                                "sop_action": "Perimeter check of law university; anti-narcotics surveillance; student security vigil.",
                                "peak_hour": 20
                            },
                            {
                                "id": "PB-KLM-06",
                                "name": "CUSAT North Gate & Academic Pockets",
                                "coords": [10.0465, 76.3220],
                                "checkpoint_type": "LOCKED_HOUSE_CHECK",
                                "checkpoint_label": "Campus Residential Check",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Faculty residential quarters locked house check; inspect boundary gates.",
                                "peak_hour": 3
                            }
                        ]
                    }
                ]
            },
            {
                "id": "ekm_south",
                "name": "Ernakulam Town South Police Station",
                "short_name": "Town South PS",
                "code": "EKM-STH-09",
                "lat": 9.9664,
                "lon": 76.2891,
                "operational_radius_km": 2.8,
                "jurisdiction": "Ernakulam Junction (South) Railway Hub, Valanjambalam, Ravipuram, Thevara",
                "patrol_vehicles": ["Railway Link Cruiser", "Beat Motorcycle 05"],
                "janamaithri_beats": [
                    {
                        "beat_id": "ekm_south_b1",
                        "name": "Janamaithri Beat 1 (South Railway Hub & Transit)",
                        "sector": "Interstate Rail Terminal & Commercial Strip",
                        "call_sign": "ALPHA-1",
                        "vehicle_type": "Railway Link Cruiser (Maruti Ertiga)",
                        "point_books": [
                            {
                                "id": "PB-STH-01",
                                "name": "Ernakulam South Railway Station Main Entry",
                                "coords": [9.9655, 76.2940],
                                "checkpoint_type": "TRANSIT_HUB",
                                "checkpoint_label": "Railway Concourse Naka",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Vigilance over late-night train passenger flows; deter luggage lifting; auto-rickshaw queue check.",
                                "peak_hour": 22
                            },
                            {
                                "id": "PB-STH-02",
                                "name": "South Railway Station East Entry Feeder",
                                "coords": [9.9665, 76.2965],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #01",
                                "priority_crime": "ASSAULT_AFFRAY",
                                "sop_action": "East gate transit feeder patrol; resolve disputes; check dark waiting sheds.",
                                "peak_hour": 23
                            },
                            {
                                "id": "PB-STH-03",
                                "name": "Valanjambalam Temple Junction",
                                "coords": [9.9680, 76.2925],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #02",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Jewelry showroom and merchant strip shutter security check; inspect ATM kiosks.",
                                "peak_hour": 1
                            }
                        ]
                    },
                    {
                        "beat_id": "ekm_south_b2",
                        "name": "Janamaithri Beat 2 (Ravipuram & Thevara)",
                        "sector": "Commercial Strip & Waterfront Link",
                        "call_sign": "BRAVO-2",
                        "vehicle_type": "Cheetah Beat Motorcycle (Royal Enfield)",
                        "point_books": [
                            {
                                "id": "PB-STH-04",
                                "name": "Ravipuram Commercial MG Road Strip",
                                "coords": [9.9635, 76.2910],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #03",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Bank branch and office complex corridor foot patrol; sign physical register.",
                                "peak_hour": 19
                            },
                            {
                                "id": "PB-STH-05",
                                "name": "Medical Trust Hospital Junction",
                                "coords": [9.9705, 76.2895],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Emergency Corridor Naka",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "Keep emergency hospital access corridor clear; check ambulance routes; regulate traffic.",
                                "peak_hour": 20
                            },
                            {
                                "id": "PB-STH-06",
                                "name": "Thevara Ferry Road Junction",
                                "coords": [9.9540, 76.2950],
                                "checkpoint_type": "LOCKED_HOUSE_CHECK",
                                "checkpoint_label": "Residential Suraksha Point",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Waterfront residential colony surveillance; inspect locked bungalows of NRI residents.",
                                "peak_hour": 3
                            }
                        ]
                    }
                ]
            },
            {
                "id": "panangad",
                "name": "Panangad Police Station",
                "short_name": "Panangad PS",
                "code": "EKM-PNG-10",
                "lat": 9.9073,
                "lon": 76.3155,
                "operational_radius_km": 3.8,
                "jurisdiction": "Nettoor Vegetable Market, Panangad KUFOS, Kumbalam Toll, Aroor Bypass Link",
                "patrol_vehicles": ["Bypass Patrol Car 110", "Highway Beat 07"],
                "janamaithri_beats": [
                    {
                        "beat_id": "panangad_b1",
                        "name": "Janamaithri Beat 1 (Nettoor Wholesale Market)",
                        "sector": "Wholesale Market & Highway Corridor",
                        "call_sign": "ALPHA-1",
                        "vehicle_type": "Bypass Patrol Car (Mahindra Bolero)",
                        "point_books": [
                            {
                                "id": "PB-PNG-01",
                                "name": "Nettoor Vegetable Market & NH 66",
                                "coords": [9.9160, 76.3140],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #01",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Wholesale night market security; protect cash carrying traders and farmers; deter pickpocketing.",
                                "peak_hour": 4
                            },
                            {
                                "id": "PB-PNG-02",
                                "name": "Nettoor Railway Overbridge Link",
                                "coords": [9.9215, 76.3115],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Dark Spot Surveillance Post",
                                "priority_crime": "ASSAULT_AFFRAY",
                                "sop_action": "Surveillance of dark stretches beneath railway overbridge; prevent drunken affrays.",
                                "peak_hour": 22
                            },
                            {
                                "id": "PB-PNG-03",
                                "name": "INTUC Junction Nettoor",
                                "coords": [9.9125, 76.3160],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #02",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "Community junction patrol; inspect closed commercial shutters; verify point book.",
                                "peak_hour": 20
                            }
                        ]
                    },
                    {
                        "beat_id": "panangad_b2",
                        "name": "Janamaithri Beat 2 (Kumbalam & KUFOS Coastal Beat)",
                        "sector": "Inter-District Toll Naka & Academic Campus",
                        "call_sign": "BRAVO-2",
                        "vehicle_type": "Highway Beat Motorcycle (TVS Apache)",
                        "point_books": [
                            {
                                "id": "PB-PNG-04",
                                "name": "Kumbalam Toll Plaza Corridor",
                                "coords": [9.9030, 76.3185],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Inter-District Border Naka",
                                "priority_crime": "VEHICLE_THEFT",
                                "sop_action": "District border vehicle inspection; check outbound stolen vehicles and illicit transport.",
                                "peak_hour": 1
                            },
                            {
                                "id": "PB-PNG-05",
                                "name": "KUFOS Fisheries University Main Gate",
                                "coords": [9.9065, 76.3130],
                                "checkpoint_type": "WOMEN_SAFETY_ZONE",
                                "checkpoint_label": "Campus Suraksha Post",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "University campus perimeter check; waterfront safety patrol; student protection.",
                                "peak_hour": 19
                            },
                            {
                                "id": "PB-PNG-06",
                                "name": "Panangad Boat Jetty & Coastal Ring",
                                "coords": [9.9015, 76.3110],
                                "checkpoint_type": "LOCKED_HOUSE_CHECK",
                                "checkpoint_label": "Coastal Suraksha Point",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Coastal fishing village beat; locked house inspection along backwater road.",
                                "peak_hour": 3
                            }
                        ]
                    }
                ]
            }
        ]
    },
    "thiruvananthapuram": {
        "id": "thiruvananthapuram",
        "name": "Thiruvananthapuram (Trivandrum)",
        "state": "Kerala",
        "district": "Thiruvananthapuram",
        "center": [8.5241, 76.9366],
        "default_zoom": 13,
        "bounds": {
            "min_lat": 8.4450,
            "max_lat": 8.5950,
            "min_lon": 76.8750,
            "max_lon": 77.0150
        },
        "grid_resolution_km": 0.45,
        "police_stations": [
            {
                "id": "tvm_thampanoor",
                "name": "Thampanoor Police Station",
                "short_name": "Thampanoor PS",
                "code": "TVM-TMP-01",
                "lat": 8.4892,
                "lon": 76.9504,
                "operational_radius_km": 2.8,
                "jurisdiction": "Central Railway Station, KSRTC Central Bus Terminal, Overbridge",
                "patrol_vehicles": ["Patrol Car 201", "Transit Beat 01"],
                "janamaithri_beats": [
                    {
                        "beat_id": "tvm_thampanoor_b1",
                        "name": "Janamaithri Beat 1 (Central Railway & Bus Concourse)",
                        "sector": "Transit Hub & Inter-State Terminal",
                        "call_sign": "ALPHA-1",
                        "vehicle_type": "Station Mobile Patrol (Mahindra Bolero)",
                        "point_books": [
                            {
                                "id": "PB-TMP-01",
                                "name": "Central Railway Station Concourse",
                                "coords": [8.4895, 76.9510],
                                "checkpoint_type": "TRANSIT_HUB",
                                "checkpoint_label": "Railway Concourse Naka",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Passenger protection, vigilance against luggage lifters, auto fare compliance check.",
                                "peak_hour": 21
                            },
                            {
                                "id": "PB-TMP-02",
                                "name": "KSRTC Central Bus Terminal Entry",
                                "coords": [8.4880, 76.9490],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #01",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Sign physical register; maintain vigil during night long-distance bus boardings.",
                                "peak_hour": 22
                            },
                            {
                                "id": "PB-TMP-03",
                                "name": "Aristo Junction Commercial Strip",
                                "coords": [8.4860, 76.9530],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #02",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Lodge and hotel strip inspection; verify guest registers; check commercial shutter locks.",
                                "peak_hour": 2
                            }
                        ]
                    },
                    {
                        "beat_id": "tvm_thampanoor_b2",
                        "name": "Janamaithri Beat 2 (Overbridge & Power House Road)",
                        "sector": "Commercial Artery & Flyover Post",
                        "call_sign": "BRAVO-2",
                        "vehicle_type": "Cheetah Beat Motorcycle (Royal Enfield)",
                        "point_books": [
                            {
                                "id": "PB-TMP-04",
                                "name": "Overbridge Junction Commercial Post",
                                "coords": [8.4920, 76.9485],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Overbridge Naka",
                                "priority_crime": "ASSAULT_AFFRAY",
                                "sop_action": "Major junction vehicle checking; disperse unruly night gatherings near cinema halls.",
                                "peak_hour": 22
                            },
                            {
                                "id": "PB-TMP-05",
                                "name": "Power House Road Wholesale Godowns",
                                "coords": [8.4910, 76.9525],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #03",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Inspect electrical wholesale shutters; foot patrol dark alleys.",
                                "peak_hour": 3
                            }
                        ]
                    }
                ]
            },
            {
                "id": "tvm_fort",
                "name": "Fort Police Station",
                "short_name": "Fort PS (TVM)",
                "code": "TVM-FRT-02",
                "lat": 8.4825,
                "lon": 76.9442,
                "operational_radius_km": 2.5,
                "jurisdiction": "Padmanabhaswamy Temple Heritage Ring, Chalai Market, East Fort",
                "patrol_vehicles": ["Temple Beat Car", "Market Beat 03"],
                "janamaithri_beats": [
                    {
                        "beat_id": "tvm_fort_b1",
                        "name": "Janamaithri Beat 1 (Temple Heritage & East Fort)",
                        "sector": "Temple Heritage Ring & City Bus Stand",
                        "call_sign": "ALPHA-1",
                        "vehicle_type": "Temple Beat Cruiser (Maruti Ertiga)",
                        "point_books": [
                            {
                                "id": "PB-TFR-01",
                                "name": "Sree Padmanabhaswamy Temple North Gate",
                                "coords": [8.4830, 76.9435],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Temple Security Post",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Heritage security verification; assist pilgrims; deter pickpocketing near temple gates.",
                                "peak_hour": 18
                            },
                            {
                                "id": "PB-TFR-02",
                                "name": "East Fort City Bus Stand",
                                "coords": [8.4845, 76.9470],
                                "checkpoint_type": "WOMEN_SAFETY_ZONE",
                                "checkpoint_label": "East Fort Women Vigil Post",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "Eve-teasing prevention at major student bus boarding terminal; foot patrol.",
                                "peak_hour": 17
                            }
                        ]
                    },
                    {
                        "beat_id": "tvm_fort_b2",
                        "name": "Janamaithri Beat 2 (Chalai Market Wholesale Core)",
                        "sector": "Historic Wholesale Bazaar",
                        "call_sign": "BRAVO-2",
                        "vehicle_type": "Cheetah Beat Motorcycle (TVS Apache)",
                        "point_books": [
                            {
                                "id": "PB-TFR-03",
                                "name": "Chalai Market Main Street",
                                "coords": [8.4810, 76.9480],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #02",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Foot patrol along 2km narrow bazaar; verify gold shop and wholesale grocery padlocks.",
                                "peak_hour": 2
                            },
                            {
                                "id": "PB-TFR-04",
                                "name": "Attakulangara Junction & Bypass Link",
                                "coords": [8.4785, 76.9460],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Attakulangara Naka",
                                "priority_crime": "VEHICLE_THEFT",
                                "sop_action": "Commercial transport vehicle checking; verify loading permits.",
                                "peak_hour": 23
                            }
                        ]
                    }
                ]
            },
            {
                "id": "tvm_museum",
                "name": "Museum Police Station",
                "short_name": "Museum PS",
                "code": "TVM-MUS-03",
                "lat": 8.5133,
                "lon": 76.9567,
                "operational_radius_km": 3.0,
                "jurisdiction": "Kowdiar Palace, Museum Compound, Raj Bhavan, Vellayambalam",
                "patrol_vehicles": ["VIP Corridor Cruiser 203"],
                "janamaithri_beats": [
                    {
                        "beat_id": "tvm_museum_b1",
                        "name": "Janamaithri Beat 1 (Museum Compound & Vellayambalam)",
                        "sector": "Public Parks & Arterial Square",
                        "call_sign": "ALPHA-1",
                        "vehicle_type": "VIP Corridor Cruiser (Mahindra Bolero)",
                        "point_books": [
                            {
                                "id": "PB-TMU-01",
                                "name": "Museum Compound & Kanakakkunnu Gate",
                                "coords": [8.5135, 76.9565],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Museum Vigil Post",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "Patrol cultural promenade and public garden perimeter; prevent nuisance.",
                                "peak_hour": 19
                            },
                            {
                                "id": "PB-TMU-02",
                                "name": "Vellayambalam Junction & Square",
                                "coords": [8.5170, 76.9605],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Vellayambalam Major Naka",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "Traffic regulation and drunken driving inspection at primary city intersection.",
                                "peak_hour": 22
                            }
                        ]
                    },
                    {
                        "beat_id": "tvm_museum_b2",
                        "name": "Janamaithri Beat 2 (Kowdiar Palace & Raj Bhavan Road)",
                        "sector": "High Security & Residential Avenue",
                        "call_sign": "BRAVO-2",
                        "vehicle_type": "Cheetah Beat Motorcycle (Royal Enfield)",
                        "point_books": [
                            {
                                "id": "PB-TMU-03",
                                "name": "Kowdiar Palace Avenue Road",
                                "coords": [8.5250, 76.9650],
                                "checkpoint_type": "LOCKED_HOUSE_CHECK",
                                "checkpoint_label": "Residential Suraksha Point",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Locked house inspection along VIP avenue; verify private residential security.",
                                "peak_hour": 3
                            }
                        ]
                    }
                ]
            },
            {
                "id": "tvm_kazhakkoottam",
                "name": "Kazhakkoottam Police Station",
                "short_name": "Kazhakkoottam PS",
                "code": "TVM-KZK-04",
                "lat": 8.5684,
                "lon": 76.8722,
                "operational_radius_km": 3.8,
                "jurisdiction": "Technopark Campus Phases 1-3, Karyavattom University, NH66 Bypass",
                "patrol_vehicles": ["Cyber Corridor Car 204", "Night Beat 08"],
                "janamaithri_beats": [
                    {
                        "beat_id": "tvm_kazhakkoottam_b1",
                        "name": "Janamaithri Beat 1 (Technopark Tech Campuses)",
                        "sector": "IT Corridor & Campus Gateways",
                        "call_sign": "ALPHA-1",
                        "vehicle_type": "Cyber Corridor Cruiser (Mahindra Bolero)",
                        "point_books": [
                            {
                                "id": "PB-TKZ-01",
                                "name": "Technopark Phase 1 Main Entrance Gate",
                                "coords": [8.5580, 76.8810],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Technopark Gate Naka",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Night cab surveillance; safeguard women tech professionals during shift changes.",
                                "peak_hour": 23
                            },
                            {
                                "id": "PB-TKZ-02",
                                "name": "Karyavattom University Campus Gate",
                                "coords": [8.5630, 76.8850],
                                "checkpoint_type": "WOMEN_SAFETY_ZONE",
                                "checkpoint_label": "Campus Suraksha Post",
                                "priority_crime": "NARCOTICS_NDPS",
                                "sop_action": "Anti-narcotics check near student eateries; campus perimeter vigil.",
                                "peak_hour": 20
                            }
                        ]
                    },
                    {
                        "beat_id": "tvm_kazhakkoottam_b2",
                        "name": "Janamaithri Beat 2 (Kazhakkoottam Junction & Bypass)",
                        "sector": "Highway Junction & Tech Residential",
                        "call_sign": "BRAVO-2",
                        "vehicle_type": "Cheetah Beat Motorcycle (Bajaj Pulsar)",
                        "point_books": [
                            {
                                "id": "PB-TKZ-03",
                                "name": "Kazhakkoottam Junction & NH66 Flyover",
                                "coords": [8.5695, 76.8715],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Kazhakkoottam Naka",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "Highway intersection vehicle check; intercept speeding vehicles.",
                                "peak_hour": 21
                            }
                        ]
                    }
                ]
            }
        ]
    },
    "kozhikode": {
        "id": "kozhikode",
        "name": "Kozhikode (Calicut)",
        "state": "Kerala",
        "district": "Kozhikode",
        "center": [11.2588, 75.7804],
        "default_zoom": 13,
        "bounds": {
            "min_lat": 11.2050,
            "max_lat": 11.3350,
            "min_lon": 75.7300,
            "max_lon": 75.8450
        },
        "grid_resolution_km": 0.45,
        "police_stations": [
            {
                "id": "clt_town",
                "name": "Kozhikode Town Police Station",
                "short_name": "Town PS (Calicut)",
                "code": "CLT-TWN-01",
                "lat": 11.2562,
                "lon": 75.7767,
                "operational_radius_km": 2.8,
                "jurisdiction": "SM Street (Sweet Meat Street), Mananchira Square, Big Bazaar",
                "patrol_vehicles": ["Town Patrol 301", "Beat Motorcycle 14"],
                "janamaithri_beats": [
                    {
                        "beat_id": "clt_town_b1",
                        "name": "Janamaithri Beat 1 (SM Street Commercial Hub)",
                        "sector": "Pedestrian Heritage Market",
                        "call_sign": "ALPHA-1",
                        "vehicle_type": "Town Patrol Cruiser (Mahindra Bolero)",
                        "point_books": [
                            {
                                "id": "PB-CTW-01",
                                "name": "SM Street (Mittai Theruvu) Commercial Strip",
                                "coords": [11.2560, 75.7765],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #01",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Foot patrol inside pedestrian-only shopping strip; inspect shutter security; deter pickpocketing.",
                                "peak_hour": 19
                            },
                            {
                                "id": "PB-CTW-02",
                                "name": "Mananchira Square Park Perimeter",
                                "coords": [11.2540, 75.7790],
                                "checkpoint_type": "WOMEN_SAFETY_ZONE",
                                "checkpoint_label": "Square Promenade Post",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "Public order surveillance around heritage pond and park walkway; eve-teasing deterrence.",
                                "peak_hour": 18
                            }
                        ]
                    },
                    {
                        "beat_id": "clt_town_b2",
                        "name": "Janamaithri Beat 2 (Beach Walkway & Big Bazaar)",
                        "sector": "Coastal Promenade & Wholesale Hub",
                        "call_sign": "BRAVO-2",
                        "vehicle_type": "Cheetah Beat Motorcycle (Royal Enfield)",
                        "point_books": [
                            {
                                "id": "PB-CTW-03",
                                "name": "Calicut Beach Walkway & Old Pier",
                                "coords": [11.2595, 75.7705],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Beach Beat Point",
                                "priority_crime": "ASSAULT_AFFRAY",
                                "sop_action": "Crowd management and dispute prevention along crowded evening beach promenade.",
                                "peak_hour": 20
                            },
                            {
                                "id": "PB-CTW-04",
                                "name": "Big Bazaar Wholesale Market Street",
                                "coords": [11.2520, 75.7740],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #02",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Wholesale grocery and spice shop night inspection; check padlocks; sign register.",
                                "peak_hour": 2
                            }
                        ]
                    }
                ]
            },
            {
                "id": "clt_kasaba",
                "name": "Kasaba Police Station",
                "short_name": "Kasaba PS",
                "code": "CLT-KAS-02",
                "lat": 11.2514,
                "lon": 75.7925,
                "operational_radius_km": 3.0,
                "jurisdiction": "Moffusil Bus Stand, Rajaji Road, Puthiyara, Link Road",
                "patrol_vehicles": ["Patrol Car 302", "Transit Beat 06"],
                "janamaithri_beats": [
                    {
                        "beat_id": "clt_kasaba_b1",
                        "name": "Janamaithri Beat 1 (Moffusil Bus Terminal & Mavoor Rd)",
                        "sector": "Central Bus Hub & Arterial Retail",
                        "call_sign": "ALPHA-1",
                        "vehicle_type": "Station Mobile Patrol (Mahindra Bolero)",
                        "point_books": [
                            {
                                "id": "PB-CKS-01",
                                "name": "Moffusil New Bus Stand Terminal",
                                "coords": [11.2520, 75.7930],
                                "checkpoint_type": "TRANSIT_HUB",
                                "checkpoint_label": "Bus Terminal Security Post",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Vigilance over night travelers; luggage theft prevention; auto stand surveillance.",
                                "peak_hour": 21
                            },
                            {
                                "id": "PB-CKS-02",
                                "name": "Rajaji Road Commercial Corridor",
                                "coords": [11.2505, 75.7890],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #01",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Inspect bank branches and commercial showrooms; sign physical register.",
                                "peak_hour": 1
                            }
                        ]
                    },
                    {
                        "beat_id": "clt_kasaba_b2",
                        "name": "Janamaithri Beat 2 (Puthiyara & Link Road)",
                        "sector": "Commercial Intersect & Residential Pockets",
                        "call_sign": "BRAVO-2",
                        "vehicle_type": "Cheetah Beat Motorcycle (TVS Apache)",
                        "point_books": [
                            {
                                "id": "PB-CKS-03",
                                "name": "Puthiyara Junction & Stadium Link",
                                "coords": [11.2470, 75.7980],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Puthiyara Naka",
                                "priority_crime": "ASSAULT_AFFRAY",
                                "sop_action": "Junction vehicle check; deter rash driving; resolve parking congestion.",
                                "peak_hour": 20
                            }
                        ]
                    }
                ]
            },
            {
                "id": "clt_nadakkavu",
                "name": "Nadakkavu Police Station",
                "short_name": "Nadakkavu PS",
                "code": "CLT-NAD-03",
                "lat": 11.2721,
                "lon": 75.7788,
                "operational_radius_km": 3.0,
                "jurisdiction": "Nadakkavu Junction, Beach Road North, English Church, Bilathikulam",
                "patrol_vehicles": ["Coastal Cruiser 303"],
                "janamaithri_beats": [
                    {
                        "beat_id": "clt_nadakkavu_b1",
                        "name": "Janamaithri Beat 1 (Nadakkavu Junction & College Strip)",
                        "sector": "Commercial Crossing & Academic Enclave",
                        "call_sign": "ALPHA-1",
                        "vehicle_type": "Station Mobile Patrol (Mahindra Bolero)",
                        "point_books": [
                            {
                                "id": "PB-CND-01",
                                "name": "Nadakkavu Junction & Vandipetta",
                                "coords": [11.2725, 75.7785],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Nadakkavu Naka",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "Major junction surveillance; verify two-wheeler riders; sign point book.",
                                "peak_hour": 20
                            },
                            {
                                "id": "PB-CND-02",
                                "name": "English Church Road Pockets",
                                "coords": [11.2690, 75.7760],
                                "checkpoint_type": "WOMEN_SAFETY_ZONE",
                                "checkpoint_label": "School Zone Vigil Post",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Student dispersal vigil; anti-harassment patrol near educational institutions.",
                                "peak_hour": 16
                            }
                        ]
                    },
                    {
                        "beat_id": "clt_nadakkavu_b2",
                        "name": "Janamaithri Beat 2 (Bilathikulam & North Beach)",
                        "sector": "Residential Enclaves & North Coast",
                        "call_sign": "BRAVO-2",
                        "vehicle_type": "Cheetah Beat Motorcycle (Royal Enfield)",
                        "point_books": [
                            {
                                "id": "PB-CND-03",
                                "name": "Bilathikulam Temple Residential Road",
                                "coords": [11.2780, 75.7795],
                                "checkpoint_type": "LOCKED_HOUSE_CHECK",
                                "checkpoint_label": "Residential Suraksha Point",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Locked house inspection; residential gate checks; interaction with residents.",
                                "peak_hour": 3
                            }
                        ]
                    }
                ]
            }
        ]
    },
    "thrissur": {
        "id": "thrissur",
        "name": "Thrissur (Trichur)",
        "state": "Kerala",
        "district": "Thrissur",
        "center": [10.5276, 76.2144],
        "default_zoom": 13,
        "bounds": {
            "min_lat": 10.4850,
            "max_lat": 10.5750,
            "min_lon": 76.1750,
            "max_lon": 76.2650
        },
        "grid_resolution_km": 0.45,
        "police_stations": [
            {
                "id": "tsr_east",
                "name": "Thrissur East Police Station",
                "short_name": "East PS",
                "code": "TSR-EST-01",
                "lat": 10.5244,
                "lon": 76.2215,
                "operational_radius_km": 2.8,
                "jurisdiction": "Swaraj Round East, High Road, Shakthan Thampuran Bus Stand",
                "patrol_vehicles": ["Round Patrol Car 401", "Beat 02"],
                "janamaithri_beats": [
                    {
                        "beat_id": "tsr_east_b1",
                        "name": "Janamaithri Beat 1 (Swaraj Round East & High Road)",
                        "sector": "Round Commercial Strip & Gold Market",
                        "call_sign": "ALPHA-1",
                        "vehicle_type": "Round Patrol Cruiser (Mahindra Bolero)",
                        "point_books": [
                            {
                                "id": "PB-TRE-01",
                                "name": "Swaraj Round East & High Road Gold Hub",
                                "coords": [10.5245, 76.2160],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #01",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Gold jewelry showroom security check; verify night padlocks and CCTV alarms.",
                                "peak_hour": 2
                            },
                            {
                                "id": "PB-TRE-02",
                                "name": "Vadakkumnathan Temple Ring East",
                                "coords": [10.5255, 76.2140],
                                "checkpoint_type": "TRANSIT_HUB",
                                "checkpoint_label": "Maidan Perimeter Post",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Thekkinkadu Maidan perimeter foot patrol; safeguard pilgrims and evening walkers.",
                                "peak_hour": 19
                            }
                        ]
                    },
                    {
                        "beat_id": "tsr_east_b2",
                        "name": "Janamaithri Beat 2 (Shakthan Thampuran Bus Stand)",
                        "sector": "Major Bus Terminal & Wholesale Markets",
                        "call_sign": "BRAVO-2",
                        "vehicle_type": "Cheetah Beat Motorcycle (Royal Enfield)",
                        "point_books": [
                            {
                                "id": "PB-TRE-03",
                                "name": "Shakthan Thampuran Bus Stand Terminal",
                                "coords": [10.5180, 76.2205],
                                "checkpoint_type": "TRANSIT_HUB",
                                "checkpoint_label": "Bus Stand Security Post",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Surveillance of interstate bus passengers; pickpocket deterrence; auto stand check.",
                                "peak_hour": 21
                            },
                            {
                                "id": "PB-TRE-04",
                                "name": "Municipal Jubilee Market Core",
                                "coords": [10.5210, 76.2185],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #02",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Night merchant godown security; sign register at market committee post.",
                                "peak_hour": 3
                            }
                        ]
                    }
                ]
            },
            {
                "id": "tsr_west",
                "name": "Thrissur West Police Station",
                "short_name": "West PS",
                "code": "TSR-WST-02",
                "lat": 10.5310,
                "lon": 76.2080,
                "operational_radius_km": 3.0,
                "jurisdiction": "Swaraj Round West, MG Road Thrissur, Vadakkechira, Poonkunnam",
                "patrol_vehicles": ["Patrol Car 402", "Beat 09"],
                "janamaithri_beats": [
                    {
                        "beat_id": "tsr_west_b1",
                        "name": "Janamaithri Beat 1 (Swaraj Round West & MG Road)",
                        "sector": "Commercial Banking Strip & Round West",
                        "call_sign": "ALPHA-1",
                        "vehicle_type": "Station Mobile Patrol (Mahindra Bolero)",
                        "point_books": [
                            {
                                "id": "PB-TRW-01",
                                "name": "Swaraj Round West Commercial Corridor",
                                "coords": [10.5250, 76.2120],
                                "checkpoint_type": "POINT_BOOK",
                                "checkpoint_label": "Janamaithri Point Book #01",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Bank branch and retail strip foot patrol; verify ATM security guard presence.",
                                "peak_hour": 1
                            },
                            {
                                "id": "PB-TRW-02",
                                "name": "Vadakkechira Pond Ring Road",
                                "coords": [10.5285, 76.2105],
                                "checkpoint_type": "WOMEN_SAFETY_ZONE",
                                "checkpoint_label": "Vadakkechira Vigil Post",
                                "priority_crime": "PUBLIC_NUISANCE",
                                "sop_action": "Waterbody walkway surveillance; disperse antisocial groups after dusk.",
                                "peak_hour": 20
                            }
                        ]
                    },
                    {
                        "beat_id": "tsr_west_b2",
                        "name": "Janamaithri Beat 2 (Poonkunnam & West Fort)",
                        "sector": "Residential Enclaves & Railway Approach",
                        "call_sign": "BRAVO-2",
                        "vehicle_type": "Cheetah Beat Motorcycle (TVS Apache)",
                        "point_books": [
                            {
                                "id": "PB-TRW-03",
                                "name": "Poonkunnam Junction & Railway Station Link",
                                "coords": [10.5390, 76.2020],
                                "checkpoint_type": "KAVALA_CHECK",
                                "checkpoint_label": "Poonkunnam Naka",
                                "priority_crime": "THEFT_SNATCHING",
                                "sop_action": "Railway feeder road vigil; verify two-wheeler commuters; sign point book.",
                                "peak_hour": 19
                            },
                            {
                                "id": "PB-TRW-04",
                                "name": "West Fort Junction & Hospital Link",
                                "coords": [10.5280, 76.2015],
                                "checkpoint_type": "LOCKED_HOUSE_CHECK",
                                "checkpoint_label": "Residential Suraksha Point",
                                "priority_crime": "BURGLARY",
                                "sop_action": "Residential colony locked house inspection; check dark pocket roads.",
                                "peak_hour": 3
                            }
                        ]
                    }
                ]
            }
        ]
    }
}

CRIME_CATEGORIES = {
    "THEFT_SNATCHING": {
        "label": "Theft & Snatching",
        "ipc_sections": "IPC 379 / BNS 303",
        "severity_weight": 1.0,
        "typical_peak_hours": "17:00 - 21:00",
        "color": "#e07a5f"
    },
    "BURGLARY": {
        "label": "Burglary & Housebreaking",
        "ipc_sections": "IPC 457 / BNS 331",
        "severity_weight": 1.5,
        "typical_peak_hours": "01:00 - 04:00",
        "color": "#d90429"
    },
    "ROBBERY": {
        "label": "Robbery & Extortion",
        "ipc_sections": "IPC 392 / BNS 309",
        "severity_weight": 2.2,
        "typical_peak_hours": "22:00 - 02:00",
        "color": "#7209b7"
    },
    "ASSAULT_AFFRAY": {
        "label": "Assault & Street Affray",
        "ipc_sections": "IPC 324, 326, 160 / BNS 115, 189",
        "severity_weight": 2.0,
        "typical_peak_hours": "20:00 - 23:30",
        "color": "#f77f00"
    },
    "VEHICLE_THEFT": {
        "label": "Motor Vehicle Theft",
        "ipc_sections": "IPC 379 / BNS 303",
        "severity_weight": 1.3,
        "typical_peak_hours": "14:00 - 18:00 & 23:00 - 03:00",
        "color": "#3a86ff"
    },
    "NARCOTICS_NDPS": {
        "label": "Narcotics & NDPS Offences",
        "ipc_sections": "NDPS Act 1985 / Abkari Act",
        "severity_weight": 2.5,
        "typical_peak_hours": "22:00 - 04:00",
        "color": "#8338ec"
    },
    "PUBLIC_NUISANCE": {
        "label": "Public Nuisance & Reckless Driving",
        "ipc_sections": "IPC 268, 279 / BNS 281",
        "severity_weight": 0.8,
        "typical_peak_hours": "18:00 - 22:00",
        "color": "#2a9d8f"
    }
}
