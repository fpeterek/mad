package org.fpeterek.mad.iris

import kotlin.math.pow

class Dataframe<T> private constructor(val data: List<T>) {

    companion object {
        fun <T> of(data: List<T>) = Dataframe(data)

        fun <T> from(file: String, parser: (List<String>) -> T) =
            Loader.loadFile(file, parser).let {
                of(it)
            }
    }

    operator fun iterator() = data.iterator()
    fun <T2> iterator(of: T.() -> T2) = data.stream().map(of).iterator()

    fun avg(of: T.() -> Double) = data.sumOf(of) / data.size

    fun avgString(of: T.() -> String) {
        val counts = mutableMapOf<String, Long>()
        iterator(of).forEach {
            counts[it] = counts.getOrDefault(it, 0) + 1
        }
    }


    private fun varianceOf(item: T, of: T.() -> Double, avg: Double) =
        (item.of() - avg).pow(2)

    fun variance(item: Int, of: T.() -> Double, withAvg: Double?) =
        varianceOf(data[item], of, (withAvg ?: avg(of)))

    fun totalVariance(of: T.() -> Double, withAvg: Double? = null) =
        (withAvg ?: avg(of)).let { average ->
            data
                .map { varianceOf(it, of, average) }
                .let {
                    it.sum() / it.size
                }
        }

}
