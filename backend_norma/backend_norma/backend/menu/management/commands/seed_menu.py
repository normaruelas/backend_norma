from django.core.management.base import BaseCommand
from menu.models import Category, Variant, Size, MenuItem, Price, Settings

class Command(BaseCommand):
    help = "Seed menú inicial"

    def handle(self, *args, **kwargs):
        cats = {
            "trancas": "Trancas",
            "tortas": "Tortas",
            "panuchos": "Panuchos",
            "tacos": "Tacos",
            "tostadas": "Tostadas",
        }
        cat_objs = {k: Category.objects.get_or_create(key=k, defaults={"name": v})[0] for k, v in cats.items()}

        sizes = {"normal": "Normal", "especial": "Especial"}
        size_objs = {k: Size.objects.get_or_create(key=k, defaults={"label": v})[0] for k, v in sizes.items()}

        variants = {
            "lechon": "Lechón",
            "rellenoNegro": "Relleno Negro",
            "pavoAsado": "Pavo Asado",
            "pocChuc": "Poc Chuc",
        }
        var_objs = {k: Variant.objects.get_or_create(key=k, defaults={"label": v})[0] for k, v in variants.items()}

        items = [
            {"public_id": 101, "name": "Tranca",   "cat": "trancas",  "desc": "Pan grande con relleno a elegir", "available": True},
            {"public_id": 201, "name": "Torta",    "cat": "tortas",   "desc": "Bolillo con relleno a elegir",   "available": True},
            {"public_id": 301, "name": "Panuchos", "cat": "panuchos", "desc": "Tortilla con frijol y relleno",  "available": True},
            {"public_id": 401, "name": "Tacos",    "cat": "tacos",    "desc": "Orden con salsas al gusto",      "available": True},
            {"public_id": 501, "name": "Tostadas", "cat": "tostadas", "desc": "Crujientes con frijol y relleno", "available": True},
        ]
        item_objs = {}
        for it in items:
            obj, _ = MenuItem.objects.get_or_create(
                public_id=it["public_id"],
                defaults={
                    "name": it["name"],
                    "category": cat_objs[it["cat"]],
                    "description": it["desc"],
                    "available": it["available"],
                }
            )
            item_objs[it["cat"]] = obj

        PRECIOS = {
            "trancas": {
                "normal":   {"lechon": 38, "rellenoNegro": 38, "pavoAsado": 42, "pocChuc": 55},
                "especial": {"lechon": 50, "rellenoNegro": 50, "pavoAsado": 60, "pocChuc": 65},
            },
            "tortas": {
                "normal":   {"lechon": 35, "rellenoNegro": 35, "pavoAsado": 37, "pocChuc": 50},
                "especial": {"lechon": 45, "rellenoNegro": 45, "pavoAsado": 55, "pocChuc": 60},
            },
            "panuchos": {
                "normal":   {"lechon": 25, "rellenoNegro": 25, "pavoAsado": 28, "pocChuc": 30},
                "especial": {"lechon": 35, "rellenoNegro": 35, "pavoAsado": 35, "pocChuc": 38},
            },
            "tacos": {
                "normal":   {"lechon": 25, "rellenoNegro": 25, "pavoAsado": 28, "pocChuc": 30},
                "especial": {"lechon": 35, "rellenoNegro": 35, "pavoAsado": 38, "pocChuc": 38},
            },
            "tostadas": {
                "normal":   {"lechon": 25, "rellenoNegro": 25, "pavoAsado": 28, "pocChuc": 30},
                "especial": {"lechon": 35, "rellenoNegro": 35, "pavoAsado": 35, "pocChuc": 38},
            },
        }

        Price.objects.all().delete()
        for cat_key, size_map in PRECIOS.items():
            item = item_objs[cat_key]
            for size_key, var_map in size_map.items():
                for var_key, amount in var_map.items():
                    Price.objects.update_or_create(
                        item=item,
                        size=size_objs[size_key],
                        variant=var_objs[var_key],
                        defaults={"amount": amount},
                    )

        settings, _ = Settings.objects.get_or_create()
        settings.addon_meat = 3
        settings.save()
        settings.meat_variants.set([var_objs[k] for k in ["lechon", "rellenoNegro", "pavoAsado", "pocChuc"]])

        self.stdout.write(self.style.SUCCESS("✅ Menú inicial cargado."))
