from engines.load_engine import LoadEngine

class LoadEngineSpark(LoadEngine):
    """Load engine for Spark"""

    def __init__(self, configuration, options, connection):
        """Initialize the LoadEngineSpark class"""

        self.configuration = configuration
        self.options = options
        self.connection = connection

    def execute(self, df_data):
        """Execute the load engine"""
        self.count = df_data.count()

        # Cast columns to specified types
        for column in self.options["cast"]:
            column_name = self.get_insensitive_item(column["name"], df_data.columns)
            column_type = column["type"]
            if column_type == "datetime":
                column_type = "timestamp"
                
            df_data = df_data.withColumn(column_name, df_data[column_name].cast(column_type))

        return df_data
