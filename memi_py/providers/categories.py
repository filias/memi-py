"""Pyrenees category providers.

The engine's default image lookup is strict (exact article title, must expose a
page image, no redirect-following). ``WikiImages`` relaxes that so natural
display names still land on the right Wikipedia article: it follows redirects
and falls back to a search when the exact title has no lead image.
"""

from functools import lru_cache
from urllib.parse import quote

import requests
from memi_engine import CategoryProvider, ScientificNameProvider, register

WIKIPEDIA_LANG = "en"
_WIKI_UA = {"User-Agent": "memi-pyrenees (+https://py.memi.click)"}


@lru_cache(maxsize=1024)
def wiki_image(query, lang=WIKIPEDIA_LANG):
    """Resolve a name to its Wikipedia lead image + article URL, or ``None``."""
    api = f"https://{lang}.wikipedia.org/w/api.php"

    def fetch(extra):
        params = {
            "action": "query",
            "format": "json",
            "prop": "pageimages",
            "piprop": "thumbnail",
            "pithumbsize": 800,
            "redirects": 1,
            **extra,
        }
        try:
            resp = requests.get(api, params=params, headers=_WIKI_UA, timeout=10)
            pages = resp.json().get("query", {}).get("pages", {})
        except Exception:
            return None
        for page in pages.values():
            thumb = page.get("thumbnail", {}).get("source")
            if thumb:
                title = page.get("title", query)
                slug = quote(title.replace(" ", "_"))
                return {
                    "name": title,
                    "image": thumb,
                    "url": f"https://{lang}.wikipedia.org/wiki/{slug}",
                }
        return None

    return fetch({"titles": query}) or fetch(
        {"generator": "search", "gsrsearch": query, "gsrlimit": 1}
    )


class WikiImages:
    """Mixin: resolve images by a per-item query.

    ``queries`` maps a display name to the term searched on Wikipedia; scientific
    providers fall back to the Latin name automatically.
    """

    queries: dict[str, str] = {}

    def get_image(self, item):
        query = self.queries.get(item) or getattr(self, "scientific_names", {}).get(item, item)
        return wiki_image(query)


# --------------------------------------------------------------------------- #
# Peaks — the great summits. Tag = elevation (shown on reveal).                #
# --------------------------------------------------------------------------- #

PEAKS = {
    "Aneto": 3404,
    "Posets": 3375,
    "Monte Perdido": 3355,
    "Vignemale": 3298,
    "Balaïtous": 3144,
    "Pica d'Estats": 3143,
    "Pic de Néouvielle": 3091,
    "Puigmal": 2910,
    "Pic du Midi d'Ossau": 2884,
    "Pic du Midi de Bigorre": 2877,
    "Mont Valier": 2838,
    "Canigou": 2784,
}


class Peaks(WikiImages, CategoryProvider):
    key = "landscapes:peaks"
    items = list(PEAKS)
    override_name = True  # keep our display names, not the Wikipedia article titles
    tag_style = "plain"
    queries = {
        "Posets": "Pico Posets",
        "Canigou": "Canigó",
    }

    def get_tag(self, item):
        return f"{PEAKS[item]:,} m"


# --------------------------------------------------------------------------- #
# Wildlife — animals of the high Pyrenees, tagged with their Latin names.      #
# --------------------------------------------------------------------------- #


class Animals(WikiImages, ScientificNameProvider):
    key = "life:animals"
    override_name = True
    items = [
        "Pyrenean chamois",
        "Alpine marmot",
        "Bearded vulture",
        "Griffon vulture",
        "Egyptian vulture",
        "Golden eagle",
        "Pyrenean desman",
        "Western capercaillie",
        "Brown bear",
        "Pyrenean brook salamander",
        "Wallcreeper",
        "Rock ptarmigan",
        "Iberian ibex",
        "Snow vole",
        "Pine marten",
        "Stoat",
        "Alpine chough",
        "Snowfinch",
        "Citril finch",
        "Black woodpecker",
        "Eurasian eagle-owl",
        "Fire salamander",
        "Pyrenean frog",
        "White-throated dipper",
    ]
    scientific_names = {
        "Pyrenean chamois": "Rupicapra pyrenaica",
        "Alpine marmot": "Marmota marmota",
        "Bearded vulture": "Gypaetus barbatus",
        "Griffon vulture": "Gyps fulvus",
        "Egyptian vulture": "Neophron percnopterus",
        "Golden eagle": "Aquila chrysaetos",
        "Pyrenean desman": "Galemys pyrenaicus",
        "Western capercaillie": "Tetrao urogallus",
        "Brown bear": "Ursus arctos",
        "Pyrenean brook salamander": "Calotriton asper",
        "Wallcreeper": "Tichodroma muraria",
        "Rock ptarmigan": "Lagopus muta",
        "Iberian ibex": "Capra pyrenaica",
        "Snow vole": "Chionomys nivalis",
        "Pine marten": "Martes martes",
        "Stoat": "Mustela erminea",
        "Alpine chough": "Pyrrhocorax graculus",
        "Snowfinch": "Montifringilla nivalis",
        "Citril finch": "Carduelis citrinella",
        "Black woodpecker": "Dryocopus martius",
        "Eurasian eagle-owl": "Bubo bubo",
        "Fire salamander": "Salamandra salamandra",
        "Pyrenean frog": "Rana pyrenaica",
        "White-throated dipper": "Cinclus cinclus",
    }


# --------------------------------------------------------------------------- #
# Flora — mountain plants, imaged and tagged by their scientific names.        #
# --------------------------------------------------------------------------- #


class Plants(WikiImages, ScientificNameProvider):
    key = "life:plants"
    override_name = True
    items = [
        "Pyrenean saxifrage",
        "Pyrenean violet",
        "Edelweiss",
        "Pyrenean lily",
        "Pyrenean eryngo",
        "Trumpet gentian",
        "Pyrenean squill",
        "Pyrenean oak",
    ]
    scientific_names = {
        "Pyrenean saxifrage": "Saxifraga longifolia",
        "Pyrenean violet": "Ramonda myconi",
        "Edelweiss": "Leontopodium nivale",
        "Pyrenean lily": "Lilium pyrenaicum",
        "Pyrenean eryngo": "Eryngium bourgatii",
        "Trumpet gentian": "Gentiana acaulis",
        "Pyrenean squill": "Scilla lilio-hyacinthus",
        "Pyrenean oak": "Quercus pyrenaica",
    }


# --------------------------------------------------------------------------- #
# Butterflies — the Pyrenees are a European butterfly hotspot. Latin tags.     #
# --------------------------------------------------------------------------- #


class Butterflies(WikiImages, ScientificNameProvider):
    key = "life:butterflies"
    override_name = True
    items = [
        "Apollo",
        "Clouded Apollo",
        "Swallowtail",
        "Scarce swallowtail",
        "Camberwell beauty",
        "Marbled white",
        "Cardinal",
        "Purple-shot copper",
        "Escher's blue",
        "Mountain clouded yellow",
        "Gavarnie blue",
        "Gavarnie ringlet",
        "Spanish argus",
        "Niobe fritillary",
        "Peak white",
    ]
    scientific_names = {
        "Apollo": "Parnassius apollo",
        "Clouded Apollo": "Parnassius mnemosyne",
        "Swallowtail": "Papilio machaon",
        "Scarce swallowtail": "Iphiclides podalirius",
        "Camberwell beauty": "Nymphalis antiopa",
        "Marbled white": "Melanargia galathea",
        "Cardinal": "Argynnis pandora",
        "Purple-shot copper": "Lycaena alciphron",
        "Escher's blue": "Polyommatus escheri",
        "Mountain clouded yellow": "Colias phicomone",
        "Gavarnie blue": "Agriades pyrenaicus",
        "Gavarnie ringlet": "Erebia gorgone",
        "Spanish argus": "Aricia morronensis",
        "Niobe fritillary": "Fabriciana niobe",
        "Peak white": "Pontia callidice",
    }


# --------------------------------------------------------------------------- #
# Lakes, valleys, passes and parks — the shapes of the range.                 #
# --------------------------------------------------------------------------- #


class Lakes(WikiImages, CategoryProvider):
    key = "landscapes:lakes"
    override_name = True
    items = [
        "Lac de Gaube",
        "Lac d'Oô",
        "Estany de Sant Maurici",
        "Ibón de Estanés",
        "Lac Bleu de Bigorre",
        "Lacs d'Ayous",
    ]
    queries = {
        "Lac de Gaube": "Gaube Lake",
        "Lacs d'Ayous": "Lac Gentau",
        "Lac Bleu de Bigorre": "Lac Bleu (Hautes-Pyrénées)",
    }


class Valleys(WikiImages, CategoryProvider):
    key = "landscapes:valleys"
    override_name = True
    items = [
        "Ordesa Valley",
        "Aran Valley",
        "Tena Valley",
        "Ossau Valley",
        "Roncal Valley",
        "Benasque",
    ]
    queries = {
        "Aran Valley": "Val d'Aran",
    }


class Passes(WikiImages, CategoryProvider):
    key = "landscapes:passes"
    override_name = True
    items = [
        "Col du Tourmalet",
        "Col d'Aubisque",
        "Col d'Aspin",
        "Col de Peyresourde",
        "Port de la Bonaigua",
        "Somport",
    ]


# --------------------------------------------------------------------------- #
# Parks — an "all" overview of the 7 parks, plus the notable landmarks inside  #
# the parks that have enough Wikipedia-imaged features to guess between.       #
# (Alt Pirineu and Cadí-Moixeró lack enough distinct imaged landmarks, so they #
# appear only in the overview, without their own landmark menu.)               #
# --------------------------------------------------------------------------- #

PARKS_ALL = [
    "Ordesa y Monte Perdido National Park",
    "Aigüestortes i Estany de Sant Maurici National Park",
    "Pyrenees National Park",
    "Posets-Maladeta Natural Park",
    "Sierra y Cañones de Guara Natural Park",
    "Alt Pirineu Natural Park",
    "Cadí-Moixeró Natural Park",
]


class AllParks(WikiImages, CategoryProvider):
    key = "parks:all"
    override_name = True
    items = PARKS_ALL
    queries = {"Pyrenees National Park": "Pyrénées National Park"}


class OrdesaLandmarks(WikiImages, CategoryProvider):
    key = "parks:Ordesa y Monte Perdido"
    override_name = True
    items = [
        "Monte Perdido",
        "Cilindro de Marboré",
        "Soum de Ramond",
        "Ordesa Valley",
        "Cola de Caballo",
        "Brèche de Roland",
        "Torla",
    ]
    queries = {"Brèche de Roland": "Roland's Breach"}


class AiguestortesLandmarks(WikiImages, CategoryProvider):
    key = "parks:Aigüestortes"
    override_name = True
    items = [
        "Els Encantats",
        "Pic de Peguera",
        "Comaloforno",
        "Besiberri",
        "Estany de Sant Maurici",
        "Vall de Boí",
        "Colomers",
    ]
    queries = {"Els Encantats": "Gran Encantat"}


class PyreneesParkLandmarks(WikiImages, CategoryProvider):
    key = "parks:Pyrénées"
    override_name = True
    items = [
        "Vignemale",
        "Balaïtous",
        "Pic du Midi d'Ossau",
        "Pic de Néouvielle",
        "Cirque de Gavarnie",
        "Cirque d'Estaubé",
        "Gavarnie Falls",
        "Pont d'Espagne",
        "Lac de Gaube",
        "Ossau Valley",
        "Cauterets",
        "Pic Long",
    ]
    queries = {"Lac de Gaube": "Gaube Lake"}


class PosetsMaladetaLandmarks(WikiImages, CategoryProvider):
    key = "parks:Posets-Maladeta"
    override_name = True
    items = [
        "Aneto",
        "Posets",
        "Maladeta",
        "Pico Maldito",
        "Forau de Aigualluts",
        "Aneto Glacier",
        "Vallibierna",
        "La Renclusa",
    ]
    queries = {"Posets": "Pico Posets", "Forau de Aigualluts": "Aigualluts"}


class GuaraLandmarks(WikiImages, CategoryProvider):
    key = "parks:Guara"
    override_name = True
    items = [
        "Rodellar",
        "Alquézar",
        "Sierra de Guara",
        "Salto de Bierge",
        "Colungo",
        "Alcanadre",
    ]


PROVIDERS = [
    Peaks(),
    Animals(),
    Plants(),
    Butterflies(),
    Lakes(),
    Valleys(),
    Passes(),
    AllParks(),
    OrdesaLandmarks(),
    AiguestortesLandmarks(),
    PyreneesParkLandmarks(),
    PosetsMaladetaLandmarks(),
    GuaraLandmarks(),
]
for _provider in PROVIDERS:
    register(_provider)
