"""Code execution engine."""

import sys
from io import StringIO
from typing import Any


class Executor:
    """Execute Python code and capture results."""

    def execute(self, code: str, timeout: int = 5) -> dict[str, Any]:
        """Execute Python code and return results."""
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        result = {
            "success": False,
            "output": "",
            "error": None,
            "return_value": None
        }
        
        try:
            # Create a namespace for execution
            namespace = {}
            
            # Execute the code
            exec(code, namespace)
            
            result["success"] = True
            result["output"] = captured_output.getvalue()
            
            # Try to get a return value if there's a main() function
            if 'main' in namespace:
                result["return_value"] = namespace['main']()
            
        except Exception as e:
            result["error"] = str(e)
            result["output"] = captured_output.getvalue()
        
        finally:
            sys.stdout = old_stdout
        
        return result

    def execute_function(self, code: str, function_name: str, *args: Any, **kwargs: Any) -> dict[str, Any]:
        """Execute a specific function from code."""
        namespace = {}
        
        try:
            exec(code, namespace)
            
            if function_name not in namespace:
                return {
                    "success": False,
                    "error": f"Function '{function_name}' not found"
                }
            
            func = namespace[function_name]
            result = func(*args, **kwargs)
            
            return {
                "success": True,
                "return_value": result
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
