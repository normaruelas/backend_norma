from collections import defaultdict
from django.http import JsonResponse
from .models import Category, Variant, Size, MenuItem, Price, Settings

def menu_export(request):
    sizes = {s.key: {"label": s.label} for s in Size.objects.all()}
    variants = {v.key: {"label": v.label} for v in Variant.objects.all()}

    precios = defaultdict(lambda: defaultdict(dict))
    qs = Price.objects.select_related("item__category", "size", "variant")
    for p in qs:
        cat_key = p.item.category.key
        precios[cat_key][p.size.key][p.variant.key] = float(p.amount)

    catalogo = []
    items = MenuItem.objects.select_related("category")
    for i in items:
        img_url = ""
        if i.image:
            img_url = request.build_absolute_uri(i.image.url)
        catalogo.append({
            "id": i.public_id,
            "name": i.name,
            "cat": i.category.key,
            "img": img_url,
            "desc": i.description,
            "available": i.available,
        })

    s = Settings.objects.first()
    addon_meat = float(s.addon_meat) if s else 3.0
    meat_variants = list(s.meat_variants.values_list("key", flat=True)) if s else []

    data = {
        "SIZES": sizes,
        "VARIANTES": variants,
        "PRECIOS": precios,
        "CATALOGO": catalogo,
        "ADDON_MEAT": addon_meat,
        "MEAT_VARIANTS": meat_variants,
    }
    return JsonResponse(data, safe=False)
