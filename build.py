"""Build Tendwell. Python 3 standard library; no network or secrets required."""
import json,html,re,shutil
from pathlib import Path
from datetime import date
from interactive import finder,routine,checklist
ROOT=Path(__file__).resolve().parent; DIST=ROOT/'dist'; DATA=ROOT/'data'
E=lambda s:html.escape(str(s),quote=True)
P=json.loads((DATA/'products.json').read_text(encoding='utf8'))
A=json.loads((DATA/'articles.json').read_text(encoding='utf8')) if (DATA/'articles.json').exists() else []
GUIDE_BY_ID={a['page_id']:a for a in A}
GUIDE_ROUTES=json.loads((DATA/'guide-routes.json').read_text(encoding='utf8'))
C={
'robots':('Robot vacuums','Everyday floors, handled.','Match your floors, furniture and pet routine to a robot that fits.','B0DHCJ571Z',['Measure furniture clearance and transitions.','Plan space to open and service the dock.','Check mop care, replacement parts and floor compatibility.']),
'floors':('Floor care','For the mess a robot misses.','Explore wet-dry cleaners and the trade-offs behind a one-pass promise.','B0F138D56C',['Confirm the surfaces approved by the exact manual.','Compare dirty-water tank and roller cleaning routines.','Check weight, reach and storage before buying.']),
'laundry':('Laundry','Make room for a better routine.','Capacity, connections and installation come before the feature list.','B0BJ73MYQY',['Measure the full installation space, including hoses and door swing.','Confirm electrical, gas, drain and ventilation requirements.','Separate washing capacity from drying capacity.']),
'lawns':('Lawn care','Less mowing. More weekend.','Choose for your actual lawn, including slopes, gates and narrow paths.','B0DRG2HMD2',['Measure mowable grass rather than total lot size.','Check slopes at boundaries as well as across the lawn.','Confirm the navigation and docking requirements of the exact variant.']),
'pools':('Pool care','A clearer path to pool time.','Understand floor cleaners, waterline scrubbing and surface skimmers.','B0DPMDQ2RD',['Separate floor, wall, waterline and floating-debris jobs.','Check pool geometry, shallow areas and retrieval weight.','Compare filter cleaning and charging routines.']),
'windows':('Window care','Think beyond the glass.','Check access, window dimensions and anchoring before automating.','B0GJDQ59J1',['Check minimum pane dimensions and compatible glass types.','Plan safe access and an approved safety-cord anchor.','Allow time to move the robot and clean its pads.']),
'dishes':('Dishwashers','Find a place for one less chore.','Countertop convenience and built-in capacity need different plans.','B08JWZZ7QG',['Measure dishes, counter depth and the open door.','Confirm water supply, drainage and electrical requirements.','Compare usable racks and installation costs.'])}
BY={p['asin']:p for p in P}
def category(a):
 n=int(a['page_id'][1:]);return 'robots' if n<=12 else 'lawns' if n<=20 else 'pools' if n<=28 else 'laundry' if n<=36 else 'floors' if n<=43 else 'windows' if n<=46 else 'dishes'
def aurl(a):return a['url']
def purl(p):return '/products/'+p['slug']+'/'
def band(p):return '$300–499' if p['budget_snapshot']<500 else '$500–999' if p['budget_snapshot']<1000 else '$1,000+'
def image(p,cls='',lazy=True):return f'<img class="{cls}" src="{E(p["image"])}" alt="{E(p["name"])}" width="560" height="560" loading="{"lazy" if lazy else "eager"}">' if p.get('image') else '<span>Product image unavailable</span>'
def shell(title,body,desc='',active='',path='/'):
 nav=''.join(f'<a href="{url}" '+('aria-current="page"' if active==label else '')+f'>{label}</a>' for url,label in [('/products/','Explore products'),('/guides/','Buying guides'),('/compare/','Compare'),('/method/','Our approach')])
 return f'''<!doctype html><html lang="en-US"><head><meta charset="utf-8"><meta name="google-site-verification" content="Q_7qT1MMAPMG2ypmXnXRJOFmGV104rJQTGo163gKCbc"><script src="/assets/analytics.js" defer></script><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>{E(title)} | Tendwell</title><meta name="description" content="{E(desc or title)}"><meta name="theme-color" content="#193e38"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/style.css"><script src="/assets/app.js" defer></script></head><body><a class="skip" href="#main">Skip to content</a><div class="topline">Less upkeep. More living.</div><header><a class="logo" href="/" aria-label="Tendwell home"><span class="logo-mark" aria-hidden="true">t<span>·</span></span>Tendwell</a><button class="menu-toggle" aria-controls="main-nav" aria-expanded="false">Menu <span>☰</span></button><nav id="main-nav" aria-label="Main">{nav}</nav></header><main id="main">{body}</main><footer><div class="footer-top"><div><a class="logo" href="/">Tendwell</a><p>Practical research for a home<br>that asks a little less of you.</p></div><div><b>Explore</b><a href="/products/">Product directory</a><a href="/guides/">All buying guides</a><a href="/compare/">Your comparison</a></div><div><b>How we work</b><button type="button" onclick="window.tendwellAnalyticsPreferences()">Analytics preferences</button><a href="/method/">Research & editorial approach</a><a href="/disclosure/">Affiliate disclosure</a><a href="/privacy/">Privacy</a></div></div><div class="footer-bottom"><span>© 2026 Tendwell · US buying guides</span><span>Research-based. No hands-on testing claimed.</span></div><p class="disclosure">We may earn a commission when you buy through our affiliate links. Retailers set current prices, availability and purchase terms. <a href="/disclosure/">Learn more</a>.</p></footer><div id="compare-tray" hidden><span id="compare-count"></span><a href="/compare/">View comparison →</a><button id="clear-compare" aria-label="Clear comparison">Clear</button></div><div id="notice" role="status" aria-live="polite"></div></body></html>'''
def write(path,title,body,desc='',active=''):
 dest=DIST/path.lstrip('/')/'index.html';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(shell(title,body,desc,active,path),encoding='utf8')
def heading(eyebrow,title,desc):return f'<section class="page-head wrap"><p class="eyebrow">{E(eyebrow)}</p><h1>{E(title)}</h1><p class="lead">{E(desc)}</p></section>'
def card(p):
 return f'''<article class="product-card" data-cat="{p['category']}" data-brand="{E(p['brand'])}" data-price="{p['budget_snapshot']}" data-search="{E((p['name']+' '+C[p['category']][0]).lower())}"><a class="product-art" href="{purl(p)}">{image(p)}<span class="art-arrow" aria-hidden="true">↗</span></a><div class="card-body"><p class="eyebrow">{E(C[p['category']][0])}</p><h3><a href="{purl(p)}">{E(p['name'])}</a></h3><p class="budget">{band(p)} <span>catalog range</span></p><div class="card-bottom"><a href="{purl(p)}">View profile →</a><button class="compare-btn" data-asin="{p['asin']}" aria-pressed="false">+ Compare</button></div></div></article>'''
def guidecard(a):
 cat=category(a);return f'<article class="guide-card" data-cat="{cat}" data-search="{E((a["title"]+" "+a.get("dek","")).lower())}"><a class="guide-card-image" href="{aurl(a)}" aria-label="Read {E(a['title'])}"><img src="/assets/guide-{E(a['page_id'])}.svg" alt="{E(a['title'])} — topic illustration" width="900" height="360" loading="lazy"></a><p class="eyebrow">{E(C[cat][0])} <span> / Guide</span></p><h3><a href="{aurl(a)}">{E(a["title"])}</a></h3><p>{E(a.get("dek",""))}</p><a class="read-link" href="{aurl(a)}">Read the guide <span>↗</span></a></article>'
def grids(items,kind='product'):return '<div class="'+('product-grid' if kind=='product' else 'guide-grid')+'">'+''.join(card(x) if kind=='product' else guidecard(x) for x in items)+'</div>'
def disclosure():return '<p class="inline-disclosure">This page may contain affiliate links. We may earn a commission if you buy. <a href="/disclosure/">How this works</a>.</p>'
def home():
 hero=BY['B0DHCJ571Z']
 body=f'''<section class="hero wrap"><div class="hero-copy"><p class="eyebrow"><span class="tiny-dot"></span> Thoughtful choices. Easier routines.</p><h1>Less to do.<br><em>More room</em><br>to live.</h1><p>Find the home helpers that fit your space, your routine, and the jobs you’d happily hand over.</p><div class="actions"><a class="button" href="#home-finder">Find your home helper <span>↗</span></a><a class="text-link" href="/guides/">Start with a guide →</a></div><div class="hero-note"><span>01 — 07</span><p>From the kitchen floor<br>to the far end of the lawn.</p></div></div><div class="hero-art"><div class="art-caption"><span>THE EVERYDAY EDIT</span><span>01 / FLOORS</span></div><div class="hero-circle"></div>{image(hero,'hero-product',False)}<div class="hero-product-label"><div><small>Meet the category</small><b>Robot vacuums & mops</b></div><a href="/categories/robots/" aria-label="Explore robot vacuums">↗</a></div></div></section><section class="principles wrap"><span>Designed around your home</span><span>Multiple brands, clear trade-offs</span><span>Source-linked buying guidance</span></section><section class="wrap section"><div class="section-head"><div><p class="eyebrow">Start with the chore</p><h2>What would you like<br>off your list?</h2></div><p>Different homes need different help.<br>Choose the job before the gadget.</p></div><div class="category-grid">'''
 for i,(k,c) in enumerate(C.items()):body+=f'<a class="category-tile" href="/categories/{k}/"><span class="category-number">0{i+1}</span><h3>{c[0]}</h3><p>{c[1]}</p><span class="category-arrow">↗</span></a>'
 body+='</div></section>'
 body=body.replace('<section class="wrap section">',finder(C,GUIDE_BY_ID)+'<section class="wrap section">',1)
 featured=[next((a for a in A if a['page_id']==id),None) for id in ['p03','p14','p34']];featured=[a for a in featured if a]
 body+='<section class="guide-band"><div class="wrap section"><div class="section-head"><div><p class="eyebrow">A good place to begin</p><h2>Buy for your life.<br>Not the longest feature list.</h2></div><a class="text-link" href="/guides/">Explore all guides ↗</a></div>'+grids(featured,'guide')+'</div></section>'
 body+='<section class="wrap section"><div class="section-head"><div><p class="eyebrow">Explore the directory</p><h2>Big decisions,<br>made more manageable.</h2></div><a class="text-link" href="/products/">See all 50 products ↗</a></div>'+grids([BY[x] for x in ['B0DHCJ571Z','B0DPMDQ2RD','B0GJDQ59J1','B0F138D56C']])+'</section>'
 body+='''<section class="approach wrap"><div><p class="eyebrow">The Tendwell approach</p><h2>Useful questions.<br>Honest answers.</h2><a class="button light" href="/method/">How we research →</a></div><div><p>Will it fit? What still needs doing? Which version are you actually buying?</p><p>We bring product information and practical buying questions together, with sources you can check. These are research-based guides, not laboratory reviews.</p></div></section>'''
 write('/','Less upkeep. More living.',body,'Research-based guides to robot vacuums, lawn mowers, pool cleaners and home appliances. Find the right fit for your home.')
def filters(kind,selected=''):
 cats='<option value="">Every chore</option>'+''.join(f'<option value="{k}" '+('selected' if k==selected else '')+f'>{c[0]}</option>' for k,c in C.items())
 extra=''
 if kind=='products':extra='<label>Budget range<select id="budget"><option value="">Any budget</option><option value="300">$300–499</option><option value="500">$500–999</option><option value="1000">$1,000+</option></select></label><label>Brand<select id="brand"><option value="">All brands</option>'+''.join(f'<option>{E(x)}</option>' for x in sorted(set(p['brand'] for p in P)))+'</select></label>'
 return f'<form class="filters" data-kind="{kind}" onsubmit="return false"><label class="search-field">Search<input id="search" type="search" placeholder="{"Search a model or brand" if kind=="products" else "Search guides and questions"}" autocomplete="off"></label><label>Chore<select id="category">{cats}</select></label>{extra}<button type="reset" class="reset">Reset</button></form><p id="result-count" class="result-count" aria-live="polite"></p><p id="empty-state" hidden>No matches. Try another search or reset your filters.</p>'
def directories():
 body=heading('The product directory','Choose your kind of help.','Explore 50 home-care products selected from US catalogs at $300 and up. Compare the fit before checking the current offer.')
 body+='<section class="wrap directory">'+filters('products')+'<p class="small-note">Budget ranges reflect catalog snapshots from October 24–26, 2026, not current prices. Check the retailer for the exact variant and final total.</p>'+grids(P)+'</section>'
 write('/products/','Explore home-care products',body,active='Explore products')
 body=heading('The reading room','A little research goes a long way.','Practical buying guides, model comparisons and the questions worth asking before a major home purchase.')+'<section class="wrap directory">'+filters('guides')+grids(A,'guide')+'</section>'
 write('/guides/','Home-care buying guides',body,active='Buying guides')
 for k,c in C.items():
  ps=[p for p in P if p['category']==k];aa=[a for a in A if category(a)==k]
  body=heading('Find help / '+c[0],c[1],c[2])+f'<section class="wrap category-intro"><div class="category-image">{image(BY[c[3]])}</div><div><p class="eyebrow">Before you shortlist</p><h2>Three checks<br>worth making.</h2><ol>'+''.join('<li>'+E(x)+'</li>' for x in c[4])+'</ol><a class="text-link" href="/compare/">Compare your choices →</a></div></section><section class="wrap section"><div class="section-head"><h2>Explore the products</h2><span>'+str(len(ps))+' catalog profiles</span></div>'+grids(ps)+'</section><section class="guide-band"><div class="wrap section"><div class="section-head"><h2>Read before you buy</h2><a href="/guides/">All guides →</a></div>'+grids(aa,'guide')+'</div></section>'
  body=body.replace('<section class="wrap section">',routine(k)+'<section class="wrap section">',1)
  write('/categories/'+k+'/',c[0]+' buying guides & products',body)
def decision_table(rows):
 return '<div class="decision-table" tabindex="0" role="region" aria-label="Home fit checklist"><table><thead><tr><th scope="col">Your home</th><th scope="col">What matters</th><th scope="col">Before you choose</th></tr></thead><tbody>'+''.join('<tr>'+''.join('<'+('th scope="row"' if i==0 else 'td')+'>'+E(v)+'</'+('th' if i==0 else 'td')+'>' for i,v in enumerate(row))+'</tr>' for row in rows)+'</tbody></table></div>'

def products():
 for p in P:
  c=C[p['category']];e=p.get('evidence',[])
  aa=sorted([a for a in A if category(a)==p['category']],key=lambda a:(p['asin'] not in a.get('product_asins',[]),a['page_id']))[:3]
  def buy(placement):
   return f'<a class="button" data-product-id="{E(p["asin"])}" data-placement="{placement}" rel="sponsored noopener" href="{E(p["buy_url"])}" target="_blank">Buy on Amazon ↗</a>' if p.get('buy_url') else '<p>A verified purchase link is currently unavailable.</p>'
  facts=[t for x in e for t in x.get('facts',[])]
  limits=[t for x in e for t in x.get('limits',[])]
  sources=''.join(f'<li><a href="{E(x["official_url"])}" rel="noopener" target="_blank">{E(x["model"])} — manufacturer source</a></li>' for x in e if x.get('official_url'))
  ul=lambda xs:'<ul>'+''.join('<li>'+E(t)+'</li>' for t in xs)+'</ul>'
  related=[x for x in P if x['category']==p['category'] and x['asin']!=p['asin']]
  related.sort(key=lambda x:abs(x['budget_snapshot']-p['budget_snapshot']))
  body=f'<div class="wrap breadcrumbs"><a href="/products/">Products</a> / <a href="/categories/{p["category"]}/">{c[0]}</a></div><section class="wrap product-detail" id="product-hero"><div class="detail-art">{image(p,lazy=False)}<p class="small-note">Product image. Confirm the selected variant on Amazon.</p></div><div class="detail-summary"><p class="eyebrow">{E(p["brand"])} / {c[0]}</p><h1>{E(p["name"])}</h1><dl class="product-metrics"><dt>Rating</dt><dd>Not independently verified</dd><dt>Review count</dt><dd>See current Amazon listing</dd><dt>Current price</dt><dd>Check Amazon for the live price</dd></dl><p class="small-note">Historical catalog range: {band(p)} · {E(p["price_date"])}. This is not a live offer.</p>{disclosure()}<div class="actions">{buy("product_summary")}<button class="compare-btn button secondary" data-asin="{p["asin"]}" aria-pressed="false">+ Compare</button></div></div></section>'
  snapshot=p.get('offer_snapshot')
  if snapshot:
   body+='<section class="wrap offer-context" aria-label="Dated price reference"><p class="eyebrow">Price context · checked November 11, 2026</p><h2>A dated reference for your budget</h2><p>The affiliate catalog reported <strong>$'+format(snapshot['price_usd'],',.2f')+'</strong> for this ASIN, with a source update dated '+E(snapshot['source_updated_at'])+'. This is a historical catalog snapshot, not a live Amazon price or a guaranteed offer.</p>'
   if snapshot.get('coupon_reported') or snapshot.get('discount_reported') not in [None,'0%']:
    body+='<p>Promotional pricing was reported in the catalog. Check whether any coupon requires selection, applies to this exact variation, or is already included in the displayed price. We have not confirmed coupon stacking or eligibility.</p>'
   body+='<p>Confirm the selected model, seller, final price and return terms on Amazon before buying.</p>'+buy('price_context')+'</section>'
  body+='<nav class="wrap product-jumps" aria-label="Product sections">'+''.join(f'<a href="#{key}">{title}</a>' for key,title in [('benefits','Benefits'),('specs','Specifications'),('features','Features'),('usage','Use at home'),('details','Details'),('included','In the box'),('reviews','Reviews'),('faq','FAQ'),('related','Alternatives')])+'</nav>'
  body+='<div class="wrap detail-body"><article class="prose">'
  if p['slug']=='roborock-saros-10r':
   body+='<section class="quick-answer"><h2>Is the Saros 10R a fit for your home?</h2><p>Start with clearance and connectivity. Roborock’s US information lists a 3.14-inch body and 2.4 GHz Wi-Fi support. Measure the entire route and dock service space before ordering; body height alone does not establish access in every setup.</p><p>Compare the stated automatic mop detachment with your carpet routine, and check the current US package. Our source-based assessment does not establish measured pet-hair pickup or obstacle-avoidance reliability.</p><a href="/blog/roborock-saros-10r-robot-vacuum/">Plan furniture clearance and dock placement →</a></section>'
  if p.get('decision_rows'):body+='<section><h2>Match this model to your home</h2>'+decision_table(p['decision_rows'])+'<p>These are source-based buying checks, not a comparative performance ranking.</p></section>'
  body+='<section id="benefits"><h2>Key benefits to evaluate</h2><p>Match this model to the job you need done. The checks below help you assess fit; they are not measured performance claims.</p>'+ul(c[4])+'</section>'
  body+=f'<section id="specs"><h2>Key specifications</h2><table><tbody><tr><th scope="row">Model</th><td>{E(p["name"])}</td></tr><tr><th scope="row">Brand</th><td>{E(p["brand"])}</td></tr><tr><th scope="row">US ASIN</th><td>{E(p["asin"])}</td></tr><tr><th scope="row">Category</th><td>{c[0]}</td></tr></tbody></table><p>Dimensions, capacity and compatibility must be checked against the exact model manual and selected package.</p></section>'
  body+='<section id="features"><h2>Product features</h2>'+ (ul(facts) if facts else '<p>Detailed manufacturer specifications have not yet been verified for this listing. Check its manual before relying on feature claims.</p>')+'<ul class="sources">'+sources+'</ul></section>'
  body+='<section id="usage"><h2>Application & usage scenarios</h2><p>'+E(c[2])+'</p><p>Before choosing this product, work through the space, compatibility and maintenance checks below.</p>'+checklist(c[4])+'</section>'
  body+='<section id="details"><h2>Product details & version checks</h2><p>'+E(p['catalog_title'])+'</p><p>This is the catalog description, not an independent performance verdict. Similar names can refer to different generations, capacities or bundles.</p>'+ul(limits)+'</section>'
  body+='<section id="included"><h2>What’s included</h2><p>Package contents have not been verified for this exact Amazon offer. Check the selected variation and “What’s in the box” on Amazon. Do not assume accessories shown in a product image are included.</p></section>'
  body+='<section id="reviews"><h2>Customer reviews</h2><p>We have not verified a customer-review dataset for this exact listing, so we do not publish a star rating, review count or customer quotations here.</p><p>On Amazon, look for reviews of the same model and generation. Read recent critical reviews alongside positive ones, paying attention to your floor type, home layout and maintenance expectations.</p>'+buy('customer_reviews')+'</section>'
  faq=[('Is this a hands-on review?','No. This page combines catalog identification, available manufacturer information and buying checks. We have not independently tested this product.'),('Where can I check the current price and rating?','Open the exact Amazon US listing. Price, review count, availability and seller terms may change.'),('How do I avoid buying the wrong version?','Match the model name and ASIN '+p['asin']+' to the selected offer. Verify the capacity, generation and package contents before ordering.'),('What should I check before ordering?', ' '.join(c[4]))]
  body+='<section id="faq"><h2>Frequently asked questions</h2>'+''.join('<details><summary>'+E(q)+'</summary><p>'+E(a)+'</p></details>' for q,a in faq)+'</section></article></div>'
  body+='<section id="related" class="wrap section"><h2>Related products to compare</h2><p>Other listings in this category, ordered by proximity to the historical catalog budget. These are comparison options, not equivalent-performance claims.</p>'+grids(related[:3])+'</section>'
  body+='<section class="wrap section"><h2>Guides for your decision</h2>'+grids(aa,'guide')+'</section>'
  body+='<section class="wrap section final-product-cta"><h2>Check the exact offer before you buy</h2><p>Confirm the model, accessories, seller and return terms on Amazon.</p>'+disclosure()+buy('product_bottom')+'</section>'
  write(purl(p),p['name']+' — features, specifications & buying guide',body,'Explore '+p['name']+' specifications, version checks, buying questions and related products. Check the current Amazon US offer.')


REGIONAL_CONTEXT={
'robots':('Southwest: dry grit at the entryway','For an Arizona or New Mexico household dealing with tracked-in dust, separate routine dry floor pickup from wet spills. Clear cords and small objects before a scheduled run, and check the exact robot manual for debris and surface restrictions. A cleaning robot is not an air purifier or a dust-storm safety measure.','https://www.weather.gov/safety/wind-dust-storm','National Weather Service: dust storms'),
'floors':('Northeast & Great Lakes: the winter entryway','Consider a home where boots bring slush and deicing residue into a mudroom. Contain wet footwear at the door, identify the floor finish, and follow its care instructions before choosing a machine or detergent. Do not assume a dry vacuum can collect liquids, or that every wet-dry cleaner can collect salt and grit.','',''),
'laundry':('Pacific Northwest: laundry after a wet commute','Consider a small apartment with rain jackets, muddy clothes and limited drying space. Check garment care labels, usable drying capacity and the actual utility connections before comparing appliances. A standalone washer needs a separate drying plan; a compact footprint does not establish installation compatibility.','',''),
'lawns':('Southeast & rolling suburbs: map the lawn first','For a sloped suburban yard, measure mowable grass rather than the whole property. Mark steep edges, drainage channels, narrow gates and separate lawn zones. Check boundary-slope limits separately from working-area slope, and match navigation requirements to trees and buildings on your own lot. These are site checks, not a claim that one mower suits an entire state.','',''),
'pools':('Sun Belt: separate floating debris from submerged dirt','For a Florida, Texas or Arizona backyard pool, first identify where debris collects: the surface, floor, walls or waterline. A floor-and-wall robot does not automatically skim floating leaves. Compare access, steps, retrieval and filter cleaning against your pool, and keep the existing water-treatment routine.','',''),
'windows':('Coastal homes: access matters more than window count','For a coastal home with exterior window residue, check whether both sides of the glass are safely accessible. Confirm compatible glass, minimum pane size and an approved safety anchor. A window robot still needs setup, pad care and movement between panes; it does not remove the need for safe access.','',''),
'dishes':('Northeast city apartments: fit the kitchen you have','For a compact city kitchen, measure counter depth, cabinet clearance, the open door and your largest plates. Confirm permitted faucet connections and drainage with your building before ordering. Countertop, portable and built-in dishwashers solve different installation problems; compare the exact type rather than the product photo.','','')
}

def article_visual(a,k):
 scenes={
 'robots':'<rect x="55" y="65" width="180" height="100" rx="10"/><rect x="210" y="210" width="180" height="80" rx="8"/><path d="M70 240H180V190H340" stroke-dasharray="9 9"/><circle cx="340" cy="190" r="36"/><circle cx="340" cy="190" r="10"/>',
 'floors':'<path d="M70 90H390M70 170H390M70 250H390M150 40V300M310 40V300" opacity=".3"/><path d="M250 65L210 245"/><rect x="150" y="245" width="130" height="40" rx="12"/><circle cx="100" cy="190" r="7"/><circle cx="120" cy="210" r="5"/>',
 'laundry':'<rect x="100" y="40" width="240" height="270" rx="18"/><path d="M100 100H340"/><circle cx="220" cy="200" r="78"/><circle cx="220" cy="200" r="58"/><circle cx="300" cy="70" r="9"/><path d="M130 70H190"/>',
 'lawns':'<path d="M50 260Q130 80 230 170T410 100V310H50Z" fill="#dbe7ce"/><path d="M80 245Q140 140 230 200T380 145" stroke-dasharray="8 8"/><rect x="200" y="170" width="80" height="50" rx="20"/><circle cx="215" cy="220" r="12"/><circle cx="265" cy="220" r="12"/>',
 'pools':'<rect x="50" y="55" width="360" height="250" rx="70" fill="#d6e7e8"/><path d="M75 130Q120 110 165 130T255 130T345 130"/><rect x="220" y="220" width="75" height="45" rx="15"/><path d="M110 95q20-40 40-5q-20 35-40 5"/>',
 'windows':'<rect x="85" y="35" width="280" height="280"/><path d="M225 35V315M85 175H365"/><rect x="120" y="80" width="60" height="70" rx="15"/><path d="M150 150Q180 210 120 290" stroke-dasharray="7 7"/>',
 'dishes':'<rect x="75" y="45" width="310" height="270" rx="15"/><path d="M75 100H385M110 270H350"/><circle cx="150" cy="195" r="48"/><circle cx="230" cy="195" r="48"/><path d="M300 150h35v90h-35z"/><circle cx="345" cy="72" r="8"/>'
 }
 name='guide-'+a['page_id']+'.svg'
 svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 360"><rect width="900" height="360" rx="20" fill="#eeeadd"/><g stroke="#31594c" stroke-width="5" fill="#faf9f4" stroke-linecap="round" stroke-linejoin="round">'+scenes[k]+'</g><text x="475" y="90" font-family="Arial" font-size="17" fill="#31594c">TENDWELL · BUYING NOTES</text>'
 import textwrap
 for j,line in enumerate(textwrap.wrap(a['title'],28)):svg+='<text x="475" y="'+str(140+j*35)+'" font-family="Georgia" font-size="27" fill="#223c36">'+E(line)+'</text>'
 svg+='<text x="475" y="315" font-family="Arial" font-size="15" fill="#64716a">Space · Compatibility · Everyday upkeep</text></svg>'
 (DIST/'assets'/name).write_text(svg,encoding='utf8')
 return '<figure class="guide-illustration"><img src="/assets/'+name+'" width="900" height="360" alt="'+E(a['title'])+' — '+E(C[k][0])+' planning illustration"><figcaption>Original Tendwell illustration. A planning aid, not a product test or scale drawing.</figcaption></figure>'

def articles():
 for a in A:
  k=category(a);c=C[k];secs=a['sections'];related=[GUIDE_BY_ID[x] for x in GUIDE_ROUTES[a['page_id']]]
  exact=[BY[x] for x in a.get('product_asins',[]) if x in BY];ps=exact[:3]
  body=f'<div class="wrap breadcrumbs"><a href="/guides/">Guides</a><span>/</span><a href="/categories/{k}/">{c[0]}</a></div><section class="article-head wrap"><p class="eyebrow">The buying guide / {E(c[0])}</p><h1>{E(a["title"])}</h1><p class="lead">{E(a.get("dek",""))}</p><div class="article-meta">Research-based guide <span>·</span> Updated {E(a.get("updated_at","October 26, 2026"))} <span>·</span> No hands-on testing</div>{disclosure()}</section><div class="article-layout wrap"><aside class="toc"><p class="eyebrow">In this guide</p>'+''.join(f'<a href="#section-{i}">{E(s["heading"])}</a>' for i,s in enumerate(secs))+'</aside><article class="prose article-copy">'
  body+=article_visual(a,k)
  if a.get("decision_rows"):body+='<section><h2>Choose for your pet-care routine</h2>'+decision_table(a["decision_rows"])+'</section>'
  body+='<section class="quick-answer" aria-label="Quick answer"><h2>The short answer</h2><p>'+E(a.get('dek',''))+'</p><ul>'+''.join('<li><a href="#section-'+str(i)+'">'+E(sec['heading'])+'</a></li>' for i,sec in enumerate(secs[:3]))+'</ul></section>'
  region,context,source,source_label=REGIONAL_CONTEXT[k]
  body+='<section class="regional-context"><p class="eyebrow">US household scenario</p><h2>'+E(region)+'</h2><p>'+E(context)+'</p><p class="small-note">An illustrative household scenario, not a local product test. Conditions vary by home and season.</p>'
  if source:body+='<a href="'+source+'" rel="noopener" target="_blank">'+E(source_label)+'</a>'
  if ps and a.get('show_products',True):
   lead=ps[0]
   body+='<figure class="article-product-visual"><a href="'+purl(lead)+'">'+image(lead)+'</a><figcaption>'+E(lead['name'])+' — product reference image, not a photo of testing in this region.</figcaption></figure><p>For the exact model, available source details and version checks, see <a href="'+purl(lead)+'">'+E(lead['name'])+' buying guide</a>. Match its manual to the conditions above before ordering.</p>'
  else:
   body+='<div class="scenario-steps" role="img" aria-label="Planning sequence: identify the household job, check compatibility, confirm maintenance"><span>1 · Identify the job</span><span>2 · Check compatibility</span><span>3 · Plan upkeep</span></div>'
  body+='</section>'
  for i,s in enumerate(secs):
   body+=f'<section id="section-{i}"><h2>{E(s["heading"])}</h2>'+''.join('<p>'+E(p)+'</p>' for p in s.get('paragraphs',[]))
   if s.get('bullets'):body+='<ul>'+''.join('<li>'+E(p)+'</li>' for p in s['bullets'])+'</ul>'
   if s.get('internal_links'):body+='<p class="context-links">'+ ' · '.join('<a href="'+E(link['url'])+'">'+E(link['label'])+'</a>' for link in s['internal_links'])+'</p>'
   body+='</section>'
  body+='<section class="source-panel"><p class="eyebrow">Check the details</p><h2>Sources & scope</h2><p>We use manufacturer information to describe stated features. It does not prove real-world performance or make every version equivalent. Confirm current US specifications and the exact bundle before buying.</p><ul class="sources">'+''.join(f'<li><a href="{E(s["url"])}" rel="noopener" target="_blank">{E(s["title"])} ↗</a></li>' for s in a.get('sources',[]))+'</ul><a href="/method/">Read our research approach →</a></section></article></div>'
  if ps and a.get('show_products',True):body+='<section class="wrap section"><div class="section-head"><div><p class="eyebrow">Keep exploring</p><h2>Products to research further</h2><p>Check the exact version. These are catalog examples, not a ranked test result.</p></div></div>'+grids(ps)+'</section>'
  body+='<section class="guide-band"><div class="wrap section"><h2>Related reading</h2>'+grids(related,'guide')+'</div></section>'
  write(aurl(a),a['title'],body,a.get('dek',''))
def other():
 body=heading('Your shortlist','Compare the fit.','Add up to three products from the directory. Compare catalog identity and practical requirements, then check the exact model’s manual.')+'<section class="wrap section"><div id="comparison"></div><p class="small-note">Budget ranges are dated catalog snapshots. This comparison does not assign performance scores or declare a winner.</p><a class="button" href="/products/">Explore products →</a></section>'
 write('/compare/','Compare your home-care shortlist',body,active='Compare')
 policies={
'method':('Our research approach','A useful guide should make the trade-offs clearer.',[
('Start with the job','We organize products around household jobs: floors, laundry, lawns, pools, windows and dishes. The directory focuses on products listed at US$300 or more in the catalogs used for this edition. A higher price is a scope choice, not a quality rating.'),
('Separate facts from performance','Our guides draw on linked manufacturer pages, manuals and product catalogs. We have not conducted hands-on tests of these products. A manufacturer’s specification is identified as such; it is not proof of results in every home. We do not publish invented scores, customer reviews or test awards.'),
('Keep variants separate','Model family names can hide different capacities, generations and packages. Product profiles show the US listing’s ASIN. A guide may discuss a family while a product profile covers a particular listing; confirm the seller’s included accessories and installation requirements.'),
('Explain commercial relationships','We may earn commissions through product links supplied by affiliate platforms, including PartnerBoost, Levanta, Wayward and ArtemisAds. Products are not ranked by commission. Editorial comparison pages can discuss products for which we have no affiliate link.'),
('Understand this edition','This is an initial research edition, prepared in October 2026. Some profiles have detailed manufacturer evidence; others establish catalog identity and the checks still needed. Budget ranges are snapshots, not live prices. Purchase links can change, and an unavailable link is not evidence that the product is discontinued.'),
('Sources and updates','Each guide provides its source links. Follow the exact US manual for installation, use and maintenance. This site does not monitor prices automatically. Editorial review and renewed link checks are required before a later edition is released.')]),
'disclosure':('Affiliate disclosure','How links support this site.',[
('Our affiliate links','Tendwell may receive a commission when a reader makes a qualifying purchase after following an affiliate link. Links labeled “Check price on Amazon” go to the selected Amazon US listing. We participate through affiliate platforms including PartnerBoost, Levanta, Wayward and ArtemisAds.'),
('Your purchase','The retailer or seller handles checkout, delivery, returns, warranty terms and customer service. Prices and stock can change. Confirm the model, included accessories, seller and final total before placing an order.'),
('Our content','Commercial eligibility does not establish cleaning quality or compatibility with your home. Our guides are research-based and do not claim personal use or laboratory testing. No consumer ratings are generated from selected reviews.')]),
'privacy':('Privacy','A small site with a simple data footprint.',[
('Browsing this site','This site uses Google Analytics and Microsoft Clarity only after you accept analytics. You can change this choice using Analytics preferences in the footer. The hosting provider may process technical access information under its own terms and privacy practices.'),
('Your comparison list','When you add a product to Compare, its product identifier is stored in your browser’s local storage. The site uses it to keep your shortlist between pages. Use “Clear” in the comparison bar or clear your browser’s site data to remove it.'),
('External websites','Affiliate links carry attribution parameters to the destination retailer and affiliate service. Those services may use cookies and other tracking technologies under their own policies. Opening a manufacturer source also takes you to an external website.'),
('Preview access','This edition is intended for a restricted owner preview. Hosting sign-in and access controls are provided by the hosting service. A public release requires review of operator contact details and any additional data collection.')])}
 for slug,(title,dek,sections) in policies.items():
  write('/'+slug+'/',title,heading('Tendwell',title,dek)+'<article class="wrap policy prose">'+''.join('<h2>'+E(h)+'</h2><p>'+E(p)+'</p>' for h,p in sections)+'</article>',active='Our approach' if slug=='method' else '')
 write('/404/','Page not found',heading('A small detour','This page isn’t here.','Head back to the directory or browse the buying guides.')+'<div class="wrap section"><a class="button" href="/">Back to home →</a></div>')
 shutil.copyfile(DIST/'404/index.html',DIST/'404.html')
def main():
 (DIST/'assets').mkdir(parents=True,exist_ok=True)
 for name in ['style.css','app.js','favicon.svg','analytics.js']:shutil.copyfile(ROOT/'src'/name,DIST/'assets'/name)
 public=[{k:p[k] for k in ['asin','name','brand','category','slug','budget_snapshot','price_date','image','catalog_title']} | {'checks':C[p['category']][4],'category_label':C[p['category']][0]} for p in P]
 (DIST/'assets/products.json').write_text(json.dumps(public,ensure_ascii=False),encoding='utf8')
 home();directories();products();articles();other()
 (DIST/'robots.txt').write_text('User-agent: *\nDisallow: /\n',encoding='utf8')
 # No sitemap submitted while this owner-only research edition remains noindex.
 print('Built',len(list(DIST.rglob('*.html'))),'HTML files;',len(P),'products;',len(A),'guides')
if __name__=='__main__':main()
