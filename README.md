# 구동 방법

- 새 터미널 생성 후, terminal에 "cd frontend" 입력 후, "streamlit run Home.py" 입력 (프론트엔드 서버 구동)
- 새 터미널 생성 후, terminal에 "cd backend" 입력 후, "uvicorn fast:app --reload" 입력 (백엔드 서버 구동)
- 프론트엔드 서버를 구동한 터미널의 Local URL: 주소 "Ctrl + click" (프론트엔드 서버 접속)

# 무슨 ai?

대화를 하면 할 수록 똑똑해지는 AI

- 지금까지 대화를 진행한 내용을 프롬프트에 쌓아가며, 대화를 참고할 수 있는 예제로 삼을 수 있도록 하는 기능을 수행한다.
- 사용자 데이터 베이스를 생성해서, 대화중 사용자의 이름을 알게되면, 데이터 베이스를 검색하는 트리거를 작동한다.
- or, 지금까지의 대화 리스트를 기반으로 retriever을 통해 특정 사용자와의 대화를 검색할 수 있도록 한다.

# 구현해야할 것

- 대화 fastapi로 서버통신하기 [완료]

- 구두대화 [구현중]
- retriever 구현

  - 주 프롬프트
  - 심리 상담 관련 문서
  - 사용자와의 대화 기록을 기반으로 '요약 GPT' 사용해서 만든 사용자 정보

    ```
    └── 📁.cache
        └── 📁docs
            └── mind.txt
            ...
        └── 📁history
            └── conversation_hisory.txt
            ...ㄹㄴㅇㄹㄴㄴ
        └── 📁prompt
            └── prompt.txt
    ```

- retrieve 된 사용자 정보 데이터 베이스 저장
- 어떤 형식으로 저장할 것인지 고민 필요

- opencv로 객체 인식하고 상호작용하기 []

# 세부적인 수정점

- 어떻게 대화를 종료할 것인가? (done)
