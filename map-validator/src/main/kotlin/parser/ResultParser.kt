package parser

import model.Connection
import model.Coordinate
import model.Egress
import model.Ingress
import org.json.JSONArray
import org.json.JSONObject

class ResultParser {
    companion object {
        @JvmStatic
        fun parse(path: String): List<Connection> {
            val content = FileUtils.readFile(path)

            val connections = mutableListOf<Connection>()

            val json = JSONObject(content)
            val jsonIngresses = json.getJSONArray("ingresses")

            for (i in 0 until jsonIngresses.length()) {
                val jsonIngress = jsonIngresses.getJSONObject(i)
                val jsonCoordinates = jsonIngress.getJSONArray("points")
                val ingressCoordinates = parseCoordinates(jsonCoordinates)

                val jsonEgresses = jsonIngress.getJSONArray("egresses")

                for (j in 0 until jsonEgresses.length()) {
                    val jsonEgress = jsonEgresses.getJSONArray(j)
                    val egressCoordinates = parseCoordinates(jsonEgress)

                    connections.add(Connection(
                            Ingress(ingressCoordinates),
                            Egress(egressCoordinates)
                    ))
                }
            }

            return connections
        }

        @JvmStatic
        private fun parseCoordinates(jsonArray: JSONArray): List<Coordinate> {
            val coordinates = mutableListOf<Coordinate>()

            for (i in 0 until jsonArray.length()) {
                val jsonCoordinate = jsonArray.getJSONObject(i)
                val latitude = jsonCoordinate.getDouble("latitude")
                val longitude = jsonCoordinate.getDouble("longitude")
                coordinates.add(Coordinate(latitude, longitude))
            }

            return coordinates
        }
    }
}