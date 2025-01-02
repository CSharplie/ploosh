class LoadEngine:
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


    def load(self):
        return None
    
    def execute(self):
        return None
