from chosco.annotation.application.annotator import Annotator
from chosco.annotation.domain.annotation import Annotation
from chosco.annotation.domain.annotation_repository import AnnotationRepository
from chosco.annotation.infrastructure.inmemory_annotation_repository import (
    InMemoryAnnotationRepository,
)
from chosco.media.retriever.domain.media_retriever import MediaRetriever
from chosco.media.retriever.infrastructure.web_media_retriever import WebMediaRetriever
from chosco.view.interactor.ipywidgets_annotation_view_interactor import (
    IpywidgetsAnnotationViewInteractor,
)
