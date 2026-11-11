(() => {
  const key='tendwell-analytics-consent';
  let loaded=false;
  const read=()=>{try{return localStorage.getItem(key);}catch{return null;}};
  function start(){
    if(loaded)return;loaded=true;
    window.dataLayer=window.dataLayer||[];
    window.gtag=function(){window.dataLayer.push(arguments);};
    window.gtag('consent','default',{analytics_storage:'granted',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});
    window.gtag('js',new Date());
    window.gtag('config','G-952F72ZS1J');
    const ga=document.createElement('script');ga.async=true;ga.src='https://www.googletagmanager.com/gtag/js?id=G-952F72ZS1J';document.head.append(ga);
    window.clarity=window.clarity||function(){(window.clarity.q=window.clarity.q||[]).push(arguments);};
    window.clarity('consentv2',{analytics_Storage:'granted',ad_Storage:'denied'});
    const cl=document.createElement('script');cl.async=true;cl.src='https://www.clarity.ms/tag/z4kitwgybe';document.head.append(cl);
  }
  function preferences(){
    if(document.getElementById('analytics-choice'))return;
    const box=document.createElement('section');box.id='analytics-choice';box.setAttribute('aria-label','Analytics preferences');
    box.style.cssText='position:fixed;bottom:16px;left:16px;right:16px;max-width:550px;padding:22px;background:#fffefb;color:#223c36;border:1px solid #64716a;border-radius:8px;z-index:50;box-shadow:0 4px 24px #0003;font:14px/1.6 Arial';
    box.innerHTML='<strong>Help us improve Tendwell?</strong><p>With your permission, Google Analytics measures visits and Microsoft Clarity records interactions to help us improve the site. Optional analytics stays off until you accept. <a href="/privacy/">Privacy details</a></p><button type="button" data-choice="yes">Accept analytics</button> <button type="button" data-choice="no">Reject analytics</button>';
    box.querySelectorAll('button').forEach(b=>{b.style.cssText='min-height:44px;padding:10px;margin:4px;border:1px solid #193e38;background:#f8f6ef;border-radius:4px';b.onclick=()=>{try{localStorage.setItem(key,b.dataset.choice);}catch{}box.remove();if(b.dataset.choice==='yes')start();else if(loaded){window.gtag('consent','update',{analytics_storage:'denied'});window.clarity('consentv2',{analytics_Storage:'denied',ad_Storage:'denied'});location.reload();}};});document.body.append(box);
  }
  document.addEventListener('click',event=>{
    const link=event.target.closest && event.target.closest('a[rel~="sponsored"]');
    if(!link || !loaded || read()!=='yes')return;
    window.gtag('event','affiliate_click',{
      product_id:link.dataset.productId || 'unknown',
      page_path:location.pathname,
      placement:link.dataset.placement || 'other',
      destination:'amazon',
      transport_type:'beacon'
    });
  });
  window.tendwellAnalyticsPreferences=preferences;
  if(read()==='yes')start();else if(read()!=='no')preferences();
})();
