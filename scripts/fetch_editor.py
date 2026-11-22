"""Download pinned editor assets at build time; no CDN script runs in users' browsers."""
from pathlib import Path
from urllib.request import urlopen
root=Path(__file__).resolve().parents[1]/'vendor'
root.mkdir(exist_ok=True)
for file in ['toastui-editor-all.min.js','toastui-editor.min.css']:
    if (root/file).exists():
        print('Using local asset:',file)
        continue
    url='https://uicdn.toast.com/editor/3.2.2/'+file
    with urlopen(url,timeout=45) as response:
        data=response.read()
    if len(data)<1000: raise RuntimeError('Unexpected editor asset response')
    (root/file).write_bytes(data)
    print('Fetched',file)
