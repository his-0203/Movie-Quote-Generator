from flask import Blueprint, request, jsonify
from api.ai_utils import generate_movie_quote_text

generate_text_bp = Blueprint('generate_text', __name__)

@generate_text_bp.route('/generate_text', methods=['POST'])
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
