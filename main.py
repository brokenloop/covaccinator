import requests
import pickle
import time
from datetime import date, timedelta
from typing import Set, List
from models import Model, Place, PlaceAvailability, Service
from pydantic import parse_obj_as
from email_sender import send_alert
from secret import authtoken

headers = {
    "authorization": f"Basic {authtoken}",
    "x-trimoz-role": "public",
    "product": "clicsante",
}


def get_availabilities_page(max_distance: int, page: int) -> Model:
    params = (
        ("page", page),
        ("dateStart", date.today()),
        ("dateStop", date.today() + timedelta(days=30)),
        # this will only have an effect if you include location info below
        ("maxDistance", max_distance),
        # ("latitude", ""),
        # ("longitude", ""),
        # ("postalCode", ""),
    )

    response = requests.get(
        "https://api3.clicsante.ca/v3/availabilities",
        headers=headers,
        params=params,
    )
    if response.status_code == 200:
        return Model(**response.json())


def get_places(max_distance: int = 1) -> List[Place]:
    keep_going = True
    i = 0
    result = {}
    while keep_going:
        model = get_availabilities_page(max_distance, i)
        if model is not None:
            print(f"page {i}")
            for place in model.places:
                result[place.place_id] = place
            i += 1
        else:
            keep_going = False
    return list(result.values())


def get_place_availabilities(place: Place):
    service_id = get_place_service_id(place)
    params = (
        ("dateStart", "2021-05-01"),
        ("dateStop", "2021-09-08"),
        ("service", service_id),
        ("timezone", "America/Toronto"),
        ("places", place.place_id),
        ("filter1", "1"),
        ("filter2", "0"),
    )

    response = requests.get(
        f"https://api3.clicsante.ca/v3/establishments/{place.establishment}/schedules/public",
        headers=headers,
        params=params,
    )
    if response.status_code == 200:
        return PlaceAvailability(**response.json())


def get_place_service_id(place: Place) -> int:
    response = requests.get(
        f"https://api3.clicsante.ca/v3/establishments/{place.establishment}/services",
        headers=headers,
    )
    service_name = "1st_dose_COVID_19_vaccine"
    services = parse_obj_as(List[Service], response.json())
    for service in services:
        if service.service_template.name == service_name:
            return service.id


def get_booking_link(place: Place) -> str:
    return f"https://clients3.clicsante.ca/{place.establishment}"


if __name__ == "__main__":
    sleep_time = 600
    cutoff = "2021-05-26"

    with open("places.pkl", "rb") as f:
        places = pickle.load(f)

    while True:
        print(f"searching for availabilities in {len(places)} places")
        for place in places:
            availabilities = get_place_availabilities(place)
            if (
                availabilities is not None
                and any(availabilities.availabilities)
                and any([x for x in availabilities.availabilities if x < cutoff])
            ):
                print(f"{place.place_id}: {place.name_en}, {place.formatted_address}")
                print(availabilities)
                print()
                send_alert(place, availabilities.availabilities)
        time.sleep(sleep_time)
