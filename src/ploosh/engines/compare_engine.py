# pylint: disable=R0903,W0613
""" Base class for the comparison engines """

class CompareEngine:
    """Base class for the comparison engines"""

    success_rate = 1
    error_type = None
    error_message = None
    df_compare_gap = None
    df_source = None
    df_expected = None
    options = None
    mode = None

    def compare(self) -> bool:
        """Compare the source and expected datasets"""
        return False
