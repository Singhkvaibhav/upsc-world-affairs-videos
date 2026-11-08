"""Episode 4 Short (vertical 1080x1920): run with ART_VERTICAL=1 python3 ../../engine/cli.py ... """
import os, importlib.util
os.environ['ART_VERTICAL'] = '1'
from engine.art import *
_s = importlib.util.spec_from_file_location('ep_spec', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ep.py'))
_m = importlib.util.module_from_spec(_s); _s.loader.exec_module(_m)
EP, TITLE, NAME, SPEC = _m.EP, _m.TITLE, _m.NAME, _m.SPEC
BEATS, CAPTIONS, EXTRA, EVENTS = build_short(EP, SPEC)
