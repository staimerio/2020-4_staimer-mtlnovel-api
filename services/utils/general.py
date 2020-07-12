"""Services for general utils"""


def get_node_item(url, title, year, host, site=''):
    """Set item structure"""
    item = {
        u'url': url,
        u'title': title,
        u'year': int(year),
        u'service': host,
        u'site': site
    }
    return item
