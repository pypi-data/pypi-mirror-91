from ipywidgets import Output

from chosco.annotation.domain.annotation import Annotation
from chosco.annotation.domain.annotation_repository import AnnotationRepository
from chosco.media.retriever.domain.media_retriever import MediaRetriever
from chosco.view.interactor.domain.view_interactor import ViewInteractor


class Annotator:
    def __init__(
        self,
        username: str,
        retriever: MediaRetriever,
        repository: AnnotationRepository,
        view_interactor: ViewInteractor,
    ):
        self.username = username
        self.retriever = retriever
        self.repository = repository
        self.view_interactor = view_interactor
        self.current_image_id = None

        def previous_item():
            image_id, image = self.retriever.previous_image()
            self.current_image_id = image_id
            progress = self.retriever.progress()
            progress_max = self.retriever.total_images
            progress_value = self.retriever.current_index + 1
            self.view_interactor.update_header_box(
                image_id, image, progress, progress_max, progress_value
            )

        def next_item():
            image_id, image = self.retriever.next_image()
            self.current_image_id = image_id
            progress = self.retriever.progress()
            progress_max = self.retriever.total_images
            progress_value = self.retriever.current_index + 1
            self.view_interactor.update_header_box(
                image_id, image, progress, progress_max, progress_value
            )

        def confirm_annotation(create_metadata):
            metadata = create_metadata()
            annotation = Annotation(self.current_image_id, metadata)
            self.repository.save(annotation)
            self.repository.show()

        self.view_interactor.set_callbacks(
            {
                "next_item": next_item,
                "previous_item": previous_item,
                "confirm_annotation": confirm_annotation,
            }
        )

    def execute(self, output: Output):
        self.view_interactor.execute(output)
