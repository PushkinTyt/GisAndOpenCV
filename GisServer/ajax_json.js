var geojsonLayer = new L.GeoJSON.AJAX("geojson.json");
var geojsonLayer = L.geoJson.ajax("route/to/esri.json",{
        middleware:function(data){
            return esri2geoOrSomething(json);
        }
    });