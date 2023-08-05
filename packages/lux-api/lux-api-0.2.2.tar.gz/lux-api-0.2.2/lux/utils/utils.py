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
import pandas as pd


def convert_to_list(x):
    """
    "a" --> ["a"]
    ["a","b"] --> ["a","b"]
    """
    if type(x) != list:
        return [x]
    else:
        return x


def pandas_to_lux(df):
    from lux.core.frame import LuxDataFrame

    values = df.values.tolist()
    ldf = LuxDataFrame(values, columns=df.columns)
    return ldf


def get_attrs_specs(intent):
    if intent is None:
        return []
    spec_obj = list(filter(lambda x: x.value == "", intent))
    return spec_obj


def get_filter_specs(intent):
    if intent is None:
        return []
    spec_obj = list(filter(lambda x: x.value != "", intent))
    return spec_obj


def check_import_lux_widget():
    import pkgutil

    if pkgutil.find_loader("luxwidget") is None:
        raise Exception(
            "luxwidget is not installed. Run `pip install luxwidget' to install the Jupyter widget.\nSee more at: https://github.com/lux-org/lux-widget"
        )


def get_agg_title(clause):
    attr = str(clause.attribute)
    if clause.aggregation is None:
        if len(attr) > 25:
            return attr[:15] + "..." + attr[-10:]
        return f"{attr}"
    elif attr == "Record":
        return f"Number of Records"
    else:
        if len(attr) > 15:
            return f"{clause._aggregation_name.capitalize()} of {attr[:15]}..."
        return f"{clause._aggregation_name.capitalize()} of {attr}"


def check_if_id_like(df, attribute):
    import re

    # Strong signals
    # so that aggregated reset_index fields don't get misclassified
    high_cardinality = df.cardinality[attribute] > 500
    attribute_contain_id = re.search(r"id", str(attribute)) is not None
    almost_all_vals_unique = df.cardinality[attribute] >= 0.98 * len(df)
    is_string = pd.api.types.is_string_dtype(df[attribute])
    if is_string:
        # For string IDs, usually serial numbers or codes with alphanumerics have a consistent length (eg., CG-39405) with little deviation. For a high cardinality string field but not ID field (like Name or Brand), there is less uniformity across the string lengths.
        if len(df) > 50:
            sampled = df[attribute].sample(50, random_state=99)
        else:
            sampled = df[attribute]
        str_length_uniformity = sampled.apply(lambda x: type(x) == str and len(x)).std() < 3
        return (
            high_cardinality
            and (attribute_contain_id or almost_all_vals_unique)
            and str_length_uniformity
        )
    else:
        # TODO: Could probably add some type of entropy measure (since the binned id fields are usually very even)
        return high_cardinality and (attribute_contain_id or almost_all_vals_unique)


def like_nan(val):
    if isinstance(val, str):
        return val.lower() == "nan"
    elif isinstance(val, float) or isinstance(val, int):
        import math

        return math.isnan(val)
