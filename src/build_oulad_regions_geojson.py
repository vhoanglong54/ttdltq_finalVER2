"""Build an auditable 13-region OULAD GeoJSON from official ONS boundaries.

OULAD's labels describe historic Open University administrative catchments,
not a current statistical geography.  This script therefore performs a
documented approximation: it downloads current UK Counties and Unitary
Authorities from the ONS Open Geography service and unions them according to
the historic OU area descriptions.  It never invents centroids or hand-draws
polygons.

Primary geometry source (Open Government Licence v3.0):
https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/
Counties_and_Unitary_Authorities_December_2025_Boundaries_UK_BGC/FeatureServer/0

Run from the repository root:

    python src/build_oulad_regions_geojson.py
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

from shapely.geometry import mapping, shape
from shapely.ops import unary_union


ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT / "dashboard" / "assets"
OUTPUT_PATH = ASSET_DIR / "oulad_regions.geojson"
AUDIT_PATH = ASSET_DIR / "oulad_regions_mapping.csv"
ANALYSIS_PATH = ROOT / "data" / "processed" / "clean_dataset.csv"

SERVICE_URL = (
    "https://services1.arcgis.com/ESMARspQHYMw9BZ9/arcgis/rest/services/"
    "Counties_and_Unitary_Authorities_December_2025_Boundaries_UK_BGC/"
    "FeatureServer/0/query"
)
SOURCE_PAGE = (
    "https://www.data.gov.uk/dataset/563f5079-796d-4190-ac7f-49219a6de896/"
    "counties-and-unitary-authorities-december-2025-boundaries-uk-bgc"
)
OU_AREA_REFERENCE = (
    "The Open University, healthcare practice qualifications prospectus "
    "(2015), regional/national centres and areas covered: "
    "https://css2.open.ac.uk/outis/docs/publications/NAH16U.pdf"
)

EXPECTED_REGIONS = {
    "East Anglian Region",
    "East Midlands Region",
    "Ireland",
    "London Region",
    "North Region",
    "North Western Region",
    "Scotland",
    "South East Region",
    "South Region",
    "South West Region",
    "Wales",
    "West Midlands Region",
    "Yorkshire Region",
}

# Current CUA names grouped from the historic county descriptions. Splits that
# cannot be represented at CUA grain are disclosed in dashboard/assets/README.md.
NORTH = {
    "Hartlepool",
    "Middlesbrough",
    "Redcar and Cleveland",
    "Stockton-on-Tees",
    "Darlington",
    "County Durham",
    "Northumberland",
    "Cumberland",
    "Westmorland and Furness",
    "Newcastle upon Tyne",
    "North Tyneside",
    "South Tyneside",
    "Sunderland",
    "Gateshead",
}
YORKSHIRE = {
    "Kingston upon Hull, City of",
    "East Riding of Yorkshire",
    "York",
    "North Yorkshire",
    "Doncaster",
    "Rotherham",
    "Bradford",
    "Calderdale",
    "Kirklees",
    "Leeds",
    "Wakefield",
    "Barnsley",
    "Sheffield",
}
NORTH_WEST = {
    "Halton",
    "Warrington",
    "Blackburn with Darwen",
    "Blackpool",
    "Cheshire East",
    "Cheshire West and Chester",
    "Bolton",
    "Bury",
    "Manchester",
    "Oldham",
    "Rochdale",
    "Salford",
    "Stockport",
    "Tameside",
    "Trafford",
    "Wigan",
    "Knowsley",
    "Liverpool",
    "St. Helens",
    "Sefton",
    "Wirral",
    "Lancashire",
}
WEST_MIDLANDS = {
    "Herefordshire, County of",
    "Telford and Wrekin",
    "Stoke-on-Trent",
    "Shropshire",
    "Birmingham",
    "Coventry",
    "Dudley",
    "Sandwell",
    "Solihull",
    "Walsall",
    "Wolverhampton",
    "Staffordshire",
    "Warwickshire",
    "Worcestershire",
}
EAST_MIDLANDS = {
    "North East Lincolnshire",
    "North Lincolnshire",
    "Derby",
    "Leicester",
    "Rutland",
    "Nottingham",
    "North Northamptonshire",
    "West Northamptonshire",
    "Derbyshire",
    "Leicestershire",
    "Lincolnshire",
    "Nottinghamshire",
}
EAST_ANGLIA = {
    "Peterborough",
    "Luton",
    "Southend-on-Sea",
    "Thurrock",
    "Bedford",
    "Central Bedfordshire",
    "Cambridgeshire",
    "Essex",
    "Hertfordshire",
    "Norfolk",
    "Suffolk",
}
SOUTH_EAST = {
    "Medway",
    "Brighton and Hove",
    "East Sussex",
    "Kent",
    "Surrey",
    "West Sussex",
}
SOUTH = {
    "Swindon",
    "Bracknell Forest",
    "West Berkshire",
    "Reading",
    "Slough",
    "Windsor and Maidenhead",
    "Wokingham",
    "Milton Keynes",
    "Portsmouth",
    "Southampton",
    "Isle of Wight",
    "Bournemouth, Christchurch and Poole",
    "Dorset",
    "Buckinghamshire",
    "Hampshire",
    "Oxfordshire",
}
SOUTH_WEST = {
    "Bath and North East Somerset",
    "Bristol, City of",
    "North Somerset",
    "South Gloucestershire",
    "Plymouth",
    "Torbay",
    "Cornwall",
    "Isles of Scilly",
    "Wiltshire",
    "Somerset",
    "Devon",
    "Gloucestershire",
}


def download_boundaries() -> dict:
    params = urlencode(
        {
            "where": "1=1",
            "outFields": "CTYUA25CD,CTYUA25NM",
            "returnGeometry": "true",
            "outSR": "4326",
            "f": "geojson",
        }
    )
    with urlopen(f"{SERVICE_URL}?{params}", timeout=180) as response:
        return json.load(response)


def assign_region(code: str, name: str) -> tuple[str, str]:
    """Return OULAD label and mapping rationale for one ONS CUA feature."""

    if code.startswith("S"):
        return "Scotland", "All current Scottish council areas"
    if code.startswith("W"):
        return "Wales", "All current Welsh principal areas"
    if code.startswith("N"):
        return "Ireland", "Northern Ireland proxy for historic OU Ireland label"
    if code.startswith("E09"):
        return "London Region", "All London boroughs and City of London"

    name_groups = (
        (NORTH, "North Region"),
        (YORKSHIRE, "Yorkshire Region"),
        (NORTH_WEST, "North Western Region"),
        (WEST_MIDLANDS, "West Midlands Region"),
        (EAST_MIDLANDS, "East Midlands Region"),
        (EAST_ANGLIA, "East Anglian Region"),
        (SOUTH_EAST, "South East Region"),
        (SOUTH, "South Region"),
        (SOUTH_WEST, "South West Region"),
    )
    for names, region in name_groups:
        if name in names:
            return region, "Historic OU area description mapped to current ONS CUA"
    raise ValueError(f"Unmapped ONS area: {code} — {name}")


def read_oulad_regions() -> set[str]:
    if not ANALYSIS_PATH.exists():
        raise FileNotFoundError(f"Missing processed OULAD table: {ANALYSIS_PATH}")
    import pandas as pd

    return set(pd.read_csv(ANALYSIS_PATH, usecols=["region"])["region"].dropna())


def main() -> None:
    source = download_boundaries()
    rows: list[dict[str, str]] = []
    grouped: dict[str, list] = {region: [] for region in EXPECTED_REGIONS}

    for feature in source.get("features", []):
        properties = feature["properties"]
        code = str(properties["CTYUA25CD"])
        name = str(properties["CTYUA25NM"])
        region, rationale = assign_region(code, name)
        grouped[region].append(shape(feature["geometry"]))
        rows.append(
            {
                "ons_code": code,
                "ons_name": name,
                "oulad_region": region,
                "mapping_rationale": rationale,
            }
        )

    empty = sorted(region for region, geometries in grouped.items() if not geometries)
    if empty:
        raise ValueError("Regions without geometry: " + ", ".join(empty))
    observed = read_oulad_regions()
    if observed != EXPECTED_REGIONS:
        raise ValueError(
            f"OULAD labels do not match contract; missing={EXPECTED_REGIONS-observed}, "
            f"unexpected={observed-EXPECTED_REGIONS}"
        )

    output_features = []
    for region in sorted(grouped):
        # Approx. 0.005 degrees keeps the dashboard asset compact while
        # preserving coastlines/topology for a national-scale view.
        geometry = unary_union(grouped[region]).simplify(
            0.005, preserve_topology=True
        )
        output_features.append(
            {
                "type": "Feature",
                "properties": {
                    "region": region,
                    "ons_area_count": len(grouped[region]),
                    "mapping_status": "documented approximation",
                },
                "geometry": mapping(geometry),
            }
        )

    collection = {
        "type": "FeatureCollection",
        "name": "OULAD historic regions — documented ONS approximation",
        "metadata": {
            "geometry_source": SERVICE_URL.rsplit("/query", 1)[0],
            "source_page": SOURCE_PAGE,
            "geometry_license": "Open Government Licence v3.0",
            "ou_area_reference": OU_AREA_REFERENCE,
            "crs": "EPSG:4326",
            "simplification_degrees": 0.005,
                    "ireland_interpretation": (
                        "Northern Ireland proxy: ONS source covers the UK; OULAD uses "
                        "the broader label Ireland"
                    ),
            "mapping_status": "documented approximation; not official OU polygons",
        },
        "features": output_features,
    }

    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    with OUTPUT_PATH.open("w", encoding="utf-8") as handle:
        json.dump(collection, handle, ensure_ascii=False, separators=(",", ":"))
    with AUDIT_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(sorted(rows, key=lambda row: (row["oulad_region"], row["ons_code"])))

    print(
        f"Map build PASS: {len(output_features)}/13 regions, "
        f"{len(rows)} ONS areas; output={OUTPUT_PATH.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
