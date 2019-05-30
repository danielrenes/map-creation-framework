package model

class Ingress(coordinates: List<Coordinate>) : Path(coordinates) {
//    override fun adjust(length: Double, segments: Int): List<Coordinate> {
//        return adjust(length, segments, coordinates.asReversed()).asReversed()
//    }

    override fun adjust(distances: List<Double>): List<Coordinate> {
        return (adjust(distances.asReversed(), coordinates.asReversed())).asReversed()
    }
}