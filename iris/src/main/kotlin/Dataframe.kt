package org.fpeterek.mad.iris

import kotlin.math.exp
import kotlin.math.pow
import kotlin.math.sqrt

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

    fun min(of: T.() -> Double) = iterator(of).asSequence().minByOrNull { it } ?:
        throw RuntimeException("Empty dataframe")

    fun max(of: T.() -> Double) = iterator(of).asSequence().maxByOrNull { it } ?:
        throw RuntimeException("Empty dataframe")

    private fun pdf(value: Double, avg: Double, variance: Double) =
        (sqrt(2*Math.PI*variance)).pow(-1) * exp(-0.5 * (value-avg).pow(2) / variance)

    fun distribution(of: T.() -> Double, samples: Int = 100) =
        (min(of) to max(of)).let { (minVal, maxVal) ->
            val diff = maxVal - minVal
            val avgVal = avg(of)
            val variance = totalVariance(of, withAvg = avgVal)
            (0..samples).associate {
                val value = minVal + (it.toDouble() / samples) * diff
                value to pdf(value, avgVal, variance)
            }
        }

    fun cumulativeDistribution(of: T.() -> Double, samples: Int = 100) =
        distribution(of, samples).let {  dist ->
            val keys = dist.keys.sorted()
            val values = mutableMapOf(
                keys.first() to dist[keys.first()]!!
            )
            keys.indices.drop(1).forEach {
                values[keys[it]] = (values[keys[it-1]]!! + dist[keys[it]]!!)
            }

            val max = values[keys.last()]!!

            values.mapValues { (_, it) -> it / max }
        }

    private fun varianceOf(item: T, of: T.() -> Double, avg: Double) =
        (item.of() - avg).pow(2)

    fun variance(item: Int, of: T.() -> Double, withAvg: Double?) =
        varianceOf(data[item], of, (withAvg ?: avg(of)))

    fun totalVariance(of: T.() -> Double, withAvg: Double? = null) =
        (withAvg ?: avg(of)).let { average ->
            data
                .asSequence()
                .map { varianceOf(it, of, average) }
                .let {
                    it.sum() / data.size
                }
        }

}
