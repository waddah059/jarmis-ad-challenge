import os, secrets, sqlite3
from urllib.parse import urlparse
import httpx
from fastapi import FastAPI, Header, HTTPException, Query

DB=os.getenv('STATE_DB','/data/state.db')
CHECKER_TOKEN=os.getenv('CHECKER_TOKEN','')
TEAM_ID=os.getenv('TEAM_ID','0')
app=FastAPI(title='Jarmis A/D Service', version='2.1.0')
MOCK_JARM={'mock-web':{'hostname':'factory-portal','signature':'MOCK-JARM-7F4A-91B2'},'gateway':{'hostname':'edge-gateway','signature':'MOCK-JARM-2A11-C8E0'}}

def db():
    os.makedirs(os.path.dirname(DB),exist_ok=True)
    con=sqlite3.connect(DB)
    con.execute('CREATE TABLE IF NOT EXISTS flags (round INTEGER PRIMARY KEY, flag TEXT NOT NULL)')
    con.commit(); return con

def put_flag(round_no,flag):
    con=db(); con.execute('INSERT OR REPLACE INTO flags(round,flag) VALUES (?,?)',(round_no,flag)); con.commit(); con.close()

@app.get('/')
def root(): return {'service':'jarmis-ad','team':TEAM_ID,'status':'online'}

@app.get('/health')
def health():
    try:
        con=db(); con.execute('SELECT 1'); con.close(); return {'status':'ok','team':TEAM_ID}
    except Exception: raise HTTPException(503,'service unavailable')

@app.get('/api/v1/search/id/{record_id}')
def search_id(record_id):
    if record_id not in MOCK_JARM: raise HTTPException(404,'record not found')
    return {'id':record_id,**MOCK_JARM[record_id]}

@app.get('/api/v1/search/signature/{signature}')
def search_signature(signature):
    for rid,record in MOCK_JARM.items():
        if record['signature']==signature: return {'id':rid,**record}
    raise HTTPException(404,'signature not found')

@app.get('/api/v1/fetch')
async def ssrf(endpoint: str=Query(...,min_length=8,max_length=2048)):
    # INTENTIONAL VULNERABILITY: user-controlled server-side URL fetch.
    parsed=urlparse(endpoint)
    if parsed.scheme not in {'http','https'} or not parsed.netloc: raise HTTPException(400,'only http/https URLs are accepted')
    try:
        async with httpx.AsyncClient(follow_redirects=True,timeout=4.0) as client: r=await client.get(endpoint)
        return {'status_code':r.status_code,'headers':dict(r.headers),'body':r.text[:12000]}
    except httpx.RequestError as exc: raise HTTPException(502,f'upstream request failed: {type(exc).__name__}')

# Control-plane flag store. It is not part of the player API and requires a deployment-only token.
@app.post('/_checker/flag')
def checker_flag(payload:dict,x_checker_token:str|None=Header(default=None)):
    if not CHECKER_TOKEN or not secrets.compare_digest(x_checker_token or '',CHECKER_TOKEN): raise HTTPException(404,'not found')
    try: round_no,flag=int(payload['round']),str(payload['flag'])
    except (KeyError,ValueError,TypeError): raise HTTPException(400,'invalid flag payload')
    if not (1<=round_no<=10000000) or not flag.startswith('JARMIS{'): raise HTTPException(400,'invalid flag')
    put_flag(round_no,flag); return {'ok':True,'round':round_no}

@app.get('/_checker/flag/{round_no}')
def checker_flag_read(round_no:int,x_checker_token:str|None=Header(default=None)):
    if not CHECKER_TOKEN or not secrets.compare_digest(x_checker_token or '',CHECKER_TOKEN): raise HTTPException(404,'not found')
    con=db(); row=con.execute('SELECT flag FROM flags WHERE round=?',(round_no,)).fetchone(); con.close()
    if not row: raise HTTPException(404,'flag not found')
    return {'round':round_no,'flag':row[0]}
