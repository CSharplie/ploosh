# pylint: disable=R0903,W0613
"""Base class for all load engines"""

class LoadEngine:
    """Base class for all load engines"""

    count = None
    configuration = None
    options = None
    connection = None
    df_data = None

    def get_insensitive_item(self, name: str, items: list) -> str:
        """Get item from list case-insensitively"""
        for item in items:
            if name.upper().strip() == item.upper().strip():
                return item
        return name

    def execute(self):
        """Execute the load engine"""
        return None
