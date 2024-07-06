from flask import Flask, render_template, request
from openai import OpenAI
from dotenv import load_dotenv
import os

# .env 파일 로드
load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# 장르와 프롬프트 설정
content_map = {
    "Comedy": {
        "prompt": "제공된 상황을 기반으로 재미있고 가벼운 영화 대사를 만들어주세요."
    },
    "Romance": {
        "prompt": "제공된 상황을 기반으로 감성적이고 사랑스러운 영화 대사를 만들어주세요."
    },
    "Action": {
        "prompt": "제공된 상황을 기반으로 강렬하고 긴장감 넘치는 영화 대사를 만들어주세요."
    },
    "Drama": {
        "prompt": "제공된 상황을 기반으로 감동적이고 깊이 있는 영화 대사를 만들어주세요."
    },
    "Fantasy": {
        "prompt": "제공된 상황을 기반으로 상상력 넘치고 마법 같은 영화 대사를 만들어주세요."
    },
    "Horror": {
        "prompt": "제공된 상황을 기반으로 무섭고 소름 끼치는 영화 대사를 만들어주세요. (그래픽 콘텐츠는 피해주세요.)"
    },
    "SciFi": {
        "prompt": "제공된 상황을 기반으로 미래지향적이고 기술적인 영화 대사를 만들어주세요."
    },
    "Thriller": {
        "prompt": "제공된 상황을 기반으로 긴박하고 미스터리한 영화 대사를 만들어주세요."
    },
    "Mystery": {
        "prompt": "제공된 상황을 기반으로 신비롭고 궁금증을 자아내는 영화 대사를 만들어주세요."
    },
    "Adventure": {
        "prompt": "제공된 상황을 기반으로 흥미롭고 탐험적인 영화 대사를 만들어주세요."
    }
}

@app.route('/', methods=['GET', 'POST'])
def home():
    selected_genre = None
    selected_style = None
    selected_decade = None
    response_text = None
    response_image = None
    user_input = ""
    if request.method == 'POST':
        selected_genre = request.form.get('genre')
        selected_style = request.form.get('style')
        selected_decade = request.form.get('decade')
        user_input = request.form.get('user_input')

        if user_input and selected_genre and selected_style and selected_decade:
            prompt = f"{content_map[selected_genre]['prompt']} {user_input} Style: {selected_style}, Decade: {selected_decade}"
            text_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a film screenwriter. Create a line of dialogue that fits the genre, style, and decade."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=50
            )
            response_text = text_response.choices[0].message.content
            
            image_prompt = f"Create a scene from a {selected_genre} film in {selected_style} style from the {selected_decade}. {user_input}"
            image_response = client.images.generate(
                model="dall-e-3",
                prompt=image_prompt,
                n=1,
                size="1024x1024",
                quality="standard"
            )
            response_image = image_response.data[0].url

    return render_template('index.html', content_map=content_map, selected_genre=selected_genre, selected_style=selected_style, selected_decade=selected_decade, user_input=user_input, response=response_text, response_image=response_image)

if __name__ == '__main__':
    app.run(debug=True)
