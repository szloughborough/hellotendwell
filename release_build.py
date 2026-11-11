import json,subprocess,sys,shutil,html,xml.etree.ElementTree as ET
from pathlib import Path
R=Path(__file__).resolve().parent
c=json.loads((R/'release.json').read_text(encoding='utf8'));base=c['domain'].rstrip('/')
public=c.get('public_release_approved',False)
if public and (not c.get('operator_name') or '@' not in c.get('contact_email','')):raise SystemExit('Public release requires real operator and contact details.')
shutil.copytree(R/'public/products',R/'dist/assets/products',dirs_exist_ok=True)
subprocess.run([sys.executable,str(R/'build.py')],check=True,cwd=R)
subprocess.run([sys.executable,str(R/'check.py')],check=True,cwd=R)
urls=[]
for p in (R/'dist').rglob('*.html'):
 rel=p.relative_to(R/'dist').as_posix();path='/' if rel=='index.html' else '/'+rel.removesuffix('index.html')
 is404=rel in ['404.html','404/index.html'];s=p.read_text(encoding='utf8')
 if not is404:
  canonical=base+path;urls.append(canonical)
  s=s.replace('</head>','<link rel="canonical" href="'+html.escape(canonical,quote=True)+'"></head>')
 if public and not is404:s=s.replace('content="noindex,nofollow"','content="index,follow"')
 if public:
  s=s.replace('This edition is intended for a restricted owner preview. Hosting sign-in and access controls are provided by the hosting service. A public release requires review of operator contact details and any additional data collection.','This site is operated by '+html.escape(c['operator_name'])+'. Contact: '+html.escape(c['contact_email'])+'. Hosting is provided by Cloudflare.').replace('<h2>Preview access</h2>','<h2>Operator and contact</h2>')
 p.write_text(s,encoding='utf8')
root=ET.Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
for url in sorted(set(urls)):ET.SubElement(ET.SubElement(root,'url'),'loc').text=url
ET.ElementTree(root).write(R/'dist/sitemap.xml',encoding='utf-8',xml_declaration=True)
(R/'dist/robots.txt').write_text('User-agent: *\n'+('Allow: /\nSitemap: '+base+'/sitemap.xml\n' if public else 'Disallow: /\n'),encoding='utf8')
(R/'dist/_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n'+('' if public else '  X-Robots-Tag: noindex, nofollow\n'),encoding='utf8')
print('Release candidate:',len(set(urls)),'canonical URLs; public indexing:',public)
