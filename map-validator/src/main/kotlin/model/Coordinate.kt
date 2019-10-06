package model

import org.json.JSONArray
import java.lang.Math.*

class Coordinate(val latitude: Double, val longitude: Double): Comparable<Coordinate> {
    companion object {
        private const val MAX_DISTANCE = 0.025
        private const val EARTH_RADIUS = 6373.0
    }

    fun distance(other: Coordinate): Double {
        val lat1 = toRadians(latitude)
        val lon1 = toRadians(longitude)
        val lat2 = toRadians(other.latitude)
        val lon2 = toRadians(other.longitude)

        val dlon = lon2 - lon1
        val dlat = lat2 - lat1

        val a = pow(sin(dlat / 2), 2.0) + cos(lat1) * cos(lat2) * pow(sin(dlon / 2), 2.0)
        val c = 2 * atan2(sqrt(a), sqrt(1 - a))

        return EARTH_RADIUS * c
    }

    fun heading(other: Coordinate): Double {
        val lat1 = toRadians(latitude)
        val lon1 = toRadians(longitude)
        val lat2 = toRadians(other.latitude)
        val lon2 = toRadians(other.longitude)

        val y = sin(lon2 - lon1) * cos(lat2)
        val x = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(lon2 - lon1)

        val initialBearing = Math.toDegrees(atan2(y, x))
        return (initialBearing + 360) % 360
    }

    fun createAt(distance: Double, heading: Double): Coordinate {
        val lat1 = toRadians(latitude)
        val lon1 = toRadians(longitude)
        val dist = distance / EARTH_RADIUS
        val head = toRadians(heading)

        val lat2 = asin(sin(lat1) * cos(dist) +
                cos(lat1) * sin(dist) * cos(head))

        var lon2 = lon1 + atan2(sin(head) * sin(dist) * cos(lat1),
                cos(dist) - sin(lat1) * sin(lat2))

        lon2 = (lon2 + 3 * Math.PI) % (2 * Math.PI) - Math.PI

        return Coordinate(toDegrees(lat2), toDegrees(lon2))
    }

    override fun compareTo(other: Coordinate): Boolean {
        val dist = distance(other)
        println("coordinate distance: $dist")
        return dist < MAX_DISTANCE
    }

    fun toJson(): JSONArray {
        val jsonArray = JSONArray()
        jsonArray.put(latitude)
        jsonArray.put(longitude)
        return jsonArray
    }
}