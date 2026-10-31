import os
import subprocess
def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs,file_path))

        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_dir):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_dir]
        if args != None:
            command.extend(args)

        subpro = subprocess.run(command, timeout=30, text=True, capture_output=True)
        
        out_str = ""
        if subpro.returncode != 0:
            out_str += f"Process exited with code {subpro.returncode}"

        if not subpro.stdout and not subpro.stderr:
            out_str += "\nNo output produced"
        elif subpro.stdout:
            out_str += f"\nSTDOUT: {subpro.stdout}"
        elif subpro.stderr:
            out_str += f"\nSTDERR: {subpro.stderr}"

        return out_str
        

    except Exception as e:
        return f"Error: {e}"