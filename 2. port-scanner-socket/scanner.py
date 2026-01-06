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