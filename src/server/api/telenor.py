"""
Ove funkcije, zasad, koriste API koji koristi
i Telenorov sajt
"""

from urllib2 import urlopen, Request
from urllib import urlencode
import json


class Location:
    def __init__(self, json_data, picture_data):
        self.id = json_data["id"]
        self.working_hours = [x[x.find(":") + 1:] for x in json_data["working_hours"].split(",")]
        self.lat = json_data["lat"]
        self.lng = json_data["lng"]
        self.address = json_data["address"]
        self.city = json_data["city"]

        """
        Za prodavnice koje imaju, vracamo i niz linkova za slike
        Zasad sam uspeo da nadjem samo dve prodavnice na Mirijevu
        koje imaju ove slike
        """
        if self.id in picture_data:
            self.map_image = ["https://telenor.rs" + x for x in picture_data[self.id]]
        else:
            self.map_image = None


def get_locations(latitude, longitude, distance_km):
    """
    Vraca listu Location objekata, na zadatoj udaljenosti
    od zadatih koordinata.
    """
    url = "https://www.telenor.rs/stores/latlong/"
    data = {"lat": str(latitude), "lng": str(longitude), "dist": str(distance_km)}
    response = urlopen(url, data=urlencode(data))
    response = json.load(response)
    stores = response["data"]["stores"]
    store_objects = []
    for store in stores:
        store_objects.append(Location(store, response["data"]["images"]))
    return store_objects


def get_metadata():
    """
    Nabalja podatke o tarifama i operativnim sistemima

    Vraca recnik u obliku:
    {
        tariffs:[
            {
                "id": id_tarife,
                "subscription": cena_pretplate,
                "name": ime_na_srpskom
            }
            ...
        ]
        "os:[
            {
                "id": id_op_sistema
                "name": ime_na_srpskom
            }
            ...
        ]
    }
    """
    url = "https://www.telenor.rs/webshop/sr/api/shopDevicesSection/Privatni-korisnici/Mobilni-telefoni/"
    response = json.load(urlopen(url))["data"]
    data = {}
    oses = []
    for os in response["shopOperatingSystems"]:
        oses.append({"id": os["opsystem_id"], "name": os["name_yu"]})
    data["os"] = oses
    tariffs = []
    for tariff in response["shopTariffPackages"]:
        tariffs.append({"id": tariff["id"], "name": tariff["name"], "subscription": tariff["subscription"]})
    data["tariffs"] = tariffs
    return data


def get_phones():
    """
    Nabavlja podatke o telefonima
    Vraca recnik u obliku:

    {
        "id_telefona":{
            "model": ime_modela,
            "thumb": link_do_male_slike,
            "url": link_do_telefona,
            "os": id_sistema,
            "image": slika,
            "brand": proizvodjac,
            "name": puno_ime,
            "prices":{
                id_tarife:{
                    "24": cena_na_24_meseca,
                    "12": cena_na_12_meseci
                }
                ...
            },
            "battery": kapacitet_baterije_mAh, [int]
            "camera": kamera_mpx, [string],
            "ram": ram_gb, [float]
            "screen" ekran_inca, [float]
            "os_name": sistem_ime_sa_verzijom, [string]
            "processor": string_o_procesoru, [string]

        }
    }

    Atributi camera, os_name i processor nisu pogodni za parsiranje,
    nemaju neki dosledan format
    U slucaju da neki atribut nije poznat, vrednost je None
    """
    url = "https://www.telenor.rs/webshop/sr/api/shopDevicesJson/Privatni-korisnici/Mobilni-telefoni/"
    response = json.load(urlopen(url))["data"]
    phones = {}
    for phoneid in response:
        phone = response[phoneid]
        prices = {}
        for price in phone["prices"]:
            contract = phone["prices"][price]
            prices[price] = {
                "12": contract["cena_ugovor12"],
                "24": contract["cena_ugovor24"],
            }
        specs = phone["shopSpecList"]
        phones[phoneid] = {
            "url": phone["url"],
            "thumb": phone["thumb"],
            "image": phone["image"],
            "brand": phone["brand"],
            "model": phone["model"],
            "name": phone["title"],
            "os": phone["opsystem"],
            "prices": prices,
            "battery": int(specs["battery"]["specs"]["value"].replace(" mAh", "")) if specs["battery"]["specs"][
                                                                                          "value"] != '-' and
                                                                                      specs["battery"]["specs"][
                                                                                          "value"].isdigit() else None,
            "camera": specs["camera"]["specs"]["value"],
            "processor": specs["processor"]["specs"]["value"],
            "screen": float(specs["screen_size"]["specs"]["value"].replace('"', "").replace(",", ".")) if
            specs["screen_size"]["specs"]["value"] != '-' else None,
            "os_name": specs["system"]["specs"]["value"],
        }
        if specs["memory"]["specs"]["value"] != '-':
            phones[phoneid]["ram"] = float(
                specs["memory"]["specs"]["value"].replace(" GB", "").replace(" RAM", "").replace(",", "."))
        else:
            phones[phoneid]["ram"] = None

    return phones
