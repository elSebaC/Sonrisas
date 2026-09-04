#!/usr/bin/env python3
"""Inlina styles.css y script.js en un unico archivo publicable (dist/index.html).

El archivo resultante no lleva doctype/html/head/body: el host de Artifacts
envuelve el contenido, y asi el mismo build sirve para publicar como Artifact.
"""
import pathlib
import re

root = pathlib.Path(__file__).parent
src = (root / "index.html").read_text(encoding="utf-8")
css = (root / "styles.css").read_text(encoding="utf-8")
js = (root / "script.js").read_text(encoding="utf-8")

title = re.search(r"<title>(.*?)</title>", src, re.S).group(0)
fonts = "\n  ".join(re.findall(r'<link [^>]*fonts\.g[^>]*>', src))
body = re.search(r"<body>(.*)</body>", src, re.S).group(1).strip()
body = re.sub(r'\s*<script src="script\.js"></script>', "", body)

out = root / "dist"
out.mkdir(exist_ok=True)
(out / "index.html").write_text(
    f"{title}\n  {fonts}\n<style>\n{css}</style>\n\n{body}\n\n<script>\n{js}</script>\n",
    encoding="utf-8",
)
print("dist/index.html escrito")
