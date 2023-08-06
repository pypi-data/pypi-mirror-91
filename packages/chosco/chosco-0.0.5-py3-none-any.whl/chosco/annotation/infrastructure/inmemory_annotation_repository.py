import json

from chosco.annotation.domain.annotation import Annotation
from chosco.annotation.domain.annotation_repository import AnnotationRepository


class InMemoryAnnotationRepository(AnnotationRepository):
    def __init__(self):
        self.items = {}

    def save(self, annotation: Annotation):
        self.items[annotation.id] = annotation.metadata

    def show(self):
        print(json.dumps(self.items, indent=4))
