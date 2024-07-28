import http.server
import socketserver
import json

with open('data.json', 'r', encoding="utf8") as f:
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
            if key in question.lower() or similarity(key.lower(), question.lower()) > 0.5:
                return responses[key]
        return "Üzgünüm, bu soruya cevap veremiyorum."

PORT = 8000

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def similarity(s1, s2):
    max_len = max(len(s1), len(s2))
    if max_len == 0:
        return 1.0  # Both strings are empty
    return (max_len - levenshtein_distance(s1, s2)) / max_len


with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()