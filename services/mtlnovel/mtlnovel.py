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
from retic.services.general.json import parse

# Utils
from services.utils.general import get_node_item, get_node_light_novel_item

# Constants
YEAR = app.config.get('MTLNOVEL_YEAR', callback=int)
URL_MAIN = app.config.get('MTLNOVEL_URL_MAIN')
INDEX = {
    u"type": 5,
    u"categories": 6,
    u"author": 3,
    u"status": 2
}


class MTLNovelEN(object):

    def __init__(self):
        """Set the variables"""
        self.site = app.config.get("MTLNOVEL_EN_SITE")
        self.host = app.config.get("MTLNOVEL_EN_HOST")
        self.url_base = app.config.get("MTLNOVEL_EN_URL")
        self.lang = app.config.get("MTLNOVEL_EN_LANG")


def get_text_from_req(url):
    """GET Request to url"""
    _req = requests.get(url)
    """Check if status code is 200"""
    if _req.status_code != 200:
        raise Exception("The request to {0} failed".format(url))
    return _req.text


def get_data_items_container(instance, path):
    """Declare all variables"""
    _items = list()
    """ Set url to consume"""
    _url = "{0}/{1}".format(instance.url_base, path)
    """Get data for request"""
    _content = get_text_from_req(_url)
    """Format the response"""
    _soup = BeautifulSoup(_content, 'html.parser')
    """Get all items"""
    _container = _soup.find(class_='post')
    _items = _container.find_all(class_='update-box')
    """Return all items"""
    return _items


def get_data_item(instance, item):
    try:
        """Find the a element"""
        _data_item = item.find('h3').find('a', href=True)
        """Get url"""
        _url = _data_item['href']
        """Check that the url exists"""
        if _url == "#":
            raise Exception('URL is invalid.')
        """Get text from data"""
        _title = _data_item.text
        _url = _url.replace(instance.url_base, "")
        return get_node_item(_url, _title, YEAR, instance.host, instance.site)
    except Exception as e:
        return None


def get_list_raw_items(instance, page, limit=100):
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
        """Validate if has the max"""
        if len(_items) >= limit:
            break
    """Return items"""
    return _items


def get_instance_from_lang(lang):
    """Get an MTLNovel instance from a language"""
    if lang == "en":
        return MTLNovelEN()
    raise ValueError("Language {0} is invalid.".format(lang))


def get_latest(lang="en", limit=10):
    """Settings environment"""
    _mtlnovel = get_instance_from_lang(lang)
    """Request to mtlnovel web site for latest novel"""
    _items_raw = get_list_raw_items(
        _mtlnovel, "", limit)
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


def get_publication_by_slug(instance, path):
    """Set url to consume"""
    _url = "{0}/{1}".format(instance.url_base, path)
    """Get content from url"""
    _content = get_text_from_req(_url)
    """Format the response"""
    _soup = BeautifulSoup(_content, 'html.parser')
    """Get json string of data"""
    json_data_raw = _content.split(
        '<script type="application/ld+json">'
    )[-1].split('</script>')[0]
    """Get json object"""
    _json_data = parse(json_data_raw)

    """Get all metadata"""
    _title = _json_data[2]['name']
    _cover = _json_data[2]['image'].replace(
        instance.url_base, URL_MAIN
    )

    _data_table = _soup.find(id='panelnovelinfo').find(class_='info')
    _data = _data_table.find_all('tr')

    _type = _data[INDEX['type']].find_all('td')[-1].text
    _categories = _data[INDEX['categories']].find_all(
        'td')[-1].text.split(", ")
    _author = _data[INDEX['author']].find_all('td')[-1].text
    _status = _data[INDEX['status']].find_all('td')[-1].text
    return get_node_light_novel_item(
        _url, _title, YEAR, _type, _author,
        _cover, _status, _categories, instance.lang,
        instance.host, instance.site
    )


def get_volumes_by_slug(instance, path, last_vol=0, last_ch=0):
    """Define all variables"""
    _chapters_list = []
    """Set url to consume"""
    _url = "{0}/{1}".format(instance.url_base, path)
    """Get content from url"""
    _content = get_text_from_req(_url)
    """Format the response"""
    _soup = BeautifulSoup(_content, 'html.parser')
    """Get volumes metadata"""
    _volumes_data = _soup.find(id='panelchapterlist').find_all('section')
    """For each volumen to do the following"""
    for _volume in _volumes_data:
        """Get chapter metadata"""
        _url_file_json = _volume.find(
            class_="ch-list").find('amp-list')['src']
        _chapters_data = parse(
            get_text_from_req(
                _url_file_json
            )
        )['items']
        """For each item to do the following"""
        for _chapter in _chapters_data:
            """Get the number of chapter or ignore it"""
            _number = _chapter['no'].replace("Chapter ", '')
            """Get all data about the chapter"""
            _title = _chapter['title']
            _url = _chapter['permalink']

            _chapters_list.append(
                {"title": _title, "url": _url, "number": _number}
            )
    return _chapters_list


def get_chapter_html_by_url(instance, url):
    """Get content from url"""
    _content = get_text_from_req(url)
    """Format the response"""
    _soup = BeautifulSoup(_content, 'html.parser')
    _container = _soup.find(class_='post')
    """Get title"""
    _title = "<h2>{0}</h2>".format(_container.find('h1').text)
    # print title
    _content_p = _container.find(class_='par').find_all('p')
    _content = str(_content_p[:]).strip('[]')
    """Transform data"""
    _content_html = _title + _content
    _content_html = _content_html.replace('\n', '').replace(">, <", "><")
    """Response content of chapter"""
    return _content_html


def get_chapters_by_slug(novel_slug, chapters_ids, limit=50, lang="en"):
    """Define all variables"""
    _chapters_list = []
    """Settings environment"""
    _mtlnovel = get_instance_from_lang(lang)
    """Get info about the novel from website"""
    _novel_publication = get_publication_by_slug(
        _mtlnovel, novel_slug
    )
    """Get all chapters references"""
    _publication_chapters = get_volumes_by_slug(
        _mtlnovel, novel_slug
    )
    """Exclude the chapter Ids"""
    _chapters = filter(
        (lambda chapter: True if chapter['title']
         not in chapters_ids else False),
        _publication_chapters
    )
    """Get content of the all chapters"""
    for _chapter in _chapters:
        try:
            """Check the max items"""
            if len(_chapters_list) >= limit:
                break
            """Get content of the chapter by url"""
            _content = get_chapter_html_by_url(
                _mtlnovel, _chapter['url']
            )
            _url = _chapter['url'].replace(_mtlnovel.url_base, '')
            _chapters_list.append({
                **_chapter,
                U"url": _url,
                u"content": _content
            })
        except Exception as e:
            continue
    """Transform data"""
    _data_response = {
        u"novel": _novel_publication,
        u"chapters": _chapters_list
    }
    """"Response to client"""
    return success_response_service(
        data=_data_response
    )
