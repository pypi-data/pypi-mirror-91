#  Copyright 2019-2020 The Lux Authors.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from .context import lux
import pytest
import pandas as pd
from lux.vis.Vis import Vis


# Test suite for checking if the expected errors and warnings are showing up correctly
def test_intent_str_error(global_var):
    df = pytest.college_df
    with pytest.raises(TypeError, match="Input intent must be either a list"):
        df.intent = "bad string input"


def test_export_b4_widget_created(global_var):
    df = pd.read_csv("lux/data/college.csv")
    with pytest.warns(UserWarning, match="No widget attached to the dataframe"):
        df.exported


def test_bad_filter(global_var):
    df = pytest.college_df
    with pytest.warns(UserWarning, match="Lux can not operate on an empty dataframe"):
        df[df["Region"] == "asdfgh"]._repr_html_()


def test_multi_vis(global_var):
    df = pytest.college_df
    multivis_msg = "The intent that you specified corresponds to more than one visualization."
    with pytest.raises(TypeError, match=multivis_msg):
        Vis(["SATAverage", "AverageCost", "Geography=?"], df)

    with pytest.raises(TypeError, match=multivis_msg):
        Vis(["SATAverage", "?"], df)

    with pytest.raises(TypeError, match=multivis_msg):
        Vis(["SATAverage", "AverageCost", "Region=New England|Southeast"], df)

    with pytest.raises(TypeError, match=multivis_msg):
        Vis(["Region=New England|Southeast"], df)

    with pytest.raises(TypeError, match=multivis_msg):
        Vis(["FundingModel", ["Region", "ACTMedian"]], df)


# Test Properties with Private Variables Readable but not Writable
def test_vis_private_properties(global_var):
    from lux.vis.Vis import Vis

    df = pytest.car_df
    vis = Vis(["Horsepower", "Weight"], df)
    vis._repr_html_()
    assert isinstance(vis.data, lux.core.frame.LuxDataFrame)
    with pytest.raises(AttributeError, match="can't set attribute"):
        vis.data = "some val"

    assert isinstance(vis.code, dict)
    with pytest.raises(AttributeError, match="can't set attribute"):
        vis.code = "some val"

    assert isinstance(vis.min_max, dict)
    with pytest.raises(AttributeError, match="can't set attribute"):
        vis.min_max = "some val"

    assert vis.mark == "scatter"
    with pytest.raises(AttributeError, match="can't set attribute"):
        vis.mark = "some val"
