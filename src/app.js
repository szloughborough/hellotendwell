(() => {
  'use strict';
  const $ = s => document.querySelector(s);
  const all = s => [...document.querySelectorAll(s)];
  const key = 'home-handled-comparison-v1';
  let saved=[];
  try {const value=JSON.parse(localStorage.getItem(key)||'[]');if(Array.isArray(value)) saved=value.filter(x=>typeof x==='string'&&/^B[A-Z0-9]{9}$/.test(x)).slice(0,3);} catch {}
  const announce = text => {$('#notice').textContent=text;setTimeout(()=>{$('#notice').textContent='';},3500);};
  const persist = () => {try{localStorage.setItem(key,JSON.stringify(saved));}catch{announce('Your browser could not save the comparison between pages.');}};
  function sync(){all('.compare-btn').forEach(b=>{const yes=saved.includes(b.dataset.asin);b.setAttribute('aria-pressed',String(yes));b.textContent=yes?'✓ Added':'+ Compare';});$('#compare-tray').hidden=!saved.length;$('#compare-count').textContent=`${saved.length} of 3 selected`;}
  all('.compare-btn').forEach(b=>b.addEventListener('click',()=>{const id=b.dataset.asin;if(saved.includes(id))saved=saved.filter(x=>x!==id);else if(saved.length<3)saved.push(id);else return announce('Your comparison has three products. Remove one to add another.');persist();sync();}));
  $('#clear-compare').addEventListener('click',()=>{saved=[];persist();sync();renderCompare();});
  const menu=$('.menu-toggle');menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));$('#main-nav').classList.toggle('open',open);});
  document.addEventListener('keydown',e=>{if(e.key==='Escape'){menu.setAttribute('aria-expanded','false');$('#main-nav').classList.remove('open');}});
  const form=$('.filters');
  if(form){
    const type=form.dataset.kind;const cards=all(type==='products'?'.product-card':'.guide-card');
    function filter(){let count=0;const search=$('#search').value.trim().toLowerCase();const cat=$('#category').value;const budget=$('#budget')?.value;const brand=$('#brand')?.value;
      cards.forEach(c=>{const n=Number(c.dataset.price);const priceMatch=!budget||(budget==='300'&&n>=300&&n<500)||(budget==='500'&&n>=500&&n<1000)||(budget==='1000'&&n>=1000);const show=(!search||c.dataset.search.includes(search))&&(!cat||c.dataset.cat===cat)&&(!brand||c.dataset.brand===brand)&&priceMatch;c.hidden=!show;if(show)count++;});
      $('#result-count').textContent=`${count} ${type==='products'?'products':'guides'} shown`;$('#empty-state').hidden=count!==0;
    }
    const preset=new URLSearchParams(location.search).get('category');
    if(preset&&[...$('#category').options].some(o=>o.value===preset))$('#category').value=preset;
    form.addEventListener('input',filter);form.addEventListener('change',filter);form.addEventListener('reset',()=>setTimeout(filter,0));filter();
  }
  const safe=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  let products;
  async function renderCompare(){const target=$('#comparison');if(!target)return;
    if(!saved.length){target.innerHTML='<div class="empty-comparison"><h2>Your shortlist starts here.</h2><p>Choose “+ Compare” on a product card to add up to three products.</p></div>';return;}
    try{if(!products){const response=await fetch('/assets/products.json');if(!response.ok)throw new Error();products=await response.json();}
      const selected=saved.map(id=>products.find(p=>p.asin===id)).filter(Boolean);
      target.innerHTML='<div class="compare-grid">'+selected.map(p=>`<article class="comparison-card"><div class="comparison-image"><img src="${safe(p.image)}" alt="${safe(p.name)}" width="400" height="400"></div><div class="comparison-content"><p class="eyebrow">${safe(p.category_label)}</p><h2><a href="/products/${safe(p.slug)}/">${safe(p.name)}</a></h2><dl><dt>US listing / ASIN</dt><dd>${safe(p.asin)}</dd><dt>Catalog budget range</dt><dd>${p.budget_snapshot<500?'$300–499':p.budget_snapshot<1000?'$500–999':'$1,000+'}</dd><dt>Snapshot date</dt><dd>${safe(p.price_date)}</dd><dt>Catalog-listed configuration</dt><dd>${safe(p.catalog_title)}</dd><dt>Evidence scope</dt><dd>Catalog profile; no hands-on test.</dd></dl><p class="eyebrow">Fit checks</p><ul>${p.checks.map(t=>`<li>${safe(t)}</li>`).join('')}</ul><a class="text-link" href="/products/${safe(p.slug)}/">View full profile →</a><br><button data-remove="${p.asin}">Remove from comparison</button></div></article>`).join('')+'</div>';
      all('[data-remove]').forEach(b=>b.addEventListener('click',()=>{saved=saved.filter(x=>x!==b.dataset.remove);persist();sync();renderCompare();}));
    }catch{target.innerHTML='<p>We couldn’t load the comparison. Please refresh this page.</p>';}
  }
  all('[data-chore]').forEach(button=>button.addEventListener('click',()=>{
    all('[data-chore]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
    all('.situation-panel').forEach(p=>p.hidden=p.id!=='situations-'+button.dataset.chore);
    $('#finder-hint').hidden=true;
  }));
  all('[data-situation]').forEach(button=>button.addEventListener('click',()=>{
    const panel=button.closest('.situation-panel');
    [...panel.querySelectorAll('[data-situation]')].forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
    [...panel.querySelectorAll('.finder-result')].forEach(r=>r.hidden=r.id!=='route-'+button.dataset.situation);
  }));
  all('.fit-checks').forEach(panel=>{
    const boxes=[...panel.querySelectorAll('input')];
    const update=()=>{const n=boxes.filter(b=>b.checked).length;panel.querySelector('progress').value=n;panel.querySelector('.check-status').textContent=n===3?'3 of 3 checked — confirm the exact offer and return terms next.':`${n} of 3 checked — ${3-n} still to confirm.`;};
    boxes.forEach(b=>b.addEventListener('change',update));
    panel.querySelector('.reset-checks').addEventListener('click',()=>{boxes.forEach(b=>b.checked=false);update();});
  });
  sync();renderCompare();
})();

// Calm, finite motion; content remains visible without JavaScript.
(() => {
 const preference = matchMedia('(prefers-reduced-motion: reduce)');
 const hero = document.querySelector('.hero-art');
 if (hero) {
  const illustration = document.createElement('div');
  illustration.innerHTML = '<svg class="calm-clean-path" viewBox="0 0 600 140" aria-hidden="true" focusable="false"><path class="clean-route" d="M35 110 H160 Q190 110 190 80 V60 Q190 30 220 30 H405 Q435 30 435 60 V85 Q435 110 465 110 H545" fill="none" stroke="#537b60" stroke-width="3" stroke-linecap="round"/><g class="clean-finish"><circle cx="550" cy="110" r="15" fill="#f6f4ec"/><path d="m543 110 5 5 9-11" fill="none" stroke="#537b60" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></g></svg>';
  hero.append(illustration.firstChild);
 }
 if (preference.matches || !('IntersectionObserver' in window)) return;
 const observer = new IntersectionObserver(entries => entries.forEach(entry => {
  if (!entry.isIntersecting) return;
  entry.target.classList.add('motion-arrive');
  observer.unobserve(entry.target);
 }), {threshold:0.12});
 document.querySelectorAll('.category-tile,.product-card,.guide-card').forEach((el,i) => {
  el.style.setProperty('--arrival-delay', `${(i % 3) * 65}ms`);
  observer.observe(el);
 });
 preference.addEventListener('change', e => {
  if (e.matches) {observer.disconnect();document.querySelectorAll('.motion-arrive').forEach(el=>el.classList.remove('motion-arrive'));}
 });
})();
