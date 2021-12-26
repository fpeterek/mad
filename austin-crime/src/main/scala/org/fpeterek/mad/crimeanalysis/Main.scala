package org.fpeterek.mad.crimeanalysis

import org.apache.spark.SparkConf
import org.apache.spark.sql.SparkSession
import org.fpeterek.mad.crimeanalysis.util.SparkUtil.CloseableSpark

object Main {


  private def setupSpark: SparkSession = {
    val conf = new SparkConf()
      .setAppName("AustinCrimeAnalysis")
      .setMaster("local[2]")
      .set("spark.executor.memory", "4g")
      .set("spark.executor.memoryOverhead", "1g")
      .set("spark.executor.cores", "1")
      .set("spark.executor.instances", "1")
      .set("spark.default.parallelism", "1")
      .set("spark.sql.shuffle.partitions", "1")

    val spark = SparkSession.builder.config(conf).getOrCreate

    spark.sparkContext.setLogLevel("ERROR")

    spark
  }


  private def withSpark(fn: SparkSession => Unit): Unit = setupSpark.use(fn)

  private def run(): Unit = withSpark { spark =>
    CrimeProcessor(spark).process("in/2018_Annual_Crime.csv")
  }

  def main(args: Array[String]): Unit = run()

}
