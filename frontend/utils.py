
def build_breadcrumbs(request, items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": request.build_absolute_uri(url)
            }
            for i, (name, url) in enumerate(items)
        ]
    }
