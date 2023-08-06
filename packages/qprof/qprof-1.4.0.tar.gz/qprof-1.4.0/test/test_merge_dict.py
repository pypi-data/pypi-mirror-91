# ======================================================================================
#
# Copyright: CERFACS, LIRMM, Total S.A. - the quantum computing team (14/10/2020)
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

from qprof._merge_dicts import merge_dict


def test_merge_empty_dicts():
    c = merge_dict({}, {})
    assert c == {}


def test_merge_empty_filled_dict():
    a, b = {}, {"a": 2, "b": 3}
    c = merge_dict(a, b)
    # Check that a and b has not been altered
    assert a == {}
    assert b == {"a": 2, "b": 3}

    # Check c
    assert c == {"a": 2, "b": 3}


def test_merge_filled_empty_dict():
    b, a = {}, {"a": 2, "b": 3}
    c = merge_dict(a, b)
    # Check that a and b has not been altered
    assert b == {}
    assert a == {"a": 2, "b": 3}

    # Check c
    assert c == {"a": 2, "b": 3}


def test_merge_filled_dict_no_conflict():
    a, b = {"a": 2}, {"b": 3}
    c = merge_dict(a, b)
    # Check that a and b has not been altered
    assert a == {"a": 2}
    assert b == {"b": 3}
    # Check c
    assert c == {"a": 2, "b": 3}


def test_merge_dict_conflict():
    a, b = {"a": 2}, {"a": 1}
    c = merge_dict(a, b)
    # Check that a and b has not been altered
    assert a == {"a": 2}
    assert b == {"a": 1}
    # Check c
    assert c == {"a": 3}


def test_merge_dict():
    a, b = {"a": 2}, {"a": 1, "b": 4}
    c = merge_dict(a, b)
    # Check that a and b has not been altered
    assert a == {"a": 2}
    assert b == {"a": 1, "b": 4}
    # Check c
    assert c == {"a": 3, "b": 4}


def test_merge_nested_dict_no_conflict():
    a, b = {"a": {"a": 2}}, {"b": {"a": 4}}
    c = merge_dict(a, b)
    # Check that a and b has not been altered
    assert a == {"a": {"a": 2}}
    assert b == {"b": {"a": 4}}
    # Check c
    assert c == {"a": {"a": 2}, "b": {"a": 4}}


def test_merge_nested_dict_conflict_first_level():
    a, b = {"a": {"a": 2}}, {"a": {"b": 4}}
    c = merge_dict(a, b)
    # Check that a and b has not been altered
    assert a == {"a": {"a": 2}}
    assert b == {"a": {"b": 4}}
    # Check c
    assert c == {"a": {"a": 2, "b": 4}}


def test_merge_nested_dict_conflicts_multi_level():
    a, b = {"a": {"a": 2}}, {"a": {"a": 4}}
    c = merge_dict(a, b)
    # Check that a and b has not been altered
    assert a == {"a": {"a": 2}}
    assert b == {"a": {"a": 4}}
    # Check c
    assert c == {"a": {"a": 6}}
