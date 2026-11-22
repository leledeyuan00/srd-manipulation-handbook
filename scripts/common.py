from pathlib import Path
from hashlib import sha256
import json, re
from markdown_it import MarkdownIt

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content'
STATE = ROOT / 'translation-state.json'
LANGS = ('en', 'ja', 'zh')
CHAPTERS = {
 '00_infrastructure': ('Lab infrastructure','研究室のインフラ','实验室基础设施'),
 '01_realtime_control': ('Real-time control','リアルタイム制御','实时控制'),
 '02_imitation_learning': ('Imitation learning','模倣学習','模仿学习'),
 '03_denso_system': ('Dual-arm DENSO system','双腕DENSOシステム','DENSO 双臂系统'),
 '04_lessons_learned': ('Lessons learned','教訓とトラブルシューティング','工程经验与教训'),
 '05_handbook_maintenance': ('Handbook maintenance','ハンドブックの保守','手册维护'),
 'appendix': ('Appendix','付録','附录'),
}
PART = re.compile(r'^[a-z0-9][a-z0-9_-]{0,79}$')

def read(p): return p.read_text(encoding='utf-8')
def write(p, s):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding='utf-8', newline='\n')
def digest(s): return sha256(s.encode('utf-8')).hexdigest()
def dump(p, obj): write(p, json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True)+'\n')
def load_state(): return json.loads(read(STATE)) if STATE.exists() else {}
def check_public_tree():
    """Structural guard only; cannot identify sensitive information in allowed files."""
    allowed = {
        'content': {'.md', 'AGENTS.md'},
        'assets': {'.png', '.jpg', '.jpeg', '.gif', '.webp', '.avif', '.gitkeep'},
        'vendor': {'README.md', 'toastui-editor-all.min.js', 'toastui-editor.min.css'},
        'web': {'editor.html', 'editor.js', 'read.js', 'style.css'},
    }
    for name, types in allowed.items():
        folder = ROOT / name
        if folder.is_symlink() or not folder.is_dir():
            raise ValueError(f'Invalid public input directory: {name}')
        for p in folder.rglob('*'):
            if p.is_symlink():
                raise ValueError(f'Symlink in public input: {p}')
            if p.is_dir():
                if name in ('web','vendor') or (name=='content' and not PART.fullmatch(p.name)):
                    raise ValueError(f'Unexpected directory in public input: {p}')
                continue
            if not p.is_file() or (p.name not in types and not (name in ('content','assets') and p.suffix.lower() in types)):
                raise ValueError(f'Unexpected public input: {p}')
            if p.name == 'AGENTS.md' and name=='content' and p.parent.relative_to(folder).parts not in [(c,) for c in CHAPTERS]:
                raise ValueError(f'Unexpected chapter instructions: {p}')

def scan():
    check_public_tree()
    pages = {}
    for p in sorted(CONTENT.rglob('*.md')):
        if p.name == 'AGENTS.md': continue
        parts = p.relative_to(CONTENT).parts
        if len(parts)<2 or p.stem not in LANGS or any(not PART.fullmatch(x) for x in parts[:-1]):
            raise ValueError(f'Invalid content path: {p}')
        ident = '/'.join(parts[:-1]); group = parts[0]
        if ident != 'home' and (group not in CHAPTERS or len(parts)<3):
            raise ValueError(f'Unknown chapter: {p}')
        pages.setdefault(ident,{})[p.stem] = read(p)
    return pages

def parser(): return MarkdownIt('commonmark', {'html':False}).enable('table').enable('strikethrough')
def title(text):
    tokens = parser().parse(text)
    if len(tokens)<3 or tokens[0].type!='heading_open' or tokens[0].tag!='h1':
        raise ValueError('Page must start with one H1 title')
    if sum(t.type=='heading_open' and t.tag=='h1' for t in tokens)!=1:
        raise ValueError('Page must have exactly one H1 title')
    return tokens[1].content

def signature(text):
    """Conservative structural guard; not a semantic/safety proof."""
    result=[]
    for t in parser().parse(text):
        if t.type in ('fence','code_block'):
            result.append((t.type,t.info,t.content))
        elif t.type in ('heading_open','bullet_list_open','ordered_list_open','list_item_open','blockquote_open','table_open','tr_open','th_open','td_open','hr'):
            result.append((t.type,t.tag,t.attrGet('start')))
        elif t.type=='inline':
            for c in t.children or []:
                if c.type=='code_inline': result.append(('code',c.content))
                elif c.type=='link_open': result.append(('link',c.attrGet('href')))
                elif c.type=='image': result.append(('image',c.attrGet('src')))
    return result
