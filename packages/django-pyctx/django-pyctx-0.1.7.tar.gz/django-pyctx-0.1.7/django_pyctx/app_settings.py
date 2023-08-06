from typing import Any, Dict

from pyctx import helpers


DJANGO_PYCTX: Dict[str, Any] = {
    'BLACK_LIST': [],
    'CONTEXT_ID_FACTORY': helpers.default_id_factory,
    'REQUEST_ID_FACTORY': helpers.default_id_factory,
    'EXTRAS_FACTORY': helpers.default_extras_factory,
}
