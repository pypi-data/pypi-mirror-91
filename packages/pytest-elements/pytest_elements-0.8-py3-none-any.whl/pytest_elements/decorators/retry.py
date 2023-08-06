from pytest_elements.helpers.retry import retry


class Retry:
    """
    Class that acts as a function decorator for retrying flaky functions

    attempts: number of attempts

    attempt_delay: time (in seconds) to wait in-between attempts

    allowed_exceptions: a list of specific exception types to ignore while retrying.
                        If left as (), ignore all exceptions.

    usage:

        @Retry(attempts=5, attempt_delay=10, allowed_exceptions=(TimeoutException))
        def do_a_thing():
            this + function = does
            a = thing.that()
            sometimes.raises(an, exception)

    """

    def __init__(
        self, attempts: int = 2, attempt_delay=5, allowed_exceptions: iter = (), timeout: int = 0,
    ):
        self._attempts = attempts
        self._attempt_delay = attempt_delay
        self._allowed_exceptions = set(allowed_exceptions)
        self._timeout = timeout

    def __call__(self, action):
        def wrapped_action(*args, **kwargs):
            return retry(
                action=action,
                action_args=args,
                action_kwargs=kwargs,
                attempts=self._attempts,
                attempt_delay=self._attempt_delay,
                allowed_exceptions=self._allowed_exceptions,
                timeout=self._timeout,
            )

        return wrapped_action
