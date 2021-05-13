from typing import List, Dict, Optional

from pydantic import BaseModel, Field


class Establishment(BaseModel):
    place_id: int = Field(..., alias="id")
    name: str
    phone: Optional[str]
    address: Optional[str]
    public_url: Optional[str]


class Su237(BaseModel):
    t07: int
    ta7: int


class Availabilities(BaseModel):
    su237: Su237


class Place(BaseModel):
    place_id: int = Field(..., alias="id")
    establishment: int
    name_fr: str
    name_en: str
    formatted_address: str
    latitude: float
    longitude: float
    is_virtual: int
    availabilities: Optional[Availabilities]


class Model(BaseModel):
    establishments: List[Establishment]
    places: List[Place]
    distanceByPlaces: Dict
    serviceIdsByPlaces: List


class PlaceAvailability(BaseModel):
    availabilities: List
    daysComplete: List[str]
    upcomingAvailabilities: List
    pastAvailabilities: List


class ServiceTemplate(BaseModel):
    id: int
    name: str
    descriptionFr: str
    descriptionEn: str


class Service(BaseModel):
    id: int
    establishment: int
    service_template: ServiceTemplate
