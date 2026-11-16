/* Local, reversible presentation translation; scientific values and IDs stay intact. */
(function(){
  const PX=window.PX;
  let language='es',catalog={},reverse={},rules=[],observer,fragments={};
  const texts=new WeakMap(),attributes=new WeakMap(),cache=new Map();
  const attrs=['aria-label','aria-valuetext','alt','title','placeholder','content'];
  const normalize=value=>String(value).replace(/\s+/g,' ').trim();
  const escape=value=>value.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
  function compile(source,target){
    const names=[];
    const parts=source.split(/(\{\w+\})/g).map(part=>{
      if(/^\{\w+\}$/.test(part)){
        const name=part.slice(1,-1);names.push(name);
        return ['count','number','total','threshold','radius','size','x','y','distance'].includes(name)?'([\\d.+-]+)':'(.+?)';
      }
      return escape(part);
    });
    return {regex:new RegExp('^'+parts.join('')+'$','u'),target,names};
  }
  function translate(value,lang=language,depth=0){
    if(typeof value!=='string'||!value.trim())return value;
    const text=normalize(value),key=lang+'|'+text;
    if(cache.has(key))return value.replace(value.trim(),cache.get(key));
    const from=lang==='en'?catalog:reverse;
    let result=from[text];
    if(result===undefined&&depth<3){
      for(const pair of rules){
        const rule=lang==='en'?pair.forward:pair.backward,match=text.match(rule.regex);
        if(!match)continue;
        const captures=Object.fromEntries(rule.names.map((n,i)=>[n,translate(match[i+1],lang,depth+1)]));
        result=rule.target.replace(/\{(\w+)\}/g,(_,n)=>captures[n]);break;
      }
    }
    if(result===undefined){
      result=text;
      if(depth<3)result=result.split(/(?<=\.)\s+(?!\d)/u).map(part=>part===text?part:translate(part,lang,depth+1)).join(' ');
      const expression=fragments[lang];
      if(expression)result=result.replace(expression,s=>from[s]);
    }
    if(cache.size>3000)cache.clear();
    cache.set(key,result);
    return value.replace(value.trim(),result);
  }
  function excluded(node){return node.parentElement?.closest('script,style,code,pre,[data-no-translate]');}
  function text(node){
    if(excluded(node)||!node.nodeValue.trim())return;
    let saved=texts.get(node);
    if(!saved||node.nodeValue!==saved.last)saved={source:translate(node.nodeValue,'es')};
    const next=translate(saved.source);saved.last=next;texts.set(node,saved);
    if(node.nodeValue!==next)node.nodeValue=next;
  }
  function element(el){
    if(el.closest('script,style,code,pre,[data-no-translate]'))return;
    let saved=attributes.get(el);if(!saved){saved={};attributes.set(el,saved);}
    for(const attr of attrs){
      if(!el.hasAttribute(attr)||attr==='content'&&el.getAttribute('name')!=='description')continue;
      const value=el.getAttribute(attr);
      if(!saved[attr]||saved[attr].last!==value)saved[attr]={source:translate(value,'es')};
      const next=translate(saved[attr].source);saved[attr].last=next;
      if(value!==next)el.setAttribute(attr,next);
    }
  }
  function apply(root=document.documentElement){
    if(root.nodeType===Node.TEXT_NODE){text(root);return;}
    if(root.nodeType!==Node.ELEMENT_NODE)return;
    element(root);
    const walker=document.createTreeWalker(root,NodeFilter.SHOW_ELEMENT|NodeFilter.SHOW_TEXT);
    let node;while((node=walker.nextNode())){if(node.nodeType===Node.TEXT_NODE)text(node);else element(node);}
  }
  function setLanguage(lang){
    if(!['es','en'].includes(lang))return;
    language=lang;document.documentElement.lang=lang;
    const picker=PX.$('languageSelect');if(picker)picker.value=lang;
    try{localStorage.setItem('px-language',lang);}catch{}
    apply();document.dispatchEvent(new CustomEvent('px:languagechange',{detail:{language:lang}}));
  }
  async function init(){
    try{
      const response=await fetch('/static/locales/en.json');
      if(!response.ok)throw new Error('Translation catalogue unavailable');
      catalog=await response.json();
      for(const [source,target] of Object.entries(catalog)){
        reverse[target]=source;
        if(source.includes('{'))rules.push({forward:compile(source,target),backward:compile(target,source)});
      }
      for(const [lang,from] of [['en',catalog],['es',reverse]]){
        const keys=Object.keys(from).filter(s=>!s.includes('{')).sort((a,b)=>b.length-a.length);
        fragments[lang]=new RegExp('(?<![\\p{L}])(?:'+keys.map(escape).join('|')+')(?![\\p{L}])','gu');
      }
    }catch(error){console.warn(error.message);PX.$('languageSelect').disabled=true;}
    let preference='es';try{preference=localStorage.getItem('px-language')||'es';}catch{}
    if(!Object.keys(catalog).length)preference='es';
    PX.$('languageSelect').addEventListener('change',event=>setLanguage(event.target.value));
    setLanguage(preference);
    observer=new MutationObserver(records=>{
      const roots=new Set();
      for(const record of records){
        if(record.type==='childList')record.addedNodes.forEach(node=>roots.add(node));
        else if(record.type==='characterData')roots.add(record.target);
        else element(record.target);
      }
      roots.forEach(root=>{if(root.isConnected)apply(root);});
    });
    observer.observe(document.documentElement,{subtree:true,childList:true,characterData:true,attributes:true,attributeFilter:attrs});
  }
  PX.t=translate;
  PX.i18n={init,setLanguage,apply,get language(){return language;}};
})();
