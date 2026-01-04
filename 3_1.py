import threading

counter = 0
mutex = threading.Lock()


def worker_increment():
    global counter
    for _ in range(100_000):
        local = counter
        local += 1
        counter = local


def worker_dicrement():
    global counter
    for _ in range(100_000):
        local = counter
        local -= 1
        counter = local


def worker_increment_with_mutex():
    global counter
    for _ in range(100_000):
        with mutex:
            local = counter
            local += 1
            counter = local


def worker_dicrement_with_mutex():
    global counter
    for _ in range(100_000):
        with mutex:
            local = counter
            local -= 1
            counter = local


def main():
    n = 4
    m = 5

    threads: list[threading.Thread] = []

    for _ in range(n):
        thread = threading.Thread(target=worker_increment_with_mutex)
        threads.append(thread)

    for _ in range(m):
        thread = threading.Thread(target=worker_dicrement_with_mutex)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(counter)


if __name__ == "__main__":
    main()
