from exporters.exporter import Exporter

class ExporterPostgreSQL(Exporter):
    """Export test case result to PostgreSQL database"""

    CREATE_TABLE_QUERY = """
        CREATE TABLE IF NOT EXISTS ploosh_results (
            execution_id VARCHAR(255),
            name VARCHAR(255),
            state VARCHAR(50),
            source_start TIMESTAMP,
            source_end TIMESTAMP,
            source_duration FLOAT,
            source_count BIGINT,
            source_executed_action VARCHAR(255),
            expected_start TIMESTAMP,
            expected_end TIMESTAMP,
            expected_duration FLOAT,
            expected_count BIGINT,
            expected_executed_action VARCHAR(255),
            compare_start TIMESTAMP,
            compare_end TIMESTAMP,
            compare_duration FLOAT,
            success_rate FLOAT 
        );
    """

    INSERT_QUERY = """
        INSERT INTO ploosh_results (
            execution_id, name, state,
            source_start, source_end, source_duration, source_count, source_executed_action,
            expected_start, expected_end, expected_duration, expected_count, expected_executed_action,
            compare_start, compare_end, compare_duration, success_rate
        ) VALUES (
            :execution_id, :name, :state,
            :source_start, :source_end, :source_duration, :source_count, :source_executed_action,
            :expected_start, :expected_end, :expected_duration, :expected_count, :expected_executed_action,
            :compare_start, :compare_end, :compare_duration, :success_rate
        );
    """

    def __init__(self):
        # Set the name of the exporter
        self.name = "POSTGRESQL"

    def export(self, cases: dict, execution_id: str):
        """Export test case results to a PostgreSQL database"""
        # Check if connection and connector are available
        if self.connection is None:
            raise RuntimeError("PostgreSQL export connection not found. Add __export__ section to connections.yml")
        if self.connector is None:
            raise RuntimeError("PostgreSQL connector not found. Make sure pg8000 is installed.")

        self.connector.execute_query(self.CREATE_TABLE_QUERY, connection=self.connection)

        try:
            for case_name, case in cases.items():
                self.connector.execute_query(
                    self.INSERT_QUERY,
                    connection=self.connection,
                    parameters={
                        "execution_id": execution_id,
                        "name": case_name,
                        "state": case.state,
                        "source_start": case.source.duration.start,
                        "source_end": case.source.duration.end,
                        "source_duration": case.source.duration.duration,
                        "source_count": case.source.count,
                        "source_executed_action": case.source.executed_action,
                        "expected_start": case.expected.duration.start,
                        "expected_end": case.expected.duration.end,
                        "expected_duration": case.expected.duration.duration,
                        "expected_count": case.expected.count,
                        "expected_executed_action": case.expected.executed_action,
                        "compare_start": case.compare_duration.start,
                        "compare_end": case.compare_duration.end,
                        "compare_duration": case.compare_duration.duration,
                        "success_rate": case.success_rate,
                    }
                )
        except RuntimeError as e:
            raise RuntimeError(f"Failed to export results to PostgreSQL: {str(e)}") from e
