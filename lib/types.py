class Artist:
    def __init__(self, id: str, name: str, followed=False):
        self.id = id
        self.name = name
        self.followed = followed


class Tag:
    def __init__(self, id: str, name: str, path=""):
        self.id = id
        self.name = name
        self.path = path


class TagCategory:
    def __init__(self, label: str):
        self.label = label
        self.tags: list[Tag] = []


class Chapter:
    def __init__(self, title: str, id: int):
        self.title = title
        self.id = id


class DisplayGallery:
    def __init__(self, title: str, thumbnail: str, id: str):
        self.title = title
        self.thumbnail = thumbnail
        self.id = id


class Gallery:
    def __init__(
        self,
        id: str,
        thumbnail: str,
        artist_ids: list[str],
        tags: dict[str, list[Tag]],
        pages: int,
        title: str,
        images: list[str],
        title_pre: str = "",
        title_suf: str = "",
        liked=False,
        reading=False,
        current_page=0,
        chapters: list[Chapter] = [],
        has_chapters: bool = False
    ):
        self.id = id
        self.thumbnail = thumbnail
        self.artistId = artist_ids
        self.tags = tags
        self.pages = pages
        self.title = title
        self.images = images
        self.title_pre = title_pre
        self.title_suf = title_suf
        self.liked = liked
        self.reading = reading
        self.current_page = current_page
        self.chapters = chapters
        self.has_chapters = has_chapters
