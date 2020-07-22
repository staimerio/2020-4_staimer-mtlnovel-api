# Retic
from retic import Request, Response, Next

# Services
from retic.services.responses import success_response_service
import services.mtlnovel.mtlnovel as mtlnovel


def get_latest(req: Request, res: Response, next: Next):
    """Get all novel from latests page"""
    _novels = mtlnovel.get_latest(
        limit=req.param('limit')
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
