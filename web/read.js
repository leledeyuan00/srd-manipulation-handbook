'use strict';
for(const button of document.querySelectorAll('.copy')) button.addEventListener('click',async()=>{
  const code=button.closest('.codebox').querySelector('code').textContent;
  try{await navigator.clipboard.writeText(code);button.textContent='Copied';setTimeout(()=>button.textContent='Copy',1500);}catch{button.textContent='Select and copy manually';}
});
const search=document.querySelector('#search');let index;
search?.addEventListener('input',async()=>{
 const q=search.value.trim().toLowerCase(),nav=document.querySelector('#nav'),results=document.querySelector('#results');
 if(!q){nav.hidden=false;results.hidden=true;return;}
 try{index??=await fetch(document.body.dataset.base+'search-'+document.body.dataset.lang+'.json').then(r=>{if(!r.ok)throw Error();return r.json()});}catch{results.hidden=false;results.textContent='Search index unavailable. Open via a local HTTP server.';return;}
 if(q!==search.value.trim().toLowerCase())return;
 results.replaceChildren();nav.hidden=true;results.hidden=false;
 for(const v of index.filter(v=>(v.title+' '+v.text).toLowerCase().includes(q)).slice(0,15)){
   const a=document.createElement('a');a.className='searchhit';a.href=document.body.dataset.base+document.body.dataset.lang+'/'+v.id+'/';a.textContent=v.title;results.append(a);
 }
 if(!results.children.length)results.textContent='No matching pages.';
});
