import logging
from typing import Any

from . import settings
from .client import get_sign_reward, get_sign_reward_list, get_user_info, sign_in
from .models import SignRewardItemGetType
from .utils import get_current_month


def main():
    logging.info("开始签到")
    sign_in()
    # do_seal(SealType.SIGN)

    # logging.info("开始点赞")
    # counter = 0
    # for _ in range(10):
    #     time.sleep(3)
    #     r = like()
    #     if r.json()["data"] == 1:
    #         counter += 1
    #         logging.info(f"第{counter}次点赞结束")

    # time.sleep(3)
    # do_seal(SealType.LIKE)

    # logging.info("开始评论")
    # time.sleep(3)
    # comment()
    # do_seal(SealType.COMMENT)

    # logging.info("任务完成")

    if settings.input_check_house_remain:
        logging.info("开始检查房屋拆除倒计时")
        user_info: dict[str, Any] = get_user_info()
        house_remain_day = (
            user_info.get("data", {}).get("characterDetail", [{}])[0].get("house_remain_day")
        )
        if house_remain_day:
            raise Exception(f"房屋拆除倒计时：{house_remain_day}")

    if settings.input_get_sign_reward:
        reward_list = get_sign_reward_list(get_current_month())
        logging.info(f"本月奖励列表：{reward_list}")
        for reward in filter(
            lambda reward: reward.is_get == SignRewardItemGetType.AVAILABLE, reward_list
        ):
            logging.info(f"开始领取签到奖励：{reward.item_name}")
            r = get_sign_reward(reward.id, get_current_month())
            logging.info(r.json())


if __name__ == "__main__":
    main()
