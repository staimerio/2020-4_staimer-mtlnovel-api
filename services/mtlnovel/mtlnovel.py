"""Services for mtlnovel controller"""
# Retic
from retic import App as app

# Requests
import requests

# bs4
from bs4 import BeautifulSoup

# Services
from retic.services.responses import success_response_service, error_response_service
from retic.services.general.urls import slugify

# Utils
from services.utils.general import get_node_item

# Constants
YEAR = 2020


class MTLNovelEN(object):

    def __init__(self):
        """Set the variables"""
        self.instance = {
            "site": app.config.get("MTLNOVEL_EN_SITE"),
            "host": app.config.get("MTLNOVEL_EN_HOST"),
            "url_base": app.config.get("MTLNOVEL_EN_URL"),
            "lang": app.config.get("MTLNOVEL_EN_LANG"),
        }


def get_text_from_req(url):
    """GET Request to url"""
    _req = requests.get(url)
    """Check if status code is 200"""
    if _req.status_code != 200:
        raise Exception("The request to {0} failed".format(url))
    return _req.text


def get_data_items_container(instance, path):
    """Declare all variables"""
    items = list()
    """ Set url to consume"""
    url = instance['url_base']+path
    """Get data for request"""
    content = get_text_from_req(url)
    """Format the response"""
    soup = BeautifulSoup(content, 'html.parser')
    """Get all items"""
    container = soup.find(class_='post')
    items = container.find_all(class_='update-box')
    """Return all items"""
    return items


def get_data_item(instance, item):
    try:
        """Find the a element"""
        _data_item = item.find('h3').find('a', href=True)
        """Get url"""
        url = _data_item['href']
        """Check that the url exists"""
        if url == "#":
            raise Exception('URL is invalid.')
        """Get text from data"""
        title = _data_item.text
        return get_node_item(url, title, YEAR, instance['host'], instance['site'])
    except Exception as e:
        return None


def get_list_raw_items(instance, page, max=100):
    """Declare all variables"""
    _items = list()
    """Get article html from his website"""
    _items_raw = get_data_items_container(instance, page)
    for _item_raw in _items_raw:
        _item_data = get_data_item(instance, _item_raw)
        """Check if item exists"""
        if not _item_data:
            continue
        """Slugify the item's title"""
        _item_data['slug'] = slugify(_item_data['title'])
        """Add item"""
        _items.append(_item_data)
    """Return items"""
    return _items


def get_instance_from_lang(lang):
    """Get an MTLNovel instance from a language"""
    if lang == "en":
        return MTLNovelEN()
    raise ValueError("Language {0} is invalid.".format(lang))


def get_latest(lang="en", max=10):
    """Settings environment"""
    _mtlnovel = get_instance_from_lang(lang)
    """Request to mtlnovel web site for latest novel"""
    _items_raw = get_list_raw_items(
        _mtlnovel.instance, "", max)
    """Validate if data exists"""
    if not _items_raw:
        """Return error if data is invalid"""
        return error_response_service(
            msg="Files not found."
        )
    """Response data"""
    return success_response_service(
        data=_items_raw
    )
