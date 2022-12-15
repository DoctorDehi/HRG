from exceptions import  *


class PigeonGender:
    HOLUB = {
        "marking": "1.0",
        "assoc_relationship": "OTEC"
    }
    HOLUBICE = {
        "marking": "0.1",
        "assoc_relationship": "MATKA"
    }

    def get_gender_from_marking(marking):
        if marking == "1.0":
            return PigeonGender.HOLUB
        elif marking == "0.1":
            return PigeonGender.HOLUBICE


def cislo_krouzku_full_from_id(pigeonID):
    parts = pigeonID.split("-")
    if len(parts)!=3:
        raise WrongPigeonIdFormat(pigeonID)
    return parts[1] + "/" + parts[2]

def split_pigeon_id(pigeonID):
    parts = pigeonID.split('-')
    if len(parts)!=3:
        raise WrongPigeonIdFormat(pigeonID)
    return parts

def pigeon_id_from_cislo_krouzku_full(cislo_krouzku_full, user_id):
    parts = cislo_krouzku_full.split("/")
    if len(parts) != 2:
        raise WrongPigeonIdFormat(cislo_krouzku_full)
    return f'{user_id}-{parts[0]}-{parts[1]}'
