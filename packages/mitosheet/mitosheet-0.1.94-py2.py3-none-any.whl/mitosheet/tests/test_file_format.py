#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Mito.
# Distributed under the terms of the Modified BSD License.

"""
Contains tests for edit events.
"""
from typing import List

from mitosheet.steps import ADD_COLUMN_STEP, STEPS
from mitosheet.steps import DELETE_COLUMN_STEP
from mitosheet.steps import RENAME_COLUMN_STEP
from mitosheet.steps import FILTER_STEP
from mitosheet.steps import PIVOT_STEP
from mitosheet.steps import MERGE_STEP
from mitosheet.steps import REORDER_COLUMN_STEP
from mitosheet.steps import SET_COLUMN_FORMULA_STEP
from mitosheet.steps import SORT_STEP
from mitosheet.steps.import_steps.simple_import import SIMPLE_IMPORT_STEP
from mitosheet.steps.import_steps.raw_python_import import RAW_PYTHON_IMPORT_STEP
from mitosheet.steps.dataframe_steps.dataframe_delete import DATAFRAME_DELETE_STEP
from mitosheet.steps.dataframe_steps.dataframe_duplicate import DATAFRAME_DUPLICATE_STEP
from mitosheet.steps.dataframe_steps.dataframe_rename import DATAFRAME_RENAME_STEP


def check_step(
        step_definition, 
        step_version: int, 
        step_type: str, 
        params: List[str],
        has_saturate: bool
    ):
    """
    Helper function that checks a given step definition against the 
    expected step_version, step_type, and params for that step. 

    Throws an assertion error if any of them do not match! 
    """
    assert step_definition['step_version'] == step_version
    assert step_definition['step_type'] == step_type
    assert step_definition['params'] == params
    assert (not has_saturate or step_definition['saturate'] is not None)

def test_params_static():
    """
    NOTE: This is a regression test! Before changing this test to make it pass, talk to 
    the engineering team and make sure you know what you're doing. 

    Remeber:
    1. Each Mito analysis is written to a file, where each step is saved with its
       parameters.
    2. If the _name_ of the step, or the _parameters to the step_ change, then this
       will break existing user analyses. 
    
    Thus, this test is to make sure that we _know_ when we're breaking things. 
    
    However, note that there are ways to break existing user analyses other than this. 
    For example, if you change how the group step flattens headers, this may cause
    issues if the user then later renames one of those flattened columns. So, this
    regression test is not perfect, but it is a good start!
    """

    check_step(
        ADD_COLUMN_STEP,
        1,
        'add_column',
        ['sheet_index', 'column_header'],
        False
    )

    check_step(
        DELETE_COLUMN_STEP,
        1,
        'delete_column',
        ['sheet_index', 'column_header'],
        False
    )

    check_step(
        RENAME_COLUMN_STEP,
        1,
        'rename_column',
        ['sheet_index', 'old_column_header', 'new_column_header'],
        False
    )

    check_step(
        FILTER_STEP,
        1,
        'filter_column',
        ['sheet_index', 'column_header', 'operator', 'filters'],
        # TODO: this param "filters" is really weakly typed here, and could totally
        # change without being detected by this test. Boo!
        False
    )
    
    check_step(
        PIVOT_STEP,
        2,
        'pivot',
        ['sheet_index', 'pivot_rows', 'pivot_columns', 'values'],
        # TODO: the param "values" is also very weakly typed, and could change
        # without this test detecting it
        False
    )

    check_step(
        MERGE_STEP,
        1,
        'merge',
        ['sheet_index_one', 'merge_key_one', 'selected_columns_one', 'sheet_index_two', 'merge_key_two', 'selected_columns_two'],
        False
    )

    check_step(
        REORDER_COLUMN_STEP,
        1,
        'reorder_column',
        ['sheet_index', 'column_header', 'new_column_index'],
        False
    )

    check_step(
        SET_COLUMN_FORMULA_STEP,
        1,
        'set_column_formula',
        ['sheet_index', 'column_header', 'old_formula', 'new_formula'],
        True
    )

    check_step(
        SORT_STEP,
        1,
        'sort',
        ['sheet_index', 'column_header', 'sort_direction'],
        False
    )

    check_step(
        SIMPLE_IMPORT_STEP,
        1,
        'simple_import',
        ['file_names'],
        False
    )

    check_step(
        DATAFRAME_DELETE_STEP,
        1,
        'dataframe_delete',
        ['sheet_index', 'old_dataframe_name'],
        True
    )

    check_step(
        DATAFRAME_DUPLICATE_STEP,
        1,
        'dataframe_duplicate',
        ['sheet_index'],
        False
    )

    check_step(
        DATAFRAME_RENAME_STEP,
        1,
        'dataframe_rename',
        ['sheet_index', 'old_dataframe_name', 'new_dataframe_name'],
        True
    )

    assert len(STEPS) == 14



