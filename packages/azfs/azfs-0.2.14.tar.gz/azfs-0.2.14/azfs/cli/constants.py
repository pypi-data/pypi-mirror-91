WELCOME_PROMPT = r"""
    ___         ___________
   /   | ____  / ____/ ___/
  / /| |/_  / / /_   \__ \ 
 / ___ | / /_/ __/  ___/ / 
/_/  |_|/___/_/    /____/  

Welcome AzFS.
"""


MOCK_FUNCTION = """
    try:
        # import required modules
        %s
        @staticmethod
        def %s%s:
            pass
    except NameError as e:
        pass
"""