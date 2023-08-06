# ======================================================================================
#
# Copyright: CERFACS, LIRMM, Total S.A. - the quantum computing team (15/10/2020)
# Contributor: Adrien Suau (adrien.suau@cerfacs.fr)
#
# This program is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your discretion) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.
#
# See the GNU Lesser General Public License for more details. You should have received
# a copy of the GNU Lesser General Public License along with this program. If not, see
# https://www.gnu.org/licenses/lgpl-3.0.txt
#
# ======================================================================================
from test.utils import _is_iterable, dict_eq


def test_is_iterable():
    assert _is_iterable(list())
    assert _is_iterable(tuple())
    assert _is_iterable(dict())
    assert _is_iterable(set())
    assert _is_iterable(iter([i for i in range(3)]))
    assert _is_iterable(range(4))
    assert not _is_iterable(1)
    assert _is_iterable("Hello")
    assert not _is_iterable(1.0)


def test_dict_eq():
    assert dict_eq({}, {})
    assert not dict_eq({}, {1: 3})
    assert dict_eq({"a": 2}, {"a": 2})
    assert not dict_eq({"a": {"a": 2}}, {"a": {"b": 2}})
    assert not dict_eq({"a": {"a": 2}}, {"a": {"b": 2, "a": 2}})
    assert dict_eq({"a": {"a": 3, "b": 2}}, {"a": {"b": 2, "a": 3}})
    assert not dict_eq({"a": []}, {"a": ()})
    assert dict_eq({"a": []}, {"a": []})
    assert not dict_eq({"a": [1]}, {"a": [2]})
