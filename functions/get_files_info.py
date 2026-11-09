import os

#=================================================================================#

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
            "required": ["directory"],
        },
    },
}

#=================================================================================#

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs # returns bool
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        try:
            contents = os.listdir(target_dir)
            contents_org: list = []
            for i in contents:
                fullpath = os.path.join(target_dir, i)
                name = i
                size = os.path.getsize(fullpath)
                isdir = os.path.isdir(fullpath)
                contents_org.append(f"- {name}: file_size={size} bytes, is_dir={isdir}")
            return "\n".join(contents_org)
        except Exception as e:
            return f"Error: {e}"
    except Exception as e:
        return f"Error: {e}"
