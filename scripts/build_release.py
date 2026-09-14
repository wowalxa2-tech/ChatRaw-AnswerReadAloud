"""Build a deterministic, installable plugin ZIP and public release assets."""
import hashlib
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / 'dist'
DIST.mkdir(exist_ok=True)
manifest = json.loads((ROOT / 'manifest.json').read_text())
archive = DIST / f"{manifest['id']}-{manifest['version']}.zip"
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as bundle:
    for name in ('manifest.json', 'main.js', 'icon.png', 'README.md', 'LICENSE'):
        info = zipfile.ZipInfo(f"{manifest['id']}/{name}", date_time=(2026, 9, 14, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o100644 << 16
        bundle.writestr(info, (ROOT / name).read_bytes())
(DIST / 'SHA256SUMS').write_text(
    f'{hashlib.sha256(archive.read_bytes()).hexdigest()}  {archive.name}\n'
)
print(f'Built {archive.name}, SHA256SUMS')
