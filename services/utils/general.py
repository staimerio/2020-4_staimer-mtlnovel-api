"""Services for general utils"""

# Services
from retic.services.general.urls import slugify


def get_node_item(url, title, year, host, site=''):
    """Set item structure"""
    _item = {
        u'url': url,
        u'title': title,
        u'year': int(year),
        u'service': host,
        u'site': site
    }
    return _item


def get_node_light_novel_item(
    url, title, year, type, author, cover,
    status, categories, lang, host, site=''
):
    _item = {
        u'url': url.replace(",", " "),
        u'slug': slugify(title),
        u'title': title,
        u'year': int(year) if (year != 'N/A') else 2020,
        u'type': type,
        u'author': author,
        u'cover': cover,
        u'status': status,
        u'categories': categories,
        u'lang': lang,
        u'service': host,
        u'site': site
    }
    return _item
