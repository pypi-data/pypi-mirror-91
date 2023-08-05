# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, Union, Any

# Pip
import stopit

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

def signal_timeoutable(
    function,
    timeout: Optional[int] = None,
    timeout_param: Optional[str] = None,
    function_name: Optional[str] = None,
    *args,
    **kwargs
) -> Union[stopit.TimeoutException, Any]:
    def wrapper(*args, **kwargs):
        return __run_with_timeout(
            function,
            stopit.SignalTimeout,
            *args,
            **kwargs
        )

    return wrapper

def threading_timeoutable(
    function,
    timeout: Optional[int] = None,
    timeout_param: Optional[str] = None,
    function_name: Optional[str] = None,
    *args,
    **kwargs
) -> Union[stopit.TimeoutException, Any]:
    def wrapper(*args, **kwargs):
        return __run_with_timeout(
            function,
            stopit.ThreadingTimeout,
            *args,
            **kwargs
        )

    return wrapper


# ----------------------------------------------------------- Private methods ------------------------------------------------------------ #

def __run_with_timeout(
    function,
    timeout_function,
    *args,
    **kwargs
) -> Union[stopit.TimeoutException, Any]:
    timeout_param = None

    if 'timeout_param' in kwargs:
        timeout_param = kwargs['timeout_param']
        del kwargs['timeout']

    timeout_param = timeout_param or 'timeout'

    if timeout_param in kwargs:
        timeout = kwargs[timeout_param]
        del kwargs[timeout_param]
    else:
        timeout = None

    if 'function_name' in kwargs:
        function_name = kwargs['function_name']
        del kwargs['function_name']
    else:
        function_name = None

    if timeout and timeout > 0:
        try:
            with timeout_function(timeout, swallow_exc=False):
                return function(*args, **kwargs)
        except stopit.TimeoutException as e:
            return stopit.TimeoutException(
                'Function \'{}\' did exceed maximum timeout value ({} {})'.format(
                    function_name or function.__name__,
                    timeout,
                    'second' if timeout == 1 else 'seconds'
                )
            )
    else:
        return function(*args, **kwargs)


# ---------------------------------------------------------------------------------------------------------------------------------------- #