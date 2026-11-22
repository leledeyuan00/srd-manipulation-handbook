import argparse, os, shutil, json, html, re
from common import *
from pygments import highlight
from pygments.lexers import get_lexer_by_name, TextLexer
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound

E=lambda s: html.escape(str(s),quote=True)
UI={
'en': ('Engineering handbook','Search handbook','On this page','Edit page','New page','Draft / review required','Home','Report a problem'),
'ja': ('技術ハンドブック','ハンドブックを検索','このページの目次','ページ編集','新規ページ','草稿・要確認','ホーム','問題を報告'),
'zh': ('机器人技术手册','搜索文档','本页目录','编辑页面','新建页面','草稿 / 待审核','首页','反馈问题')}

def render(text, base):
    md=parser(); tokens=md.parse(text); headings=[]; count=0
    for i,t in enumerate(tokens):
        if t.type=='heading_open':
            count+=1; anchor=f'section-{count}'; t.attrSet('id',anchor)
            if t.tag!='h1': headings.append((t.tag,anchor,tokens[i+1].content))
        if t.type=='inline':
            for c in t.children or []:
                key='src' if c.type=='image' else 'href' if c.type=='link_open' else None
                if key and (c.attrGet(key) or '').startswith('assets/'):
                    c.attrSet(key,base+c.attrGet(key))
    def fence(items, i, options, env):
        t=items[i]; name=t.info.split()[0] if t.info.strip() else 'text'
        try: lexer=get_lexer_by_name(name)
        except ClassNotFound: lexer=TextLexer()
        code=highlight(t.content,lexer,HtmlFormatter(nowrap=True))
        return f'<div class="codebox"><div class="codebar"><span>{E(name)}</span><button class="copy" type="button">Copy</button></div><pre><code>{code}</code></pre></div>'
    md.renderer.rules['fence']=fence
    return md.renderer.render(tokens,md.options,{}), headings

def href(base,lang,ident): return f'{base}{lang}/{ident}/'

def page_html(ident,lang,text,pages,repo):
    base='../'*(len(ident.split('/'))+1); ui=UI[lang]; idx=LANGS.index(lang)
    nav=f'<a class="navlink {"active" if ident=="home" else ""}" href="{href(base,lang,"home")}">{ui[6]}</a>'
    for group,labels in CHAPTERS.items():
        children=[p for p in pages if p.startswith(group+'/')]
        if not children: continue
        order = {'index':0,'data_collection':1,'dataset':2,'training':3,'deployment':4}
        children.sort(key=lambda p:(order.get(p.rsplit('/',1)[-1], 10),p))
        nav+=f'<div class="navgroup">{E(labels[idx])}</div>'
        for p in children:
            nav+=f'<a class="navlink {"active" if p==ident else ""}" href="{href(base,lang,p)}">{E(title(pages[p][lang]))}</a>'
    links=''.join(f'<a class="lang {"selected" if l==lang else ""}" href="{href(base,l,ident)}">{label}</a>' for l,label in zip(LANGS,['EN','日本語','中文']))
    body,headings=render(text,base)
    toc=''.join(f'<a class="toc-{tag}" href="#{anchor}">{E(label)}</a>' for tag,anchor,label in headings)
    edit=f'{base}edit/?page={ident}&amp;lang={lang}'
    new=f'{base}edit/?new=1&amp;lang={lang}'
    issue=f'<a href="https://github.com/{E(repo)}/issues/new" rel="noopener noreferrer">{ui[7]}</a>' if repo else ''
    path='content/'+ident+'/'+lang+'.md'
    github=f'<a href="https://github.com/{E(repo)}/commits/HEAD/{E(path)}" rel="noopener noreferrer">History</a>' if repo else ''
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="referrer" content="no-referrer"><title>{E(title(text))} · SRD Handbook</title><link rel="stylesheet" href="{base}style.css"><link rel="stylesheet" href="{base}syntax.css"><script defer src="{base}read.js"></script></head><body data-base="{base}" data-lang="{lang}"><header><a class="brand" href="{href(base,lang,'home')}"><span class="logo">SRD</span><span>Manipulation Handbook<small>{ui[0]}</small></span></a><div class="headlinks">{links}<a class="editbutton" href="{edit}">{ui[3]}</a></div></header><div class="layout"><aside class="sidebar"><input id="search" type="search" placeholder="{ui[1]}" aria-label="{ui[1]}"><div id="results" hidden></div><nav id="nav">{nav}</nav><a class="newlink" href="{new}">＋ {ui[4]}</a></aside><main><div class="crumb">SRD / {E(CHAPTERS[ident.split('/')[0]][idx]) if ident!='home' else ui[6]}</div><article>{body}</article><footer><a href="{edit}">{ui[3]}</a>{github}{issue}<span>{ui[5]} · SRD</span></footer></main><aside class="toc"><strong>{ui[2]}</strong>{toc}</aside></div></body></html>'''

def build(output,repo):
    pages=scan()
    if 'home' not in pages: raise ValueError('Missing home page')
    for p,versions in pages.items():
        if set(versions)!=set(LANGS): raise ValueError(f'Missing languages: {p}')
        for s in versions.values(): title(s)
    if output.exists(): shutil.rmtree(output)
    output.mkdir(parents=True)
    for p in (ROOT/'web').iterdir():
        if p.is_file() and p.name!='editor.html': shutil.copy(p,output/p.name)
    shutil.copytree(ROOT/'assets',output/'assets',dirs_exist_ok=True)
    shutil.copytree(ROOT/'vendor',output/'vendor',dirs_exist_ok=True)
    write(output/'syntax.css',HtmlFormatter().get_style_defs('.codebox'))
    for lang in LANGS:
        search=[]
        for ident,versions in pages.items():
            text=versions[lang]; write(output/lang/ident/'index.html',page_html(ident,lang,text,pages,repo))
            search.append({'id':ident,'title':title(text),'text':text})
        dump(output/f'search-{lang}.json',search)
    write(output/'edit/index.html',read(ROOT/'web/editor.html').replace('__REPO__',E(repo)))
    write(output/'index.html','<!doctype html><html><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=en/home/"><title>SRD Handbook</title></head><body><a href="en/home/">Open handbook</a> · <a href="ja/home/">日本語</a> · <a href="zh/home/">中文</a></body></html>')
    write(output/'.nojekyll','')
    print(f'Built {len(pages)*3} static pages in {output}')

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--output',default=str(ROOT/'site')); p.add_argument('--repo',default=os.environ.get('GITHUB_REPOSITORY','')); a=p.parse_args()
    if a.repo and not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',a.repo): raise ValueError('Invalid repo')
    output=Path(a.output).resolve()
    if output!=ROOT/'site' and (output.exists() or ROOT in output.parents): raise ValueError('Use site/ or a new external output directory.')
    build(output,a.repo)
