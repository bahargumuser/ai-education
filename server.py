import http.server
import socketserver
import json

with open('data.json', 'r') as f:
    data = json.load(f)

responses = data['responses']

class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = json.loads(post_data)
        question = data['question']
        
        response = self.get_response(question)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"response": response}).encode('utf-8'))

    def get_response(self, question):
        for key in responses.keys():
            if key in question.lower():
                return responses[key]
        return "Üzgünüm, bu soruya cevap veremiyorum."

PORT = 8000

with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()