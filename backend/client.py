import socket
import json

class Server:
    def start_server(self, username, conv_summary):
        # 서버에 메시지를 보내는 함수
        def send_request(server_host, server_port, request):
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((server_host, server_port))
            print(f"[서버 연결 성공] {server_host}:{server_port}")

            try:
                # 요청을 JSON 문자열로 변환하여 송신
                json_request = json.dumps(request)
                client_socket.send(json_request.encode('utf-8'))
                print(f"[전송 성공] 서버로 요청을 전송했습니다.")

                # 서버의 응답 수신
                response = client_socket.recv(1024).decode('utf-8')
                response_data = json.loads(response)
                print(f"[서버 응답] {response_data}")
            finally:
                client_socket.close()

        # 클라이언트 실행
        if True:#__name__ == "__main__":
            # 데이터 저장 요청 => 입력 값을 저장하도록 수정
            save_request = {
                "action": "save",
                "data": {
                    "user_id": 1,   ##첫 번째 사람 쓸거니까 1
                    "name": username, ##이름 value로 변경경
                    "history": conv_summary #알아서 수정
                }
            }
            send_request("172.17.144.246", 5000, save_request)

            # 데이터 조회 요청 => 입력값으로 받도록 수정정
            fetch_request = {
                "action": "fetch",
                "user_id": 1
            }
            send_request("172.17.144.246", 5000, fetch_request)