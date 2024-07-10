from flask import Flask, send_from_directory
from api.generate_text import generate_text_bp
from api.generate_image import generate_image_bp

app = Flask(__name__)

# 블루프린트 등록
app.register_blueprint(generate_text_bp, url_prefix='/api')
app.register_blueprint(generate_image_bp, url_prefix='/api')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)