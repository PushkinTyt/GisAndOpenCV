var flag = 1;
var myStyle = {
    "color": "#ff7800",
    "weight": 5,
    "opacity": 0.65
};
var map = L.map('map').setView([58.05418,56.22439], 17);

var line_way = L.polyline([
    [3.05569, 56.21787],
    [3.055, 56.22627]],
    {
        color: "#ff7800",
        weight: 5,
        opacity: 0.65
    }
    ).addTo(map);

var custom_way = L.polyline([
    ],
    {
        color: "red",
        weight: 5,
        opacity: 0.65
    }
    ).addTo(map);

    //L.geoJson(myLines, {
                    //	style: myStyle
                    //}).addTo(map);
var popup = L.popup();
var marker = L.marker([51.5, -0.09]).addTo(map);
get_loc();

L.easyButton( '<span class="star">&neArr;</span>', function(btn, map){
    url = "/GIS2/send/way"
    xhr = new XMLHttpRequest();
    xhr.open("POST", url, true);
    xhr.send(JSON.stringify(custom_way.toGeoJSON()));
    //xhr.send(custom_way.toGeoJSON());
    xhr.onreadystatechange = function()
    {
        var loading = document.getElementById ( "wait" );
        var msg = document.getElementById ( "msg" );
        if ( xhr.readyState <= 3 )
            loading.style.visibility = "visible";
            window.setTimeout(function(){ loading.style.visibility = "hidden"; }, 3000);
            msg.style.visibility = "visible";
            window.setTimeout(function(){ msg.style.visibility = "hidden"; }, 3000);
            console.log('visible')
        if (xhr.readyState == 4)
        {
            if (xmlhttp.status == 200)
            {
                xhr.onloadend = function ()
                {
                    // done
                };
                document.getElementById("msg").innerHTML = xhr.responseText;
                loading.style.visibility = "hidden";
                //window.setTimeout(function(){ loading.style.visibility = "hidden"; }, 3000);
                window.setTimeout(function(){ msg.style.visibility = "hidden"; }, 3000);

                line_way = line_way.setLatLngs(custom_way.getLatLngs());
                custom_way = custom_way.setLatLngs([]);
                flag = 1;

            }
            else
            {
                //
            }
        }
    }
}).addTo(map);//building way button

L.easyButton( '<span class="star">&xopf;</span>', function(btn, map){
  //new L.latLng(myLines.geometry.coordinates[index][1], myLines.geometry.coordinates[index][0]);
  custom_way = custom_way.setLatLngs([]);
  flag = 1;
}).addTo(map);

L.tileLayer('TileGenPerm/{z}/{x}/{y}.png', {
    maxZoom: 17,
    minZoom: 13
}).addTo(map);

function send_json(JSON_Data){
    //var xhr = new XMLHttpRequest();
    //xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');

    // send the collected data as JSON
    //xhr.send(JSON.stringify(JSON_Data));

    //xhr.onloadend = function () {
        // done
    //};
}

function get_loc() {
    xmlhttp = new XMLHttpRequest();
    try
    {
        xmlhttp.open("GET", "/GIS2/get/current_loc");
        xmlhttp.onreadystatechange = function()
        {
            if (xmlhttp.readyState == 4)
            {
                if (xmlhttp.status == 200)
                {
                    //var marker = L.marker([lat,lng]).addTo(map);
                    //console.log(xmlhttp.responseText)
                    geojsonFeature = JSON.parse(xmlhttp.responseText);
                    //console.log(geojsonFeature)
                    //L.marker([51.5, -0.09]).addTo(map)

                    //x = L.geoJson(geojsonFeature).addTo(map);
                    //console.log(geojsonFeature.geometry.coordinates[0], geojsonFeature.geometry.coordinates[1]);
                    //console.log(geojsonFeature['coordinates'][0]);
                    //marker.setLatLng(L.geoJson(geojsonFeature));
                    cur_loc = new L.LatLng(geojsonFeature.geometry.coordinates[1], geojsonFeature.geometry.coordinates[0]);
                    //console.log(cur_loc)
                    marker.setLatLng(cur_loc);
                }

                else
                {
                    //delete marker
                }
            }
        }

        xmlhttp.send(null);
    }
    catch (e)
    {
        //delete marker
    }
}

function get_way()
{
    xmlhttp = new XMLHttpRequest();
    try
    {
        xmlhttp.open("GET", "/GIS2/get/way");
        xmlhttp.onreadystatechange = function()
        {
            if (xmlhttp.readyState == 4)
            {
                if (xmlhttp.status == 200)
                {
                    myLines = JSON.parse(xmlhttp.responseText);
                    //L.geoJson(myLines, {
                    //	style: myStyle
                    //}).addTo(map);

                    ///set line
                    //console.log(myLines.geometry.coordinates)
                    var Arr1 = myLines.geometry.coordinates

                    var LtLnArray = new Array(Arr1.length);
                    var index = 0;
                    //console.log(myLines)
                    while(index < LtLnArray.length){
                        LtLnArray[index] = new L.latLng(myLines.geometry.coordinates[index][1], myLines.geometry.coordinates[index][0]);
                        //console.log(LtLnArray[index])
                        index++;
                    }
                    //console.log(LtLnArray);
                    //latlng_way = new L.latLng(myLines.geometry.coordinates);
                    //console.log(latlng_way)
                    //console.log('DO')
                    //console.log(line_way);
                    line_way = line_way.setLatLngs(LtLnArray);
                    //console.log('POSLE')
                    //console.log(line_way);
                }

                else
                {
                    //delete marker
                }
            }
        }
        xmlhttp.send(null);
    }

    catch (e)
    {
        //delete marker
    }
}

var timer_loc = window.setInterval("get_loc();", 3000);
var timer_way = window.setInterval("get_way();", 2000);

function cust_way(){
    //if(flag == 1){
        get_loc();
        custom_way.addLatLng(marker.getLatLng());
        //custom_way.setLatLngs(marker.getLatLng());
        console.log(flag)
        flag = 0
        console.log(flag)
    //}
}

function onMapClick(e) {
    popup
        .setLatLng(e.latlng)
        .setContent("New way point " + e.latlng.toString())
        .openOn(map);
        console.log(e.latlng);
    custom_way = custom_way.setLatLngs([]);
    cust_way();
    custom_way.addLatLng(e.latlng);
}
map.on('click', onMapClick);