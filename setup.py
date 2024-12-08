import venv
import sys
import os

def create_venv(venv_path, with_pip=True):
    """
    Create a virtual environment at the specified path
    
    Parameters:
        venv_path: str - Path where virtual environment should be created
        with_pip: bool - Whether to include pip in the virtual environment
    """
    # Create virtual environment
    builder = venv.EnvBuilder(
        system_site_packages=False,  # Don't include system site-packages
        clear=True,                  # Clear the directory if it exists
        with_pip=with_pip,          # Include pip
        upgrade_deps=True,           # Upgrade core dependencies (pip, setuptools)
        symlinks=True               # Use symlinks instead of copying files
    )
    
    # Build the virtual environment
    builder.create(venv_path)

# Example usage
if __name__ == "__main__":
    venv_name = "ner-venv"
    venv_path = os.path.join(os.getcwd(), venv_name)
    create_venv(venv_path)
    print(f"Virtual environment created at: {venv_path}")