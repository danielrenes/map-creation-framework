package model

import org.json.JSONArray
import java.io.File
import kotlin.math.abs

abstract class Path(var coordinates: List<Coordinate>): Comparable<Path> {
    companion object {
        private const val MAX_HEADING_DIFF = 2.0
    }

    init {
        if (coordinates.isNotEmpty()) {
            val simplifiedCoordinates = mutableListOf<Coordinate>()
            simplifiedCoordinates.add(coordinates[0])

            val headings = mutableListOf<Double>()

            for (i in 0 until (coordinates.size - 1)) {
                headings.add(coordinates[i].heading(coordinates[i + 1]))
            }

            var i = 0

            while (i < headings.size) {
                val heading1 = headings[i]

                var j = i

                while (++j < headings.size) {
                    val heading2 = headings[j]

                    if (abs(heading1 - heading2) > MAX_HEADING_DIFF) {
                        simplifiedCoordinates.add(coordinates[j])
                        break
                    }
                }

                i = j
            }

            val lastCoordinate = coordinates[coordinates.size - 1]
            if (!simplifiedCoordinates.contains(lastCoordinate)) {
                simplifiedCoordinates.add(lastCoordinate)
            }

            coordinates = simplifiedCoordinates
        }
    }

    fun length(): Double {
        var l = 0.0

        for (i in 1 until coordinates.size) {
            l += coordinates[i - 1].distance(coordinates[i])
        }

        return l
    }

//    protected fun adjust(length: Double, nPoints: Int, coordinates: List<Coordinate>): List<Coordinate> {
//        if (coordinates.size != 2) {
//            throw IllegalStateException("Adjust is only valid for paths with 2 points")
//        }
//
//        val adjusted = mutableListOf(coordinates[0])
//        val segments = nPoints - 1
//        val step = length / segments
//        val heading = coordinates[0].heading(coordinates[1])
//
//        for (i in 1..segments) {
//            val coordinate = adjusted.last().createAt(step, heading)
//            adjusted.add(coordinate)
//        }
//
//        return adjusted
//    }
//
//    open fun adjust(length: Double, segments: Int): List<Coordinate> {
//        return adjust(length, segments, coordinates)
//    }

    protected fun adjust(distances: List<Double>, coordinates: List<Coordinate>): List<Coordinate> {
        if (coordinates.size != 2) {
            throw IllegalStateException("Adjust is only valid for paths with 2 points")
        }

        val adjusted = mutableListOf(coordinates[0])
        val heading = coordinates[0].heading(coordinates[1])

        for (distance in distances) {
            val coordinate = adjusted.last().createAt(distance, heading)
            adjusted.add(coordinate)
        }

        return adjusted
    }

    open fun adjust(distances: List<Double>): List<Coordinate> {
        return adjust(distances, coordinates)
    }

    override fun compareTo(other: Path): Boolean {
//        val adjusted = adjust(other.length(), other.coordinates.size)

        val distances = mutableListOf<Double>()
        for (i in 1 until other.coordinates.size) {
            distances.add(other.coordinates[i - 1].distance(other.coordinates[i]))
        }

        val adjusted = adjust(distances)

//        debug(adjusted, other.coordinates)

        for ((coord1, coord2) in adjusted.zip(other.coordinates)) {
            if (!coord1.compareTo(coord2)) {
                return false
            }
        }

        return true
    }

    fun toJson(): JSONArray {
        val jsonArray = JSONArray()
        for (coordinate in coordinates) {
            jsonArray.put(coordinate.toJson())
        }
        return jsonArray
    }

    // TODO: remove later
    fun debug(coordinates1: List<Coordinate>, coordinates2: List<Coordinate>) {
        val template = """<html>
    <head>
    <title>Debug</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.5.1/leaflet.css"/>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.5.1/leaflet.js"></script>
    </head>

    <body>
    <div id="map" style="height: 600px"></div>
    <script>
    const data = {
        %s
    };

    const map = L.map("map", {
        center: [47.5, 19.0],
        zoom: 12
    });

    L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        subdomains: ['a','b','c']
    }).addTo(map);

    for (const key in data) {
        const points = data[key];
        let color = "rgb(255, 0, 0)";
        if (key === "other") {
            color = "rgb(0, 0, 255)";
        }

        L.polyline(points, {color: color}).addTo(map);
    }
    </script>
    </body>
</html>"""

        val stringBuilder = StringBuilder()
        stringBuilder.append("\"adjusted\": [\n")
        for (coord in coordinates1) {
            stringBuilder.append("[${coord.latitude}, ${coord.longitude}],")
        }
        stringBuilder.append("],\n")
        stringBuilder.append("\"other\": [\n")
        for (coord in coordinates2) {
            stringBuilder.append("[${coord.latitude}, ${coord.longitude}],")
        }
        stringBuilder.append("],\n")

        File("/home/rd/Documents/Diplomamunka/0_FINAL/debug2.html").writeText(String.format(template, stringBuilder.toString()))
    }
}