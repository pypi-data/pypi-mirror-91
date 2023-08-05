# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Optional, Union, Callable, Any

# Pip
import stopit

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------ Public methods ------------------------------------------------------------ #

def signal_timeoutable(
    name: Optional[str] = None,
    timeout_param: Optional[str] = None
) -> Union[stopit.TimeoutException, Any]:
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            return __run_with_timeout(
                function,
                timeout_function=stopit.SignalTimeout,
                name=name,
                timeout_param=timeout_param,
                *args,
                **kwargs
            )

        return wrapper
    return real_decorator

def threading_timeoutable(
    name: Optional[str] = None,
    timeout_param: Optional[str] = None
) -> Union[stopit.TimeoutException, Any]:
    def real_decorator(function):
        def wrapper(*args, **kwargs):
            return __run_with_timeout(
                function,
                timeout_function=stopit.ThreadingTimeout,
                name=name,
                timeout_param=timeout_param,
                *args,
                **kwargs
            )

        return wrapper
    return real_decorator


# ----------------------------------------------------------- Private methods ------------------------------------------------------------ #

def __run_with_timeout(
    function,
    timeout_function: Callable,
    name: Optional[str] = None,
    timeout_param: Optional[str] = None,
    *args,
    **kwargs
) -> Union[stopit.TimeoutException, Any]:
    timeout_param = timeout_param or 'timeout'

    if timeout_param in kwargs:
        timeout = kwargs[timeout_param]
        del kwargs[timeout_param]
    else:
        timeout = None

    if timeout and timeout > 0:
        try:
            with timeout_function(timeout, swallow_exc=False):
                return function(*args, **kwargs)
        except stopit.TimeoutException as e:
            return stopit.TimeoutException(
                '{} did exceed maximum timeout value ({} {})'.format(
                    '\'{}\''.format(name) or 'Function \'{}\''.format(function.__name__),
                    timeout,
                    'second' if timeout == 1 else 'seconds'
                )
            )
    else:
        return function(*args, **kwargs)


# ---------------------------------------------------------------------------------------------------------------------------------------- #