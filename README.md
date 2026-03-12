# Health Facilities Visualization - QGIS Exploration

A project to visualize health facilities (hospitals, PHCs, labs) across Indian states using GIS tools, with capability to find nearest health facility from any location.

## Project Goals

1. **Visualize health facilities** on a map with state-level granularity
2. **Find nearest health facility** from a given location
3. **Multi-layer visualization** - Hospitals, Health Centers, and Lab facilities as separate layers

---

## Data Sources for Health Facility Coordinates

### Primary Sources (Government of India)

| Source | Description | Link |
|--------|-------------|------|
| **National Hospital Directory** | Hospitals with geo-codes, contact details, specializations | [data.gov.in](https://data.gov.in/resource/national-hospital-directory-geo-code-and-additional-parameters-updated-till-last-month) |
| **All India Health Centres Directory** | PHCs, Sub-centres, CHCs, District/State hospitals with lat/long | [data.gov.in](https://data.gov.in/catalog/all-india-health-centres-directory) |
| **Hospital Directory (NHP)** | State-wise hospitals via National Health Portal | [data.gov.in](https://data.gov.in/catalog/hospital-directory-national-health-portal) |
| **PMGSY Rural Facilities** | ~700,000 geo-tagged rural facilities (Medical, Agro, Education) | [pmgsy.nic.in](https://pmgsy.nic.in) |

### Secondary Sources

| Source | Description | Link |
|--------|-------------|------|
| **Health Heatmap of India** | Aggregated health data with spatial references | [PMC Article](https://pmc.ncbi.nlm.nih.gov/articles/PMC7568941/) |
| **OpenStreetMap** | Community-contributed health facility data | [OSM Wiki](https://wiki.openstreetmap.org/wiki/India_Health_Facilities_Import) |
| **ESRI Living Atlas** | Healthcare facilities 2021 dataset | [ArcGIS](https://www.arcgis.com/home/item.html?id=870c1906b8d74ff89323bcae38bce511) |
| **Bharat Maps (WebGIS)** | All India constituency maps and services | [webgis1.nic.in](https://webgis1.nic.in/publishing/rest/services/) |

### For Lab Facilities (Additional Layer)

- **ICMR Lab Network**: [icmr.gov.in](https://www.icmr.gov.in) - COVID/diagnostic lab listings
- **NABL Accredited Labs**: [nabl-india.org](https://nabl-india.org) - Searchable directory
- **State-specific portals**: Many states publish lab directories (e.g., TN, KA, MH health departments)

---

## Tool Comparison

### Recommended: QGIS (for this use case)

| Tool | Best For | Nearest Facility Analysis | Learning Curve | Platform |
|------|----------|--------------------------|----------------|----------|
| **QGIS** | Full GIS analysis, multi-layer maps | Built-in (Distance Matrix, NNJoin plugin) | Medium | Desktop |
| **Kepler.gl** | Quick visualization of large datasets | Not supported | Low | Web |
| **Leaflet** | Custom web applications | Requires custom code | High (dev skills) | Web/JS |
| **Folium** | Python-based quick maps | Requires Python scripting | Medium | Python |
| **Google Earth Pro** | Simple visualization | Limited | Low | Desktop |

### Why QGIS is Best for This Project

1. **Nearest Facility Analysis**: Built-in tools for proximity analysis
   - `Distance Matrix` - Calculate distances to all facilities
   - `NNJoin Plugin` - Find nearest neighbor
   - `Service Area Analysis` - Define reachable areas

2. **Multi-layer Support**: Easily manage hospitals, PHCs, labs as separate layers

3. **State Boundaries**: Import Indian state shapefiles from [Survey of India](https://surveyofindia.gov.in) or [GADM](https://gadm.org/download_country.html)

4. **Data Format Flexibility**: Supports CSV (with lat/long), GeoJSON, Shapefiles, KML

5. **Free & Open Source**: No licensing costs

### When to Consider Alternatives

| Scenario | Recommended Tool |
|----------|------------------|
| Quick one-time visualization | Kepler.gl |
| Building a public web app | Leaflet + custom backend |
| Python data pipeline integration | Folium / GeoPandas |
| Sharing with non-technical users | Google My Maps |

---

## QGIS Setup Guide

### Installation

```bash
# macOS
brew install --cask qgis

# Ubuntu/Debian
sudo apt install qgis qgis-plugin-grass

# Windows
# Download from https://qgis.org/download/
```

### Recommended Plugins

Install via `Plugins > Manage and Install Plugins`:

1. **NNJoin** - Nearest neighbor spatial join
2. **mmqgis** - Geocoding and geometry tools
3. **QuickMapServices** - Add base maps (OpenStreetMap, Google, etc.)
4. **DataPlotly** - Data visualization charts

---

## Project Structure

```
qgis-exploration/
├── README.md
├── data/
│   ├── raw/                    # Downloaded CSV/JSON files
│   │   ├── hospitals.csv
│   │   ├── health_centers.csv
│   │   └── labs.csv
│   ├── processed/              # Cleaned data with valid coordinates
│   └── shapefiles/             # State boundaries, districts
├── projects/
│   └── health_facilities.qgz   # QGIS project file
├── scripts/
│   ├── download_data.py        # Fetch data from data.gov.in
│   ├── clean_coordinates.py    # Validate and clean lat/long
│   └── nearest_facility.py     # Python script for proximity analysis
└── exports/
    ├── maps/                   # Exported map images
    └── reports/                # Analysis reports
```

---

## Step-by-Step Workflow

### 1. Download Data

```python
# scripts/download_data.py
import requests
import pandas as pd

# Example: Download from data.gov.in API (if available)
# Or manually download CSV from the portal

# National Hospital Directory
hospitals_url = "https://data.gov.in/resource/national-hospital-directory-geo-code-and-additional-parameters-updated-till-last-month"
# Download CSV manually from the portal
```

### 2. Clean and Prepare Data

```python
# scripts/clean_coordinates.py
import pandas as pd

df = pd.read_csv('data/raw/hospitals.csv')

# Remove rows with invalid coordinates
df = df.dropna(subset=['latitude', 'longitude'])
df = df[(df['latitude'].between(6, 38)) & (df['longitude'].between(68, 98))]  # India bounds

# Save cleaned data
df.to_csv('data/processed/hospitals_clean.csv', index=False)
```

### 3. Import into QGIS

1. Open QGIS
2. `Layer > Add Layer > Add Delimited Text Layer`
3. Select your CSV file
4. Set X field = longitude, Y field = latitude
5. Set CRS to `EPSG:4326` (WGS 84)

### 4. Add State Boundaries

1. Download India shapefiles from [GADM](https://gadm.org/download_country.html)
2. `Layer > Add Layer > Add Vector Layer`
3. Select the `.shp` file

### 5. Find Nearest Facility

**Method 1: Using Distance Matrix**
1. `Processing > Toolbox > Distance Matrix`
2. Input: Your location point layer
3. Target: Health facilities layer
4. Output: Nearest facility with distance

**Method 2: Using NNJoin Plugin**
1. Install NNJoin plugin
2. `Vector > NNJoin`
3. Join your points to nearest facility

**Method 3: Python Script**
```python
# scripts/nearest_facility.py
from scipy.spatial import cKDTree
import pandas as pd
import numpy as np

def find_nearest(user_lat, user_lon, facilities_df):
    coords = facilities_df[['latitude', 'longitude']].values
    tree = cKDTree(coords)

    user_point = np.array([[user_lat, user_lon]])
    distance, idx = tree.query(user_point, k=5)  # Get 5 nearest

    return facilities_df.iloc[idx[0]]

# Usage
facilities = pd.read_csv('data/processed/hospitals_clean.csv')
nearest = find_nearest(12.9716, 77.5946, facilities)  # Bangalore coordinates
print(nearest[['name', 'address', 'latitude', 'longitude']])
```

---

## Layer Organization

| Layer | Color | Data Source |
|-------|-------|-------------|
| State Boundaries | Gray outline | GADM / Survey of India |
| District Boundaries | Light gray | GADM |
| Hospitals | Red markers | National Hospital Directory |
| Primary Health Centers (PHCs) | Blue markers | All India Health Centres Directory |
| Community Health Centers (CHCs) | Green markers | All India Health Centres Directory |
| Diagnostic Labs | Purple markers | ICMR / NABL / State portals |
| User Location | Yellow star | Manual input |

---

## Troubleshooting

### Common Issues

1. **Coordinates not showing on map**
   - Check if lat/long are swapped
   - Verify CRS is set to EPSG:4326
   - Check for invalid values (0,0 or blanks)

2. **Data quality issues**
   - Many govt datasets have ~10-20% invalid coordinates
   - Use OpenStreetMap as supplementary source

3. **Large dataset performance**
   - Use spatial indexing in QGIS
   - Consider Kepler.gl for >100k points

---

## Future Enhancements

- [ ] Add real-time location for nearest facility search
- [ ] Integrate with routing APIs (OSRM/Google) for travel time
- [ ] Build a simple web interface using Leaflet
- [ ] Add hospital bed availability data (if available)
- [ ] Create time-based accessibility maps (isochrones)

---

## References

- [Open Government Data Platform India](https://data.gov.in)
- [QGIS Documentation](https://docs.qgis.org)
- [Kepler.gl](https://kepler.gl)
- [Health Heatmap of India](https://pmc.ncbi.nlm.nih.gov/articles/PMC7568941/)
- [OpenStreetMap India Health Import](https://wiki.openstreetmap.org/wiki/India_Health_Facilities_Import)

---

## License

This project is for educational/research purposes. Data from data.gov.in is under [GODL-India](https://data.gov.in/government-open-data-license-india) license.
