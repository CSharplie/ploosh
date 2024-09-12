"""Export test case result to TRX format"""

import html
import os
import uuid
import xml.dom.minidom
import numpy as np
from exporters.exporter import Exporter
from case import StateStatistics


class ExporterTRX(Exporter):
    """Export test case result to TRX format"""

    def __init__(self):
        # Set the name of the exporter
        self.name = "TRX"

    def get_failed_blocks(self, case_name, current_case, execution_id, output_folder):
        """Get XML code for failed cases"""
        # Escape the error message to be XML-safe
        error_message = html.escape(current_case.error_message, quote=False)

        # Create the XML block for the error message
        output_message_xml = f"<Output><ErrorInfo><Message>{error_message}</Message></ErrorInfo></Output>"
        result_files_xml = ""

        # If there is a comparison gap, export it to an Excel file
        if current_case.df_compare_gap is not None:
            detail_file_path = f"{output_folder}/test_results/In/{execution_id}/{case_name}.xlsx"
            result_files_xml = f"<ResultFiles><ResultFile path='{case_name}.xlsx'/></ResultFiles>"

            # Create directories if they do not exist
            os.makedirs(os.path.dirname(detail_file_path), exist_ok=True)
            current_case.df_compare_gap.to_excel(detail_file_path)

        return output_message_xml, result_files_xml

    def export(self, cases: dict):
        """Export test case results to a TRX file"""

        # Generate a unique ID for the TRX file
        trx_id = str(uuid.uuid4())

        # Define the output folder and file path
        output_folder = f"{self.output_path}/trx"
        output_file = f"{output_folder}/test_results.xml"

        # Generate a unique ID for the test list
        test_list_id = str(uuid.uuid4())

        # Initialize lists to store execution and test IDs
        execution_id_list = []
        test_id_list = []

        # Generate unique IDs for each test case
        for _ in list(range(0, len(cases))):
            execution_id_list.append(str(uuid.uuid4()))
            test_id_list.append(str(uuid.uuid4()))

        # Initialize XML blocks for unit test results, test definitions, and test entries
        xml_unit_test_result = ""
        xml_test_definitions = ""
        xml_test_entry = ""

        # Initialize state statistics
        state_statistics = StateStatistics()

        # Initialize lists to store start and end times
        start_times = []
        end_times = []

        # Iterate over each test case and collect data
        for i, case_name in enumerate(cases):
            current_case = cases[case_name]

            # Collect start and end times for the test case
            if current_case.global_duration.start is not None:
                start_times.append(current_case.global_duration.start)
                end_times.append(current_case.global_duration.end)

            execution_id = execution_id_list[i]
            test_id = test_id_list[i]

            # Update state statistics
            state_statistics.add_state(current_case.state)

            output_message_xml = ""
            result_files_xml = ""

            # If the test case failed, get the XML blocks for the error message and result files
            if current_case.state != "passed" and current_case.error_message is not None:
                output_message_xml, result_files_xml = self.get_failed_blocks(
                    case_name, current_case, execution_id_list[i], output_folder
                )

            outcome = current_case.state
            if outcome == "error":
                outcome = "failed"

            # Create the XML block for the unit test result
            xml_unit_test_result += f"""<UnitTestResult
                executionId='{execution_id}'
                testId='{test_id}'
                testName='{case_name}'
                duration='{current_case.global_duration.duration}'
                startTime='{Exporter.date_to_string(current_case.global_duration.start)}'
                endTime='{Exporter.date_to_string(current_case.global_duration.end)}'
                outcome='{outcome}'
                testListId='{test_list_id}'>{output_message_xml}{result_files_xml}</UnitTestResult>"""

            # Create the XML block for the test definition
            xml_test_definitions += f"<UnitTest id='{test_id}' name='{case_name}'><Execution id='{execution_id}'/></UnitTest>"

            # Create the XML block for the test entry
            xml_test_entry += f"<TestEntry testId='{test_id}' executionId='{execution_id}' testListId='{test_list_id}'/>"

        # Get the global start and end times
        global_start_date = Exporter.date_to_string(np.min(np.array(start_times)))
        global_end_date = Exporter.date_to_string(np.max(np.array(end_times)))

        # Create the final XML string for the TRX file
        xml_string = f"""<?xml version='1.0' encoding='UTF-8'?>
            <TestRun xmlns='http://microsoft.com/schemas/VisualStudio/TeamTest/2010' id='{trx_id}'>
                <Times creation='{global_start_date}' queueing='{global_start_date}' start='{global_start_date}' finish='{global_end_date}' />
                <TestSettings id='{trx_id}'/>
                <Results>{xml_unit_test_result}</Results>
                <TestDefinitions>{xml_test_definitions}</TestDefinitions>
                <TestEntries>{xml_test_entry}</TestEntries>
                <TestLists><TestList id='{test_list_id}' name='All Loaded Results'/></TestLists>
                <ResultSummary outcome='Complete'>
                    <Counters 
                        total='{state_statistics.total}'
                        executed='{state_statistics.executed}'
                        passed='{state_statistics.passed}'
                        failed='{state_statistics.failed}'
                        error='{state_statistics.error}'
                        notExecuted='{state_statistics.not_executed}' />
                    <Output StdOut='' />
                </ResultSummary>
            </TestRun>"""

        # Create directories if they do not exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Write the XML string to the TRX file
        with open(output_file, "w", encoding="UTF-8") as file:
            dom_string = xml.dom.minidom.parseString(xml_string).toprettyxml()
            dom_string = os.linesep.join([s for s in dom_string.splitlines() if s.strip()])
            file.write(dom_string)
