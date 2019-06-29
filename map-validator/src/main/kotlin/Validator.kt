import model.Connection
import org.json.JSONArray
import parser.ExpectedParser
import parser.ResultParser
import java.io.File
import java.nio.file.Paths

class ComparisonResult(
        val numberOfConnections: Int,
        val numberOfMatches: Int,
        val numberOfDuplicates: Int
) {
    override fun toString(): String {
        return "Connections: $numberOfConnections\n" +
                "Matches: $numberOfMatches\n" +
                "Duplicates: $numberOfDuplicates"
    }
}

fun main(args: Array<String>) {
    if (args.size != 2) {
        println("Two arguments needed: <result path> <expected path>")
        return
    }

    val (result, expected) = parse(args[0], args[1])

    println(result)

    for (conn in result) {
        println(conn.ingress.coordinates.size)
        println(conn.egress.coordinates.size)
    }

    println(expected)

    for (conn in expected) {
        println(conn.ingress.coordinates.size)
        println(conn.egress.coordinates.size)
    }

    val comparisonResult = compare(result, expected)

    println(comparisonResult)

    createOutDir()
    saveConnections("result", result)
    saveConnections("expected", expected)
}

private fun parse(resultPath: String, expectedPath: String): Pair<List<Connection>, List<Connection>> {
    val result = ResultParser.parse(resultPath)
    val expected = ExpectedParser.parse(expectedPath)
    return Pair(result, expected)
}

private fun compare(result: List<Connection>, expected: List<Connection>): ComparisonResult {
    val matched = hashMapOf<Connection, Connection>()

    for (conn1 in result) {
        for (conn2 in expected) {
            if (conn2.compareTo(conn1)) {
                matched[conn1] = conn2
                break
            }
        }
    }

    val nConnections = expected.size
    val nMatches = expected.intersect(matched.values).size
    val nDuplicates = matched.entries.size - nMatches

    return ComparisonResult(nConnections, nMatches, nDuplicates)
}

private fun connectionsToJson(connections: List<Connection>): JSONArray {
    val jsonArray = JSONArray()
    for (connection in connections) {
        jsonArray.put(connection.toJson())
    }
    return jsonArray
}

private fun createOutDir() {
    val dir = File("out")

    if (!dir.exists()) {
        dir.mkdir()
    } else {
        dir.listFiles().forEach { it.deleteRecursively() }
    }
}

private fun saveConnections(filename: String, connections: List<Connection>) {
    val dir = File("out")
    val filenameWithExtension = if (filename.endsWith(".json")) filename else "$filename.json"
    val file = Paths.get(dir.path, filenameWithExtension).toFile()
    val jsonArray = connectionsToJson(connections)

    file.writeText(jsonArray.toString(2))
}