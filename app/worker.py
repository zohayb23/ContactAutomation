from rq import Worker

from app.queue import redis_conn


def main() -> None:
    worker = Worker(["email_sends"], connection=redis_conn)
    worker.work(with_scheduler=True)


if __name__ == "__main__":
    main()
