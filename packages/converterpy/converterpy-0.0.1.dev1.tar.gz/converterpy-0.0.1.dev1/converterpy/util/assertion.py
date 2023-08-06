
def assert_list_is_instance(iterable, expected_type):
    for i in iterable:
        assert isinstance(i, expected_type)