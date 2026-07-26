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
# Peaks — the great summits. Tag = elevation, clue = which side of the range.  #
# --------------------------------------------------------------------------- #

PEAKS = {
    "Aneto": (3404, "Spain — the highest summit of the Pyrenees"),
    "Posets": (3375, "Spain — second highest of the range"),
    "Monte Perdido": (3355, "Spain — the highest limestone massif in Europe"),
    "Vignemale": (3298, "France / Spain border — highest French Pyrenean peak"),
    "Balaïtous": (3144, "France / Spain border"),
    "Pica d'Estats": (3143, "Spain / France — highest point of Catalonia"),
    "Pic de Néouvielle": (3091, "France"),
    "Puigmal": (2910, "France / Spain border, eastern Pyrenees"),
    "Pic du Midi d'Ossau": (2884, "France — the unmistakable fang of the Ossau valley"),
    "Pic du Midi de Bigorre": (2877, "France — famous for its observatory"),
    "Mont Valier": (2838, "France — the emblem of the Ariège"),
    "Canigou": (2784, "France — sacred mountain of the Catalans"),
}


class Peaks(WikiImages, CategoryProvider):
    key = "peaks"
    items = list(PEAKS)
    override_name = True  # keep our display names, not the Wikipedia article titles
    tag_style = "plain"
    queries = {
        "Posets": "Pico Posets",
        "Canigou": "Canigó",
    }

    def get_tag(self, item):
        elevation, _ = PEAKS[item]
        return f"{elevation:,} m"

    def get_clue(self, item):
        _, clue = PEAKS[item]
        return clue


# --------------------------------------------------------------------------- #
# Wildlife — animals of the high Pyrenees, tagged with their Latin names.      #
# --------------------------------------------------------------------------- #


class Animals(WikiImages, ScientificNameProvider):
    key = "nature:animals"
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
    }


# --------------------------------------------------------------------------- #
# Flora — mountain plants, imaged and tagged by their scientific names.        #
# --------------------------------------------------------------------------- #


class Plants(WikiImages, ScientificNameProvider):
    key = "nature:plants"
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
# Lakes, valleys, passes and parks — the shapes of the range.                 #
# --------------------------------------------------------------------------- #


class Lakes(WikiImages, CategoryProvider):
    key = "lakes"
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
    key = "valleys"
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
    key = "passes"
    override_name = True
    items = [
        "Col du Tourmalet",
        "Col d'Aubisque",
        "Col d'Aspin",
        "Col de Peyresourde",
        "Port de la Bonaigua",
        "Somport",
    ]


class Parks(WikiImages, CategoryProvider):
    key = "parks"
    light_bg = True
    override_name = True
    items = [
        "Pyrenees National Park",
        "Ordesa y Monte Perdido National Park",
        "Aigüestortes i Estany de Sant Maurici National Park",
    ]
    queries = {
        "Pyrenees National Park": "Pyrénées National Park",
    }


PROVIDERS = [Peaks(), Animals(), Plants(), Lakes(), Valleys(), Passes(), Parks()]
for _provider in PROVIDERS:
    register(_provider)
