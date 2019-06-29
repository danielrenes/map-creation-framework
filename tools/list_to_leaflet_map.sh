#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: ./list_to_leaflet_map.sh <filepath> <html_out>"
    exit 1
fi

FILE=$1
HTML_OUT=$2

POLYLINES=$(sed 's/^\[/    new L.Polyline([/gI' $FILE |\
    sed 's/^\t\[/      [/gI' |\
    sed 's/^\],/    ], {color: \"blue\", weight: 5, opacity: 0.5}).addTo(map);/gI' |\
    sed 's/^]/    ], {color: \"blue\", weight: 5, opacity: 0.5}).addTo(map);/gI'
)

rm $HTML_OUT

cat << END >> $HTML_OUT
<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.5.1/leaflet.css" />
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.5.1/leaflet.js"></script>
  </head>
  <body>
    <div id="map" style="width: 800px; height: 600px"></div>
    <script>
    const map = L.map('map', {
      'center': [0, 0],
      'zoom': 0,
      'layers': [
        L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          'attribution': 'Map data &copy; OpenStreetMap contributors'
        })
      ]
    });
$POLYLINES
    </script>
  </body>
</html>
END

firefox $HTML_OUT
