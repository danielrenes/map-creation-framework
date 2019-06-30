package model

import org.junit.Test

import org.junit.Assert.*

class PathTest {

    @Test
    fun testLength() {
        val coordinates = listOf(
                Coordinate(47.45636, 19.04640),
                Coordinate(47.45609, 19.04631),
                Coordinate(47.45557, 19.04611)
        )

        val path = Ingress(coordinates)

        assertEquals(path.length(), 0.089, 0.002)
    }

    @Test
    fun testAdjust() {
        val coordinates = listOf(
                Coordinate(47.45636, 19.04640),
                Coordinate(47.45609, 19.04631),
                Coordinate(47.45557, 19.04611)
        )

        val path = Ingress(coordinates)

        val distances = listOf(12.0, 24.0, 6.0, 38.0, 9.0, 14.0)

        val adjusted = path.adjust(distances)

        assertTrue(adjusted[adjusted.size - 1].compareTo(coordinates[coordinates.size - 1]))

        for (i in 0 until adjusted.size - 1) {
            assertEquals(adjusted[i].distance(adjusted[i + 1]), distances[i], 0.0001)
        }
    }

    @Test
    fun testCompareTo() {
        val coordinates1 = listOf(
                Coordinate(47.45636, 19.04640),
                Coordinate(47.45609, 19.04631),
                Coordinate(47.45557, 19.04611)
        )

        val path1 = Ingress(coordinates1)

        val coordinates2 = listOf(
                Coordinate(47.45621, 19.04637),
                Coordinate(47.45595, 19.04630),
                Coordinate(47.45556, 19.04617)
        )

        val path2 = Ingress(coordinates2)

        val coordinates3 = listOf(
                Coordinate(47.45621, 19.04636),
                Coordinate(47.45572, 19.04622),
                Coordinate(47.45528, 19.04608)
        )

        val path3 = Ingress(coordinates3)

        assertTrue(path1.compareTo(path2))

        assertFalse(path1.compareTo(path3))
    }
}