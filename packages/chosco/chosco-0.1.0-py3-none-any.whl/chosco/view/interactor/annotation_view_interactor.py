import functools
from typing import Dict, Callable
from ipywidgets import Button, IntProgress, Label, Layout, Box, Output, Image, Accordion
from IPython.core.display import display

from chosco.view.interactor.domain.metadata_formatter import MetadataFormatter
from chosco.annotation.domain.annotation_task_status import AnnotationTaskStatus
from chosco.view.interactor.domain.view_interactor import ViewInteractor


class AnnotationViewInteractor(ViewInteractor):
    def __init__(self, annotations_box: Box, username: str = None):
        self.annotations_box = annotations_box
        self.row_layout = Layout(flex_flow="row", align_items="center", width="100%")
        self.column_layout = Layout(
            flex_flow="column", align_items="center", width="100%"
        )
        self.default_annotation_correspondences = MetadataFormatter.from_box(
            self.annotations_box
        )
        self.username = username

    def set_callbacks(self, callbacks: Dict[str, Callable]):
        self.callbacks = callbacks

    def _create_controller_box(self, output):
        previous_button = Button(description="Previous", button_style="info")
        next_button = Button(description="Next", button_style="info")
        self.progress = IntProgress()
        clear_button = Button(description="Clear", button_style="danger")
        confirm_button = Button(description="Confirm")
        confirm_button.style.button_color = "lightgreen"
        self.item_id = Label("Click on Next to start the labeling")

        controller_box = Box(
            children=[
                previous_button,
                next_button,
                self.progress,
                clear_button,
                confirm_button,
            ],
            layout=Layout(
                display="flex", flex_flow="row", align_items="center", width="100%"
            ),
            border="solid",
        )
        info_box = Box(children=[self.item_id], layout=self.row_layout)
        controller_box_with_info = Box(
            children=[controller_box, info_box], layout=self.column_layout
        )

        # Controller Buttons
        @output.capture(clear_output=True, wait=True)
        def update(b, callback):
            current_metadata = MetadataFormatter.from_box(self.annotations_box)
            if current_metadata == self.default_annotation_correspondences:
                self.item_id.value = "Please, annotate the following id before moving forward (or backward)"
            else:
                callback()

        previous_button.on_click(
            functools.partial(update, callback=self.callbacks.get("previous_item"))
        )
        next_button.on_click(
            functools.partial(update, callback=self.callbacks.get("next_item"))
        )

        # Confirm Button
        def create_metadata() -> Dict:
            return MetadataFormatter.from_box(self.annotations_box)

        @output.capture(clear_output=False, wait=True)
        def update(b, callback, create_metadata):
            callback(create_metadata)

        confirm_button.on_click(
            functools.partial(
                update,
                callback=self.callbacks.get("confirm_annotation"),
                create_metadata=create_metadata,
            )
        )

        # Clear Button
        @output.capture(clear_output=False, wait=True)
        def clear(b):
            self.clear_annotation_box()

        clear_button.on_click(clear)

        return controller_box_with_info

    def execute(self, output: Output):
        self.output = output
        controller_box = self._create_controller_box(output)

        controller_fancy_box = Box(
            children=[controller_box],
            layout=Layout(
                display="flex", flex_flow="row", align_items="center", width="100%"
            ),
            border="solid",
        )

        annotation_fancy_box = Box(
            children=[self.annotations_box],
            layout=Layout(
                display="flex", flex_flow="column", align_items="center", width="100%"
            ),
            border="solid",
        )

        top_box = Box(
            children=[
                Label("Controls"),
                controller_fancy_box,
                Label("Annotations"),
                annotation_fancy_box,
            ],
            layout=Layout(flex_flow="column", align_items="center", width="100%"),
        )

        main_layout = Layout(flex_flow="column", width="100%")
        main_box = Box(children=[top_box, output], layout=main_layout)

        labeler_accordion = Accordion([main_box])
        labeler_accordion.set_title(0, f"Hello {self.username}!")

        # display(headers_box)
        display(labeler_accordion)

    def update_header_box(
        self, image_id: str, image: Image, status: AnnotationTaskStatus
    ):

        self.progress.description = status.get_progress()
        self.progress.max = status.total_annotations
        self.progress.value = status.number_of_annotations + 1
        self.item_id.value = f"Waiting for annotation: {image_id}"
        with self.output:
            display(image)

    def update_annotation_box_with_correspondence(self, correspondences):
        def update_box(box, correspondences):
            if (
                hasattr(box, "description")
                and hasattr(box, "value")
                and not isinstance(box, Label)
            ):
                key = box.description.lower().replace(" ", "_")
                try:
                    box.value = correspondences.get(key, False)
                except:  # noqa
                    pass
            else:
                if hasattr(box, "children"):
                    for children_box in box.children:
                        update_box(children_box, correspondences)

        if self.annotations_box:
            update_box(self.annotations_box, correspondences)

    def clear_annotation_box(self):
        self.update_annotation_box_with_correspondence(
            self.default_annotation_correspondences
        )

    def update_annotation_box(self, metadata: dict):
        self.update_annotation_box_with_correspondence(metadata)
