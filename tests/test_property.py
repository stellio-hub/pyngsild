from pyngsild.property import Property


def test_create_name_value_as_str():
    p = Property('name', '3')
    assert p._name == 'name' and isinstance(p._value, str)


def test_create_name_value_as_number():
    p = Property('name', 3)
    assert p._name == 'name' and isinstance(p._value, (int, float))
