from abc import ABC, abstractmethod
from typing import List, Tuple, Any


class MediaRetriever(ABC):
    def __init__(self, folder: str):
        self.folder = folder

    @abstractmethod
    def previous_image(self, not_allowed_images: List[str] = None) -> Tuple[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def next_image(self, not_allowed_images: List[str] = None) -> Tuple[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def progress(self) -> str:
        raise NotImplementedError
