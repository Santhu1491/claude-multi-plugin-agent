"""Base plugin contract."""

from abc import ABC, abstractmethod


class BasePlugin(ABC):
    @abstractmethod
    def execute(self, request: dict) -> dict:
        raise NotImplementedError
