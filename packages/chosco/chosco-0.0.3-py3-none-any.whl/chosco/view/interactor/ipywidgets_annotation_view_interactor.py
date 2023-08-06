import functools
from typing import Dict, Callable, List
from ipywidgets import (
    Button,
    IntProgress,
    Label,
    Layout,
    Box,
    Output,
    Image,
    Tab,
    CoreWidget,
)
from IPython.core.display import display

from chosco.view.interactor.domain.view_interactor import ViewInteractor


class IpywidgetsAnnotationViewInteractor(ViewInteractor):
    def __init__(self, widgets: List[CoreWidget]):
        self.widgets = widgets
        self.row_layout = Layout(
            display="flex", flex_flow="row", align_items="center", width="100%"
        )
        self.column_layout = Layout(
            display="flex", flex_flow="column", align_items="stretch", width="100%"
        )

    def set_callbacks(self, callbacks: Dict[str, Callable]):
        self.callbacks = callbacks

    def _create_headers_box(self, output):
        previous_button = Button(description="Previous")
        next_button = Button(description="Next")
        self.progress = IntProgress()
        self.item_id = Label("Click on Next to start the labeling")
        controller_box = Box(
            children=[previous_button, next_button, self.progress],
            layout=self.row_layout,
        )
        info_box = Box(children=[self.item_id], layout=self.row_layout)
        headers_box = Box(
            children=[controller_box, info_box], layout=self.column_layout
        )

        @output.capture(clear_output=True, wait=True)
        def update(b, callback):
            callback()

        previous_button.on_click(
            functools.partial(update, callback=self.callbacks.get("previous_item"))
        )
        next_button.on_click(
            functools.partial(update, callback=self.callbacks.get("next_item"))
        )

        return headers_box

    def _create_labeler_box(self, output):
        confirm_button = Button(description="Confirm")
        self.widgets.append(confirm_button)
        create_labeler_box = Box(children=self.widgets, layout=self.column_layout)

        def create_metadata() -> Dict:
            metadata = {}
            for widget in self.widgets:
                if isinstance(widget, Button):
                    continue
                metadata[widget.description] = widget.value
            return metadata

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
        return create_labeler_box

    def execute(self, output: Output):
        self.output = output
        headers_box = self._create_headers_box(output)
        labeler_box = self._create_labeler_box(output)

        main_layout = Layout(flex_flow="column", width="100%")
        main_box = Box(children=[labeler_box, output], layout=main_layout)

        labeler_tab = Tab([main_box])
        labeler_tab.set_title(0, "Annotator")

        display(headers_box)
        display(labeler_tab)

    def update_header_box(
        self,
        image_id: str,
        image: Image,
        progress: str,
        progress_max: int,
        progress_value: int,
    ):

        self.progress.description = progress
        self.progress.max = progress_max
        self.progress.value = progress_value
        self.item_id.value = image_id
        with self.output:
            display(image)
