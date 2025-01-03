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

        # TODO: Implement Spark specific data transformations

        return df_data
