from flask import Flask, render_template, request
from openai import OpenAI, BadRequestError
from dotenv import load_dotenv
from langdetect import detect
import os

# .env 파일 로드
load_dotenv()

app = Flask(__name__)
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# 장르와 프롬프트 설정
movie_genre = {
    "Comedy": {
        "prompt_ko": "제공된 상황을 기반으로 재미있고 가벼운 영화 대사를 한국어로 만들어주세요.",
        "prompt_en": "Create a humorous and light-hearted movie quote based on the situation provided."
    },
    "Romance": {
        "prompt_ko": "제공된 상황을 기반으로 감성적이고 사랑스러운 영화 대사를 한국어로 만들어주세요.",
        "prompt_en": "Create a romantic and heartfelt movie quote based on the situation provided."
    },
    "Action": {
        "prompt_ko": "제공된 상황을 기반으로 강렬하고 긴장감 넘치는 영화 대사를 한국어로 만들어주세요.",
        "prompt_en": "Create an intense and thrilling movie quote based on the situation provided."
    },
    "Drama": {
        "prompt_ko": "제공된 상황을 기반으로 감동적이고 깊이 있는 영화 대사를 한국어로 만들어주세요.",
        "prompt_en": "Create an emotional and deep movie quote based on the situation provided."
    },
    "Fantasy": {
        "prompt_ko": "제공된 상황을 기반으로 상상력 넘치고 마법 같은 영화 대사를 한국어로 만들어주세요.",
        "prompt_en": "Create an imaginative and magical movie quote based on the situation provided."
    },
    "Horror": {
        "prompt_ko": "제공된 상황을 기반으로 무섭고 소름 끼치는 영화 대사를 한국어로 만들어주세요. (그래픽 콘텐츠는 피해주세요.)",
        "prompt_en": "Create a suspenseful and eerie movie quote based on the situation provided, avoiding any graphic content."
    },
    "SciFi": {
        "prompt_ko": "제공된 상황을 기반으로 미래지향적이고 기술적인 영화 대사를 한국어로 만들어주세요.",
        "prompt_en": "Create a futuristic and technical movie quote based on the situation provided."
    },
    "Thriller": {
        "prompt_ko": "제공된 상황을 기반으로 긴박하고 미스터리한 영화 대사를 한국어로 만들어주세요.",
        "prompt_en": "Create a tense and mysterious movie quote based on the situation provided."
    },
    "Mystery": {
        "prompt_ko": "제공된 상황을 기반으로 신비롭고 궁금증을 자아내는 영화 한국어로 대사를 만들어주세요.",
        "prompt_en": "Create a puzzling and intriguing movie quote based on the situation provided."
    },
    "Adventure": {
        "prompt_ko": "제공된 상황을 기반으로 흥미롭고 탐험적인 영화 대사를 한국어로 만들어주세요.",
        "prompt_en": "Create an exciting and adventurous movie quote based on the situation provided."
    }
}

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
        
        try:
            # 입력된 텍스트의 언어 감지
            language = detect(user_input)
            if language == 'ko':
                prompt = f"{movie_genre[selected_genre]['prompt_ko']} {user_input} 스타일: {selected_style}, 연도: {selected_period}"
            else:
                prompt = f"{movie_genre[selected_genre]['prompt_en']} {user_input} Style: {selected_style}, Decade: {selected_period}"


            if user_input and selected_genre and selected_style and selected_period:
                text_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a movie writer. Write one line of dialog that fits the genre, style, and time period."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8,
                )
                response_text = text_response.choices[0].message.content
                
                image_prompt = f"Create a scene from a {selected_genre} film in {selected_style} style from the {selected_period}. {user_input}"
                image_response = client.images.generate(
                    model="dall-e-3",
                    prompt=image_prompt,
                    n=1,
                    size="1024x1024",
                    quality="standard"
                )
                response_image = image_response.data[0].url
                
        except BadRequestError as e:
            show_error_modal = True

    return render_template('index.html', movie_genre=movie_genre, selected_genre=selected_genre, selected_style=selected_style, selected_period=selected_period, user_input=user_input, response=response_text, response_image=response_image, show_error_modal=show_error_modal)

if __name__ == '__main__':
    app.run(debug=True)
