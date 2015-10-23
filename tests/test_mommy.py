from unittest import TestCase
from sqlalchemy import Integer, String, SmallInteger, BigInteger, Boolean
from sqlalchemy_mommy import mommy
from . import BaseTest
from .dummy_models import Session, Spam, Ham, BaseModel


mommy.BaseModel = BaseModel


class MakeTest(BaseTest):
    def setUp(self):
        self.s = Session()

    def test_create_record_with_default_values_for_non_nullable_columns(self):
        mommy.make(self.s, Spam)

        spam = self.s.query(Spam.id, Spam.purpose, Spam.flavor).first()
        self.assertEqual(spam.id, 1)
        self.assertEqual(spam.purpose, None)
        self.assertIsInstance(spam.flavor, int)

    def test_create_record_with_specified_values(self):
        mommy.make(self.s, Spam, id=9, purpose='Nothing')
        self.assertEqual(self.s.query(Spam.id, Spam.purpose).all(), [(9, 'Nothing')])

    def test_create_non_nullable_relationships(self):
        mommy.make(self.s, Ham)

        self.assertEqual(self.s.query(Ham.id, Ham.spam_id).all(), [(1, 1)])
        self.assertEqual(self.s.query(Spam.id).all(), [(1,)])


class IntegerValueGeneratorTest(TestCase):
    def test_generate_random_value_for_smallint(self):
        for i in range(100):
            self.assertIn(mommy.generate_value(SmallInteger()), [0, 1])

    def test_generate_random_value_for_integer(self):
        for i in range(100):
            value = mommy.generate_value(Integer())
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 2147483647)

    def test_generate_random_value_for_bigint(self):
        for i in range(100):
            value = mommy.generate_value(BigInteger())
            self.assertGreaterEqual(value, 0)
            self.assertLessEqual(value, 9223372036854775807)


class StringValueGeneratorTest(TestCase):
    def test_generate_random_value_for_string(self):
        self.assertIsInstance(mommy.generate_value(String()), str)

    def test_generate_random_value_for_string_with_max_chars(self):
        self.assertEquals(5, len(mommy.generate_value(String(5))))


class BooleanValueGeneratorTest(TestCase):
    def test_generate_random_value_for_boolean(self):
        generated_values = {mommy.generate_value(Boolean()) for val in range(100)}
        self.assertEquals(generated_values, {True, False})
