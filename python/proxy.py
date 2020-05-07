#from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import http.server
import urllib.parse
import requests
import time

class ProxyHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
	protocol_version = 'HTTP/1.0'

	def do_GET(self, body=True):
		try:
			target_url = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query).get('url', None)
			print("[INFO] target_url: "+str(target_url))
			if target_url != None:
				target_url = target_url[0]
				req_header = self.parse_headers()
				#resp = requests.get(target_url, headers=req_header, verify=False, stream=True)
				resp = requests.get(target_url, headers=req_header, verify="certs.pem", stream=True)
				print("[INFO] resp.status_code: %d " % resp.status_code)
				if resp.status_code == 404:
					self.send_response(404)
					self.send_header('Content-Type','text/html')
					self.end_headers()
					self.wfile.write("NOT FOUND".encode())
				else:
					self.send_response(resp.status_code)
					for k in resp.headers.keys():
						print("[INFO] resp.headers: [%s][%s]" % (k, resp.headers[k]) )
						self.send_header(k, resp.headers[k])
					self.end_headers()
					for chunk in resp.iter_content(chunk_size=1024):
						if chunk:
							self.wfile.write(chunk)
							self.wfile.flush()
						else:
							time.sleep(0.05)
				
			else:
				self.send_response(404)
				self.send_header('Content-Type','text/html')
				self.end_headers()
				self.wfile.write("NOT FOUND".encode())
		finally:
			self.finish()

	def parse_headers(self):
		req_header = {}
		for line in self.headers:
			line_parts = [o.strip() for o in line.split(':', 1)]
			if len(line_parts) == 2:
				req_header[line_parts[0]] = line_parts[1]
		return self.inject_header(req_header)
    
	def inject_header(self, headers):
		headers['Referer'] = 'https://example.com/'
       
		return headers
	

if __name__ == '__main__':
	server_address = ('0.0.0.0', 8081)
	httpd = http.server.HTTPServer(server_address, ProxyHTTPRequestHandler)
	print('http server is running')
	httpd.serve_forever()
