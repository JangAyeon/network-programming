import socket


if __name__ == "__main__":
    ## define the socket parameters
    host = "127.0.0.1"
    port = 8080
    print(f"Server is running on {host}:{port}")
    totalClients = int(input("Enter the total number of clients: "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Allow port reuse
    sock.bind((host, port))
    sock.listen(totalClients)
    connections = []
    print(f"Waiting for {totalClients} clients to connect...")

    ## Loop to accept connections from clients
    for i in range(totalClients):
        conn,addr = sock.accept()
        connections.append(conn)
        print(f"Client {i+1} connected: {addr}")


    # 파일 수신 처리
    fileNo = 0
    idx = 0
    for conn in connections:
        idx += 1
        fileName = f"output_{fileNo}.txt"
        fileNo += 1
        print(f"[클라이언트 {idx}] 파일 수신 시작: {fileName}")
        
        # 파일 열기 (쓰기 모드)
        fo = open(fileName, "w")
        
        # 클라이언트로부터 데이터를 청크 단위로 수신
        while True:
            # 1. 네트워크에서 데이터 수신 (최대 1024바이트)
            data_bytes = conn.recv(1024)
            
            # 2. 연결이 닫혔는지 확인 (빈 바이트 = 연결 종료)
            if not data_bytes:
                print(f"[클라이언트 {idx}] 연결이 닫혔습니다. 수신 완료.")
                break
            
            # 3. 바이트를 문자열로 디코딩
            data = data_bytes.decode()
            
            # 4. 파일에 데이터 쓰기
            fo.write(data)
            fo.flush()  # 즉시 디스크에 저장 (버퍼 비우기)
            print(f"[클라이언트 {idx}] 데이터 수신: {len(data)} bytes")
        
        # 5. 파일 닫기 (자동으로 flush됨)
        fo.close()
        print(f"[클라이언트 {idx}] 파일 저장 완료: {fileName}\n")
    
    # 모든 연결 닫기
    print("모든 클라이언트 연결 종료 중...")
    for conn in connections:
        conn.close()
    sock.close()
    print("서버 종료")
