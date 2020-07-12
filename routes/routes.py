# Retic
from retic import Router

# Controllers
import controllers.mtlnovel as mtlnovel

router = Router()

router.get("/novels/mtlnovel/latest", mtlnovel.get_latest)
