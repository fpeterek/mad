package org.fpeterek.mad.iris

import jetbrains.letsPlot.letsPlot
import jetbrains.datalore.plot.PlotSvgExport
import jetbrains.letsPlot.geom.geomLine
import jetbrains.letsPlot.intern.toSpec
import java.awt.Desktop
import java.io.File


fun plotFunction(
    df: Dataframe<IrisRecord>,
    fn: Dataframe<IrisRecord>.(IrisRecord.() -> Double) -> Map<Double, Double>,
    of: IrisRecord.() -> Double,
    outFile: String) {

    val slDist = df.fn(of).toList()
    val slPlotValues = mapOf(
        "range" to slDist.map { it.first },
        "probability" to slDist.map { it.second },
    )

    val plot = letsPlot(slPlotValues) {
        x = "range"
        y = "probability"
    } + geomLine(color = "black", alpha=0.8, size=1.0)

    val content = PlotSvgExport.buildSvgImageFromRawSpecs(plot.toSpec())
    val file = File(outFile)
    file.createNewFile()
    file.writeText(content)
    Desktop.getDesktop().browse(file.toURI())

}


fun plotDist(df: Dataframe<IrisRecord>, of: IrisRecord.() -> Double, outFile: String) = plotFunction(
    df,
    Dataframe<IrisRecord>::distribution,
    of,
    outFile,
)

fun plotActualDist(df: Dataframe<IrisRecord>, of: IrisRecord.() -> Double, outFile: String) = plotFunction(
    df,
    Dataframe<IrisRecord>::actualDistribution,
    of,
    outFile,
)

fun plotCumulative(df: Dataframe<IrisRecord>, of: IrisRecord.() -> Double, outFile: String) = plotFunction(
    df,
    Dataframe<IrisRecord>::cumulativeDistribution,
    of,
    outFile,
)

fun plotActualCumulative(df: Dataframe<IrisRecord>, of: IrisRecord.() -> Double, outFile: String) = plotFunction(
    df,
    Dataframe<IrisRecord>::actualCumulativeDistribution,
    of,
    outFile,
)

fun loadIrisDf(filename: String) = Dataframe.from(filename) {
    IrisRecord(
        it[0].toDouble(),
        it[1].toDouble(),
        it[2].toDouble(),
        it[3].toDouble(),
        it[4],
    )
}

fun plotDistributions(df: Dataframe<IrisRecord>) {
    plotDist(df, IrisRecord::sepalLength, "slDistribution.svg")
    plotDist(df, IrisRecord::sepalWidth, "swDistribution.svg")
    plotDist(df, IrisRecord::petalLength, "plDistribution.svg")
    plotDist(df, IrisRecord::petalWidth, "pwDistribution.svg")
}

fun plotCumulativeDistributions(df: Dataframe<IrisRecord>) {
    plotCumulative(df, IrisRecord::sepalLength, "slCumulative.svg")
    plotCumulative(df, IrisRecord::sepalWidth, "swCumulative.svg")
    plotCumulative(df, IrisRecord::petalLength, "plCumulative.svg")
    plotCumulative(df, IrisRecord::petalWidth, "pwCumulative.svg")
}

fun plotActualDistributions(df: Dataframe<IrisRecord>) {
    plotActualDist(df, IrisRecord::sepalLength, "slActualDistribution.svg")
    plotActualDist(df, IrisRecord::sepalWidth, "swActualDistribution.svg")
    plotActualDist(df, IrisRecord::petalLength, "plActualDistribution.svg")
    plotActualDist(df, IrisRecord::petalWidth, "pwActualDistribution.svg")
}

fun plotActualCumulativeDistributions(df: Dataframe<IrisRecord>) {
    plotActualCumulative(df, IrisRecord::sepalLength, "slActualCumulative.svg")
    plotActualCumulative(df, IrisRecord::sepalWidth, "swActualCumulative.svg")
    plotActualCumulative(df, IrisRecord::petalLength, "plActualCumulative.svg")
    plotActualCumulative(df, IrisRecord::petalWidth, "pwActualCumulative.svg")
}

fun main() {

    val df = loadIrisDf("iris.csv")

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

    plotDistributions(df)
    plotActualDistributions(df)
    plotCumulativeDistributions(df)
    plotActualCumulativeDistributions(df)

}
