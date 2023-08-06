# --------------------------------------------------------------- Imports ---------------------------------------------------------------- #

# System
from typing import Callable, Optional, Union
import time
from datetime import datetime

# Pip
from colored_logs.logger import Logger
from kcu import ktime
import stopit

# ---------------------------------------------------------------------------------------------------------------------------------------- #



# ----------------------------------------------------------- class: DailyTask ----------------------------------------------------------- #

class DailyTask:

    # -------------------------------------------------------- Public methods -------------------------------------------------------- #

    @classmethod
    def do_daily_task(
        cls,
        start_time: str,
        stop_time: str,
        function: Callable,
        utc: bool = True,
        *args,
        **kwargs
    ):
        start_s = ktime.time_str_to_seconds(start_time)
        stop_s = ktime.time_str_to_seconds(stop_time)

        try:
            while True:
                cls.__sleep_till_start(start_s, stop_s, utc=utc)
                cls.__wrapper_func(function=function, __timeout=ktime.seconds_till(stop_s, utc=utc), *args, **kwargs)
                cls.__sleep_till_start(start_s, stop_s, utc=utc, force=True)
        except KeyboardInterrupt:
            exit(0)


    # ------------------------------------------------------- Private methods -------------------------------------------------------- #

    @classmethod
    def __sleep_till_start(
        cls,
        start_s: float,
        stop_s: float,
        utc: bool,
        force: bool = False
    ) -> None:
        log = Logger()
        started = False
        stop_time_str = ktime.seconds_to_time_str(stop_s)

        try:
            while not ktime.is_between_seconds(start_s, stop_s, utc=utc) or force:
                if not started:
                    started = True
                    log.start_process(
                        'Sleeping ~ {} hours till {}'.format(
                            round(ktime.seconds_till(start_s, utc=utc)/ktime.seconds_in_hour),
                            stop_time_str
                        )
                    )

                time.sleep(1)

            log.stop_process()
        except KeyboardInterrupt:
            log.stop_process()

            raise# KeyboardInterrupt

    @staticmethod
    @stopit.signal_timeoutable(default=Exception('Operation has timed out.'), timeout_param='__timeout')
    def __wrapper_func(
        function: Callable,
        *args,
        __timeout: Optional[int] = None,
        **kwargs,
    ) -> Optional:
        try:
            return function(*args, **kwargs)
        except Exception as e:
            print(e)

        return None


# ---------------------------------------------------------------------------------------------------------------------------------------- #