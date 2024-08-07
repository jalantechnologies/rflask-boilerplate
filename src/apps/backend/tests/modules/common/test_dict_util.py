from modules.common.dict_util import DictUtil
from modules.error.custom_errors import MissingKeyError, ValueTypeMismatchError


class TestDictUtil:
    fixture = {"int_value": 44, "str_value": "str"}

    def test_throw_error_on_value_mismatch(self) -> None:
        try:
            DictUtil.required_get_str(input_dict=TestDictUtil.fixture, key="int_value")
            assert False, "Swallow exception on false entity type"
        except ValueTypeMismatchError:
            assert True

    def test_throw_error_on_missing_key(self) -> None:
        try:
            DictUtil.required_get_int(input_dict=TestDictUtil.fixture, key="invalid_key")
            assert False, "Swallow exception on invalid dict key"
        except MissingKeyError:
            assert True

    def test_dict_key_is_loaded(self) -> None:
        val_int = DictUtil.required_get_int(input_dict=TestDictUtil.fixture, key="int_value")
        assert val_int == TestDictUtil.fixture.get("int_value")

        val_str = DictUtil.required_get_str(input_dict=TestDictUtil.fixture, key="str_value")
        assert val_str == TestDictUtil.fixture.get("str_value")
