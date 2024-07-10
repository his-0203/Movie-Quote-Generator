from flask import Flask, request, jsonify
from ai_utils import generate_movie_quote_text, generate_movie_quote_image

app = Flask(__name__)

@app.route('/api/generate_text', methods=['POST'])
def generate_text():
    data = request.json
    user_input = data.get('user_input')
    selected_genre = data.get('genre')
    selected_style = data.get('style')
    selected_period = data.get('period')

    if not user_input or not selected_genre or not selected_style or not selected_period:
        return jsonify({'error': 'Missing parameters'}), 400

    response_text = generate_movie_quote_text(user_input, selected_genre, selected_style, selected_period)
    if not response_text:
        return jsonify({'error': 'Failed to generate text'}), 500

    return jsonify({'quote': response_text})

@app.route('/api/generate_image', methods=['POST'])
def generate_image():
    data = request.json
    user_input = data.get('user_input')
    selected_genre = data.get('genre')
    selected_style = data.get('style')
    selected_period = data.get('period')

    if not user_input or not selected_genre or not selected_style or not selected_period:
        return jsonify({'error': 'Missing parameters'}), 400

    response_image = generate_movie_quote_image(user_input, selected_genre, selected_style, selected_period)
    if not response_image:
        return jsonify({'error': 'Failed to generate image'}), 500

    return jsonify({'image': response_image})

if __name__ == '__main__':
    app.run(debug=True)
