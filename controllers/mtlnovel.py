# Retic
from retic import Request, Response, Next, App as app

# Services
from retic.services.responses import success_response_service
import services.mtlnovel.mtlnovel as mtlnovel
MTLNOVEL_LIMIT_LATEST = app.config.get('MTLNOVEL_LIMIT_LATEST')
MTLNOVEL_PAGES_LATEST = app.config.get('MTLNOVEL_PAGES_LATEST')
MTLNOVEL_EN_HREFLANG = app.config.get('MTLNOVEL_EN_HREFLANG')


def get_latest(req: Request, res: Response, next: Next):
    """Get all novel from latests page"""
    _novels = mtlnovel.get_latest(
        limit=req.param('limit', MTLNOVEL_LIMIT_LATEST, int),
        pages=req.param('pages', MTLNOVEL_PAGES_LATEST, int)
    )
    """Check if exist an error"""
    if _novels['valid'] is False:
        return res.bad_request(_novels)
    """Transform the data response"""
    _data_response = {
        u"novels": _novels.get('data')
    }
    """Response the data to client"""
    res.ok(success_response_service(_data_response))


def get_chapters_by_slug(req: Request, res: Response, next: Next):
    """Get all chapters from novel page"""
    _novel = mtlnovel.get_chapters_by_slug(
        req.param('slug_novel'),
        req.args.getlist('chapters_ids'),
        int(req.param('limit'))
    )
    """Check if exist an error"""
    if _novel['valid'] is False:
        return res.bad_request(_novel)
    else:
        """Response the data to client"""
        res.ok(_novel)


def get_all_search(req: Request, res: Response):
    if req.param('search'):
        return get_search(req, res)
    return res.bad_request("Bad request")


def get_search(req: Request, res: Response):
    """Get all novel from latests page"""
    _novels = mtlnovel.get_search(
        search=req.param('search'),
        limit=req.param('limit', MTLNOVEL_LIMIT_LATEST, callback=int),
        hreflang=req.param('hreflang', MTLNOVEL_EN_HREFLANG),
    )
    """Check if exist an error"""
    if _novels['valid'] is False:
        return res.not_found(_novels)
    """Transform the data response"""
    _data_response = {
        u"novels": _novels.get('data')
    }
    """Response the data to client"""
    res.ok(success_response_service(_data_response))
