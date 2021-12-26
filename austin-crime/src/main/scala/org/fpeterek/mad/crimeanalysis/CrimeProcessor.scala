package org.fpeterek.mad.crimeanalysis

import org.apache.spark.sql.functions.{asc, col, desc, udf}
import org.apache.spark.sql.types._
import org.apache.spark.sql.{DataFrame, Row, SparkSession}
import org.fpeterek.mad.crimeanalysis.util.SparkUtil.{RowUtils, kryoEncoder, withCached}
import org.joda.time.Days
import org.joda.time.format.DateTimeFormat

object CrimeProcessor {
  def apply(spark: SparkSession) = new CrimeProcessor(spark)
}

class CrimeProcessor(private val spark: SparkSession) extends Serializable {

  private def dateFormatter = DateTimeFormat.forPattern("d-MMM-yy")

  private def colNames = Seq(
    "primaryKey", "councilDistrict", "highestOffense", "crimeType",
    "reportDate", "location", "xCoordinate", "yCoordinate", "clearanceStatus",
    "clearanceDate", "goDistrict", "goZipCode", "goCensusTract"
  )

  private def DateType = new StructType()
    .add("year", IntegerType, nullable=false)
    .add("month", IntegerType, nullable=false)
    .add("day", IntegerType, nullable=false)

  private def schema = new StructType()
    .add("primaryKey", LongType, nullable=false)
    .add("councilDistrict", IntegerType, nullable=true)
    .add("highestOffense", StringType, nullable=false)
    .add("crimeType", StringType, nullable=false)
    .add("reportDate", DateType, nullable=false)
    .add("location", StringType, nullable=true)
    .add("xCoordinate", DoubleType, nullable=true)
    .add("yCoordinate", DoubleType, nullable=true)
    .add("clearanceStatus", StringType, nullable=true)
    .add("clearanceDate", DateType, nullable=true)
    .add("goDistrict", StringType, nullable=false)
    .add("goZipCode", IntegerType, nullable=true)
    .add("goCensusTract", DoubleType, nullable=true)
    .add("clearanceTime", IntegerType, nullable=true)

  private def getDF(filename: String): DataFrame = {
    val rdd = spark.read.csv(filename)
      .map { row =>
        val reportDate = row.dateOrNull(4, dateFormatter)
        val clearanceDate = row.dateOrNull(9, dateFormatter)

        val clearanceTime = if (reportDate == null || clearanceDate == null) {
          null
        } else {
          Days.daysBetween(reportDate, clearanceDate).getDays
        }

        Row(
          row.getString(0).toLong,
          row.intOrNull(1),
          row.getString(2),
          row.getString(3),
          Row(reportDate.getYear, reportDate.getMonthOfYear, reportDate.getDayOfMonth),
          row.getString(5),
          row.doubleOrNull(6),
          row.doubleOrNull(7),
          row.getString(8),
          clearanceDate match {
            case null => null
            case _ => Row(clearanceDate.getYear, clearanceDate.getMonthOfYear, clearanceDate.getDayOfMonth)
          },
          row.getString(10),
          row.intOrNull(11),
          row.doubleOrNull(12),
          clearanceTime
        )
      }
      .rdd

    spark.createDataFrame(rdd, schema)
  }

  private def mostCommon(df: DataFrame, column: String) = df
    .groupBy(col(column))
    .count()

  private def parseStreet(str: String) = str match {
    case null => null
    case _ => str.dropWhile(char => char.isDigit || char.isSpaceChar)
  }

  private val parseStreetUdf = udf(parseStreet _)
  spark.udf.register("parseStreet", parseStreetUdf)

  implicit class DFUtils(df: DataFrame) {

    def filterByAddress(address: String): DataFrame = df
      .filter(!_.isNullAt(5))
      .filter(_.getString(5) contains address)

    def streetsOnly: DataFrame = df
      .withColumn("location", parseStreetUdf(col("location")))

  }

  private def mostCommonOffense(df: DataFrame) = mostCommon(df, "highestOffense")
  private def mostCommonCrime(df: DataFrame) = mostCommon(df, "crimeType")
  private def mostCommonMonth(df: DataFrame) = mostCommon(df, "reportDate.month")
  private def mostCommonDistrict(df: DataFrame) = mostCommon(df, "councilDistrict")
  private def mostCommonClearanceMonth(df: DataFrame) = mostCommon(df, "clearanceDate.month")
  private def mostCommonStatus(df: DataFrame) = mostCommon(df, "clearanceStatus")

  private def slaughterLaneType(df: DataFrame) =
    mostCommon(df.filterByAddress("SLAUGHTER"), "crimeType")

  private def slaughterLaneOffense(df: DataFrame) =
    mostCommon(df.filterByAddress("SLAUGHTER"), "highestOffense")

  private def streetCrime(df: DataFrame) = df
    .streetsOnly
    .groupBy("location")
    .count()

  private def worstStreets(df: DataFrame) = streetCrime(df)
    .orderBy(desc("count"))
    .limit(10)

  private def bestStreets(df: DataFrame) = streetCrime(df)
    .orderBy(asc("count"))
    .limit(10)

  private def avgClearanceTime(df: DataFrame) = df
    .filter(!_.isNullAt(13))
    .selectExpr("avg(clearanceTime)")
    .take(1).head(0).asInstanceOf[Double]

  private def topClearanceTimes(df: DataFrame) = df
    .filter(!_.isNullAt(13))
    .select(col("crimeType"), col("clearanceTime"))
    .orderBy(desc("clearanceTime"))
    .limit(10)

  private def varianceOfClearanceTime(df: DataFrame) = {
    val avg = avgClearanceTime(df)

    val squares = df
      .filter(!_.isNullAt(13))
      .collect()
      .map(row => row.getInt(13).toDouble - avg)
      .map(diff => diff*diff)

    squares.sum / squares.length
  }

  private def medianClearanceTime(df: DataFrame) = {
    val times = df
      .filter(!_.isNullAt(13))
      .map(row => java.lang.Integer.valueOf(row.getInt(13)))
      .collect()
      .sorted

    times.length % 2 match {
      case 1 => times(1 + times.length / 2).toDouble
      case _ => times(times.length / 2) * times(1 + times.length / 2) / 2.0
    }
  }

  private def clearedCrimes(df: DataFrame) = df
    .filter(row => !row.isNullAt(8) && row.getString(8).nonEmpty && row.getString(8) != "N")

  private def clearanceByCrime(df: DataFrame) = clearedCrimes(df)
    .groupBy("crimeType")
    .mean("clearanceTime")

  private def solvedByCrime(df: DataFrame) = df
    .groupByKey(_.getString(3))
    .mapGroups { (offense, iter) =>
      var count = 0
      var solved = 0
      iter.foreach { row =>
        count += 1
        if (!row.isNullAt(8) && row.getString(8).nonEmpty && row.getString(8) != "N") {
          solved += 1
        }
      }

      Row(offense, count, solved, solved.toDouble / count)
    }

  private def solvedTotal(df: DataFrame) = {
    val total = df.count()
    val solved = clearedCrimes(df).count()

    (total, solved, total.toDouble / solved)
  }


  def process(filename: String): Unit = withCached(getDF(filename)) { df: DataFrame =>

    df.printSchema()
    println(df.take(10).mkString("Array(", ", ", ")"))

    mostCommonOffense(df).write.csv("out/mostCommonOffense/")
    mostCommonCrime(df).write.csv("out/mostCommonCrime/")
    mostCommonMonth(df).write.csv("out/mostCommonMonth/")
    mostCommonDistrict(df).write.csv("out/mostCommonDistrict/")
    mostCommonClearanceMonth(df).write.csv("out/mostCommonClearanceMonth/")
    mostCommonStatus(df).write.csv("out/mostCommonStatus/")
    slaughterLaneType(df).write.csv("out/slaughterLaneType/")
    slaughterLaneOffense(df).write.csv("out/slaughterLaneOffense/")
    worstStreets(df).write.csv("out/worstStreets/")
    bestStreets(df).write.csv("out/bestStreets/")
    topClearanceTimes(df).write.csv("out/topClearanceTimes/")
    clearanceByCrime(df).write.csv("out/clearanceByCrime/")
    solvedByCrime(df).write.csv("out/solvedByCrime/")

    println(s"Average clearance time: ${avgClearanceTime(df)}")
    println(s"Median clearance time: ${medianClearanceTime(df)}")
    println(s"Clearance time variance: ${varianceOfClearanceTime(df)}")
    println(s"Solved total : ${solvedTotal(df)}")
  }

}
