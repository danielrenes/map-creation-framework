package parser

import model.Connection
import model.Coordinate
import model.Egress
import model.Ingress
import org.json.JSONArray
import org.json.JSONObject
import java.io.File
import java.io.IOException
import java.util.stream.Collectors

class ExpectedParser {
    companion object {
        @JvmStatic
        fun parse(path: String): List<Connection> {
            val content = FileUtils.readFile(path)

            val connections = mutableListOf<Connection>()

            val json = JSONObject(content)
            val jsonArray = json.getJSONArray("expected")

            for (i in 0 until jsonArray.length()) {
                val jsonConnection = jsonArray.getJSONObject(i)
                val jsonIngress = jsonConnection.getJSONArray("ingress")
                val jsonEgress = jsonConnection.getJSONArray("egress")

                val ingressCoordinates = parseCoordinates(jsonIngress)
                val egressCoordinates = parseCoordinates(jsonEgress)

                connections.add(Connection(
                        Ingress(ingressCoordinates),
                        Egress(egressCoordinates)
                ))
            }

            return connections
        }

        @JvmStatic
        fun parseCoordinates(jsonArray: JSONArray): List<Coordinate> {
            val coordinates = mutableListOf<Coordinate>()

            for (i in 0 until jsonArray.length()) {
                val jsonCoordinate = jsonArray.getJSONArray(i)
                val latitude = jsonCoordinate.getDouble(0)
                val longitude = jsonCoordinate.getDouble(1)
                coordinates.add(Coordinate(latitude, longitude))
            }

            return coordinates
        }
    }
}