from typing import List, Tuple

from IPython.core.display import Image
from chosco.media.retriever.domain.media_retriever import MediaRetriever


class WebMediaRetriever(MediaRetriever):
    def __init__(self, max_width: int = 1200):
        self.url = [
            "https://participa.podemos.info/assets/user_verifications/dni-sample1-489cd19dc5c69fc6b386e4da711536cc5579d903f9d80ab84af5d90f56b687fa.png",
            "https://cadenaser00.epimg.net/ser/imagenes/2020/02/06/sociedad/1581019912_200613_1581093640_noticia_normal.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Deutscher_Personalausweis_im_ab_2021_vorgesehenen_Design%2C_Bundesregierung_der_Bundesrepublik_Deutschland%2C_Entwurf_eines_Gesetzes_zur_St%C3%A4rkung_der_Sicherheit_im_Pass-%2C_Ausweis-_und_ausl%C3%A4nderrechtlichen_Dokumentenwesen.jpeg/542px-thumbnail.jpeg",
            "https://www.journalducameroun.com/en/wp-content/uploads/2020/08/Digital-ID-1-780x440.png",
        ]
        self.current_index = None
        self.total_images = len(self.url)
        self.max_width = max_width

    def _increase_index(self):
        if self.current_index is None:
            self.current_index = 0
        else:
            if self.current_index < self.total_images - 1:
                self.current_index += 1

    def _decrease_index(self):
        if self.current_index is None:
            self.current_index = 0
        else:
            if self.current_index >= 1:
                self.current_index -= 1

    def previous_image(self, not_allowed_images: List[str] = None) -> Tuple[str, Image]:
        self._decrease_index()
        url = self.url[self.current_index]
        return url, Image(url, unconfined=True, width=self.max_width)

    def next_image(self, not_allowed_images: List[str] = None) -> Tuple[str, Image]:
        self._increase_index()
        url = self.url[self.current_index]
        return url, Image(url, unconfined=True, width=self.max_width)

    def progress(self) -> str:
        return f"{self.current_index + 1} of {self.total_images}"
