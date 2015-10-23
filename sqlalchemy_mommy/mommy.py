import random
import string
from sqlalchemy import Integer, String, SmallInteger, BigInteger, Boolean


BaseModel = None


def make(session, model_, **kwargs):
    record = model_(**kwargs)

    for column in _non_nullable_columns(model_):
        if column.foreign_keys:
            for foreign_key in column.foreign_keys:
                fk_value = make(session, _get_class_by_tablename(foreign_key.column.table.name))
                setattr(record, foreign_key.parent.name, getattr(fk_value, foreign_key.column.name))
        else:
            setattr(record, column.name, generate_value(column.type))

    session.add(record)
    session.flush()
    return record


def generate_value(type_):
    value_generator = TYPE_VALUE_GENERATOR_MAPPER.get(type_.__class__)

    if value_generator:
        return value_generator(type_)


def _generate_int(type_=None, max=2147483647):
    return random.randint(0, max)


def _generate_smallint(type_=None):
    return _generate_int(type_, 1)


def _generate_bigint(type_=None):
    return _generate_int(type_, 9223372036854775807)


def _generate_str(type_=None):
    length = type_.length if type_.length else 50
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))


def _generate_bool(type_=None):
    return random.choice((True, False))


TYPE_VALUE_GENERATOR_MAPPER = {
    SmallInteger: _generate_smallint,
    Integer: _generate_int,
    BigInteger: _generate_bigint,
    String: _generate_str,
    Boolean: _generate_bool,
}


def _non_nullable_columns(model_):
    return {column[1] for column in model_.__table__.columns.items()
            if not column[1].nullable and not column[1].primary_key}


def _get_class_by_tablename(tablename):
  if not BaseModel:
      raise Exception('BaseModel must be defined')

  for c in BaseModel._decl_class_registry.values():
    if hasattr(c, '__tablename__') and c.__tablename__ == tablename:
      return c