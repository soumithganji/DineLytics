# Cached REPL instance — avoids re-creating a subprocess on every call
_repl = None

def _get_repl():
    global _repl
    if _repl is None:
        from langchain_experimental.utilities import PythonREPL
        _repl = PythonREPL()
    return _repl