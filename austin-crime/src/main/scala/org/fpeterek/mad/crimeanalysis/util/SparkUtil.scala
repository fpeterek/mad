package org.fpeterek.mad.crimeanalysis.util

import org.apache.spark.sql.{DataFrame, Dataset, Encoder, Row, SparkSession}
import org.apache.spark.storage.StorageLevel
import org.joda.time.LocalDate
import org.joda.time.format.DateTimeFormatter

object SparkUtil {

  /* Generic implicit which creates a kryo encoder for functions */
  /* which require encoder implicits (eg. map)                   */
  import scala.reflect.ClassTag
  implicit def kryoEncoder[A](implicit ct: ClassTag[A]): Encoder[A] =
    org.apache.spark.sql.Encoders.kryo[A](ct)

  implicit class RowUtils(row: Row) {
    def doubleOrNull(idx: Int): java.lang.Double = row.isNullAt(idx) match {
      case true => null
      case false => row.getString(idx).toDouble
    }

    def intOrNull(idx: Int): java.lang.Integer = row.isNullAt(idx) match {
      case true => null
      case false => row.getString(idx).toInt
    }

    def dateOrNull(idx: Int, formatter: DateTimeFormatter): LocalDate = row.isNullAt(idx) match {
      case true => null
      case false => LocalDate.parse(row.getString(idx), formatter)
    }
  }

  def withCached[DT, RT](ds: Dataset[DT], level: StorageLevel): (Dataset[DT] => RT) => RT =  {

    def cachedFun(fn: Dataset[DT] => RT): RT = {
      val cached = ds.persist(level)
      val res = fn(cached)
      cached.unpersist()
      res
    }

    cachedFun
  }

  def withCached[DT, RT](ds: Dataset[DT]): (Dataset[DT] => RT) => RT = withCached(ds, StorageLevel.MEMORY_AND_DISK)

  implicit class CloseableSpark(ss: SparkSession) {
    def use[T](fn: SparkSession => T): T = try {
      fn(ss)
    } finally {
      ss.close()
    }
  }
}
