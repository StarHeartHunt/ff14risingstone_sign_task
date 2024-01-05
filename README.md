# FF14 石之家签到脚本

## 使用方法

- Fork 本仓库或者通过手动在已有或新建的仓库中新建 `.github/workflows/daily.yml` 文件，内容如下：

```yaml
name: Daily Tasks

on:
  schedule:
    # Runs at 10:30 am UTC+8 every day
    - cron: "30 2 * * *"
  workflow_dispatch:

jobs:
  run-tasks:
    name: Run FF14 Risingstones Tasks
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: docker://ghcr.io/starhearthunt/ff14risingstone_sign_task:master
        with:
          cookie: ${{ secrets.COOKIE }}
```

- 在 Settings > Secrets and variables > Actions 中，添加 COOKIE 键，值为 F12 获得的 cookie。

## 配置项

### 必填配置项

- `cookie`：石之家 API 的 cookie 字符串

### 可选配置项

可选配置项可以从 action 文件的 with 段传入，和必填项一样。

- `base_url`：API 的入口域名。默认值：`https://apiff14risingstones.web.sdo.com`
- `user_agent`：请求 API 时使用的用户代理。默认值：`Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36`
- `comment_content`：完成评论任务时的评论内容。默认值：`<p><span class="at-emo">[emo6]</span>&nbsp;</p>`
- `like_post_id`：完成点赞任务时要点赞的根帖子 id。默认值：`8`
- `comment_post_id`：完成评论任务时要评论的根帖子 id。默认值：`8`
- `check_house_remain`：是否检查角色房屋拆除倒计时。默认值：`false`

## 许可证

本仓库使用 MIT 许可证
