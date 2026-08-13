import threading
import queue
import time
import random

# URL을 크롤링하는 함수
def crawl_url(url):
    """URL 크롤링 시뮬레이션"""
    time.sleep(random.uniform(0.5, 1.5))  # 네트워크 지연 시뮬레이션
    return f"{url}의 컨텐츠 (크기: {random.randint(1000, 5000)}KB)"

# 워커 스레드
def worker(url_queue, result_queue, worker_id):
    """큐에서 URL을 가져와 크롤링"""
    while True:
        try:
            url = url_queue.get(timeout=1)
            print(f"[워커 {worker_id}] {url} 크롤링 시작...")

            result = crawl_url(url)
            result_queue.put((url, result))

            print(f"[워커 {worker_id}] {url} 크롤링 완료")
            url_queue.task_done()
        except queue.Empty:
            break

# 크롤링할 URL 목록
urls = [
    "https://example.com/page1",
    "https://example.com/page2",
    "https://example.com/page3",
    "https://example.com/page4",
    "https://example.com/page5",
    "https://example.com/page6",
    "https://example.com/page7",
    "https://example.com/page8",
]

# Queue 생성
url_queue = queue.Queue()
result_queue = queue.Queue()

# URL을 큐에 추가
for url in urls:
    url_queue.put(url)

print(f"=== 웹 크롤러 시작 (총 {len(urls)}개 URL) ===\n")
start_time = time.time()

# 워커 스레드 4개 생성
num_workers = 4
threads = []

for i in range(num_workers):
    t = threading.Thread(target=worker, args=(url_queue, result_queue, i+1))
    threads.append(t)
    t.start()

# 모든 URL 크롤링 완료 대기
url_queue.join()

# 모든 워커 스레드 종료 대기
for t in threads:
    t.join()

end_time = time.time()

print(f"\n=== 크롤링 완료 ===")
print(f"총 소요 시간: {end_time - start_time:.2f}초")
print(f"수집된 결과 수: {result_queue.qsize()}개\n")

# 결과 출력
print("수집된 데이터:")
while not result_queue.empty():
    url, content = result_queue.get()
    print(f"  - {url}: {content}")
