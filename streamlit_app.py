import streamlit as st
import random
import string
import time
import math

# 유효한 문자 리스트
english_characters = string.ascii_letters + string.digits + " .,!?\"'():;"
korean_characters = [chr(i) for i in range(0xAC00, 0xD7A4)] + list(string.digits + " .,!?\"'():;")

# 무작위 문자열 생성 함수
def generate_random_string(length, characters):
    return ''.join(random.choice(characters) for _ in range(length))

# 무한 원숭이 이론 소개글
intro_text = """
무한 원숭이 이론은 무한한 시간 동안 무작위로 타자기를 두드리는 원숭이가 
결국 셰익스피어의 작품과 같은 특정 텍스트를 작성할 수 있다는 수학적 개념입니다.

아래에 입력한 텍스트와 동일한 문자열이 무작위로 생성될 때까지 
프로그램이 계속해서 텍스트를 생성합니다.
"""
language='English'
st.title('무한 원숭이 이론 테스트')
st.markdown(intro_text)

# 사용자 입력 텍스트
if language == "한국어":
    input_text = st.text_input("한글 텍스트를 입력하세요 (한글, 숫자, 특수기호(.,?!()\"':;) 사용 가능):", value="")
    valid_characters = korean_characters
    is_valid_input = all('가' <= char <= '힣' for char in input_text)
else:
    input_text = st.text_input("영문 텍스트를 입력하세요 (대소문자 알파벳, 숫자, 특수기호(.,?!()\"':;) 사용 가능):", value="")
    valid_characters = english_characters
    is_valid_input = all(char in valid_characters for char in input_text)

# 입력 검증
if input_text and not is_valid_input:
    st.error("입력한 텍스트가 유효하지 않습니다. 다시 입력해주세요.")

if is_valid_input and input_text:
    # 입력된 텍스트의 길이와 유효한 문자 개수
    input_length = len(input_text)
    num_valid_characters = len(valid_characters)

    # 평균적으로 필요한 문자 생성 횟수 계산
    if input_length > 0:
        average_attempts = int(math.pow(num_valid_characters, input_length))
    else:
        average_attempts = 0

    st.write(f"입력한 텍스트가 나오기까지 평균적으로 필요한 문자 생성 횟수: {format(average_attempts, ',')}")

    # 생성 버튼 및 중지 버튼
    start_button = st.button("생성 시작")
    stop_button = st.button("중지")

    # 상태 변수 초기화
    if 'generated_text' not in st.session_state:
        st.session_state.generated_text = ''
    if 'running' not in st.session_state:
        st.session_state.running = False
    if 'char_count' not in st.session_state:
        st.session_state.char_count = 0

    # 텍스트 생성을 중지하는 함수
    def stop_generation():
        st.session_state.running = False
        char_count_display = st.empty()
        text_area = st.empty()
        char_count_display.write(f"현재까지 입력된 문자 개수: {format(st.session_state.char_count,',')}")
        text_area.markdown(f"<div style='word-wrap: break-word;'>{st.session_state.generated_text[-2000:]}</div>", unsafe_allow_html=True)
            


    # 텍스트 생성을 시작하는 함수
    def start_generation():
        st.session_state.running = True
        st.session_state.generated_text = ''
        st.session_state.char_count = 0
        
        char_count_display = st.empty()
        text_area = st.empty()

        while st.session_state.running:
            st.session_state.char_count += 1
            new_char = random.choice(valid_characters)
            st.session_state.generated_text += new_char

            if st.session_state.generated_text[-input_length:] == input_text:
                st.success(f"입력한 텍스트 '{input_text}'와 동일한 문자열이 생성되었습니다!")
                stop_generation()

            # 생성된 텍스트와 문자 개수 표시
            char_count_display.write(f"현재까지 입력된 문자 개수: {format(st.session_state.char_count,',')}")
            text_area.markdown(f"<div style='word-wrap: break-word; word-break: break-all;'>{st.session_state.generated_text[-1000:]}</div>", unsafe_allow_html=True)
            # UI 업데이트를 위해 슬립 추가
            time.sleep(0.005)

    # 버튼 동작 설정
    if start_button:
        start_generation()

    if stop_button:
        stop_generation()

    
