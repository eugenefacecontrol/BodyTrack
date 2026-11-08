"""Create a GitHub Pages artifact without changing the Sites build in dist/."""
import argparse
from pathlib import Path
import re
import shutil


def prepare(source: Path, target: Path, base: str):
    if not base.startswith('/') or '?' in base or '#' in base or '..' in base:
        raise ValueError('Base path must be an absolute URL path without traversal')
    base = base.rstrip('/')
    if source.resolve() == target.resolve() or source.resolve() in target.resolve().parents:
        raise ValueError('Output must be separate from source')
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)
    for path in target.rglob('*.html'):
        text = path.read_text()
        text = re.sub(r'''(\b(?:href|src|action)\s*=\s*["'])(/)(?!/)''',
                      lambda m: m[1] + base + '/', text)
        path.write_text(text)
    (target / '.nojekyll').touch()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-path', required=True)
    parser.add_argument('--source', type=Path, default=Path('dist'))
    parser.add_argument('--output', type=Path, default=Path('_site'))
    args = parser.parse_args()
    prepare(args.source, args.output, args.base_path)
    print(f'Pages artifact ready at {args.output} for {args.base_path}')
