package org.fpeterek.mad.crimeanalysis.util

import org.apache.spark.sql.{Dataset, Encoder, SparkSession}
import org.apache.spark.storage.StorageLevel

object SparkUtil {

  /* Generic implicit which creates a kryo encoder for functions */
  /* which require encoder implicits (eg. map)                   */
  import scala.reflect.ClassTag
  implicit def kryoEncoder[A](implicit ct: ClassTag[A]): Encoder[A] =
    org.apache.spark.sql.Encoders.kryo[A](ct)

  def withCached[T](ds: Dataset[T], level: StorageLevel): (Dataset[T] => Unit) => Unit =  {

    def cachedFun(fn: Dataset[T] => Unit): Unit = {
      val cached = ds.persist(level)
      fn(cached)
      cached.unpersist()
    }

    cachedFun
  }

  def withCached[T](ds: Dataset[T]): (Dataset[T] => Unit) => Unit = withCached(ds, StorageLevel.MEMORY_AND_DISK)

  implicit class CloseableSpark(ss: SparkSession) {
    def use[T](fn: SparkSession => T): T = try {
      fn(ss)
    } finally {
      ss.close()
    }
  }
}
