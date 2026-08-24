"""Sandboxed code execution."""

import sys
from io import StringIO
from typing import Any


class Sandbox:
    """Execute code in a restricted environment."""

    def __init__(self) -> None:
        """Initialize the sandbox."""
        self.allowed_builtins = {
            'abs', 'all', 'any', 'bin', 'bool', 'chr', 'dict', 'dir',
            'divmod', 'enumerate', 'filter', 'float', 'format', 'frozenset',
            'hex', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'list',
            'map', 'max', 'min', 'next', 'oct', 'ord', 'pow', 'print',
            'range', 'reversed', 'round', 'set', 'slice', 'sorted', 'str',
            'sum', 'tuple', 'type', 'zip'
        }

    def execute(self, code: str) -> dict[str, Any]:
        """Execute code in a sandboxed environment."""
        # Capture output
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        result = {
            "success": False,
            "output": "",
            "error": None
        }
        
        try:
            # Create restricted namespace
            safe_builtins = {
                name: __builtins__[name]
                for name in self.allowed_builtins
                if name in __builtins__
            }
            
            namespace = {"__builtins__": safe_builtins}
            
            # Execute in restricted environment
            exec(code, namespace)
            
            result["success"] = True
            result["output"] = captured_output.getvalue()
        
        except Exception as e:
            result["error"] = str(e)
            result["output"] = captured_output.getvalue()
        
        finally:
            sys.stdout = old_stdout
        
        return result

    def evaluate(self, expression: str) -> dict[str, Any]:
        """Evaluate an expression safely."""
        try:
            safe_builtins = {
                name: __builtins__[name]
                for name in self.allowed_builtins
                if name in __builtins__
            }
            
            namespace = {"__builtins__": safe_builtins}
            value = eval(expression, namespace)
            
            return {
                "success": True,
                "value": value
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
