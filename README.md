# Simple Chat Server
---
# 실행 방법
## 요구사항
- Docker 설치 필요
## 서버 실행
```bash
docket compose up --build
```
`http://localhost:8000/` 으로 접속 가능

# 전체 구조
![image](https://github.com/user-attachments/assets/61bbfe98-e8c0-4c50-9bc0-1ff92e663d4d)
- RDB 에서는 기본 유저 정보와 채팅방 정보, 유저가 채팅방 진입 후의 상태를 관리합니다
- RDB는 API 와 통신하며 Websocket과는 연결하지 않습니다
- Websocket은 Django channels를 이용하여 연결합니다
- Redis pub/sub을 이용해 메시지를 전달합니다
- MongoDB에는 사용자가 채팅방에 접속하여 Websocket이 연결되거나 연결 해제된 경우를 기록합니다
- MongoDB에는 사용자의 메시지를 저장합니다
