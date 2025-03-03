# 憨憨PT站签到插件

自动执行憨憨PT站签到任务的插件

### 功能
- 支持定时自动签到
- 支持签到结果通知
- 使用Selenium模拟真实浏览器签到

### 配置
- enabled: 插件开关
- cron: 定时任务时间表达式，如"0 8 * * *"
- cookie: 憨憨PT站Cookie信息
- notify: 是否开启消息通知

### 依赖
- selenium

### 注意事项
- 插件依赖MoviePilot的Chrome浏览器组件
- 请确保Cookie配置正确且未过期
