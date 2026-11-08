"""Check Pages links with repository prefixes, including the root landing page."""
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlsplit, unquote
from prepare_pages import prepare

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ('src', 'href', 'action') and value:
                self.urls.append(value)

for base in ('/BodyTrack', '/renamed-repository', '/'):
    with TemporaryDirectory() as directory:
        output = Path(directory) / 'site'
        prepare(Path('dist'), output, base)
        count = 0
        for page in output.rglob('*.html'):
            parser = Links()
            parser.feed(page.read_text())
            for url in parser.urls:
                parsed = urlsplit(url)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                path = unquote(parsed.path)
                if path.startswith('/'):
                    prefix = base.rstrip('/') + '/'
                    assert path.startswith(prefix), (page, url, base)
                    target = output / path[len(prefix):]
                else:
                    target = page.parent / path
                assert target.resolve().is_relative_to(output.resolve()), (page, url)
                assert target.exists(), (page, url, target)
                count += 1
        assert (output / '.nojekyll').exists()
        print(f'PASS: {count} local links/assets at {base}')
