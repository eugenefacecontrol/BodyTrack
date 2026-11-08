#!/usr/bin/env python3
"""Offline structural and JavaScript checks for the EN/RU static site.

No browser or network calls. Spanish findings are review hints, not proof of an
untranslated UI: quoted JS strings can also be internal identifiers.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent / 'dist'
errors = []
warnings = []
checked_scripts = 0
checked_links = 0

SPANISH = re.compile(
    r'\b(?:biomecánica|ejercicio|ejercicios|sentadilla|cuádriceps|glúteos|'
    r'rodilla|cadera|tobillo|espalda|pies|talones|punteras|arrastrar|arrastra|'
    r'cargando|reiniciar|cerrar|mostrar|ocultar|pausar|reproducir|guardar|'
    r'volver|ángulo|ángulos|fuerza|resistencia|recorrido|repeticiones|'
    r'velocidad|músculos|músculo|suscripción|correo|privacidad|siguiente|'
    r'anterior|votar|voto|gratuito|gratis|acepto|enviado|desplazamiento|'
    r'pantalla|cambiar|configuración|ajustes|selecciona|desliza|presiona|'
    r'apoyo|altura|longitud|inclinación|duración|bloqueado|simulación)\b',
    re.IGNORECASE,
)


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.lang = None
        self.ids = set()
        self.links = []
        self.text = []
        self.scripts = []
        self.handlers = []
        self.styles = []
        self.script = None
        self.style = None
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.lang = attrs.get('lang')
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'form':
            errors.append(f'{self.path.relative_to(ROOT)}: unexpected <form>')
        for key in ['href', 'src', 'poster', 'action']:
            if attrs.get(key):
                self.links.append((tag, key, attrs[key]))
        if attrs.get('srcset'):
            for entry in attrs['srcset'].split(','):
                if entry.strip():
                    self.links.append((tag, 'srcset', entry.split()[0]))
        for key, value in attrs.items():
            if key.startswith('on') and value:
                self.handlers.append((key, value))
        for key in ['aria-label', 'title', 'placeholder', 'alt']:
            if attrs.get(key):
                self.text.append(attrs[key])
        if attrs.get('style'):
            self.styles.append(attrs['style'])
        if tag == 'script':
            self.script = {'type': attrs.get('type', ''), 'src': attrs.get('src'), 'text': ''}
        elif tag == 'style':
            self.style = ''

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag == 'script' and self.script is not None:
            self.scripts.append(self.script)
            self.script = None
        elif tag == 'style' and self.style is not None:
            self.styles.append(self.style)
            self.style = None

    def handle_data(self, data):
        if self.script is not None:
            self.script['text'] += data
        elif self.style is not None:
            self.style += data
        elif data.strip():
            self.text.append(data.strip())


def local_target(origin, url):
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or url.startswith('//'):
        return None
    raw_path = unquote(parsed.path)
    path = ROOT / raw_path.lstrip('/') if raw_path.startswith('/') else origin.parent / raw_path
    if not raw_path:
        path = origin
    path = path.resolve()
    if path.is_dir() or raw_path.endswith('/'):
        path = path / 'index.html'
    return path, unquote(parsed.fragment)


def syntax(code, label, module=False):
    global checked_scripts
    if not code.strip():
        return
    checked_scripts += 1
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mjs' if module else '.js') as f:
        f.write(code)
        f.flush()
        result = subprocess.run(['node', '--check', f.name], text=True, capture_output=True)
        if result.returncode:
            errors.append(f'{label}: JavaScript syntax check failed\n{result.stderr[:1600]}')


def check_url(origin, label, url, pages):
    global checked_links
    result = local_target(origin, url)
    if result is None:
        return
    checked_links += 1
    path, fragment = result
    if not path.is_relative_to(ROOT.resolve()):
        errors.append(f'{label}: path escapes site: {url}')
    elif not path.is_file():
        errors.append(f'{label}: missing local target: {url}')
    elif fragment and path.suffix == '.html' and path in pages and fragment not in pages[path].ids:
        warnings.append(f'{label}: fragment not present in static HTML: {url}')


def spanish_hints(text, label):
    found = sorted(set(match.group(0) for match in SPANISH.finditer(text)))
    if found:
        warnings.append(f'{label}: possible Spanish UI: {", ".join(found)}')


def main():
    if not ROOT.is_dir():
        print(f'FAIL: missing output directory {ROOT}')
        return 1
    paths = sorted(ROOT.glob('en/*.html')) + sorted(ROOT.glob('ru/*.html'))
    for locale in ['en', 'ru']:
        for name in ['index', 'prensa', 'pendu', 'hipo']:
            if not (ROOT / locale / f'{name}.html').is_file():
                errors.append(f'{locale}/{name}.html: expected localized page is missing')
    pages = {path.resolve(): Page(path.resolve()) for path in paths}
    for path, page in pages.items():
        label = str(path.relative_to(ROOT))
        if page.lang != path.parent.name:
            errors.append(f'{label}: html lang={page.lang!r}, expected {path.parent.name!r}')
        source = path.read_text()
        # Check executable script and markup, excluding source comments.
        active = re.sub(r'<!--.*?-->', '', source, flags=re.S)
        if re.search(r'https?://[^\s\"\']*mailerlite\.com|mlFrame|fields\[email\]', active, re.I):
            errors.append(f'{label}: original mailing-list integration is still present')
        for tag, attr, url in page.links:
            check_url(path, f'{label} <{tag}> {attr}', url, pages)
        for style in page.styles:
            for url in re.findall(r'url\(\s*[\"\']?([^\)\"\']+)', style):
                check_url(path, f'{label} CSS', url.strip(), pages)
        spanish_hints(' '.join(page.text), f'{label} HTML')
        for i, script in enumerate(page.scripts, 1):
            if script['src'] or script['type'] not in ['', 'module', 'text/javascript', 'application/javascript']:
                continue
            syntax(script['text'], f'{label} inline script {i}', script['type'] == 'module')
            # Only quoted strings: comments and normal JS identifiers are omitted.
            strings = re.findall(r'([\"\'`])((?:\\.|(?!\1).)*?)\1', script['text'], re.S)
            spanish_hints(' '.join(s for _, s in strings if ' ' in s or SPANISH.fullmatch(s)),
                          f'{label} JS strings (review context)')
        for i, (event, handler) in enumerate(page.handlers, 1):
            syntax(f'function inlineHandler(event) {{\n{handler}\n}}', f'{label} {event} #{i}')
    for path in sorted(ROOT.rglob('*.js')) + sorted(ROOT.rglob('*.mjs')):
        syntax(path.read_text(), str(path.relative_to(ROOT)), path.suffix == '.mjs')
    for path in sorted(ROOT.rglob('*.css')):
        for url in re.findall(r'url\(\s*[\"\']?([^\)\"\']+)', path.read_text()):
            check_url(path, str(path.relative_to(ROOT)), url.strip(), pages)
    for message in errors:
        print('ERROR:', message)
    for message in warnings:
        print('REVIEW:', message)
    print(f'{"PASS" if not errors else "FAIL"}: {len(pages)} localized pages, '
          f'{checked_links} local references, {checked_scripts} JS syntax checks; '
          f'{len(errors)} errors, {len(warnings)} review hints.')
    print('Limit: static checks only; no interaction, rendering, or simulator-physics verification.')
    return 1 if errors else 0


if __name__ == '__main__':
    sys.exit(main())
