import socket

if __name__ == "__main__":
    ## define the socket parameters
    host = "127.0.0.1"
    port = 8080
    print(f"Client is connecting to {host}:{port}")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print(f"Connected to {host}:{port}")

    ## File transfer loop
    while True:
        fileName = input("Enter the file name to send: (or 'exit' to end) ")
        if fileName == "exit":
            break
        else:
            try:
                # 1. 파일 열기 (읽기 모드)
                fi = open(fileName, "r")
                print(f"[전송 시작] 파일: {fileName}")
                
                # 2. 파일을 청크 단위로 읽어서 전송
                while True:
                    # 파일에서 1024바이트씩 읽기
                    data = fi.read(1024)
                    
                    # 파일 끝에 도달하면 종료
                    if not data:
                        print(f"[전송 완료] 파일: {fileName}")
                        break
                    
                    # 3. 네트워크로 데이터 전송
                    sock.send(data.encode())
                    print(f"[전송 중] {len(data)} bytes 전송됨")
                
                # 4. 파일 닫기
                fi.close()
                
            except IOError:
                print(f"[오류] 파일을 찾을 수 없습니다: {fileName}")
    
    # 연결 종료
    sock.close()
    print("클라이언트 종료")
