import sys
import unittest
import logging

from pyspark.sql import SparkSession


class ReusedPySparkTestCase(unittest.TestCase):
    """A base class to reuse a SparkSession across test cases.

    Initilizing a SparkSession takes time. All subclasses of this
    class will use the same SparkSession for testing.

    References:
        [1] https://github.com/apache/spark/blob/master/python/pyspark/testing/utils.py#L117
    """

    @classmethod
    def setUpClass(cls):
        logging.getLogger("py4j").setLevel(logging.ERROR)
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
        cls.spark = (
            SparkSession.builder
            .master('local')
            .appName(cls.__name__)
            .getOrCreate()
        )

    @classmethod
    def tearDownClass(cls):
        cls.spark.stop()
