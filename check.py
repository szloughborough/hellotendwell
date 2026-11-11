"""Check generated HTML, local destinations, affiliate identity and packaging safety."""
import json,re
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
R=Path(__file__).resolve().parent;D=R/'dist'
class Page(HTMLParser):
 def __init__(self):super().__init__();self.refs=[];self.ids=set();self.h1=0;self.meta={};self.buy=[];self.imgs=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='h1':self.h1+=1
  if a.get('id'):self.ids.add(a['id'])
  if tag=='meta':self.meta[a.get('name')]=a.get('content')
  if tag in ['a','link','script','img']:
   v=a.get('href',a.get('src',''))
   if v:self.refs.append(v)
  if tag=='a' and 'amazon.com' in a.get('href',''):self.buy.append(a)
  if tag=='img':self.imgs.append(a)
pages={};errors=[]
for f in D.rglob('*.html'):
 p=Page();p.feed(f.read_text(encoding='utf8'));pages[f]=p
 if p.h1!=1:errors.append(str(f.relative_to(D))+': h1 count')
 if not p.meta.get('description'):errors.append(str(f)+': no description')
 if p.meta.get('robots')!='noindex,nofollow':errors.append(str(f)+': incorrect preview index policy')
 for im in p.imgs:
  if not im.get('alt') or not im.get('width') or not im.get('height'):errors.append(str(f)+': image accessibility/dimensions')
 for a in p.buy:
  if not all(x in a.get('rel','') for x in ['sponsored','noopener']):errors.append(str(f)+': affiliate rel')
for f,p in pages.items():
 for ref in p.refs:
  u=urlsplit(ref)
  if u.scheme or u.netloc:continue
  target=D/unquote(u.path).lstrip('/') if u.path.startswith('/') else f.parent/unquote(u.path) if u.path else f
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'{f.relative_to(D)} -> missing {ref}')
  elif u.fragment and target in pages and u.fragment not in pages[target].ids:errors.append(f'{f.relative_to(D)} -> missing anchor {ref}')
products=json.loads((R/'data/products.json').read_text(encoding='utf8'));articles=json.loads((R/'data/articles.json').read_text(encoding='utf8'))
if len(products)!=50 or len({p['asin'] for p in products})!=50:errors.append('Expected 50 unique ASINs')
if len(articles)!=50 or len({a['page_id'] for a in articles})!=50:errors.append('Expected 50 unique articles')
routes=json.loads((R/'data/guide-routes.json').read_text(encoding='utf8'))
by_id={a['page_id']:a for a in articles};incoming=set()
if set(routes)!=set(by_id):errors.append('Reading routes must cover every guide')
for src,targets in routes.items():
 if len(targets)!=len(set(targets)) or src in targets:errors.append('Duplicate/self reading route: '+src)
 for target in targets:
  if target not in by_id:errors.append('Unknown reading route: '+target);continue
  incoming.add(target)
  if src in by_id:
   source_page=D/by_id[src]['url'].strip('/')/'index.html'
   if by_id[target]['url'] not in pages[source_page].refs:errors.append('Missing rendered reading route: '+src+' -> '+target)
if set(by_id)-incoming:errors.append('Guides without curated incoming routes: '+str(sorted(set(by_id)-incoming)))
for p in products:
 if p.get('buy_url'):
  u=urlsplit(p['buy_url'])
  if u.hostname not in ['www.amazon.com','amazon.com'] or '/dp/'+p['asin'] not in u.path or p['link_status']!='verified':errors.append('Mismatched affiliate '+p['asin'])
 if p['budget_snapshot']<300:errors.append('Below threshold '+p['asin'])
for f in R.rglob('*'):
 if not f.is_file() or '.git' in f.parts:continue
 if f.name=='.env' or f.suffix=='.env' or f.name.startswith('api.env'):errors.append('Forbidden secret filename')
 if f.suffix in ['.json','.js','.html','.py','.md'] and re.search(r'Bearer\s+(?:aa\.oa2|sk-)',f.read_text(encoding='utf8',errors='ignore')):errors.append('Potential secret pattern')
word_counts=[sum(len(p.split()) for s in a['sections'] for p in s.get('paragraphs',[])) for a in articles]
report={'html_files':len(pages),'products':len(products),'articles':len(articles),'enabled_affiliate_ctas':sum(bool(p.get('buy_url')) for p in products),'manufacturer_matched_profiles':sum(bool(p.get('evidence')) for p in products),'unique_article_sources':len({s['url'] for a in articles for s in a.get('sources',[])}),'article_paragraph_word_range':[min(word_counts),max(word_counts)],'errors':errors,'index_policy':'owner-private preview, noindex/nofollow, robots disallow','browser_qa':'separate evidence required'}
print(json.dumps(report,ensure_ascii=True,indent=2));raise SystemExit(1 if errors else 0)
