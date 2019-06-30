package model

class Ingress(coordinates: List<Coordinate>) : Path(coordinates) {
    override fun adjust(distances: List<Double>): List<Coordinate> {
        return (adjust(distances.asReversed(), coordinates.asReversed())).asReversed()
    }
}