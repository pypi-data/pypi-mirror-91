import time
import datetime
from selenium.common.exceptions import TimeoutException
from typing import List, Dict, Any, Type


def retry(
    action,
    action_args: List[Any] = [],
    action_kwargs: Dict[str, Any] = {},
    attempts: int = 2,
    attempt_delay=5,
    allowed_exceptions: List[Type[Exception]] = [],
    timeout=0,
):
    """
    A wrapper function that attempts to execute a given action
    'attempts' times with supplied args and kwargs.

    See also: decorators.retry

    :param action: the action to execute

    :param action_args: positional arguments passed to the action on execution

    :param action_kwargs: keyword arguments passed to the action on execution

    :param attempts: number of attempts

    :param attempt_delay: time (in seconds) to wait in-between attempts

    :param allowed_exceptions: a list of specific exception types to ignore while retrying.
                               If left as (), ignore all exceptions.
                               If supplied, raise non-allowed exceptions

    :param timeout: Maximum number of seconds to retry the action for.

    """
    allowed_exceptions = list(set(allowed_exceptions))
    if type(action_kwargs) == tuple:
        action_kwargs = {}
    start_time = datetime.datetime.now()
    for i in range(attempts - 1):
        if timeout and datetime.datetime.now() - start_time > datetime.timedelta(seconds=timeout):
            raise TimeoutException(f"Action was not completed successfully after {timeout} seconds, giving up.")
        debug = (
            f"In {action.__name__}\n"
            f"Attempt {i + 1}/{attempts} at "
            f"{datetime.datetime.now().strftime('%H:%M:%S, %m/%d/%Y')}"
        )
        try:
            return action(*action_args, **action_kwargs)
        except Exception as e:
            if any(allowed_exceptions) and e.__class__ not in allowed_exceptions:
                print(f"\n\nCaught unexpected exception type: {e.__class__} \n{debug}\n")
                raise e
            else:
                print(f"\n\nCaught allowed exception type: {e.__class__} \n{debug}\n")
                time.sleep(attempt_delay)
    return action(*action_args, **action_kwargs)
