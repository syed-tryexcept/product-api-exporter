from exporter import find_items, get_name


def test_find_items_nested_response():
    assert find_items({"data": {"items": [{"id": 1}]}}) == [{"id": 1}]


def test_find_items_unknown_shape():
    assert find_items({"foo": "bar"}) == []


def test_get_name_strips_spaces():
    assert get_name({"name": "  Wireless Mouse  "}) == "Wireless Mouse"


def test_get_name_missing():
    assert get_name({}) == ""