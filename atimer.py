from threading import Thread
from time import sleep


class AsyncCountdownTimer(Thread):
    """
    异步倒计时定时器。使用给定的倒计时量和反馈事件初始化，调用start方法开始计时。
    若时间到，则调用给定的反馈事件。在定时器触发前，可以调用reset方法停止计时并复位。
    时间到且反馈事件被触发前，定时器将自动复位。
    """

    def __init__(self, seconds, callback, **kwargs):
        super().__init__()
        self.__seconds = seconds
        self.__callback = callback
        self.__kwargs = kwargs
        self.__run = True

    def start(self) -> None:
        """
        启动定时器。
        """
        super().start()

    def run(self) -> None:
        __in = 0.25
        counter = self.__seconds
        self.__run = True
        while counter > 0:
            counter -= __in
            sleep(__in)
            if not self.__run:  # 定时器被复位
                return
        if not self.__run:
            return
        self.__callback(**self.__kwargs)

    def reset(self):
        """
        停止计时、复位定时器。若定时器已触发，则无任何效果。
        """
        self.__run = False
