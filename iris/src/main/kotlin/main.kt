package org.fpeterek.mad.iris

fun main() {

    val df = Dataframe.from("iris.csv") {
        IrisRecord(
            it[0].toDouble(),
            it[1].toDouble(),
            it[2].toDouble(),
            it[3].toDouble(),
            it[4],
        )
    }

    val avgSepalWidth = df.avg(IrisRecord::sepalWidth)
    val swVariance = df.totalVariance(IrisRecord::sepalWidth, avgSepalWidth)

    println("Avg=$avgSepalWidth; variance=$swVariance")

}
