# Port Scanner Socket 프로그램

TCP 소켓을 사용한 간단한 포트 스캐너입니다. 특정 호스트의 열린 포트를 검색할 수 있습니다.

## 📋 목차

- [프로젝트 개요](#프로젝트-개요)
- [기능](#기능)
- [파일 구조](#파일-구조)
- [사용 방법](#사용-방법)
- [동작 원리](#동작-원리)
- [코드 설명](#코드-설명)
- [주의사항](#주의사항)

## 🎯 프로젝트 개요

이 프로젝트는 Python의 `socket` 모듈을 사용하여 TCP/IP 기반 포트 스캐닝을 구현합니다. 특정 호스트의 열린 포트를 검색하여 네트워크 보안 및 진단에 활용할 수 있습니다.

## ✨ 기능

- ✅ TCP 소켓을 통한 포트 스캔
- ✅ 범위 포트 스캔 (50-500)
- ✅ 스캔 시간 측정
- ✅ 호스트 이름을 IP 주소로 변환
- ✅ 실시간 열린 포트 출력

## 📁 파일 구조

```
2. port-scanner-socket/
├── scanner.py          # 포트 스캐너 프로그램
└── README.md           # 이 파일
```

## 🚀 사용 방법

### 실행 방법

터미널에서 실행합니다:

```bash
cd "2. port-scanner-socket"
python3 scanner.py
```

### 실행 예시

프로그램을 실행하면 타겟 호스트를 입력하라는 메시지가 나타납니다:

```
Enter the target host ip Address:
```

**입력 예시:**

- `127.0.0.1` (로컬 호스트)
- `localhost` (로컬 호스트)
- `google.com` (도메인 이름)
- `192.168.1.1` (IP 주소)

### 출력 예시

**로컬 호스트 스캔:**

```
Enter the target host ip Address: 127.0.0.1
Scanning Target: 127.0.0.1 ( 127.0.0.1 )
Scanning Started at: 2024-01-15 14:30:00
Port 80 is open
Port 443 is open
Port 8080 is open
Time taken: 12.45
```

**도메인 이름 스캔:**

```
Enter the target host ip Address: google.com
Scanning Target: google.com ( 142.250.191.14 )
Scanning Started at: 2024-01-15 14:30:00
Port 80 is open
Port 443 is open
Time taken: 15.67
```

## 🔄 동작 원리

### 전체 흐름도

```
┌─────────┐                    ┌─────────┐
│ 스캐너   │                    │ 타겟 호스트│
└────┬────┘                    └────┬────┘
     │                              │
     │  1. 호스트 이름 → IP 변환     │
     │                              │
     │  2. socket() 생성             │
     │                              │
     │  3. connect_ex((IP, port))   │
     ├─────────────────────────────>│
     │                              │
     │  4. 연결 결과 확인             │
     │<─────────────────────────────┤
     │                              │
     │  5. close()                  │
     ├─────────────────────────────>│
     │                              │
     │  (다음 포트로 반복 50-500)     │
```

### 상세 동작 과정

1. **호스트 이름 변환**

   - 사용자가 입력한 도메인 이름 또는 IP 주소를 처리
   - `gethostbyname()` 함수로 도메인 이름을 IP 주소로 변환
   - 예: `google.com` → `142.250.191.14`

2. **포트 스캔 시작**

   - 스캔 시작 시간을 기록
   - 포트 50부터 499까지 순차적으로 스캔

3. **각 포트에 대한 연결 시도**

   - TCP 소켓 생성 (`socket(AF_INET, SOCK_STREAM)`)
   - `connect_ex()`로 연결 시도
   - 반환값 확인:
     - **0**: 연결 성공 → 포트가 열려있음
     - **0이 아님**: 연결 실패 → 포트가 닫혀있거나 필터링됨
   - 소켓 닫기

4. **결과 출력**
   - 열린 포트를 발견하면 즉시 출력
   - 모든 포트 스캔 완료 후 총 소요 시간 출력

## 💻 코드 설명

### 전체 코드 구조

```python
from socket import *
import time

startTime = time.time()

if __name__ == "__main__":
    target = input("Enter the target host ip Address: ")
    t_IP = gethostbyname(target)
    print(f"Scanning Target: {target} ( {t_IP} )")
    print("Scanning Started at: ", time.strftime("%Y-%m-%d %H:%M:%S"))
    for i in range(50, 500):
        s = socket(AF_INET, SOCK_STREAM)
        conn = s.connect_ex((t_IP, i))
        if(conn == 0):
            print(f"Port {i} is open")
        s.close()
    print(f"Time taken: {time.time() - startTime}")
```

### 주요 단계별 설명

#### 1. 시간 측정 시작

```python
startTime = time.time()
```

- 프로그램 시작 시점의 시간을 기록
- 나중에 총 소요 시간을 계산하기 위함

#### 2. 타겟 호스트 입력

```python
target = input("Enter the target host ip Address: ")
t_IP = gethostbyname(target)
```

- 사용자로부터 타겟 호스트 입력 받기
- `gethostbyname()`: 도메인 이름을 IP 주소로 변환
  - IP 주소를 입력하면 그대로 반환
  - 도메인 이름을 입력하면 DNS 조회 후 IP 주소 반환

#### 3. 스캔 정보 출력

```python
print(f"Scanning Target: {target} ( {t_IP} )")
print("Scanning Started at: ", time.strftime("%Y-%m-%d %H:%M:%S"))
```

- 스캔 대상 정보 출력
- 스캔 시작 시간을 읽기 쉬운 형식으로 출력

#### 4. 포트 스캔 루프

```python
for i in range(50, 500):
    s = socket(AF_INET, SOCK_STREAM)
    conn = s.connect_ex((t_IP, i))
    if(conn == 0):
        print(f"Port {i} is open")
    s.close()
```

**단계별 설명:**

- `range(50, 500)`: 포트 50부터 499까지 스캔
- `socket(AF_INET, SOCK_STREAM)`:
  - `AF_INET`: IPv4 주소 체계 사용
  - `SOCK_STREAM`: TCP 프로토콜 사용
- `connect_ex((t_IP, i))`:
  - 타겟 IP와 포트에 연결 시도
  - `connect()`와 달리 예외를 발생시키지 않고 에러 코드 반환
  - 반환값 0: 연결 성공 (포트 열림)
  - 반환값 != 0: 연결 실패 (포트 닫힘)
- `s.close()`: 소켓 연결 종료

#### 5. 총 소요 시간 출력

```python
print(f"Time taken: {time.time() - startTime}")
```

- 현재 시간에서 시작 시간을 빼서 총 소요 시간 계산
- 초 단위로 출력

## ⚠️ 주의사항

### 1. 법적 및 윤리적 고려사항

- ⚠️ **매우 중요**: 허가 없이 다른 사람의 시스템을 스캔하는 것은 불법일 수 있습니다
- 자신의 시스템이나 명시적으로 허가를 받은 시스템만 스캔하세요
- 교육 및 학습 목적으로만 사용하세요
- 무단 스캔은 사이버 범죄로 간주될 수 있습니다

### 2. 방화벽 및 보안 소프트웨어

- 방화벽이 포트 스캔을 차단하거나 감지할 수 있습니다
- 보안 소프트웨어가 스캔을 악성 활동으로 감지할 수 있습니다
- 로컬 호스트(`127.0.0.1`)로 테스트하는 것이 가장 안전합니다

### 3. 스캔 시간

- 포트 범위가 넓을수록 스캔 시간이 오래 걸립니다
- 현재 코드는 순차적으로 스캔하므로 느릴 수 있습니다
- 50-500 포트 스캔은 약 10-30초 정도 소요될 수 있습니다
- 네트워크 상태에 따라 더 오래 걸릴 수 있습니다

### 4. 네트워크 타임아웃

- `connect_ex()`는 기본 타임아웃이 길어서 느릴 수 있습니다
- 닫힌 포트에 대한 연결 시도가 타임아웃까지 기다려야 합니다
- 타임아웃을 설정하면 스캔 속도를 향상시킬 수 있습니다:
  ```python
  s.settimeout(0.5)  # 0.5초 타임아웃
  ```

### 5. 에러 처리 부족

- 존재하지 않는 도메인 이름을 입력하면 `gethostbyname()`이 예외를 발생시킵니다
- 네트워크 오류 시 프로그램이 중단될 수 있습니다
- 에러 처리를 추가하는 것을 권장합니다

### 6. 포트 범위 제한

- 현재 코드는 하드코딩된 포트 범위(50-500)를 사용합니다
- 다른 범위를 스캔하려면 코드를 수정해야 합니다

## 🔧 개선 가능한 사항

- [ ] 타임아웃 설정으로 스캔 속도 향상
- [ ] 멀티스레딩으로 병렬 스캔 구현
- [ ] 사용자 정의 포트 범위 입력 기능
- [ ] 에러 처리 추가 (호스트 이름 오류, 네트워크 오류 등)
- [ ] 결과를 파일로 저장하는 기능
- [ ] 스캔 진행률 표시 (진행 바 또는 퍼센트)
- [ ] UDP 포트 스캔 지원
- [ ] 서비스 버전 감지 기능
- [ ] 명령줄 인자(CLI) 지원

## 📚 학습 포인트

이 프로젝트를 통해 학습할 수 있는 내용:

### 1. TCP 소켓 프로그래밍

- `socket.socket()` 소켓 생성
- `connect_ex()` 연결 시도 및 에러 코드 처리
- `close()` 소켓 종료
- IPv4 주소 체계 (`AF_INET`)
- TCP 프로토콜 (`SOCK_STREAM`)

### 2. 네트워크 스캐닝 기초

- 포트 스캔의 기본 원리
- TCP 3-way handshake 과정
- 연결 상태 확인 방법
- 열린 포트와 닫힌 포트 구분

### 3. 네트워크 주소 변환

- DNS 조회 (`gethostbyname()`)
- 도메인 이름 → IP 주소 변환
- 호스트 이름 해석

### 4. 성능 측정

- 시간 측정 (`time.time()`)
- 스캔 효율성 분석
- 타임아웃 최적화

### 5. 네트워크 보안

- 포트 스캔의 보안적 의미
- 방화벽과 포트 필터링
- 네트워크 진단 도구

## 🧪 테스트 방법

### 로컬 호스트 테스트

1. **간단한 서버 실행** (다른 터미널에서):

   ```bash
   # Python으로 간단한 HTTP 서버 실행 (포트 8080)
   python3 -m http.server 8080
   ```

2. **포트 스캐너 실행** (새 터미널에서):

   ```bash
   cd "2. port-scanner-socket"
   python3 scanner.py
   ```

3. **입력 및 결과 확인**:

   ```
   Enter the target host ip Address: 127.0.0.1
   Scanning Target: 127.0.0.1 ( 127.0.0.1 )
   Scanning Started at: 2024-01-15 14:30:00
   Port 8080 is open
   Time taken: 12.34
   ```

### 여러 포트 테스트

여러 포트에서 서비스를 실행하여 테스트할 수 있습니다:

```bash
# 터미널 1: 포트 3000에서 서버 실행
python3 -m http.server 3000

# 터미널 2: 포트 4000에서 서버 실행
python3 -m http.server 4000

# 터미널 3: 스캐너 실행
python3 scanner.py
# Enter the target host ip Address: 127.0.0.1
```

## 🔍 에러 코드 참고

`connect_ex()`가 반환하는 주요 에러 코드:

- **0**: 연결 성공 (포트 열림)
- **61**: Connection refused (포트 닫힘, 연결 거부)
- **60**: Operation timed out (타임아웃)
- **51**: Network is unreachable (네트워크 도달 불가)
- **64**: Host is down (호스트 다운)

## 📖 참고 자료

- [Python socket 모듈 공식 문서](https://docs.python.org/3/library/socket.html)
- [TCP/IP 소켓 프로그래밍](https://en.wikipedia.org/wiki/Network_socket)
- [포트 스캐닝 기초](https://en.wikipedia.org/wiki/Port_scanner)
- [TCP 3-way Handshake](https://en.wikipedia.org/wiki/Transmission_Control_Protocol#Connection_establishment)

## 💡 활용 예시

### 1. 로컬 서버 포트 확인

자신의 컴퓨터에서 실행 중인 서비스의 포트를 확인:

```bash
python3 scanner.py
# Enter the target host ip Address: 127.0.0.1
```

### 2. 네트워크 장치 진단

로컬 네트워크의 장치 포트 상태 확인:

```bash
python3 scanner.py
# Enter the target host ip Address: 192.168.1.1
```

### 3. 학습 및 실습

네트워크 프로그래밍과 포트 스캐닝 개념 학습에 활용
