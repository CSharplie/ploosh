"""Export test case result to TRX format"""

import dataclasses
import html
import os
import uuid
import xml.dom.minidom
import numpy as np
from exporters.exporter import Exporter

@dataclasses.dataclass
class StateCounter:
    """Store number of states occurence"""
    count_failed = 0
    count_passed = 0
    count_errors = 0

    def add_state(self, state):
        """Add new state in the object"""
        match state:
            case "failed":
                self.count_failed += 1
            case "passed":
                self.count_passed += 1
            case _:
                self.count_errors += 1

class ExporterTRX(Exporter):
    """Export test case result to TRX format"""

    def __init__(self):
        self.name = "TRX"

    def get_failed_blocks(self, case_name, current_case, execution_id, output_folder):
        """Get XML code for failed cases"""
        error_message = html.escape(current_case.error_message, quote = False)

        output_message_xml = f"<Output><ErrorInfo><Message>{error_message}</Message></ErrorInfo></Output>"
        result_files_xml = ""
        
        if current_case.df_compare_gap is not None:
            detail_path = os.path.abspath(f"{output_folder}/in/{execution_id}")
            detail_file_path = os.path.abspath(f"{detail_path}/{case_name}.xlsx")
            result_files_xml = f"<ResultFiles><ResultFile path='{case_name}.xlsx' comment='test'/></ResultFiles>"

            if not os.path.exists(detail_path):
                os.makedirs(detail_path)

            current_case.df_compare_gap.to_excel(detail_file_path)

        return output_message_xml, result_files_xml


    def export(self, cases:dict):
        """Export test case"""

        trx_id = str(uuid.uuid4())

        output_folder = f"{self.output_path}/trx"
        output_file = f"{output_folder}/test_results.xml"

        test_list_id = str(uuid.uuid4())

        execution_id_list = []
        test_id_list = []

        for i in list(range(0, len(cases))):
            execution_id_list.append(str(uuid.uuid4()))
            test_id_list.append(str(uuid.uuid4()))


        xml_unit_test_result = ""
        xml_test_definitions = ""
        xml_test_entry = ""

        state_counter = StateCounter()

        start_times = []
        end_times = []
        for i, case_name in enumerate(cases):
            current_case = cases[case_name]

            start_times.append(current_case.global_duration.start)
            end_times.append(current_case.global_duration.end)

            execution_id = execution_id_list[i]
            test_id = test_id_list[i]

            state_counter.add_state(current_case.state)

            output_message_xml = ""
            result_files_xml = ""

            if current_case.state != "passed":
                output_message_xml, result_files_xml = self.get_failed_blocks(case_name, current_case, execution_id_list[i], output_folder)

            xml_unit_test_result += f"""<UnitTestResult
                executionId='{execution_id}'
                testId='{test_id}'
                testName='{case_name}'
                duration='{current_case.global_duration.duration}'
                startTime='{Exporter.date_to_string(current_case.global_duration.start)}'
                endTime='{Exporter.date_to_string(current_case.global_duration.end)}'
                outcome='{current_case.state}'
                testListId='{test_list_id}'>{output_message_xml}{result_files_xml}</UnitTestResult>"""

            xml_test_definitions += f"<UnitTest id='{test_id}' name='{case_name}'><Execution id='{execution_id}'/></UnitTest>"
            xml_test_entry += f"<TestEntry testId='{test_id}' executionId='{execution_id}' testListId='{test_list_id}'/>"

            global_start_date = Exporter.date_to_string(np.min(np.array(start_times)))
            global_end_date = Exporter.date_to_string(np.max(np.array(end_times)))

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
                        total='{len(cases)}'
                        executed='{len(cases)}'
                        passed='{state_counter.count_passed}'
                        failed='{state_counter.count_failed}'
                        error='{state_counter.count_errors}'
                        timeout='0'
                        aborted='0'
                        inconclusive='0'
                        passedButRunAborted='0'
                        notRunnable='0'
                        notExecuted='0'
                        disconnected='0'
                        warning='0'
                        completed='0'
                        inProgress='0'
                        pending='0' />
                    <Output StdOut='' />
                </ResultSummary>
            </TestRun>"""

        with open(output_file, "w", encoding="UTF-8") as file:
            dom_string = xml.dom.minidom.parseString(xml_string).toprettyxml()
            dom_string = os.linesep.join([s for s in dom_string.splitlines() if s.strip()])
            file.write(dom_string)