from flask import Blueprint, request, jsonify
from api.ai_utils import generate_movie_quote_image

generate_image_bp = Blueprint('generate_image', __name__)

@generate_image_bp.route('/generate_image', methods=['POST'])
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
