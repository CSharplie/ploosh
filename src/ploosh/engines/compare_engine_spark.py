"""Comparison engine for spark connectors"""

from pyspark.sql import DataFrame, Window
from pyspark.sql.functions import col, lower, trim, abs, when, lit, row_number
from pyspark.sql.types import NumericType
from engines.compare_engine import CompareEngine

class CompareEngineSpark(CompareEngine):
    """Comparison engine for spark connectors"""

    def __init__(self, df_source: DataFrame, df_expected: DataFrame, options: dict):
        """Initialize the CompareEngineSpark class"""

        self.df_source = df_source
        self.df_expected = df_expected
        self.options = options
        self.mode = options["compare_mode"].upper()

    def compare(self) -> bool:
        """Compare the source and expected datasets"""
        if self.mode == "ORDER":
            if self.df_source.count() == 0 and self.df_expected.count() == 0 and self.options["allow_no_rows"]:
                return True
            if not self.compare_structure():
                return False
            if not self.compare_length():
                return False
            if not self.compare_data():
                return False
            return True
        elif self.mode == "JOIN":
            if self.df_source.count() == 0 and self.df_expected.count() == 0 and self.options["allow_no_rows"]:
                return True
            if not self.compare_structure():
                return False
            if not self.compare_data():
                return False
            return True

    def compare_length(self) -> bool:
        """Compare the length of the source and expected datasets"""
        count_source = self.df_source.count()
        count_expected = self.df_expected.count()

        if count_source != count_expected:
            self.error_type = "count"
            self.error_message = f"The count in source dataset ({count_source}) is different than the count in the expected dataset ({count_expected})"
            return False

        return True

    def compare_structure(self) -> bool:
        """Compare the structure of the source and expected datasets"""
        # Normalize column names to lowercase
        self.df_source = self.df_source.select(*[col(c).alias(c.lower()) for c in self.df_source.columns])
        self.df_expected = self.df_expected.select(*[col(c).alias(c.lower()) for c in self.df_expected.columns])

        # Remove columns specified in the ignore options
        if self.options is not None and self.options["ignore"] is not None:
            columns_to_ignore = [col.lower() for col in self.options["ignore"]]

            self.df_source = self.df_source.drop(*columns_to_ignore)
            self.df_expected = self.df_expected.drop(*columns_to_ignore)

        # Compare column headers
        source_cols = set(self.df_source.columns)
        expected_cols = set(self.df_expected.columns)

        missing_columns = expected_cols - source_cols
        if missing_columns:
            self.error_type = "headers"
            self.error_message = f"Missing columns: {', '.join(missing_columns)}"
            return False

        extra_columns = source_cols - expected_cols
        # remove extra columns from source
        if extra_columns:
            self.df_source = self.df_source.drop(*extra_columns)

        return True

    def compare_data(self) -> bool:
        """Compare the source and expected datasets with "order" mode"""

        # Sort the data based on the specified columns
        if self.options is not None and self.options["sort"] is not None:
            sort_columns = self.options["sort"]
            sort_columns = [x.lower() for x in sort_columns]

            if len(self.options["sort"]) > 0 and self.options["sort"][0] == "*":
                sort_columns = self.df_expected.columns
        else:
            sort_columns = self.df_expected.columns

        if self.mode == "ORDER":
            df_window = Window.orderBy(*sort_columns)
            self.df_source = self.df_source.withColumn("__ploosh_order_key", row_number().over(df_window))
            self.df_expected = self.df_expected.withColumn("__ploosh_order_key", row_number().over(df_window))

        tolerance = self.options["tolerance"]
        join_keys = self.options["join_keys"]

        # Trim the data if the trim option is specified
        if self.options["trim"]:
            for col_name in self.df_source.columns:
                self.df_source = self.df_source.withColumn(col_name, trim(col(col_name)))
            for col_name in self.df_expected.columns:
                self.df_expected = self.df_expected.withColumn(col_name, trim(col(col_name)))

        # Convert all string values to lowercase if the case_insensitive option is specified
        if self.options["case_insensitive"]:
            for col_name in self.df_source.columns:
                self.df_source = self.df_source.withColumn(col_name, lower(col(col_name)))
            for col_name in self.df_expected.columns:
                self.df_expected = self.df_expected.withColumn(col_name, lower(col(col_name)))

        # Add a suffix to the column names to avoid conflicts
        df1 = self.df_source.select([col(c).alias(f"{c}_source") for c in self.df_source.columns])
        df2 = self.df_expected.select([col(c).alias(f"{c}_expected") for c in self.df_source.columns])

        # Clean up the order key column
        if self.mode == "ORDER":
            df1 = df1.withColumnRenamed("__ploosh_order_key_source", "__ploosh_order_key")
            df2 = df2.withColumnRenamed("__ploosh_order_key_expected", "__ploosh_order_key")

            # Join the two dataframes on the order key
            joined_df = df1.join(df2, on=["__ploosh_order_key"], how="inner")
            joined_df = joined_df.drop("__ploosh_order_key")

            # Drop the order key column from the source and expected dataframes
            self.df_source = self.df_source.drop("__ploosh_order_key")
            self.df_expected = self.df_expected.drop("__ploosh_order_key")
        elif self.mode == "JOIN":
            # Join the two dataframes on the columns
            joined_df = df1.join(df2, on=[col(f"{c.lower()}_source") == col(f"{c.lower()}_expected") for c in join_keys], how="inner")

        diff_columns = []
        for c in self.df_source.columns:
            source_col = f"{c}_source"
            expected_col = f"{c}_expected"
 
            source_is_numeric = isinstance(df1.schema[source_col].dataType, NumericType)
            expected_is_numeric = isinstance(df2.schema[expected_col].dataType, NumericType)

            # Check if the column is numeric and the tolerance is greater than 0
            if source_is_numeric and expected_is_numeric and tolerance > 0:
                filters = (abs(col(source_col) - col(expected_col)) > tolerance)
            else:
                filters = (col(source_col) != col(expected_col))

            # Add state columns to show the differences
            diff_columns.append(when(filters, lit(False)).alias(f"{c}_state"))

            # Add the source and expected columns to the diff_columns
            diff_columns.append(when(filters, col(source_col)).alias(source_col))
            diff_columns.append(when(filters, col(expected_col)).alias(expected_col))

        # Filter the joined dataframe to get the differences
        result = joined_df.select(*diff_columns).filter(
            " OR ".join([f"{c}_state = FALSE" for c in self.df_source.columns])
        ).drop(*[f"{c}_state" for c in self.df_source.columns])

        datasource_count = self.df_source.count()

        # Set the success rate and error message if there are differences
        if result.count() > 0:
            # Convert the result to a pandas dataframe for the output report
            df_differences = result.toPandas()

            self.success_rate = (datasource_count - len(df_differences)) / datasource_count
            if self.success_rate < self.options["pass_rate"]:
                self.error_message = "Some rows are not equal between source dataset and expected dataset"
                self.error_type = "data"

            self.df_compare_gap = df_differences.reindex(sorted(df_differences.columns), axis=1)

            return False

        # Set the error message if the source and expected datasets are empty
        if self.error_message is None and datasource_count == 0 and not self.options["allow_no_rows"]:
            self.error_message = "Source and exptected datasets are empty but no allow_no_rows option is set to False"
            self.error_type = "data"

            return False

        return True
