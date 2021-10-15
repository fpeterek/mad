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

    val avgInstance = IrisRecord(
        sepalLength = df.avg(IrisRecord::sepalLength),
        sepalWidth = df.avg(IrisRecord::sepalWidth),
        petalLength = df.avg(IrisRecord::petalLength),
        petalWidth = df.avg(IrisRecord::petalWidth),
        variety = df.median(IrisRecord::variety, String::compareTo),
    )

    val slVariance = df.totalVariance(IrisRecord::sepalLength, avgInstance.sepalLength)
    val swVariance = df.totalVariance(IrisRecord::sepalWidth, avgInstance.sepalWidth)
    val plVariance = df.totalVariance(IrisRecord::petalLength, avgInstance.petalLength)
    val pwVariance = df.totalVariance(IrisRecord::petalWidth, avgInstance.petalWidth)

    println("Average instance: $avgInstance")

    println("Sepal length variance: $slVariance")
    println("Sepal width variance: $swVariance")
    println("Petal length variance: $plVariance")
    println("Petal width variance: $pwVariance")

}
