# 南诏工匠官网发布与回滚记录

日期：2026-11-02。状态：第一轮修复版已发布到正式环境。

## 正式地址与源代码

- 官网：https://www.nanzhaoarts.com/
- 根域名：https://nanzhaoarts.com/
- 部署仓库：https://github.com/vane1202/nanzhaoarts
- 发布源代码提交：28511f7e433a5960295f78045c158c0dc0c4e9d1
- 发布前源代码提交：069a19005e1dfea2df7f45831a3f17f89f95d63d
- 发布前备份分支：before-round1-20261102

Cloudflare Pages 项目 nanzhaoarts 使用直接上传模式。仓库已同步源代码；GitHub 提交目前不会自动触发部署。本次没有修改 DNS，也没有迁移部署方式。

## 线上版本

- 新生产部署：8a10ed26-fd6e-4444-99b9-d6b79c9aa6ca
- 新版独立地址：https://8a10ed26.nanzhaoarts.pages.dev/
- 发布前生产部署：7f7c88e5-7049-45dc-ac72-f13df0b258da
- 旧版独立地址：https://7f7c88e5.nanzhaoarts.pages.dev/
- 项目后台：https://dash.cloudflare.com/c5e647d7c968bcef886d5eda410bc2eb/pages/view/nanzhaoarts

本次上传 production/ 内的47个文件，不包含本地预览提示及 noindex。上传包为 nanzhaoarts-production-2026-11-02-unix.zip；不要使用同目录中不带 unix 后缀的早期打包文件。

## 已验证

- www 与根域名返回正常；/a/a1 顾问入口返回正常。
- 44个非HTML静态资源逐文件 SHA-256 与正式发布清单一致。
- 正式页面没有预览条或 noindex，四位团队成员与六件作品保留。
- 正式域名作品弹窗可打开、图片加载正常，关闭后恢复操作；浏览器未记录错误日志。
- 英文390×844手机布局无横向溢出；导航展开后点击 Gallery 正常关闭，aria-expanded 恢复 false。
- 本地 baseline → round1 回滚演练已完成。线上旧版的“回滚到此部署”入口已确认，但未执行线上回滚，以保持新版在线。

机器验证见 docs/production-verification.json。既有资历、年份、地图坐标及服务承诺等事实的待核实状态不因本次发布而改变；本轮未验证真实消息收发。

## 线上回滚方法

1. 登录 Cloudflare，打开上方项目后台，进入部署列表。
2. 找到旧生产部署 7f7c88e5-7049-45dc-ac72-f13df0b258da。
3. 打开该部署的“更多选项”，选择“回滚到此部署”，完成平台确认。
4. 重新检查正式域名、图片、导航与联系入口。

线上回滚以 Cloudflare 已保留的历史部署为准。GitHub 备份分支用于源代码恢复；切换仓库分支本身不会改变当前线上网站。

## 本地交付

- 项目：D:/Codex/nanzhaoarts-round1-20261102
- 正式文件：production/
- 本地预览：site/，默认端口4319
- 发布前公开文件归档：D:/Codex/nanzhaoarts-backups/before-round1-2026-11-02
- 本地回滚：node scripts/release.mjs baseline
- 恢复本地修复版：node scripts/release.mjs round1

本地回滚只切换 site/，不会操作正式环境。公开文件归档不包含账户设置、数据库或外部视频源。
