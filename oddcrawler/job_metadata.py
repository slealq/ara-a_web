from dataclasses import dataclass
from oddcrawler import WebpageExtractor

@dataclass(eq=True, frozen=True)
class NewsFilter:
    class_filter: str

@dataclass(eq=True, frozen=True)
class ExtractorJob:
    # The class, not an instance
    target_extractor: WebpageExtractor
    periodicity_in_seconds: int
    words_filter: NewsFilter

    def __repr__(self):
        build_dict =\
            {'Target Extractor': self.target_extractor.__name__,
             'Periodicity in secs': self.periodicity_in_seconds,
             'Words filter': self.words_filter}

        return repr(build_dict)
