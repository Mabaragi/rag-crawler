from abc import ABC, abstractmethod


class RawDataCrawlerScheduleRepository(ABC):
    @abstractmethod
    def add_schedule(self, schedule: dict) -> None:
        pass

    @abstractmethod
    def get_schedules(self) -> list[dict]:
        pass

    # @abstractmethod
    # def clear_schedules(self) -> None:
    #     pass
