#!/usr/bin/env python3
import os
from typing import Union, Optional

import pandas as pd
from pandas import DataFrame


def blacklist(
    path: str,
    column: int = 1,
    blacklist_column: int = 0,
    header: Optional[Union[int, list[int]]] = None,
    **pd_read_excel_kwargs
) -> pd.DataFrame:
    """Find all values from :code:`column` not in :code:`blacklist_column`.

    Args:
        path: Path to file.
        column: Column number from which to take values.
        blacklist_column: Column number to use as blacklist_column.
        header: Indicates header row(s) to ignore.

    Returns:
        The blacklisted column.
    """
    df: DataFrame = pd.read_excel(path, header=header, **pd_read_excel_kwargs)
    filtered: DataFrame = df[
        ~df.iloc[:, column].isin(df.iloc[:, blacklist_column])
    ].iloc[:, [column]]
    filtered.columns = [0]
    return filtered.reset_index(drop=True).sort_index()


def _derive_output_path(input_path: str) -> str:
    return os.path.join(
        os.path.dirname(input_path), "filtered_" + os.path.basename(input_path)
    )


def filter_file(
    input_path: str, column: int = 1, blacklist_column: int = 0, output_path: str = None
):
    """Apply :meth:`blacklist` to `input_path` and save the output.

    Args:
        input_path: Path to file with the first two columns poetry.
        column: Column number from which to take values.
        blacklist_column: Column number to use as blacklist_column.
        output_path: Path to save output (:code:`"filtered_{input_filename}"`
            if not specified).
    """
    if output_path is None:
        output_path = _derive_output_path(input_path)
    out: DataFrame = blacklist(input_path, column, blacklist_column)
    out.to_excel(output_path, index=False, header=False)
