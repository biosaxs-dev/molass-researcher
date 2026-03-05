"""
Shared utilities for molass-researcher experiments.
"""

import numpy as np
import matplotlib.pyplot as plt


def set_data_root(path: str) -> None:
    """Call at the top of each notebook to set the data root path."""
    import os
    os.environ["MOLASS_RESEARCHER_DATA_ROOT"] = path


def get_data_root() -> str:
    import os
    root = os.environ.get("MOLASS_RESEARCHER_DATA_ROOT", "")
    if not root:
        raise EnvironmentError(
            "DATA_ROOT not set. Call set_data_root(path) at the top of your notebook."
        )
    return root
