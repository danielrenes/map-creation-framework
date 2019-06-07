#!/bin/bash

if [[ "$#" != 2 ]]; then
    echo "Usage: ./create.sh <directory> <#cars>"
    exit 1
fi

DIR=$1
N_CARS=$2

E=$(LC_NUMERIC="en_US.UTF-8" printf "%.0f" $(echo $N_CARS*1.75 | bc))

rm -f $DIR/*.xml

netconvert --osm-files $DIR/map.osm \
           --geometry.remove \
           --roundabouts.guess \
           --ramps.guess \
           --junctions.join \
           --tls.guess-signals \
           --tls.discard-simple \
           --tls.join \
	   --no-turnarounds \
           --type-files $SUMO_HOME/data/typemap/osmNetconvertUrbanDe.typ.xml \
           -o $DIR/map.net.xml

polyconvert --net-file $DIR/map.net.xml \
            --osm-files $DIR/map.osm \
            --type-file $SUMO_HOME/data/typemap/osmPolyconvert.typ.xml \
            -o $DIR/map.typ.xml

while [ "$(grep "<vehicle" $DIR/map.rou.xml 2>/dev/null | wc -l)" != "$N_CARS" ]; do
    $SUMO_HOME/tools/randomTrips.py -n $DIR/map.net.xml \
                                    -e $E \
                                    -o $DIR/map.trips.xml \
                                    -r $DIR/map.rou.xml \

    sed -i 's/depart="[0-9]*/depart="0/' $DIR/map.trips.xml
    sed -i 's/depart="[0-9]*/depart="0/' $DIR/map.rou.xml
done

rm -f $DIR/map.sumocfg

echo "<configuration>" >> $DIR/map.sumocfg
echo "   <input>" >> $DIR/map.sumocfg
echo "       <net-file value=\"map.net.xml\"/>" >> $DIR/map.sumocfg
echo "       <route-files value=\"map.rou.xml\"/>" >> $DIR/map.sumocfg
echo "    </input>" >> $DIR/map.sumocfg
echo "    <time>" >> $DIR/map.sumocfg
echo "        <begin value=\"0\"/>" >> $DIR/map.sumocfg
echo "        <end value=\"100\"/>" >> $DIR/map.sumocfg
echo "        <step-length value=\"1\"/>" >> $DIR/map.sumocfg
echo "    </time>" >> $DIR/map.sumocfg
echo "</configuration>" >> $DIR/map.sumocfg
