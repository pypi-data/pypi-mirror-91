from abc import ABC, abstractmethod
from typing import List, Any


class MediaRepository(ABC):
    @abstractmethod
    def retrieve_all_ids(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def retrieve(self, media_id: str, width: int = None) -> Any:
        raise NotImplementedError
