from typing import List

from pydantic import BaseModel


class PageData(BaseModel):
    id: str


class Image(BaseModel):
    alt: str
    url: str


class Section(BaseModel):
    type: str
    headline: str
    subtitle: str
    image: Image


class ContentSchema(BaseModel):
    hero: Section


class LandingSectionContent(BaseModel):
    hero: Section


class LandingSection(BaseModel):
    type: str
    order: int
    content: LandingSectionContent


class PageWithSections(BaseModel):
    page_data: PageData
    landing: List[LandingSection]
