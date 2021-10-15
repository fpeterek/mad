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

    fun <T2> median(of: T.() -> T2, cmp: Comparator<T2>): T2 {
        val counts = mutableMapOf<T2, Long>()
        iterator(of).forEach {
            counts[it] = counts.getOrDefault(it, 0L) + 1L
        }
        val keys = counts.keys.toList().sortedWith(cmp)
        val size = data.size
        var current = 0L
        var i = 0
        while (current < size/2) {
            current += counts[keys[i]!!]!!
            i += 1
        }

        return keys[i]
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
