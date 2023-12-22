import os, uuid, html, shutil
import numpy as np

import pandas as pd
import xml.dom.minidom
from core.miscellaneous import get_parameter_value

def export_test_results(root_directory, settings, all_results):
    export_settings = get_parameter_value(settings, "export", "04x001")
    export_folder = get_parameter_value(export_settings, "folder", "04x002")
    export_clear = get_parameter_value(export_settings, "clear", "04x002", False)
    export_to_trx = get_parameter_value(export_settings, "export_to_trx", "04x002", False)
    export_to_csv = get_parameter_value(export_settings, "export_to_csv", "04x002", False)

    export_folder = os.path.abspath(f"{root_directory}/{export_folder}")

    if export_clear and os.path.exists(export_folder):
        shutil.rmtree(export_folder)

    if export_to_csv:
        export_test_csv(export_folder, all_results)

    if export_to_trx:
        export_test_trx(export_folder, all_results)

def export_test_csv(export_folder, all_results):
    export_folder = f"{export_folder}/csv/"
    export_path = os.path.abspath(f"{export_folder}/summary.csv")

    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    export_data = []
    for result in all_results:
        export_data.append({
            "state": result["state"],
            "error_message": result["error_message"],
            "error_type": result["error_type"],
            "source_duration": result["source_duration"],
            "expected_duration": result["expected_duration"],
            "compare_duration": result["compare_duration"],
        })

    df = pd.DataFrame.from_records(export_data)
    df.to_csv(export_path)

def export_test_trx(export_folder, all_results):
    trx_id = str(uuid.uuid4())

    date_format = "%Y-%m-%dT%H:%M:%SZ"
    export_folder = os.path.abspath(f"{export_folder}/trx")
    export_file_path = os.path.abspath(f"{export_folder}/summary.xml")

    test_list_id = str(uuid.uuid4())

    if not os.path.exists(export_folder):
        os.makedirs(export_folder)

    execution_id_list = []
    test_id_list = []

    for i in list(range(0, len(all_results))):
        execution_id_list.append(str(uuid.uuid4()))
        test_id_list.append(str(uuid.uuid4()))


    xml_unit_test_result = ""
    xml_test_definitions = ""
    xml_test_entry = ""

    count_failed = 0
    count_passed = 0
    count_errors = 0

    start_times = []
    end_times = []
    for i in list(range(0, len(all_results))):
        result = all_results[i]

        start_times.append(result["start_time"])
        end_times.append(result["end_time"])

        test_name = result["test_name"]
        state = result["state"]

        execution_id = execution_id_list[i]
        test_id = test_id_list[i]
        state_time = result["start_time"].strftime(date_format)
        end_time = result["end_time"].strftime(date_format)
        duration = result["source_duration"] + result["expected_duration"] + result["compare_duration"] + result["unknow_duration"]

        match state:
            case "failed":
                count_failed += 1
            case "passed":
                count_passed += 1
            case _:
                count_errors += 1

        output_message_xml = ""
        result_files_xml = ""
        if state != "passed":
            error_message = html.escape(result["error_message"], quote = False)
            execution_id = execution_id_list[i]
            execution_id = execution_id_list[i]
            df_details = result["df_details"]

            output_message_xml = f"<Output><ErrorInfo><Message>{error_message}</Message></ErrorInfo></Output>"

            if df_details is not None:
                detail_path = os.path.abspath(f"{export_folder}/in/{execution_id}")
                detail_file_path = os.path.abspath(f"{detail_path}/{test_name}.xlsx")
                result_files_xml = f"<ResultFiles><ResultFile path='{test_name}.xlsx' comment='test'/></ResultFiles>"

                if not os.path.exists(detail_path):
                    os.makedirs(detail_path)

                df_details.to_excel(detail_file_path)

        xml_unit_test_result += f"<UnitTestResult executionId='{execution_id}' testId='{test_id}' testName='{test_name}' duration='{duration}' startTime='{state_time}' endTime='{end_time}' outcome='{state}' testListId='{test_list_id}'>{output_message_xml}{result_files_xml}</UnitTestResult>"
        xml_test_definitions += f"<UnitTest id='{test_id}' name='{test_name}'><Execution id='{execution_id}'/></UnitTest>"
        xml_test_entry += f"<TestEntry testId='{test_id}' executionId='{execution_id}' testListId='{test_list_id}'/>"

        global_start_date = np.min(np.array(start_times)).strftime(date_format)
        global_end_date = np.max(np.array(end_times)).strftime(date_format)

        number_of_tests = len(all_results)

        xml_string = f"""<?xml version='1.0' encoding='UTF-8'?>
            <TestRun xmlns='http://microsoft.com/schemas/VisualStudio/TeamTest/2010' id='{trx_id}'>
                <Times creation='{global_start_date}' queueing='{global_start_date}' start='{global_start_date}' finish='{global_end_date}' />
                <TestSettings id='{trx_id}'/>
                <Results>{xml_unit_test_result}</Results>
                <TestDefinitions>{xml_test_definitions}</TestDefinitions>
                <TestEntries>{xml_test_entry}</TestEntries>
                <TestLists><TestList id='{test_list_id}' name='All Loaded Results'/></TestLists>
                <ResultSummary outcome='Complete'>
                    <Counters total='{number_of_tests}' executed='{number_of_tests}' passed='{count_passed}' failed='{count_failed}' error='{count_errors}' timeout='0' aborted='0' inconclusive='0' passedButRunAborted='0' notRunnable='0' notExecuted='0' disconnected='0' warning='0' completed='0' inProgress='0' pending='0' />
                    <Output StdOut='' />
                </ResultSummary>
            </TestRun>"""

    with open(export_file_path, "w") as f:
        f.write(xml.dom.minidom.parseString(xml_string).toprettyxml())
        f.close()