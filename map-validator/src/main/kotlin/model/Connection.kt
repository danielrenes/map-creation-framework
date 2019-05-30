package model

import org.json.JSONObject

class Connection(val ingress: Ingress, val egress: Egress) : Comparable<Connection> {
    override fun compareTo(other: Connection): Boolean {
        return ingress.compareTo(other.ingress)
                && egress.compareTo(other.egress)
    }

    fun toJson(): JSONObject {
        val jsonObject = JSONObject()
        jsonObject.put("ingress", ingress.toJson())
        jsonObject.put("egress", egress.toJson())
        return jsonObject
    }
}