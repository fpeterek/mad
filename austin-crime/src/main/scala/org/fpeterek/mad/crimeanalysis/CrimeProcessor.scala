package org.fpeterek.mad.crimeanalysis

import org.apache.spark.sql.functions.col
import org.apache.spark.sql.types.{DoubleType, IntegerType, LongType, StringType, StructType}
import org.apache.spark.sql.{DataFrame, Row, SparkSession}
import org.fpeterek.mad.crimeanalysis.util.SparkUtil.{RowUtils, kryoEncoder, withCached}
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

  private def getDF(filename: String): DataFrame = {
    val rdd = spark.read.csv(filename)
      .map { row =>
        val reportDate = row.dateOrNull(4, dateFormatter)
        val clearanceDate = row.dateOrNull(9, dateFormatter)

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
          row.doubleOrNull(12)
        )
      }
      .rdd

    spark.createDataFrame(rdd, schema)
  }

  private def mostCommon(df: DataFrame, column: String) = df
    .groupBy(col(column))
    .count()
    .collect()

  private def mostCommonOffense(df: DataFrame) = mostCommon(df, "highestOffense")
  private def mostCommonCrime(df: DataFrame) = mostCommon(df, "crimeType")
  private def mostCommonMonth(df: DataFrame) = mostCommon(df, "reportDate.month")
  private def mostCommonDistrict(df: DataFrame) = mostCommon(df, "councilDistrict")
  private def mostCommonClearanceMonth(df: DataFrame) = mostCommon(df, "clearanceDate.month")
  private def mostCommonStatus(df: DataFrame) = mostCommon(df, "clearanceStatus")

  def process(filename: String): Unit = withCached(getDF(filename)) { df: DataFrame =>

    df.printSchema()
    println(df.take(10).mkString("Array(", ", ", ")"))

    println(mostCommonOffense(df).mkString("Array(", ", ", ")"))
    println(mostCommonCrime(df).mkString("Array(", ", ", ")"))
    println(mostCommonMonth(df).mkString("Array(", ", ", ")"))
    println(mostCommonDistrict(df).mkString("Array(", ", ", ")"))
    println(mostCommonClearanceMonth(df).mkString("Array(", ", ", ")"))
    println(mostCommonStatus(df).mkString("Array(", ", ", ")"))
  }

}
