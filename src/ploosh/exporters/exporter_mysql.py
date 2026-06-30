from exporters.exporter import Exporter

class ExporterMySQL(Exporter):
    """Export test case result to MySQL database"""

    CREATE_TABLE_QUERY = """
        CREATE TABLE IF NOT EXISTS ploosh_results (
            execution_id VARCHAR(255),
            name VARCHAR(255),
            state VARCHAR(50),
            source_start DATETIME,
            source_end DATETIME,
            source_duration FLOAT,
            source_count BIGINT,
            source_executed_action VARCHAR(255),
            expected_start DATETIME,
            expected_end DATETIME,
            expected_duration FLOAT,
            expected_count BIGINT,
            expected_executed_action VARCHAR(255),
            compare_start DATETIME,
            compare_end DATETIME,
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
        self.name = "MYSQL"

    def export(self, cases: dict, execution_id: str):
        """Export test case results to a MySQL database"""

        self.connector.execute_query(self.CREATE_TABLE_QUERY, connection=self.connection)

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
