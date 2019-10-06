package model

import org.json.JSONArray
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
        println("compare paths")

        val distances = mutableListOf<Double>()
        for (i in 1 until other.coordinates.size) {
            distances.add(other.coordinates[i - 1].distance(other.coordinates[i]))
        }

        val adjusted = adjust(distances)

        println("adjusted size: ${adjusted.size}")
        println("other size: ${other.coordinates.size}")

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
}