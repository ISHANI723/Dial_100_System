
let poly;
let map;
let marker;
let firstMarker;
let oldRoads = [];
let isLocationOnEdge;


RoadDataPoints=[
    [{lat: 23.32962393577972, lng: 77.48162019865883},{lat: 23.32892366149808, lng: 77.4813561740502},{lat: 23.328450616051402, lng: 77.48081630493382},{lat: 23.32769486115252, lng: 77.48056229802336},{lat: 23.31399200035118,lng: 77.47640803995446},{lat: 23.3088613263554,lng: 77.47569950413255},{lat: 23.304202266110526, lng: 77.47439901750771}],
    [{lat: 23.197102918941187, lng: 77.32623962597603},{lat: 23.197153413160592, lng: 77.32251888750746},{lat: 23.194654182053508, lng: 77.31726285716753},{lat: 23.192582634907957, lng: 77.31306584181543}],
    [{lat: 23.199608652800464, lng: 77.30682247948077},{lat: 23.200475582425465, lng: 77.30225000531239}],
    [{lat: 23.202317936252292, lng: 77.29693019540794},{lat: 23.20294269002214, lng: 77.2931078569802}],
    [{lat: 24.931437929112363, lng: 80.80399310281373},{lat: 24.93954582616204, lng: 80.79959060021167},{lat: 24.94253025230772, lng: 80.80152479477522},{lat: 24.94660265383243, lng: 80.80006402469417},{lat: 24.953426506458662, lng: 80.8000059577573},{lat: 24.95743314656743, lng: 80.79965959036778},{lat: 24.958664723213868, lng: 80.79720085115787},{lat: 24.960247449761265, lng: 80.79534151686273},{lat: 24.963224256804704, lng: 80.79555117129314},{lat: 24.965198349757305, lng: 80.79354444536135},{lat: 24.966384956220214, lng: 80.79280631218228},{lat: 24.971639971683302, lng: 80.7945784715962},{lat: 24.977209182041044, lng: 80.79729303631736},{lat: 24.98379118446514, lng: 80.80053044154471},{lat: 24.992741470233266, lng: 80.80460793290047},{lat: 24.996080988870606, lng: 80.80527148985072},{lat: 24.996867395069085, lng: 80.8028983832687},{lat: 25.000586489479943, lng: 80.8007629135824},{lat: 25.002169160034157, lng: 80.7994403389862},{lat: 25.00457867639725, lng: 80.80231308634451},{lat: 25.012494518153712, lng: 80.80852416803857},{lat: 25.015742225846804, lng: 80.80874311075878},{lat: 25.022732285306446, lng: 80.81456958534443},{lat: 25.026266861113292, lng: 80.8172174672495},{lat: 25.032491032827078, lng: 80.82064950381364},{lat: 25.040262512143823, lng: 80.81845232381372},{lat: 25.041118514781875, lng: 80.81899489134642},{lat: 25.047809173803827, lng: 80.82087777386296},{lat: 25.055472117288257, lng: 80.82157247311747},{lat: 25.062007190625867, lng: 80.82459849840778},{lat: 25.06692680871078, lng: 80.8225740398569},{lat: 25.06792488412319, lng: 80.8213467098553},{lat: 25.071210933772385, lng: 80.82269332150696},{lat: 25.07314228193344, lng: 80.82122736887116},{lat: 25.07383298934704, lng: 80.82333478821546},{lat: 25.075435737098854, lng: 80.82262834633369},{lat: 25.07397107480721, lng: 80.82342047279337},{lat: 25.07540722079904, lng: 80.82278697072047},{lat: 25.076033375125615, lng: 80.8240769016802},{lat: 25.077361438755133, lng: 80.82404938255614},{lat: 25.077592368940753, lng: 80.82518572107631},{lat: 25.07914034853817, lng: 80.82622293296089},{lat: 25.080809032229542, lng: 80.82544305554728},{lat: 25.082972426947357, lng: 80.82414989071222},{lat: 25.09093441278831, lng: 80.82786019766392},{lat: 25.09623090282094, lng: 80.83533524163738},{lat: 25.100486658233752, lng: 80.83379536608331},{lat: 25.100728868319887, lng: 80.83227786087626},{lat: 25.102702627873413, lng: 80.83323920826797},{lat: 25.104379518697836, lng: 80.83650667544332}]
    ]

RoadData=[]

let oldRoadsPoly=[];


function initMap() {
    isLocationOnEdge = google.maps.geometry.poly.isLocationOnEdge
    map = new google.maps.Map(document.getElementById("RouteMap"), {
        zoom: 17,
        //center: { lat: 22.598576940415658, lng: 88.40287426753889 },
        //center: { lat: 22.60719525900128, lng: 88.41133619141767 },
        center: {lat: 24.958664723213868, lng: 80.79720085115787},
    });


        const lineSymbol = {
            path: google.maps.SymbolPath.CIRCLE,
            scale: 8,
            strokeColor: "#393",
          };

    // Plot old roads
    RoadDataPoints.forEach((points,i) => {
        const path = new google.maps.Polyline({
            path: points,
            strokeColor: "#0000FF",
            strokeOpacity: 1.0,
            strokeWeight: 5,
            clickable: true,
            icons: (i == 4) ? [
                {
                  icon: lineSymbol,
                  offset: "100%",
                },
              ]: [],
            });
        path.setMap(map);
        path.onPath=true
        path.addListener('click', addLatLng)
        path.setVisible(true);
        oldRoads.push(path);
    })


    animateCircle(oldRoads[4])
    oldRoads[4].addListener('click', (event)=> {
        const content= `
        <div id="content">
            <div id="siteNotice"></div>
            <h5 id="firstHeading" class="firstHeading">Majhgawa - Chitrakoot Highway - NH11</h5>
            <div id="bodyContent">
            <strong>
            <p>Width: 27m</p>
            <p>Material: Concrete Road</p>
            </strong>
            </div>
        </div>
      `
        const infoWindow = new google.maps.InfoWindow({
                content: content,
                position: event.latLng
            });
            infoWindow.open(map);
    });

    // Add a listener for the click event
    // map.addListener("click", addLatLng);


function animateCircle(line) {
    let count = 0;
  
    window.setInterval(() => {
      count = (count + 1) % 200;
  
      const icons = line.get("icons");
  
      icons[0].offset = count / 2 + "%";
      line.set("icons", icons);
    }, 100);
    google.maps.event.clearInstanceListeners(line);
  }

}
// Handles click events on a map, and adds a new point to the Polyline.
function addLatLng(event) {
    const path = poly.getPath();
    let onRoad = false;

    oldRoads.forEach(road => {
        onRoad = false
        // Because path is an MVCArray, we can simply append a new coordinate
        // and it will automatically appear.

        if (road.onPath || isLocationOnEdge(event.latLng, road)) {
            onRoad = true
        } else {
            onRoad = false
        }
    })
    
        path.push(event.latLng);
        // Add a new marker at the new plotted point on the polyline.
        if (firstMarker) {
            if (marker) {
                marker.setMap(null);
            }
            marker = new google.maps.Marker({
                position: event.latLng,
                title: "#" + path.getLength(),
                map: map,
            });
        } else {
            firstMarker = new google.maps.Marker({
                position: event.latLng,
                title: "#" + path.getLength(),
                map: map,
            })
        }

        function getCookie(key) {
            var cookies = document.cookie;
            var value = cookies.split(key + '=');
            if (value.length > 1) {
                return value[1].split(';')[0]
        
            }
        }

        console.log(event.latLng.lat(), event.latLng.lng())

        ajaxfunction(event.latLng.lat(), event.latLng.lng());
        
        function ajaxfunction(lat,lng){
            $.ajax({
              type: "POST",
              url: "/draw",
              data: {
                lat: lat,
                lng:lng,
                csrfmiddlewaretoken: getCookie('csrftoken')
              },
              success: (response) => {
                if (response.status == 'OK') console.log('frv journey started')
              }
              });
        }
    // }
}
//        JSON.stringify(mapsMouseEvent.latLng.toJSON(), null, 2)


window.initMap = initMap;
