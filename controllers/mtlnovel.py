# Retic
from retic import Request, Response, Next

# Services
import services.mtlnovel.mtlnovel as mtlnovel


def get_latest(req: Request, res: Response, next: Next):
    """Get all novel from latests page"""
    _novels = mtlnovel.get_latest()
    """Check if exist an error"""
    if _novels['valid'] is False:
        return res.bad_request(_novels)
    """Transform the data response"""
    _data_response = {
        u"novels": _novels
    }
    """Response the data to client"""
    res.ok(_data_response)
