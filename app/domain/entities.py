from dataclasses import dataclass, field
from typing import Optional, List, Tuple
import re

YOUTUBE_ID_PATTERN = re.compile(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*")


@dataclass
class Meal:
    id: str
    name: str
    alternate_name: Optional[str] = None
    category: Optional[str] = None
    area: Optional[str] = None
    instructions: Optional[str] = None
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    tags: Optional[str] = None
    youtube_url: Optional[str] = None
    ingredients: List[str] = field(default_factory=list)
    measures: List[str] = field(default_factory=list)
    source: Optional[str] = None
    ingredient_measures: List[Tuple[str, str]] = field(default_factory=list)
    youtube_video_id: Optional[str] = None


@dataclass
class Category:
    id: str
    name: str
    thumbnail_url: str
    description: str


@dataclass
class Area:
    name: str


@dataclass
class Ingredient:
    id: Optional[str]
    name: str
    description: str
    type: str
