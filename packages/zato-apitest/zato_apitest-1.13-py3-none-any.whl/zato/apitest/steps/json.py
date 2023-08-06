# -*- coding: utf-8 -*-

"""
Copyright (C) Zato Source s.r.o. https://zato.io

Licensed under LGPLv3, see LICENSE.txt for terms and conditions.
"""

# Part of Zato - Open-Source ESB, SOA, REST, APIs and Cloud Integrations in Python
# https://zato.io

# stdlib
from ast import literal_eval

# base32_crockford
from base32_crockford import decode as crockford_decode

# Behave
from behave import given, then

# datadiff
from datadiff.tools import assert_equals

# jsonpointer
from jsonpointer import resolve_pointer as get_pointer, set_pointer as _set_pointer

# json
from .common import needs_json
import json

# Zato
from .. import util
from .. import INVALID

import uuid

# Integer types for testing 'path {path} is any integer'
try:
    int_types = (int, long)
except:
    int_types = (int,)     # python 3 doesn't have the long type


# ################################################################################################################################

def set_pointer(ctx, path, value):
    if 'data_impl' not in ctx.zato.request:
        raise ValueError('path called but no request set')

    _set_pointer(ctx.zato.request.data_impl, path, value)

# ################################################################################################################################

@given('path "{path}" in request is "{value}"')
@util.obtain_values
def given_json_pointer_in_request_is(ctx, path, value):
    set_pointer(ctx, path, value)

@given('path "{path}" in request is "{value}" (with literal_eval)')
@util.obtain_values
def given_json_pointer_in_request_is_with_literal_eval(ctx, path, value):
    set_pointer(ctx, path, literal_eval(value))

@given('path "{path}" in request is a UUID')
@util.obtain_values
def given_json_pointer_in_request_is_a_uuid(ctx, path):
    set_pointer(ctx, path, uuid.uuid4().hex)

@given('path "{path}" in request is an integer "{value}"')
@util.obtain_values
def given_json_pointer_in_request_is_an_integer(ctx, path, value):
    set_pointer(ctx, path, int(value))

@given('path "{path}" in request is a float "{value}"')
@util.obtain_values
def given_json_pointer_in_request_is_a_float(ctx, path, value):
    set_pointer(ctx, path, float(value))

@given('path "{path}" in request is a list "{value}"')
@util.obtain_values
def given_json_pointer_in_request_is_a_list(ctx, path, value):
    set_pointer(ctx, path, util.parse_list(value))

@given('path "{path}" in request is a random string')
@util.obtain_values
def given_json_pointer_in_request_is_a_random_string(ctx, path):
    set_pointer(ctx, path, util.rand_string())

@given('path "{path}" in request is a random integer')
@util.obtain_values
def given_json_pointer_in_request_is_a_random_integer(ctx, path):
    set_pointer(ctx, path, util.rand_int())

@given('path "{path}" in request is a random float')
@util.obtain_values
def given_json_pointer_in_request_is_a_random_float(ctx, path):
    set_pointer(ctx, path, util.rand_float())

@given('path "{path}" in request is one of "{value}"')
@util.obtain_values
def given_json_pointer_in_request_is_one_of(ctx, path, value):
    set_pointer(ctx, path, util.any_from_list(value))

@given('path "{path}" in request is True')
@util.obtain_values
def given_json_pointer_in_request_is_true(ctx, path):
    set_pointer(ctx, path, True)

@given('path "{path}" in request is False')
@util.obtain_values
def given_json_pointer_in_request_is_true(ctx, path):
    set_pointer(ctx, path, False)

# ################################################################################################################################

@given('path "{path}" in request is a random date "{format}"')
@util.obtain_values
def given_json_pointer_is_rand_date(ctx, path, format):
    set_pointer(ctx, path, util.rand_date(ctx.zato.date_formats[format]))

@given('path "{path}" in request is now "{format}"')
@util.obtain_values
def given_json_pointer_is_now(ctx, path, format):
    set_pointer(ctx, path, util.now(format=ctx.zato.date_formats[format]))

@given('path "{path}" in request is UTC now "{format}"')
@util.obtain_values
def given_json_pointer_is_utc_now(ctx, path, format):
    set_pointer(ctx, path, util.utcnow(format=ctx.zato.date_formats[format]))

@given('path "{path}" in request is UTC now "{format}" minus one hour')
@util.obtain_values
def given_json_pointer_is_utc_now_minus_one_hour(ctx, path, format):
    set_pointer(ctx, path, util.utcnow_minus_hour(format=ctx.zato.date_formats[format]))

@given('path "{path}" in request is a random date after "{date_start}" "{format}"')
@util.obtain_values
def given_json_pointer_is_rand_date_after(ctx, path, date_start, format):
    set_pointer(ctx, path, util.date_after(date_start, ctx.zato.date_formats[format]))

@given('path "{path}" in request is a random date before "{date_end}" "{format}"')
@util.obtain_values
def given_json_pointer_is_rand_date_before(ctx, path, date_end, format):
    set_pointer(ctx, path, util.date_before(date_end, ctx.zato.date_formats[format]))

@given('path "{path}" in request is a random date between "{date_start}" and "{date_end}" "{format}"')
@util.obtain_values
def given_json_pointer_is_rand_date_between(ctx, path, date_start, date_end, format):
    set_pointer(ctx, path, util.date_between(date_start, date_end, ctx.zato.date_formats[format]))

# ################################################################################################################################

def assert_value(ctx, path, value, wrapper=None):
    if 'data_impl' not in ctx.zato.response:
        raise ValueError('Assertion called but no format set')

    value = wrapper(value) if wrapper else value
    actual = get_pointer(ctx.zato.response.data_impl, path)
    assert_equals(value, actual)
    return True

@then('path "{path}" is "{value}"')
@util.obtain_values
def then_json_pointer_is(ctx, path, value):
    return assert_value(ctx, path, value)

@then('path "{path}" is "{value}" (with literal_eval)')
@util.obtain_values
def then_json_pointer_is_with_literal_eval(ctx, path, value):
    return assert_value(ctx, path, literal_eval(value))

@then('path "{path}" is JSON "{value}"')
@needs_json
@util.obtain_values
def then_json_pointer_is_json(ctx, path, value):
    return assert_value(ctx, path, json.loads(value))

@then('path "{path}" is JSON equal to that from "{value}"')
@needs_json
@util.obtain_values
def then_json_pointer_is_json_equal_to_that_from(ctx, path, value):
    return assert_value(ctx, path, json.loads(util.get_data(ctx, 'response', value)))

@then('path "{path}" is an integer "{value}"')
@util.obtain_values
def then_json_pointer_is_an_integer(ctx, path, value):
    return assert_value(ctx, path, value, int)

@then('path "{path}" is any integer')
@util.obtain_values
def then_json_pointer_is_any_integer(ctx, path):
    actual = get_pointer(ctx.zato.response.data_impl, path)
    assert isinstance(actual, int_types), \
        'Expected an integer in {}, got a `{}`'.format(path, type(actual))
    return True

@then('path "{path}" is a float "{value}"')
@util.obtain_values
def then_json_pointer_is_a_float(ctx, path, value):
    return assert_value(ctx, path, value, float)

@then('path "{path}" is any float')
@util.obtain_values
def then_json_pointer_is_any_float(ctx, path):
    actual = get_pointer(ctx.zato.response.data_impl, path)
    assert isinstance(actual, float), \
        'Expected a float in {}, got a `{}`'.format(path, type(actual))
    return True

@then('path "{path}" is any bool')
@util.obtain_values
def then_json_pointer_is_any_bool(ctx, path):
    actual = get_pointer(ctx.zato.response.data_impl, path)
    assert isinstance(actual, bool), \
        'Expected a bool in {}, got a `{}`'.format(path, type(actual))
    return True

@then('path "{path}" is a list "{value}"')
@util.obtain_values
def then_json_pointer_is_a_list(ctx, path, value):
    return assert_value(ctx, path, value, util.parse_list)

@then('path "{path}" is empty')
@util.obtain_values
def then_json_pointer_is_empty(ctx, path):
    return assert_value(ctx, path, '')

@then('path "{path}" is not empty')
@util.obtain_values
def then_json_pointer_isnt_empty(ctx, path):
    actual = get_pointer(ctx.zato.response.data_impl, path, INVALID)
    assert actual != INVALID, 'Path `{}` Should not be empty'.format(path)

@then('path "{path}" is not an empty list')
@util.obtain_values
def then_json_pointer_isnt_an_empty_list(ctx, path):
    actual = get_pointer(ctx.zato.response.data_impl, path, [])
    assert isinstance(actual, list), 'Path `{}` should be a list'.format(path)
    assert actual, 'Path `{}` should not be an empty list'.format(path)

@then('path "{path}" is one of "{value}"')
@util.obtain_values
def then_json_pointer_is_one_of(ctx, path, value):
    actual = get_pointer(ctx.zato.response.data_impl, path)
    value = util.parse_list(value)
    assert actual in value, 'Expected for `{}` ({}) to be in `{}`'.format(actual, path, value)

@then('path "{path}" is not one of "{value}"')
@util.obtain_values
def then_json_pointer_isnt_one_of(ctx, path, value):
    actual = get_pointer(ctx.zato.response.data_impl, path)
    value = util.parse_list(value)
    assert actual not in value, 'Expected for `{}` ({}) not to be in `{}`'.format(actual, path, value)

@then('path "{path}" is a BASE32 Crockford, checksum "{checksum}"')
@util.obtain_values
def then_json_pointer_is_a_base32_crockford(ctx, path, checksum):
    actual = get_pointer(ctx.zato.response.data_impl, path)
    crockford_decode(actual.replace('-', ''), checksum.lower() == 'true')

# ###############################################################################################################################

@then('path "{path}" is True')
@util.obtain_values
def then_json_pointer_is_true(ctx, path):
    return assert_value(ctx, path, True)

@then('path "{path}" is False')
@util.obtain_values
def then_json_pointer_is_false(ctx, path):
    return assert_value(ctx, path, False)

@then('path "{path}" is null')
@util.obtain_values
def then_json_pointer_is_null(ctx, path):
    return assert_value(ctx, path, None)

@then('path "{path}" is an empty list')
@util.obtain_values
def then_json_pointer_is_an_empty_list(ctx, path):
    return assert_value(ctx, path, [])

@then('path "{path}" is an empty dict')
@util.obtain_values
def then_json_pointer_is_an_empty_dict(ctx, path):
    return assert_value(ctx, path, {})

@then('path "{path}" is not a string "{value}"')
@util.obtain_values
def then_json_pointer_isnt_a_string(ctx, path, value):
    actual = get_pointer(ctx.zato.response.data_impl, path)
    assert actual != value, 'Expected `{}` != `{}`'.format(actual, value)

@then('JSON response exists')
@util.obtain_values
def then_json_response_exists(ctx):
    assert ctx.zato.response.data_impl

@then('JSON response does not exist')
@util.obtain_values
def then_json_response_doesnt_exist(ctx):
    assert not ctx.zato.response.data_impl

@then('path "{path}" starts with "{value}"')
@util.obtain_values
def then_json_pointer_starts_with(ctx, path, value):
    actual = get_pointer(ctx.zato.response.data_impl, path)
    assert actual.startswith(value), 'Expected for `{}` to start with `{}`'.format(actual, value)

@then('path "{path}" starts with any of "{value}"')
@util.obtain_values
def then_json_pointer_starts_with_any_of(ctx, path, value):
    actual = get_pointer(ctx.zato.response.data_impl, path)
    value = util.parse_list(value)
    for elem in value:
        if actual.startswith(elem):
            break
    else:
        raise AssertionError('Path `{}` ({}) does not start with any of `{}`'.format(path, actual, value))

@then('path "{path}" ends with "{value}"')
@util.obtain_values
def then_json_pointer_ends_with(ctx, path, value):
    actual = get_pointer(ctx.zato.response.data_impl, path)
    assert actual.endswith(value), 'Expected for `{}` to end with `{}`'.format(actual, value)

# ###############################################################################################################################

def _then_json_pointer_contains(ctx, path, expected):
    actual_list = get_pointer(ctx.zato.response.data_impl, path)

    for item in actual_list:
        try:
            assert_equals(item, expected)
        except AssertionError:
            pass
        else:
            return True
    else:
        raise AssertionError('Expected data `{}` not in `{}`'.format(expected, actual_list))

@then('path "{path}" contains "{value}"')
@util.obtain_values
def then_json_pointer_contains(ctx, path, value):
    return _then_json_pointer_contains(ctx, path, json.loads(value))

@then('path "{path}" contains data from "{value}"')
@util.obtain_values
def then_json_pointer_contains_data_from(ctx, path, value):
    return _then_json_pointer_contains(ctx, path, json.loads(util.get_data(ctx, 'response', value)))

# ###############################################################################################################################
