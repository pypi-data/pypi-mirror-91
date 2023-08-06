"""
Testing module for
"""
import pytest
import uuid
from datetime import datetime


def test_get_summary_invalid_time_zone(client):
    """Tests that an exception is raised if an invalid time zone is passed to get_summary"""
    start = datetime(2020, 12, 14)
    end = datetime(2020, 12, 14)
    tz = 'THIS AINT IT CHIEF'
    with pytest.raises(KeyError):
        client.task.get_completed(start, end, tz=tz)


def test_get_summary_single_day_good_return(client):
    """Tests that on good inputs for a single day get_summary values are returned"""
    # start = datetime.today()
    # task_name = str(uuid.uuid4())
    # task = client.task.create(task_name, start=datetime(2033, 12, 14))
    # task_complete = client.task.complete(task['id'])
    # tasks = client.task.get_completed(start)
    # found = False
    # for t in tasks:
    #     if task_name == t['title']:
    #         found = True
    #         obj = t
    # assert found
    # obj['status'] = 0
    # new = client.task.update(obj)
    # client.task.delete(new['id'])


def test_get_summary_single_day_full_day_false(client):
    """Tests that input still works for a single day even when full_day is false"""
    start = datetime(2020, 12, 14, 8)
    tasks = client.task.get_completed(start, full=False)
    assert tasks[0] != ''


def test_get_summary_multi_day_full_good_return(client):
    """Tests that a multi day range returns a value"""
    start = datetime(2020, 12, 10)
    end = datetime(2020, 12, 14)
    tasks = client.task.get_completed(start, end)
    assert tasks[0] != ''


def test_get_summary_multi_day_not_full_day_good_return(client):
    """Tests that multi day with full_day=false returns a value"""
    start = datetime(2020, 12, 10, 12, 5, 6)
    end = datetime(2020, 12, 14, 12, 5, 6)
    tasks = client.task.get_completed(start, end, full=False)
    assert tasks[0] != ''


def test_get_summary_multi_day_good_return(client):
    """Tests that multi day works normally"""
    start = datetime(2020, 12, 10)
    end = datetime(2020, 12, 14)
    tasks = client.task.get_completed(start, end)
    assert tasks[0] != ''


def test_get_summary_bad_start_and_end(client):
    start = datetime(2020, 11, 14)
    end = datetime(2020, 11, 10)
    with pytest.raises(ValueError):
        client.task.get_completed(start, end)
