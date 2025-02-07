# FF14 石之家签到脚本

## 使用方法

- Fork 本仓库或者通过手动在仓库中新建 `.github/workflows/daily.yml` 文件，内容如下：

```yaml
name: Daily Tasks

on:
  schedule:
    # Runs at 10:30 am UTC+8 every day
    - cron: "30 2 * * *"
  workflow_dispatch:

jobs:
  run-tasks:
    name: Run FF14 Risingstone Tasks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: docker://ghcr.io/starhearthunt/ff14risingstone_sign_task:master
        with:
          cookie: ${{ secrets.COOKIE }}
          user_agent: ${{ secrets.USER_AGENT }}
```

在 Settings > Secrets and variables > Actions，添加如下 Secret

1. `COOKIE`

   值为 `Cookie` 头中以等号 `=` 分割的 `ff14risingstones` 键值对，其中右值为 urlencode 后的结果。

   例：

   ```bash
   ff14risingstones=s%3A1111.2222222%2F33333
   ```

2. `USER_AGENT`

   > [!NOTE]
   > 由于石之家 API 新增的检测机制，需要设置与登录（获取 Cookie）时相同的 User-Agent 头，详情参考 [#17](https://github.com/StarHeartHunt/ff14risingstone_sign_task/issues/17)

   值为登录时向石之家 API 所发送的 `User-Agent` 头。

   例：

   ```bash
   Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36
   ```

## 配置项

### 必填配置项

- `cookie`：石之家 API cookie 中的 `ff14risingstones` 键值对
- `user_agent`：请求 API 时使用的用户代理

### 可选配置项

可选配置项可以从 action 文件的 with 段传入，和必填项一样。

- `base_url`：API 的入口域名。默认值：`https://apiff14risingstones.web.sdo.com`
- `comment_content`：完成评论任务时的评论内容。默认值：`<p><span class="at-emo">[emo6]</span>&nbsp;</p>`
- `like_post_id`：完成点赞任务时要点赞的根帖子 id。默认值：`8`
- `comment_post_id`：完成评论任务时要评论的根帖子 id。默认值：`8`
- `check_house_remain`：是否检查角色房屋拆除倒计时。默认值：`false`
- `get_sign_reward`：是否使用脚本领取当月签到奖励。默认值：`true`

## 许可证

本仓库使用 MIT 许可证
