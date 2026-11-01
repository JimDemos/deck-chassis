"""Deck-player JS. CORE_JS is always on (nav, sync, notes toggle). The
terminal/demo panel and the narration overlay are each optional, switched by
the per-deck feature config so a meeting-mode deck can drop the panel and a
quiet read-along deck can drop narration, without forking the chassis."""

import json

CORE_JS = """
const slides=document.querySelectorAll('.slide');let current=0;const total=slides.length;const channel=new BroadcastChannel('%(sync_channel)s');
function show(n,r){n=Math.max(0,Math.min(n,total-1));if(r&&n===current&&slides[current].classList.contains('active'))return;slides[current].classList.remove('active');current=Math.max(0,Math.min(n,total-1));slides[current].classList.add('active');document.getElementById('progress').style.width=((current+1)/total*100)+'%%';document.getElementById('counter').textContent=(current+1)+' / '+total;if(!r)channel.postMessage({slide:current});}
channel.onmessage=e=>{if(typeof e.data.slide==='number')show(e.data.slide,true);%(term_onmessage)s};
document.addEventListener('keydown',e=>{%(term_keydown)s
if(e.key==='Escape'){%(term_escape)sif(document.activeElement)document.activeElement.blur();return;}
if(e.key==='n'||e.key==='N'){e.preventDefault();document.body.classList.toggle('show-notes');return;}
if(document.activeElement&&document.activeElement.tagName==='IFRAME')return;
if(e.key==='ArrowRight'||e.key==='ArrowDown'||e.key===' '||e.key==='PageDown'){e.preventDefault();show(current+1);}
if(e.key==='ArrowLeft'||e.key==='ArrowUp'||e.key==='PageUp'){e.preventDefault();show(current-1);}
if(e.key==='Home'){e.preventDefault();show(0);}if(e.key==='End'){e.preventDefault();show(total-1);}},{capture:true});
let tx=0;document.addEventListener('touchstart',e=>{tx=e.changedTouches[0].screenX;});document.addEventListener('touchend',e=>{const dx=e.changedTouches[0].screenX-tx;if(dx<-50)show(current+1);if(dx>50)show(current-1);});
const params=new URLSearchParams(window.location.search);if(params.get('notes')==='1')document.body.classList.add('show-notes');
if(params.get('presenter')==='child'){document.body.classList.add('presenter-child');window.addEventListener('message',e=>{if(e.data&&typeof e.data.showSlide==='number')show(e.data.showSlide,true);});}
show(0);
"""

TERM_JS = """const DEMO_HOSTS = %(demo_hosts)s;
const termPanel=document.getElementById('term-panel'),termFrame=document.getElementById('term-frame'),termTag=document.getElementById('term-tag'),termHost=document.getElementById('term-host');let termLoaded=null;
function openTerm(k){if(document.body.classList.contains('presenter-child'))return;if(!k){k=slides[current].getAttribute('data-term')||Object.keys(DEMO_HOSTS)[0];}const h=DEMO_HOSTS[k];if(!h)return;if(typeof narrator!=='undefined'){narrator.pause();}if(termLoaded!==k){termFrame.src=h.url;termLoaded=k;}termTag.textContent=k;termHost.textContent=h.label;termPanel.classList.add('open');document.body.classList.add('term-open');}
function closeTerm(){if(termFrame){termFrame.src='about:blank';termLoaded=null;}termPanel.classList.remove('open');document.body.classList.remove('term-open');}
function toggleTerm(r){if(termPanel.classList.contains('open'))closeTerm();else openTerm();if(!r)channel.postMessage({term:termPanel.classList.contains('open')});}
"""

TERM_ONMESSAGE = "if(typeof e.data.term==='boolean')e.data.term?openTerm():closeTerm();"
TERM_KEYDOWN = "if((e.key==='t'||e.key==='T')&&!e.ctrlKey&&!e.metaKey){if(document.activeElement&&document.activeElement.tagName==='IFRAME')return;e.preventDefault();toggleTerm();return;}"
TERM_ESCAPE = "if(termPanel.classList.contains('open')){closeTerm();return;}"

NARRATION_JS = """const NARR_RATE=%(rate)s;
const AUDIO=%(audio_manifest)s;const narrator=document.createElement('audio');narrator.id='narrator';narrator.preload='auto';document.body.appendChild(narrator);
let audioOn=!new URLSearchParams(location.search).has('presenter'),autoAdv=false;const abadge=document.createElement('div');abadge.id='abadge';abadge.style.cssText='position:fixed;left:18px;bottom:14px;font:12px "Red Hat Mono",monospace;color:#9aa5b1;z-index:60;letter-spacing:.04em';document.body.appendChild(abadge);
function abadgeUpd(){abadge.textContent=(!narrOwner()?'narration muted: another window owns it':audioOn?'narration on':'narration off')+(autoAdv?' · auto-advance':'')+' · M mute · A auto';}
const NARR_ID=Math.random().toString(36).slice(2);function narrOwner(){try{const v=JSON.parse(localStorage.getItem('%(lock_key)s')||'{}');if(v.id===NARR_ID)return true;if(!v.ts||Date.now()-v.ts>5000){localStorage.setItem('%(lock_key)s',JSON.stringify({id:NARR_ID,ts:Date.now()}));return true;}return false;}catch(e){return true;}}setInterval(()=>{if(narrOwner())localStorage.setItem('%(lock_key)s',JSON.stringify({id:NARR_ID,ts:Date.now()}));},2000);window.addEventListener('beforeunload',()=>{try{const v=JSON.parse(localStorage.getItem('%(lock_key)s')||'{}');if(v.id===NARR_ID)localStorage.removeItem('%(lock_key)s');}catch(e){}});document.addEventListener('visibilitychange',()=>{if(document.hidden)narrator.pause();else playCurrent();});function playCurrent(){if(!audioOn||document.hidden||document.body.classList.contains('presenter-child')||!narrOwner()){narrator.pause();abadgeUpd();return;}const f=AUDIO[current];if(!f){narrator.pause();return;}narrator.src='%(audio_dir)s/'+f+'.mp3';narrator.playbackRate=NARR_RATE;narrator.play().catch(()=>{});}
narrator.addEventListener('ended',()=>{if(autoAdv&&narrOwner()&&!document.hidden&&current<total-1)setTimeout(()=>show(current+1),700);});
const _show=show;show=function(n,r){_show(n,r);playCurrent();};
document.addEventListener('keydown',e=>{if(e.key==='m'||e.key==='M'){e.preventDefault();audioOn=!audioOn;if(!audioOn)narrator.pause();else playCurrent();abadgeUpd();}if(e.key==='a'||e.key==='A'){e.preventDefault();autoAdv=!autoAdv;abadgeUpd();}},{capture:true});
abadgeUpd();document.addEventListener('click',()=>{if(audioOn&&narrator.paused&&narrator.src)narrator.play().catch(()=>{});},{once:true});
"""


def build_player_js(features, *, sync_channel):
    """features: dict with optional keys 'terminal' (dict: demo_hosts) and
    'narration' (dict: audio_manifest, audio_dir, rate, lock_key)."""
    term = features.get("terminal")
    narr = features.get("narration")

    js = CORE_JS % {
        "sync_channel": sync_channel,
        "term_onmessage": TERM_ONMESSAGE if term else "",
        "term_keydown": TERM_KEYDOWN if term else "",
        "term_escape": TERM_ESCAPE if term else "",
    }
    prefix = (TERM_JS % {"demo_hosts": json.dumps(term["demo_hosts"])}) if term else ""

    if narr:
        i = js.rfind("show(0);") + len("show(0);")
        js = js[:i] + (NARRATION_JS % {
            "rate": narr.get("rate", 1.0),
            "audio_manifest": json.dumps(narr["audio_manifest"]),
            "audio_dir": narr["audio_dir"],
            "lock_key": narr.get("lock_key", "chassis-narrator"),
        }) + js[i:]

    return prefix + js
