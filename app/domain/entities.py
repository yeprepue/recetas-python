from dataclasses import dataclass, field
from typing import Optional, List


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
