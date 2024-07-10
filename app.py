from flask import Flask, render_template, request, jsonify
from api.ai_utils import generate_movie_quote, movie_genre

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    selected_genre = None
    selected_style = None
    selected_period = None
    response_text = None
    response_image = None
    user_input = ""
    show_error_modal = False

    if request.method == 'POST':
        selected_genre = request.form.get('genre')
        selected_style = request.form.get('style')
        selected_period = request.form.get('period')
        user_input = request.form.get('user_input')

        if user_input and selected_genre and selected_style and selected_period:
            response_text, response_image = generate_movie_quote(user_input, selected_genre, selected_style, selected_period)
            if not response_text or not response_image:
                show_error_modal = True

    return render_template('index.html', movie_genre=movie_genre, selected_genre=selected_genre, selected_style=selected_style, selected_period=selected_period, user_input=user_input, response=response_text, response_image=response_image, show_error_modal=show_error_modal)

@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.json
    user_input = data.get('user_input')
    selected_genre = data.get('genre')
    selected_style = data.get('style')
    selected_period = data.get('period')

    if not user_input or not selected_genre or not selected_style or not selected_period:
        return jsonify({'error': 'Missing parameters'}), 400

    response_text, response_image = generate_movie_quote(user_input, selected_genre, selected_style, selected_period)
    if not response_text or not response_image:
        return jsonify({'error': 'Failed to generate quote'}), 500

    return jsonify({'quote': response_text, 'image': response_image})

if __name__ == '__main__':
    app.run(debug=True)
