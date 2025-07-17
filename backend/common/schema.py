#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field, validate_email

from backend.core.conf import settings

# Custom validation error messages, references:
# https://github.com/pydantic/pydantic-core/blob/a5cb7382643415b716b1a7a5392914e50f726528/tests/test_errors.py#L266
# https://github.com/pydantic/pydantic/blob/caa78016433ec9b16a973f92f187a7b6bfde6cb5/docs/errors/errors.md?plain=1#L232
CUSTOM_VALIDATION_ERROR_MESSAGES = {
    'no_such_attribute': "Object has no attribute '{attribute}'",
    'json_invalid': 'Invalid JSON: {error}',
    'json_type': 'JSON input should be string, bytes, or bytearray',
    'recursion_loop': 'Recursion error - cycle detected',
    'model_type': 'Input should be a valid dict or instance of {class_name}',
    'model_attributes_type': 'Input should be a valid dict or object with extractable fields',
    'dataclass_exact_type': 'Input should be an instance of {class_name}',
    'dataclass_type': 'Input should be a dict or instance of {class_name}',
    'missing': 'Field is required',
    'frozen_field': 'Field is frozen',
    'frozen_instance': 'Instance is frozen',
    'extra_forbidden': 'Extra input is not allowed',
    'invalid_key': 'Key should be a string',
    'get_attribute_error': 'Error extracting attribute: {error}',
    'none_required': 'Input should be None',
    'enum': 'Input should be {expected}',
    'greater_than': 'Input should be greater than {gt}',
    'greater_than_equal': 'Input should be greater than or equal to {ge}',
    'less_than': 'Input should be less than {lt}',
    'less_than_equal': 'Input should be less than or equal to {le}',
    'finite_number': 'Input should be a finite number',
    'too_short': '{field_type} should have at least {min_length} items after validation, not {actual_length}',
    'too_long': '{field_type} should have at most {max_length} items after validation, not {actual_length}',
    'string_type': 'Input should be a valid string',
    'string_sub_type': 'Input should be a string, not an instance of a str subclass',
    'string_unicode': 'Input should be a valid string, cannot parse raw data as Unicode string',
    'string_pattern_mismatch': "String should match pattern '{pattern}'",
    'string_too_short': 'String should have at least {min_length} characters',
    'string_too_long': 'String should have at most {max_length} characters',
    'dict_type': 'Input should be a valid dict',
    'mapping_type': 'Input should be a valid mapping, error: {error}',
    'iterable_type': 'Input should be iterable',
    'iteration_error': 'Error iterating object, error: {error}',
    'list_type': 'Input should be a valid list',
    'tuple_type': 'Input should be a valid tuple',
    'set_type': 'Input should be a valid set',
    'bool_type': 'Input should be a valid boolean',
    'bool_parsing': 'Input should be a valid boolean, cannot interpret input',
    'int_type': 'Input should be a valid integer',
    'int_parsing': 'Input should be a valid integer, cannot parse string as integer',
    'int_parsing_size': 'Cannot parse input string as integer, exceeds maximum size',
    'int_from_float': 'Input should be a valid integer, got a number with a fractional part',
    'multiple_of': 'Input should be a multiple of {multiple_of}',
    'float_type': 'Input should be a valid number',
    'float_parsing': 'Input should be a valid number, cannot parse string as number',
    'bytes_type': 'Input should be valid bytes',
    'bytes_too_short': 'Data should have at least {min_length} bytes',
    'bytes_too_long': 'Data should have at most {max_length} bytes',
    'value_error': 'Value error, {error}',
    'assertion_error': 'Assertion failed, {error}',
    'literal_error': 'Input should be {expected}',
    'date_type': 'Input should be a valid date',
    'date_parsing': 'Input should be a valid date in YYYY-MM-DD format, {error}',
    'date_from_datetime_parsing': 'Input should be a valid date or datetime, {error}',
    'date_from_datetime_inexact': 'Datetime provided to date should have zero time - i.e. be an exact date',
    'date_past': 'Date should be in the past',
    'date_future': 'Date should be in the future',
    'time_type': 'Input should be a valid time',
    'time_parsing': 'Input should be a valid time format, {error}',
    'datetime_type': 'Input should be a valid datetime',
    'datetime_parsing': 'Input should be a valid datetime, {error}',
    'datetime_object_invalid': 'Invalid datetime object, got {error}',
    'datetime_past': 'Input should be in the past',
    'datetime_future': 'Input should be in the future',
    'timezone_naive': 'Input should not contain timezone info',
    'timezone_aware': 'Input should contain timezone info',
    'timezone_offset': 'Timezone offset should be {tz_expected}, got {tz_actual}',
    'time_delta_type': 'Input should be a valid timedelta',
    'time_delta_parsing': 'Input should be a valid timedelta, {error}',
    'frozen_set_type': 'Input should be a valid frozenset',
    'is_instance_of': 'Input should be an instance of {class}',
    'is_subclass_of': 'Input should be a subclass of {class}',
    'callable_type': 'Input should be callable',
    'union_tag_invalid': "Input tag '{tag}' found using {discriminator} does not match any expected tags: {expected_tags}",
    'union_tag_not_found': 'Could not extract tag using discriminator {discriminator}',
    'arguments_type': 'Arguments must be tuple, list, or dict',
    'missing_argument': 'Missing required argument',
    'unexpected_keyword_argument': 'Unexpected keyword argument',
    'missing_keyword_only_argument': 'Missing required keyword-only argument',
    'unexpected_positional_argument': 'Unexpected positional argument',
    'missing_positional_only_argument': 'Missing required positional-only argument',
    'multiple_argument_values': 'Multiple values provided for argument',
    'url_type': 'URL input should be string or URL',
    'url_parsing': 'Input should be a valid URL, {error}',
    'url_syntax_violation': 'Input violates strict URL syntax rules, {error}',
    'url_too_long': 'URL should have at most {max_length} characters',
    'url_scheme': 'URL scheme should be {expected_schemes}',
    'uuid_type': 'UUID input should be string, bytes, or UUID object',
    'uuid_parsing': 'Input should be a valid UUID, {error}',
    'uuid_version': 'Expected UUID version is {expected_version}',
    'decimal_type': 'Decimal input should be int, float, string, or Decimal object',
    'decimal_parsing': 'Input should be a valid decimal',
    'decimal_max_digits': 'Decimal input should have at most {max_digits} total digits',
    'decimal_max_places': 'Decimal input should have at most {decimal_places} decimal places',
    'decimal_whole_digits': 'Decimal input should have at most {whole_digits} digits before the decimal point',
}

CustomPhoneNumber = Annotated[str, Field(pattern=r'^1[3-9]\d{9}$')]


class CustomEmailStr(EmailStr):
    """Custom email type"""

    @classmethod
    def _validate(cls, __input_value: str) -> str:
        return None if __input_value == '' else validate_email(__input_value)[1]


class SchemaBase(BaseModel):
    """Base model configuration"""

    model_config = ConfigDict(
        use_enum_values=True,
        json_encoders={datetime: lambda x: x.strftime(settings.DATETIME_FORMAT)},
    )
