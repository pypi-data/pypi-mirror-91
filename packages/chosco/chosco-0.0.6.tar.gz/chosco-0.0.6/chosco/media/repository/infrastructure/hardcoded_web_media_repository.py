from typing import List
from IPython.core.display import Image

from chosco.media.repository.domain.media_repository import MediaRepository


class HardcodedWebMediaRepository(MediaRepository):
    def __init__(self):
        self.media_ids = [
            "https://participa.podemos.info/assets/user_verifications/dni-sample1-489cd19dc5c69fc6b386e4da711536cc5579d903f9d80ab84af5d90f56b687fa.png",
            "https://cadenaser00.epimg.net/ser/imagenes/2020/02/06/sociedad/1581019912_200613_1581093640_noticia_normal.jpg",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/7/70/Deutscher_Personalausweis_im_ab_2021_vorgesehenen_Design%2C_Bundesregierung_der_Bundesrepublik_Deutschland%2C_Entwurf_eines_Gesetzes_zur_St%C3%A4rkung_der_Sicherheit_im_Pass-%2C_Ausweis-_und_ausl%C3%A4nderrechtlichen_Dokumentenwesen.jpeg/542px-thumbnail.jpeg",
            "https://www.journalducameroun.com/en/wp-content/uploads/2020/08/Digital-ID-1-780x440.png",
        ]

    def retrieve_all_ids(self) -> List[str]:
        return self.media_ids

    def retrieve(self, media_id: str, width: int = None) -> Image:
        if media_id not in self.media_ids:
            raise IndexError(
                f"media_id {media_id} not found on HardcodedWebMediaRepository"
            )
        return Image(media_id, unconfined=True, width=width)
