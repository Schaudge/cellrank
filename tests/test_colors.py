# -*- coding: utf-8 -*-
import pytest

import numpy as np
import pandas as pd
from pandas.api.types import is_categorical_dtype

from matplotlib.colors import is_color_like

from cellrank.tl._colors import _map_names_and_colors, _create_categorical_colors


class TestColors:
    def test_create_categorical_colors_too_many_colors(self):
        with pytest.raises(ValueError):
            _create_categorical_colors(1000)

    def test_create_categorical_colors_no_categories(self):
        c = _create_categorical_colors(0)

        assert c == []

    def test_create_categorical_colors_neg_categories(self):
        with pytest.raises(RuntimeError):
            _create_categorical_colors(-1)

    def test_create_categorical_colors_normal_run(self):
        colors = _create_categorical_colors(79)

        assert len(colors) == 79
        assert all(map(lambda c: isinstance(c, str), colors))
        assert all(map(lambda c: is_color_like(c), colors))

    def test_mapping_colors_not_categorical(self):
        query = pd.Series(["foo", "bar", "baz"], dtype="str")
        reference = pd.Series(["foo", np.nan, "bar", "baz"], dtype="category")

        with pytest.raises(TypeError):
            _map_names_and_colors(reference, query)

    def test_mapping_colors_invalid_size(self):
        query = pd.Series(["foo", "bar", "baz"], dtype="category")
        reference = pd.Series(["foo", np.nan, "bar", "baz"], dtype="category")

        with pytest.raises(ValueError):
            _map_names_and_colors(reference, query)

    def test_mapping_colors_different_index(self):
        query = pd.Series(["foo", "bar", "baz"], dtype="category", index=[2, 3, 4])
        reference = pd.Series(["foo", "bar", "baz"], dtype="category", index=[1, 2, 3])

        with pytest.raises(ValueError):
            _map_names_and_colors(reference, query)

    def test_mapping_colors_invalid_colors(self):
        query = pd.Series(["foo", "bar", "baz"], dtype="category")
        reference = pd.Series(["foo", "bar", "baz"], dtype="category")

        with pytest.raises(ValueError):
            _map_names_and_colors(
                reference, query, colors_reference=["red", "green", "foo"]
            )

    def test_mapping_colors_too_few_colors(self):
        query = pd.Series(["foo", "bar", "baz"], dtype="category")
        reference = pd.Series(["foo", "bar", "baz"], dtype="category")

        with pytest.raises(ValueError):
            _map_names_and_colors(reference, query, colors_reference=["red", "green"])

    def test_mapping_colors_simple(self):
        query = pd.Series(["foo", "bar", "baz"], dtype="category")
        reference = pd.Series(["foo", "bar", "baz"], dtype="category")

        res = _map_names_and_colors(reference, query)

        assert isinstance(res, pd.Series)
        assert len(res) == 3
        assert is_categorical_dtype(res)

    def test_mapping_colors_simple_colors(self):
        query = pd.Series(["foo", "bar", "baz"], dtype="category")
        reference = pd.Series(["foo", "bar", "baz"], dtype="category")

        res, c = _map_names_and_colors(
            reference, query, colors_reference=["red", "green", "blue"]
        )

        assert isinstance(res, pd.Series)
        assert len(res) == 3
        assert is_categorical_dtype(res)

        assert isinstance(c, list)
        assert c == ["#ff0000", "#008000", "#0000ff"]

    def test_mapping_colors_too_many_colors(self):
        query = pd.Series(["foo", "bar", "baz"], dtype="category")
        reference = pd.Series(["foo", "bar", "baz"], dtype="category")

        res, c = _map_names_and_colors(
            reference, query, colors_reference=["red", "green", "blue", "black"]
        )

        assert isinstance(res, pd.Series)
        assert len(res) == 3
        assert is_categorical_dtype(res)

        assert isinstance(c, list)
        assert c == ["#ff0000", "#008000", "#0000ff"]

    def test_mapping_colors_non_unique_colors(self):
        query = pd.Series(["foo", "bar", "baz"], dtype="category")
        reference = pd.Series(["foo", "bar", "baz"], dtype="category")

        res, c = _map_names_and_colors(
            reference, query, colors_reference=["red", "red", "red"]
        )

        assert isinstance(res, pd.Series)
        assert len(res) == 3
        assert is_categorical_dtype(res)

        assert isinstance(c, list)
        assert c == ["#ff0000", "#ff0000", "#ff0000"]

    def test_mapping_colors_same_reference(self):
        query = pd.Series(["foo", "bar", "baz"], dtype="category")
        reference = pd.Series(["foo", "foo", "foo"], dtype="category")

        r, c = _map_names_and_colors(
            reference, query, colors_reference=["red", "red", "red"]
        )

        assert list(r.index) == ["bar", "baz", "foo"]
        assert list(r.values) == ["foo_1", "foo_2", "foo_3"]
        assert c == ["#b20000", "#d13200", "#f07300"]

    def test_mapping_colors_diff_query_reference(self):
        query = pd.Series(["bar", "bar", "bar"], dtype="category")
        reference = pd.Series(["foo", "foo", "foo"], dtype="category")

        r, c = _map_names_and_colors(
            reference, query, colors_reference=["red", "red", "red"]
        )

        assert list(r.index) == ["bar"]
        assert list(r.values) == ["foo"]
        assert c == ["#ff0000"]

    def test_mapping_colors_empty(self):
        query = pd.Series([], dtype="category")
        reference = pd.Series([], dtype="category")

        r, c = _map_names_and_colors(reference, query, colors_reference=[])

        assert isinstance(r, pd.Series)
        assert is_categorical_dtype(r)
        assert isinstance(c, list)
        assert len(c) == 0
