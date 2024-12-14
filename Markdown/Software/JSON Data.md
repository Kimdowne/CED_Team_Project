우리가 저장할 데이터 베이스를 JSON 형태로 나타냄

```
user = {
	"name": username,
	"age": userage,
	"record" : [
		{ "type": human, "id": id, "conversation": 요약된 질문 },
		{ "type": ai, "id": id, "conversation": 요약된 답변 },
		{ "type": human, "id": id, "conversation": 요약된 질문 },
		...
	]
	"emotion": "모델에 의해 크게 정의된 사용자의 현재 정서를 다룸."
}
```

데이터의 종류

사용자 정보 데이터
- 위 정보를 통해 만든 사용자 id()
- 사용자 이름
- 사용자 나이
- 사용자의 정서
- 

사용자 대화 내용
- input
- output
- datatime