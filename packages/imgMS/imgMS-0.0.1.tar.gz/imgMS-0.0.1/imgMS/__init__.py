
# Let users know if they're missing any of our hard dependencies
from imgMS.side_functions import *
from imgMS import MSData, MSEval
hard_dependencies = ("numpy", "pandas", "matplotlib")
missing_dependencies = []

for dependency in hard_dependencies:
    try:
        __import__(dependency)
    except ImportError as e:
        missing_dependencies.append(f"{dependency}: {e}")

if missing_dependencies:
    raise ImportError(
        "Unable to import required dependencies:\n" +
        "\n".join(missing_dependencies)
    )
del hard_dependencies, dependency, missing_dependencies
