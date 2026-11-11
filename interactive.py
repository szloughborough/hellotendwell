"""Editorial decision aids. No inferred product compatibility or performance scores."""
from html import escape as E

SCENARIOS={
'robots':[('Pet hair','p03','Brush access and recurring hair cleanup come first.'),('Rugs + hard floors','p02','Check how the mop avoids carpet and crosses transitions.'),('Hardwood floors','p05','Your flooring instructions set the water-use limit.')],
'floors':[('Everyday kitchen mess','p37','Compare washing with the cleanup required afterward.'),('Carpet spots','p41','Separate spot extraction from ordinary vacuuming.'),('Steam or wet pickup?','p43','Choose the cleaning process your surface permits.')],
'lawns':[('A small yard','p15','Narrow passages and dock placement can be the limiting factors.'),('About one acre','p14','Measure mowable grass, then allow time for charging.'),('Slopes and hills','p16','Check working-area and boundary slope limits separately.')],
'pools':[('An inground pool','p23','Document steps, ledges and the surfaces you need cleaned.'),('An above-ground pool','p24','Confirm liner compatibility and removal over the rim.'),('Floating leaves','p25','A surface skimmer does a different job from a floor cleaner.')],
'laundry':[('An apartment','p33','Confirm landlord approval, connections and delivery access.'),('A tight laundry space','p32','Measure service clearances as well as the appliance.'),('One machine or two?','p34','Compare a real laundry day, including overlapping loads.')],
'windows':[('Choosing my first robot','p44','Check pane size, safe access and setup between windows.'),('Considering W3 OMNI','p45','Match the exact model and included station.'),('Comparing W2S versions','p46','Keep W2S, OMNI and PRO OMNI specifications separate.')],
'dishes':[('Counter space available','p48','Measure the open door and the space below cabinets.'),('A portable floor unit','p47','Check faucet compatibility and the operating position.'),('Replacing a built-in','p50','Document the opening and the complete installation scope.')]
}
ROUTINES={
'robots':('Measure floors & dock','Clear cords and check the route','Empty, rinse or replace parts as the manual requires'),
'floors':('Confirm surface & solution','Fill, guide and move the washer','Empty dirty water; clean and dry components'),
'lawns':('Map boundaries & slopes','Check the lawn for obstacles','Inspect blades and maintain the map'),
'pools':('Confirm surfaces & retrieval','Deploy the supported cleaning mode','Lift out, rinse the filter and recharge if needed'),
'laundry':('Confirm connections & clearance','Sort loads and choose a cycle','Remove laundry and clean specified filters'),
'windows':('Check glass & safe anchoring','Position and move between panes','Clean cloths and store the equipment'),
'dishes':('Check water, drain & opening','Load suitable dishes and select a cycle','Unload and clean filters as instructed')}

def finder(categories,articles):
 out='<section id="home-finder" class="wrap decision-finder section" aria-labelledby="finder-title"><div class="section-head"><div><p class="eyebrow">Start with your home</p><h2 id="finder-title">Which job needs<br>a little less you?</h2></div><p>Pick a chore, then the situation closest to yours. Get a focused reading route before choosing a model.</p></div><div class="finder-layout"><div><p class="step-label">01 / Choose the chore</p><div class="chore-choices">'
 for k,c in categories.items():out+=f'<button type="button" data-chore="{k}" aria-pressed="false" aria-controls="situations-{k}">{E(c[0])}<span aria-hidden="true">↗</span></button>'
 out+='</div></div><div class="finder-detail"><p class="step-label">02 / What sounds like your home?</p><p id="finder-hint">Choose a chore to see the situations.</p>'
 for k,choices in SCENARIOS.items():
  out+=f'<div id="situations-{k}" class="situation-panel" hidden><div class="situation-choices">'
  for i,(label,pid,reason) in enumerate(choices):out+=f'<button type="button" data-situation="{k}-{i}" aria-pressed="false" aria-controls="route-{k}-{i}">{E(label)}</button>'
  out+='</div>'
  for i,(label,pid,reason) in enumerate(choices):
   a=articles[pid]
   out+=f'<div id="route-{k}-{i}" class="finder-result" hidden><p class="eyebrow">Your next useful step</p><h3>{E(a["title"])}</h3><p>{E(reason)}</p><a class="button" href="{a["url"]}">Read this guide →</a><a class="text-link" href="/products/?category={k}">Browse {E(categories[k][0].lower())} →</a></div>'
  out+='</div>'
 out+='</div></div><p class="small-note">A guide to the decision, not a product compatibility test. No signup needed.</p><noscript><p>Browse the chore categories below to find your guide.</p></noscript></section>'
 return out

def routine(k):
 out='<section class="wrap routine-panel" aria-label="The whole ownership routine"><div><p class="eyebrow">See the whole job</p><h2>What stays on your list?</h2><p>Automation changes the routine. Tap a stage to see what to plan for.</p></div><div class="routine-steps">'
 for i,(label,detail) in enumerate(zip(['Before buying','Each session','After the job'],ROUTINES[k])):
  out+=f'<details><summary><span class="stage-number">0{i+1}</span><span>{label}</span><span class="expand-mark" aria-hidden="true">+</span></summary><p>{E(detail)}.</p></details>'
 return out+'</div><p class="small-note">Typical planning steps; follow the exact model’s instructions.</p></section>'

def checklist(checks):
 return '<div class="fit-checks"><p>Mark only what you have confirmed for this exact model.</p>'+''.join(f'<label><input type="checkbox"><span>{E(x)}</span></label>' for x in checks)+'<progress value="0" max="3" aria-label="Fit checks completed"></progress><p class="check-status" role="status">0 of 3 checked — start with the measurements.</p><button type="button" class="reset-checks">Reset checks</button><p class="small-note">Your checklist, not a compatibility guarantee. Resets when you leave this page.</p></div>'
