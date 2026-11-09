import os

#=================================================================================#

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Write to a file within the working directory, creating any missing directories to the file path",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write files to, relative to the working directory (default is the working directory itself)"
                },
                "content": {
                    "type": "string",
                    "description": "Text to be written to the file"
                },
            },
            "required": ["file_path", "content"],
        },
    },
}

#=================================================================================#

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs # returns bool
        if not valid_target_dir:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_dir):
            return f'Error: "Cannot write to {file_path}" as it is a directory'
        parents = os.path.dirname(target_dir)
        os.makedirs(parents, exist_ok=True)
        with open(target_dir, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
