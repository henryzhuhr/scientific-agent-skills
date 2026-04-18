# 多语言地理空间编程

跨 8 种语言的地理空间编程：R、Julia、JavaScript、C++、Java、Go、Rust 和 Python。

## R Geospatial

### sf（简单功能）

```r
library(sf)
library(dplyr)
library(ggplot2)

# Read spatial data
roads <- st_read("roads.shp")
zones <- st_read("zones.geojson")

# Basic operations
st_crs(roads)  # Check CRS
roads_utm <- st_transform(roads, 32610)  # Reproject

# Geometric operations
roads_buffer <- st_buffer(roads, dist = 100)  # Buffer
roads_simplify <- st_simplify(roads, tol = 0.0001)  # Simplify
roads_centroid <- st_centroid(roads)  # Centroid

# Spatial joins
joined <- st_join(roads, zones, join = st_intersects)

# Overlay
intersection <- st_intersection(roads, zones)

# Plot
ggplot() +
  geom_sf(data = zones, fill = NA) +
  geom_sf(data = roads, color = "blue") +
  theme_minimal()

# Calculate area
zones$area <- st_area(zones)  # In CRS units
zones$area_km2 <- st_area(zones) / 1e6  # Convert to km2
```

### terra（栅格）处理）

```r
library(terra)

# Load raster
r <- rast("elevation.tif")

# Basic info
r
ext(r)  # Extent
crs(r)  # CRS
res(r)  # Resolution

# Raster calculations
slope <- terrain(r, v = "slope")
aspect <- terrain(r, v = "aspect")

# Multi-raster operations
ndvi <- (s2[[8]] - s2[[4]]) / (s2[[8]] + s2[[4]])

# Focal operations
focal_mean <- focal(r, w = matrix(1, 3, 3), fun = mean)
focal_sd <- focal(r, w = matrix(1, 5, 5), fun = sd)

# Zonal statistics
zones <- vect("zones.shp")
zonal_mean <- zonal(r, zones, fun = mean)

# Extract values at points
points <- vect("points.shp")
values <- extract(r, points)

# Write output
writeRaster(slope, "slope.tif", overwrite = TRUE)
```

### R 工作流程

```r
# Complete land cover classification
library(sf)
library(terra)
library(randomForest)
library(caret)

# 1. Load data
training <- st_read("training.shp")
s2 <- rast("sentinel2.tif")

# 2. Extract training data
training_points <- st_centroid(training)
values <- extract(s2, training_points)

# 3. Combine with labels
df <- data.frame(values)
df$class <- as.factor(training$class_id)

# 4. Train model
set.seed(42)
train_index <- createDataPartition(df$class, p = 0.7, list = FALSE)
train_data <- df[train_index, ]
test_data <- df[-train_index, ]

rf_model <- randomForest(class ~ ., data = train_data, ntree = 100)

# 5. Predict
predicted <- predict(s2, model = rf_model)

# 6. Accuracy
conf_matrix <- confusionMatrix(predict(rf_model, test_data), test_data$class)
print(conf_matrix)

# 7. Export
writeRaster(predicted, "classified.tif", overwrite = TRUE)
```

## Julia Geospatial

### ArchGDAL.jl

```julia
using ArchGDAL
using GeoInterface

# Register drivers
ArchGDAL.registerdrivers() do
    # Read shapefile
    data = ArchGDAL.read("countries.shp") do dataset
        layer = dataset[1]
        features = []
        for feature in layer
            geom = ArchGDAL.getgeom(feature)
            push!(features, geom)
        end
        features
    end
end

# Create geometries
using GeoInterface

point = GeoInterface.Point(-122.4, 37.7)
polygon = GeoInterface.Polygon([GeoInterface.LinearRing([
    GeoInterface.Point(-122.5, 37.5),
    GeoInterface.Point(-122.3, 37.5),
    GeoInterface.Point(-122.3, 37.8),
    GeoInterface.Point(-122.5, 37.8),
    GeoInterface.Point(-122.5, 37.5)
])])

# Geometric operations
buffered = GeoInterface.buffer(point, 1000)
intersection = GeoInterface.intersection(poly1, poly2)
```

### GeoStats.jl

```julia
using GeoStats
using GeoStatsBase
using Variography

# Load point data
data = georef((value = [1.0, 2.0, 3.0],),
              [Point(0.0, 0.0), Point(1.0, 0.0), Point(0.5, 1.0)])

# Experimental variogram
γ = variogram(EmpiricalVariogram, data, :value, maxlag = 1.0)

# Fit theoretical variogram
γfit = fit(EmpiricalVariogram, γ, SphericalVariogram)

# Ordinary kriging
problem = OrdinaryKriging(data, :value, γfit)
solution = solve(problem)

# Simulate
simulation = SimulationProblem(data, :value, SphericalVariogram, 100)
result = solve(simulation)
```

## JavaScript（Node.js 和浏览器）

### Turf.js（浏览器/节点）

```javascript
// npm install @turf/turf
const turf = require('@turf/turf');

// Create features
const pt1 = turf.point([-122.4, 37.7]);
const pt2 = turf.point([-122.3, 37.8]);

// Distance (in kilometers)
const distance = turf.distance(pt1, pt2, { units: 'kilometers' });

// Buffer
const buffered = turf.buffer(pt1, 5, { units: 'kilometers' });

// Bounding box
const bbox = turf.bbox(buffered);

// Along a line
const line = turf.lineString([[-122.4, 37.7], [-122.3, 37.8]]);
const along = turf.along(line, 2, { units: 'kilometers' });

// Within
const points = turf.points([
  [-122.4, 37.7],
  [-122.35, 37.75],
  [-122.3, 37.8]
]);
const polygon = turf.polygon([[[-122.4, 37.7], [-122.3, 37.7], [-122.3, 37.8], [-122.4, 37.8], [-122.4, 37.7]]]);
const ptsWithin = turf.pointsWithinPolygon(points, polygon);

// Nearest point
const nearest = turf.nearestPoint(pt1, points);

// Area
const area = turf.area(polygon); // square meters

```

### 传单（Web）映射)

```javascript
// Initialize map
const map = L.map('map').setView([37.7, -122.4], 13);

// Add tile layer
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Add GeoJSON layer
fetch('data.geojson')
  .then(response => response.json())
  .then(data => {
    L.geoJSON(data, {
      style: function(feature) {
        return { color: feature.properties.color };
      },
      onEachFeature: function(feature, layer) {
        layer.bindPopup(feature.properties.name);
      }
    }).addTo(map);
  });

// Add markers
const marker = L.marker([37.7, -122.4]).addTo(map);
marker.bindPopup("Hello!").openPopup();

// Draw circles
const circle = L.circle([37.7, -122.4], {
  color: 'red',
  fillColor: '#f03',
  fillOpacity: 0.5,
  radius: 500
}).addTo(map);
```

## C++ 地理空间

### GDAL C++ API

```cpp
#include "gdal_priv.h"
#include "ogr_api.h"
#include "ogr_spatialref.h"

// Open raster
GDALDataset *poDataset = (GDALDataset *) GDALOpen("input.tif", GA_ReadOnly);

// Get band
GDALRasterBand *poBand = poDataset->GetRasterBand(1);

// Read data
int nXSize = poBand->GetXSize();
int nYSize = poBand->GetYSize();
float *pafScanline = (float *) CPLMalloc(sizeof(float) * nXSize);
poBand->RasterIO(GF_Read, 0, 0, nXSize, 1,
                 pafScanline, nXSize, 1, GDT_Float32, 0, 0);

// Vector data
GDALDataset *poDS = (GDALDataset *) GDALOpenEx("roads.shp",
    GDAL_OF_VECTOR, NULL, NULL, NULL);
OGRLayer *poLayer = poDS->GetLayer(0);

OGRFeature *poFeature;
poLayer->ResetReading();
while ((poFeature = poLayer->GetNextFeature()) != NULL) {
    OGRGeometry *poGeometry = poFeature->GetGeometryRef();
    // Process geometry
    OGRFeature::DestroyFeature(poFeature);
}

GDALClose(poDS);
```

## Java 地理空间

### GeoTools

```java
import org.geotools.data.FileDataStore;
import org.geotools.data.FileDataStoreFinder;
import org.geotools.data.simple.SimpleFeatureCollection;
import org.geotools.data.simple.SimpleFeatureIterator;
import org.geotools.data.simple.SimpleFeatureSource;
import org.geotools.geometry.jts.JTS;
import org.geotools.referencing.CRS;
import org.opengis.feature.simple.SimpleFeature;
import org.opengis.referencing.crs.CoordinateReferenceSystem;

import org.locationtech.jts.geom.Coordinate;
import org.locationtech.jts.geom.GeometryFactory;
import org.locationtech.jts.geom.Point;

// Load shapefile
File file = new File("roads.shp");
FileDataStore store = FileDataStoreFinder.getDataStore(file);
SimpleFeatureSource featureSource = store.getFeatureSource();

// Read features
SimpleFeatureCollection collection = featureSource.getFeatures();
try (SimpleFeatureIterator iterator = collection.features()) {
    while (iterator.hasNext()) {
        SimpleFeature feature = iterator.next();
        Geometry geom = (Geometry) feature.getDefaultGeometryProperty().getValue();
        // Process geometry
    }
}

// Create point
GeometryFactory gf = new GeometryFactory();
Point point = gf.createPoint(new Coordinate(-122.4, 37.7));

// Reproject
CoordinateReferenceSystem sourceCRS = CRS.decode("EPSG:4326");
CoordinateReferenceSystem targetCRS = CRS.decode("EPSG:32633");
MathTransform transform = CRS.findMathTransform(sourceCRS, targetCRS);
Geometry reprojected = JTS.transform(point, transform);
```

## Go Geospatial

### 简单功能 Go

```go
package main

import (
    "fmt"
    "github.com/paulmach/orb"
    "github.com/paulmach/orb/geojson"
    "github.com/paulmach/orb/planar"
)

func main() {
    // Create point
    point := orb.Point{122.4, 37.7}

    // Create linestring
    line := orb.LineString{
        {122.4, 37.7},
        {122.3, 37.8},
    }

    // Create polygon
    polygon := orb.Polygon{
        {{122.4, 37.7}, {122.3, 37.7}, {122.3, 37.8}, {122.4, 37.8}, {122.4, 37.7}},
    }

    // GeoJSON feature
    feature := geojson.NewFeature(polygon)
    feature.Properties["name"] = "Zone 1"

    // Distance (planar)
    distance := planar.Distance(point, orb.Point{122.3, 37.8})

    // Area
    area := planar.Area(polygon)

    fmt.Printf("Distance: %.2f meters\n", distance)
    fmt.Printf("Area: %.2f square meters\n", area)
}
```

有关所有语言的更多代码示例，请参阅 [code-examples.md](code-examples.md)。

## Rust Geospatial

### GeoRust (地理 Rust)

Rust 地理空间生态系统包括用于几何操作、投影和文件 I/O 的包。

\`\`\`rust
// Cargo.toml 依赖项:
// geo = "0.28"
// 地理类型 = "0.7"
// 项目 = "0.27"
// shapefile = "0.5"

use geo::{坐标、点、线串、多边形、几何};
use geo::prelude::*;
use proj::Proj;

fn main() -> Result<(), Box<dyn std::error::Error>> {
 // 创建一个点
 let point = Point::new(-122.4_f64, 37.7_f64);

 // 创建线串
 let linestring = LineString::new(vec![
 Coord { x: -122.4, y: 37.7 },
 Coord { x: -122.3, y: 37.8 },
 Coord { x: -122.2, y: 37.9 },
 ]);

 // 创建多边形
 let Polygon = Polygon::new(
 LineString::new(vec![
 Coord { x: -122.4, y: 37.7 },
 坐标 { x: -122.3, y: 37.7 },
 坐标 { x: -122.3, y: 37.8 },
 坐标 { x: -122.4, y: 37.8 },
 Coord { x: -2.4, y: 37.7 }, // 闭合环
 ]),
 vec![], // 无内部环
 );

// 几何运算
 let buffered = Polygon.buffer(1000.0); // 以 CRS 为单位的缓冲区
 let centroid = Polygon.centroid();
 letconvex_hull = Polygon.convex_hull();
 let simple = Polygon.simplify(&1.0); // 容差

 // 空间关系
 let point_within = point.within(&polygon);
 let line_intersects = linestring.intersects(&polygon);

 // 坐标变换
 let from = "EPSG:4326";
 let to = "EPSG:32610";
 let proj = Proj::new_known_crs(from, to, None)?;
 lettransformed = proj.convert(point)?;

 println!("Point: {:?}", point);
 println!("多边形内：{}", point_within);

 好的(())
}
\`\`\`
