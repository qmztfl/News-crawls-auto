from threading import Thread


from app import flask_main
from start import scrapy_main


def start_background_task():
    # 设置为守护线程，这样它会在主线程退出时自动终止
    thread = Thread(target=scrapy_main, daemon=True)
    thread.start()


if __name__ == '__main__':
    # app.run(host='0.0.0.0')
    start_background_task()
    flask_main()
