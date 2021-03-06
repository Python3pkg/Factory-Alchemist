from unittest import TestCase
from datetime import date, datetime
from sqlalchemy import Integer, String, SmallInteger, BigInteger, Boolean, Date, DateTime, Enum, Float
from factory_alchemist import factory
from . import BaseTest
from .dummy_models import Session, Spam, Ham, BaseModel, FishTable


factory.BaseModel = BaseModel


class MakeTest(BaseTest):
    def setUp(self):
        self.s = Session()

    def test_create_record_with_default_values_for_non_nullable_columns(self):
        factory.make(self.s, Spam)

        spam = self.s.query(Spam.id, Spam.purpose, Spam.flavor).first()
        self.assertEqual(spam.id, 1)
        self.assertEqual(spam.purpose, None)
        self.assertIsInstance(spam.flavor, int)

    def test_create_record_with_specified_values(self):
        factory.make(self.s, Spam, id=9, purpose='Nothing')
        self.assertEqual(self.s.query(Spam.id, Spam.purpose).all(), [(9, 'Nothing')])

    def test_create_non_nullable_relationships(self):
        factory.make(self.s, Ham)

        self.assertEqual(self.s.query(Ham.id, Ham.spam_id).all(), [(1, 1)])
        self.assertEqual(self.s.query(Spam.id).all(), [(1,)])


class MakeFromTableTest(BaseTest):
    def test_create_from_table_object(self):
        fish_1 = factory.make_t(FishTable, id=5)
        fish_2 = factory.make_t(FishTable, id=11)

        self.assertItemsEqual(list(FishTable.select().execute()), [(5, 1), (11, 2)])

        self.assertEqual(fish_1.id, 5)
        self.assertEqual(fish_1.spam_id, 1)
        self.assertEqual(fish_2.id, 11)
        self.assertEqual(fish_2.spam_id, 2)


class IntegerValueGeneratorTest(TestCase):
    def test_generate_random_value_for_smallint(self):
        for i in range(100):
            self.assertIn(factory.generate_value(SmallInteger()), [0, 1])

    def test_generate_random_value_for_integer(self):
        for i in range(100):
            value = factory.generate_value(Integer())
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 2147483647)

    def test_generate_random_value_for_bigint(self):
        for i in range(100):
            value = factory.generate_value(BigInteger())
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 9223372036854775807)


class FloatValueGeneratorTest(TestCase):
    def test_generate_random_float(self):
        value = factory.generate_value(Float())
        self.assertIsInstance(value, float)

    def test_generate_random_float_between_in_interval(self):
        for _ in range(100):
            value = factory.generate_value(Float())

            self.assertGreaterEqual(value, 0.0)
            self.assertLessEqual(value, 99999.0)


class StringValueGeneratorTest(TestCase):
    def test_generate_random_value_for_string(self):
        self.assertIsInstance(factory.generate_value(String()), str)

    def test_generate_random_value_for_string_with_max_chars(self):
        self.assertEquals(5, len(factory.generate_value(String(5))))


class BooleanValueGeneratorTest(TestCase):
    def test_generate_random_value_for_boolean(self):
        generated_values = {factory.generate_value(Boolean()) for val in range(100)}
        self.assertEquals(generated_values, {True, False})


class DateValueGeneratorTest(TestCase):
    def test_generate_random_value_between_dates(self):
        for i in range(100):
            value = factory.generate_value(Date())
            self.assertTrue(value > date(1950, 1, 1))
            self.assertTrue(value < date(2050, 12, 31))

    def test_generate_date_type(self):
        self.assertIsInstance(factory.generate_value(Date()), date)


class DateTimeValueGeneratorTest(TestCase):
    def test_generate_random_value_between_datetimes(self):
        for i in range(100):
            value = factory.generate_value(DateTime())
            self.assertTrue(value > datetime(1950, 1, 1, 0, 0, 0))
            self.assertTrue(value < datetime(2050, 12, 31, 23, 59, 59))

    def test_generate_datetime_type(self):
        self.assertIsInstance(factory.generate_value(DateTime()), datetime)


class EnumValueGeneratorTest(TestCase):
    def test_generate_list_of_strings(self):
        for _ in range(100):
            value = factory.generate_value(Enum('ham', 'spam'))
            self.assertIn(value, ['ham', 'spam'])
