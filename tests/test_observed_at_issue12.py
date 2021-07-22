from pyngsild.proprel import Property, is_dt_aware
from pyngsild.proprel import as_isoformat
from datetime import datetime, timezone
import pytest
from . conftests import ConfTests


conf = ConfTests()


# TEST for is_dt_aware()

# NAIVE datetime object
# is_dt_aware() shall return False
def test_is_aware_false():
    dt = datetime.now()
    assert is_dt_aware(dt) is False


# AWARE datetime object
# is_dt_aware() shall return True
def test_is_aware_true():
    dt = datetime.now(timezone.utc)
    assert is_dt_aware(dt) is True


# TESTS for as_isoformat()

# NAIVE datetime object
# ### This works only on system with 'Europe/Paris' timezone ! ###
def test_as_isoformat_naive():
    dt = conf.NAIVE_DATETIME
    assert as_isoformat(dt) == conf.NAIVE_DATETIME_STR


# AWARE datetime object
def test_as_isoformat_aware():
    dt = conf.AWARE_DATETIME
    assert as_isoformat(dt) == conf.AWARE_DATETIME_STR


# TESTS for Property class

# Create property with observed_at as datetime object
def test_create_property_datetime_object():
    p = Property(conf.P_NAME, conf.P_VALUE, conf.NAIVE_DATETIME)
    assert p.name == conf.P_NAME and p.value == conf.P_VALUE \
        and p.observed_at == conf.NAIVE_DATETIME_STR


# Create property with observed_at as str object
def test_create_property_datetime_str():
    p = Property(conf.P_NAME, conf.P_VALUE, conf.NAIVE_DATETIME_STR)
    assert p.name == conf.P_NAME and p.value == conf.P_VALUE \
        and p.observed_at == conf.NAIVE_DATETIME_STR


# Create property with observed_at being of other types than str and datetime
def test_create_property_datetime_incorrect_type():
    with pytest.raises(ValueError):
        Property(conf.P_NAME, conf.P_VALUE, 1234)
