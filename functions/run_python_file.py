import os
import subprocess

#=================================================================================#

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file within the working directory and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path for the python file to run, relative to the working directory (default is the working directory itself)"
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional list of arguments to pass to the Python script",
                },
            },
            "required": ["file_path"],
        },
    },
}

#=================================================================================#

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs # returns bool
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_dir.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_dir]
        if args != None:
            command.extend(args)
        result = subprocess.run(command, cwd=working_directory, capture_output=True, text=True, check=False, timeout=30)
        returnstring = ""
        if result.returncode != 0:
            returnstring += f"Process exited with code {result.returncode}"
        if not result.stdout and not result.stderr:
            returnstring += "\nNo output produced"
        if result.stdout:
            returnstring += f"\nSTDOUT: {result.stdout}"
        if result.stderr:
            returnstring += f"\nSTDERR: {result.stderr}"
        return returnstring

    except Exception as e:
        return f"Error: {e}"
