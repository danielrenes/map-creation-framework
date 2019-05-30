package model

interface Comparable<T> {
    fun compareTo(other: T): Boolean
}