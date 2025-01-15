"""Comparison engine for native connectors"""

import numpy as np
import pandas as pd

from engines.compare_engine import CompareEngine

class CompareEngineNative(CompareEngine):
    """Comparison engine for native connectors"""

    def __init__(self, df_source, df_expected, options):
        """Initialize the CompareEngineNative class"""

        self.df_source = df_source
        self.df_expected = df_expected
        self.options = options
        self.mode = options["compare_mode"].upper()

    def compare(self) -> bool:
        """Compare the source and expected datasets"""

        if self.mode == "ORDER":
            if len(self.df_source) == 0 and len(self.df_expected) == 0 and self.options["allow_no_rows"]:
                return True
            if not self.compare_structure():
                return False
            if not self.compare_length():
                return False
            if not self.compare_data_with_order():
                return False
            return True

    def compare_length(self) -> bool:
        """Compare the length of the source and expected datasets"""

        count_source = len(self.df_source)
        count_expected = len(self.df_expected)

        if count_source != count_expected:
            self.error_type = "count"
            self.error_message = f"The count in source dataset ({count_source}) is different than the count in the expected dataset ({count_expected})"
            return False

        return True

    def compare_structure(self) -> bool:
        """Compare the structure of the source and expected datasets"""

        # Normalize column names to lowercase
        self.df_source.columns = map(str.lower, self.df_source.columns)
        self.df_expected.columns = map(str.lower, self.df_expected.columns)

        # Remove columns specified in the ignore options
        if self.options is not None and self.options["ignore"] is not None:
            columns_to_ignore = [x.lower() for x in self.options["ignore"]]

            self.df_source = self.df_source.drop(columns=columns_to_ignore, axis=1, errors="ignore")
            self.df_expected = self.df_expected.drop(columns=columns_to_ignore, axis=1, errors="ignore")

        # Sort headers before comparison
        df_columns_source = pd.DataFrame({"columns": self.df_source.columns}).sort_values(by=["columns"]).reset_index(drop=True)
        df_columns_expected = pd.DataFrame({"columns": self.df_expected.columns}).sort_values(by=["columns"]).reset_index(drop=True)

        # Compare column headers
        mask = ~df_columns_expected[["columns"]].apply(tuple, axis=1).isin(df_columns_source[["columns"]].apply(tuple, axis=1))
        missing_columns = df_columns_expected[mask]

        # Set error message if missing columns are found in the source
        if not missing_columns.empty:
            missing_columns_list = ", ".join(missing_columns["columns"].to_list())
            self.error_type = "headers"
            self.error_message = f"Missing columns: {missing_columns_list}"
            return False

        # Remove columns that are not in the expected dataframe
        self.df_source = self.df_source[df_columns_expected["columns"]]
        self.df_expected = self.df_expected[df_columns_expected["columns"]]

        return True

    def compare_data_with_order(self) -> bool:
        """Compare the source and expected datasets with "order" mode"""

        # Sort the datasets if the sort option is specified
        if self.options is not None and self.options["sort"] is not None:
            sort_columns = self.options["sort"]
            sort_columns = [x.lower() for x in sort_columns]

            if len(self.options["sort"]) > 0 and self.options["sort"][0] == "*":
                sort_columns = self.df_expected.columns["columns"].to_list()

            self.df_source = self.df_source.sort_values(by=sort_columns).reset_index(drop=True)
            self.df_expected = self.df_expected.sort_values(by=sort_columns).reset_index(drop=True)

        tolerance = self.options["tolerance"]

        df_source_preprocessed = self.df_source.copy()
        df_expected_preprocessed = self.df_expected.copy()

        datasource_count = len(self.df_source)

        # Trim the data if the trim option is specified
        if self.options["trim"]:
            df_source_preprocessed = df_source_preprocessed.applymap(lambda x: x.strip() if isinstance(x, str) else x)
            df_expected_preprocessed = df_expected_preprocessed.applymap(lambda x: x.strip() if isinstance(x, str) else x)

        # Convert all string values to lowercase if the case_insensitive option is specified
        if self.options["case_insensitive"]:
            df_source_preprocessed = df_source_preprocessed.applymap(lambda x: x.lower() if isinstance(x, str) else x)
            df_expected_preprocessed = df_expected_preprocessed.applymap(lambda x: x.lower() if isinstance(x, str) else x)

        def compare_with_tolerance(val1, val2):
            """Compare two values with tolerance"""
            if str(val1.dtype) in ("float64", "Int64") and str(val2.dtype) in ("float64", "Int64"):
                return abs(val1 - val2) > tolerance
            return val1 != val2

        # Compare the source and expected datasets with tolerance
        diff_with_tol = df_source_preprocessed.combine(df_expected_preprocessed, compare_with_tolerance)

        # Get the indices of the differences
        diff_indices = np.where(diff_with_tol)

        # Create a dataframe to store the differences
        df_differences = pd.DataFrame(index=self.df_source.index, columns=pd.MultiIndex.from_tuples([(col, "source") for col in self.df_source.columns] + [(col, "expected") for col in self.df_source.columns]))

        # Fill the differences dataframe with the values from the source and expected datasets
        for i, j in zip(*diff_indices):
            col = self.df_source.columns[j]
            df_differences.loc[self.df_source.index[i], (col, "source")] = self.df_source.iat[i, j]
            df_differences.loc[self.df_source.index[i], (col, "expected")] = self.df_expected.iat[i, j]

        # Drop rows and columns with all NaN values
        df_differences = df_differences.dropna(axis=1, how="all").dropna(axis=0, how="all")

        # Set the success rate and error message
        if len(df_differences) > 0:
            self.success_rate = (datasource_count - len(df_differences)) / datasource_count
            if self.success_rate < self.options["pass_rate"]:
                self.error_message = "Some rows are not equal between source dataset and expected dataset"
                self.error_type = "data"

            self.df_compare_gap = df_differences.reindex(sorted(df_differences.columns), axis=1)

            return False

        # Set the error message if the source and expected datasets are empty
        if self.error_message is None and datasource_count == 0 and not self.options["allow_no_rows"]:
            self.error_message = "Source and expected datasets are empty but no allow_no_rows option is set to False"
            self.error_type = "data"

            return False

        return True
