import time

import httpx

from .config import Config
from .models import SealType

config = Config()
client = httpx.Client(
    headers={"User-Agent": config.user_agent, "Cookie": config.cookie}
)
base_url = config.base_url


def do_seal(type_: SealType):
    r = client.post(
        f"{base_url}/api/home/active/online2312/doSeal", data={"type": type_}
    )

    print(r.text)


def sign_in():
    r = client.post(f"{base_url}/api/home/sign/signIn")

    print(r.text)


def like():
    r = client.post(f"{base_url}/api/home/posts/like", data={"id": 8, "type": 1})
    print(r.text)

    return r


def comment():
    r = client.post(
        f"{base_url}/api/home/posts/comment",
        data={
            "content": '<p><span class="at-emo">[emo6]</span>&nbsp;</p>',
            "posts_id": "8",
            "parent_id": "0",
            "root_parent": "0",
            "comment_pic": "",
        },
    )

    print(r.text)


def main():
    print("开始签到")
    sign_in()
    time.sleep(3)
    do_seal(SealType.SIGN)

    print("开始点赞")
    counter = 0
    for _ in range(10):
        time.sleep(3)
        r = like()
        if r.json()["data"] == 1:
            counter += 1
            print(f"第{counter}次点赞结束")

    time.sleep(3)
    do_seal(SealType.LIKE)

    print("开始评论")
    time.sleep(3)
    comment()
    do_seal(SealType.COMMENT)


if __name__ == "__main__":
    main()
