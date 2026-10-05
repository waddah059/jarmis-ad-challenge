import json, os, sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

DB = os.getenv('STATE_DB', '/data/state.db')
TEAM = os.getenv('TEAM_ID', '0')

def flag():
    try:
        con=sqlite3.connect(DB); row=con.execute('SELECT flag FROM flags ORDER BY round DESC LIMIT 1').fetchone(); con.close()
        return row[0] if row else None
    except Exception:
        return None

class H(BaseHTTPRequestHandler):
    def reply(self, code, body):
        data=json.dumps(body).encode(); self.send_response(code); self.send_header('Content-Type','application/json'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        p=urlparse(self.path); q=parse_qs(p.query)
        if p.path == '/health': self.reply(200, {'status':'ok','team':TEAM}); return
        if p.path == '/api/info': self.reply(200, {'team':TEAM,'service':'internal-management','version':'2.0'}); return
        if p.path == '/api/metadata': self.reply(200, {'team':TEAM,'management':'restricted','hint':'status endpoint is used by monitoring'}); return
        if p.path == '/api/run' and q.get('cmd',[''])[0] == 'status': self.reply(200, {'team':TEAM,'status':'running','flag':flag()}); return
        self.reply(404, {'error':'not found'})
    def log_message(self,*args): pass

HTTPServer(('0.0.0.0',9000),H).serve_forever()
