from enum import IntEnum
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

InputCookie = Annotated[
    str,
    BeforeValidator(lambda x: str.strip(str(x))),
]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    input_base_url: str = "https://apiff14risingstones.web.sdo.com"
    input_cookie: InputCookie = Field(default=...)
    input_user_agent: str = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML,"
        " like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    input_comment_content: str = '<p><span class="at-emo">[emo6]</span>&nbsp;</p>'
    input_like_post_id: int = 8
    input_comment_post_id: int = 8
    input_check_house_remain: bool = False
    input_get_sign_reward: bool = True


class SealType(IntEnum):
    SIGN = 1
    LIKE = 2
    COMMENT = 3


class SignRewardItem(BaseModel):
    id: int
    begin_date: str
    end_date: str
    rule: int
    item_name: str
    item_pic: str
    num: int
    item_desc: str
    is_get: int


class SignRewardItemGetType(IntEnum):
    UNMET = -1
    AVAILABLE = 0
    GOTTEN = 1


class SignRewardListResponse(BaseModel):
    code: int
    msg: str
    data: list[SignRewardItem]
