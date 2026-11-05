# 南诏工匠官网 · 第一轮修复

## 当前发布方式（2026-11-05 更新）

仓库已配置 `.github/workflows/deploy.yml`：推送或合并到 main 会通过 GitHub Actions 使用 Wrangler 发布到现有 Cloudflare Pages 项目 nanzhaoarts。项目仍使用直接上传 API，但不再需要手动上传。以下 2026-11-02 的手动上传说明仅作为历史记录。

SEO 修复前源代码：69372682d682ae04d8bd38938c16110500e7d45f；修复前生产部署：f651353d-05b1-4c27-8a7d-f5691f46cec3。规范主域为 https://nanzhaoarts.com/ 。顾问路由 `/a/* /index.html 200` 保留。

回滚时在 Pages 部署列表选择修复前生产部署；同时恢复 GitHub 对应源码，防止下一次 main 推送覆盖回滚结果。www 跳转规则需在 Cloudflare 域名规则中单独停用才能回滚。

生产静态文件位于仓库根目录；保留原有团队、繁简英、作品和门店导航。

## 发布

Cloudflare Pages 项目 nanzhaoarts 当前使用直接上传，未连接 Git 自动部署。将仓库根目录静态文件（含 img、round1、_headers、_redirects）上传到现有项目生产环境。不要上传本地预览目录、归档目录或 Node 预览服务器。

## 线上回滚

本次修改前生产部署：7f7c88e5-7049-45dc-ac72-f13df0b258da。
部署地址：https://7f7c88e5.nanzhaoarts.pages.dev/

发布后如需回退，在 Cloudflare Pages 的 nanzhaoarts 部署列表找到该部署，选择“回滚到此部署”。仓库分支 before-round1-20261102 保存修改前公开静态文件；main 保存修复版。公开归档不包含账号配置、后台源码或外部视频文件。

## 本轮改动

隐藏缺资料渠道及占位内容；手机按钮避让；作品详情可滚动、切换、重试；弹层焦点与键盘操作；菜单状态和正文标记。没有补造团队、作品、资历或服务信息。现有称谓、时间节点和地图坐标仍需后续核验。
