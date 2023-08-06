import pandas as pd

from ovretl.tasks_utils.so_tasks_filter import so_tasks_filter


def test_so_tasks_filter():
    tasks_df = pd.DataFrame(data={"id": ["1", "2"], "so_id": ["1", None]})
    result_should_be = pd.DataFrame(data={"id": ["1"], "so_id": ["1"]})
    result = so_tasks_filter(tasks_df)
    pd.testing.assert_frame_equal(result, result_should_be)
