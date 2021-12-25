package org.fpeterek.mad.crimeanalysis

import org.apache.spark.sql.types.{BinaryType, DoubleType, IntegerType, LongType, StringType, StructType}
import org.apache.spark.sql.{DataFrame, Row, SparkSession}
import org.fpeterek.mad.crimeanalysis.util.SparkUtil.kryoEncoder
import org.joda.time.LocalDate
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
    .add("councilDistrict", IntegerType, nullable=false)
    .add("highestOffense", StringType, nullable=false)
    .add("crimeType", StringType, nullable=false)
    .add("reportDate", DateType, nullable=false)
    .add("location", StringType, nullable=false)
    .add("xCoordinate", DoubleType, nullable=false)
    .add("yCoordinate", DoubleType, nullable=false)
    .add("clearanceStatus", StringType, nullable=false)
    .add("clearanceDate", DateType, nullable=false)
    .add("goDistrict", StringType, nullable=false)
    .add("goZipCode", IntegerType, nullable=false)
    .add("goCensusTract", DoubleType, nullable=false)

  private def getDF(filename: String): DataFrame = {
    val rdd = spark.read.csv(filename)
      .map { row =>
        val reportDate = LocalDate.parse(row.getString(4), dateFormatter)
        val clearanceDate = LocalDate.parse(row.getString(9), dateFormatter)

        Row(
          row.getString(0).toLong,
          row.getString(1).toInt,
          row.getString(2),
          row.getString(3),
          Row(reportDate.getYear, reportDate.getMonthOfYear, reportDate.getDayOfMonth),
          row.getString(5),
          row.getString(6).toDouble,
          row.getString(7).toDouble,
          row.getString(8),
          Row(clearanceDate.getYear, clearanceDate.getMonthOfYear, clearanceDate.getDayOfMonth),
          row.getString(10),
          row.getString(11).toInt,
          row.getString(12).toDouble
        )
      }
      .rdd

    spark.createDataFrame(rdd, schema)
  }

  def process(filename: String): Unit = {
    val df = getDF(filename)

    df.printSchema()
    println(df.take(10).mkString("Array(", ", ", ")"))
  }

}
