#!/bin/bash

check_vehicle_count() {
    actual=$1
    expected=$2
    min=$(LC_NUMERIC="en_US.UTF-8" printf "%.0f" $(echo $expected*0.75 | bc))
    max=$(LC_NUMERIC="en_US.UTF-8" printf "%.0f" $(echo $expected*1.25 | bc))

    if [[ $actual -ge $min && $actual -le $max ]]; then
        return 1
    else
        return 0
    fi
}

if [[ "$#" -lt 2 ]]; then
    echo "Usage: ./create.sh <directory> <n_cars> [sim_end]"
    exit 1
fi

DIR=$1
N_CARS=$2
SIM_END=100

if [[ "$#" -gt 2 ]]; then
    SIM_END=$3
fi

PERIOD=$(LC_NUMERIC="en_US.UTF-8" printf "%.0f" $(echo $SIM_END/$N_CARS/2 | bc))

echo "Directory: $DIR"
echo "Number of cars: $N_CARS"
echo "Simulation end: $SIM_END"
echo "Period: $PERIOD"

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

while : ; do
    $SUMO_HOME/tools/randomTrips.py -n $DIR/map.net.xml \
                                    -o $DIR/map.trips.xml \
                                    -r $DIR/map.rou.xml \
                                    -b 0 \
                                    -e $SIM_END \
                                    -p $PERIOD

    success=$(check_vehicle_count $(grep "<vehicle" $DIR/map.rou.xml 2>/dev/null | wc -l) $N_CARS)

    [[ success == 1 ]] || break
done

rm -f $DIR/map.sumocfg

echo "<configuration>" >> $DIR/map.sumocfg
echo "   <input>" >> $DIR/map.sumocfg
echo "       <net-file value=\"map.net.xml\"/>" >> $DIR/map.sumocfg
echo "       <route-files value=\"map.rou.xml\"/>" >> $DIR/map.sumocfg
echo "    </input>" >> $DIR/map.sumocfg
echo "    <time>" >> $DIR/map.sumocfg
echo "        <begin value=\"0\"/>" >> $DIR/map.sumocfg
echo "        <end value=\"$SIM_END\"/>" >> $DIR/map.sumocfg
echo "        <step-length value=\"1\"/>" >> $DIR/map.sumocfg
echo "    </time>" >> $DIR/map.sumocfg
echo "</configuration>" >> $DIR/map.sumocfg
