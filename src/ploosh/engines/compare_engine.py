class CompareEngine:

   success_rate = 1
   error_type = None
   error_message = None
   df_compare_gap = None

   df_source = None
   df_expected = None
   options = None
   mode = None

   def compare(self) -> bool:
        return False