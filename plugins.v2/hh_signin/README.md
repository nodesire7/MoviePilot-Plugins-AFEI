# 憨憨PT站签到插件

自动执行憨憨PT站签到任务的插件

### 功能
- 支持定时自动签到
- 支持签到结果通知
- 支持失败重试
- 使用Selenium模拟真实浏览器签到

### 配置
- enabled: 插件开关
- cron: 定时任务时间表达式，如"0 8 * * *"
- cookie: 憨憨PT站Cookie信息
- notify: 是否开启消息通知
- site_url: 站点地址
- retry_count: 失败重试次数
- retry_timeout: 重试等待时间(秒)

### 依赖
- selenium
- MoviePilot Chrome组件

### 使用说明
1. 配置站点Cookie
2. 开启插件
3. 设置定时任务时间
4. 保存配置后自动执行签到任务

### 注意事项
- 请确保Cookie配置正确且未过期
- 建议将重试次数设置在1-3次之间

### 配置示例
```json
{
  "enabled": true,
  "cron": "0 8 * * *",
  "cookie": "your_cookie_here",
  "notify": true,
  "chromedriver_path": "path_to_chromedriver"
}
```
