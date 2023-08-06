from abc import ABC, abstractmethod
from typing import Tuple, Any

from chosco.annotation.domain.annotation_task_status import AnnotationTaskStatus


class MediaRetriever(ABC):
    @abstractmethod
    def previous_media(self) -> Tuple[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def next_media(self) -> Tuple[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def confirm(self, media_id: str) -> Tuple[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> AnnotationTaskStatus:
        raise NotImplementedError
