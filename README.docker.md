# Docker 部署指南

## 快速启动（三步）

### 1. 确保已安装 Docker Desktop
- Windows/Mac 下载：https://www.docker.com/products/docker-desktop
- 安装后启动 Docker Desktop

### 2. 在项目根目录执行构建
```bash
# 第一次构建（需要下载镜像，较慢，约 5-10 分钟）
docker-compose up --build

# 后台运行（推荐，不占用终端）
docker-compose up -d --build

# 查看日志
docker-compose logs -f
```

### 3. 访问系统
- 前端页面：http://localhost
- 后端 API 文档：http://localhost:8000/docs
- MySQL 连接：localhost:3306（用户名 root，密码 wxsadc421）

## 常用命令

```bash
# 停止所有服务
docker-compose down

# 停止并删除数据卷（会清空数据库！）
docker-compose down -v

# 只重启某个服务
docker-compose restart backend

# 进入容器内部调试
docker exec -it health_backend /bin/bash
docker exec -it health_mysql mysql -uroot -p

# 查看容器状态
docker-compose ps
```

## 生产环境注意事项

1. **修改密钥**：把 `SECRET_KEY` 改成随机长串
2. **修改密码**：把 `MYSQL_ROOT_PASSWORD` 和数据库密码改成强密码
3. **CORS 限制**：把 `ALLOW_ORIGINS` 改成你的域名，不要 `"*"`
4. **HTTPS**：使用 Nginx 或 CDN 配置 SSL 证书
5. **数据备份**：定期备份 `mysql_data` 卷

## 架构说明

```
用户浏览器 → http://localhost
    ↓
Nginx (frontend 容器，80 端口)
    ├── /api/* → 转发到 backend:8000 (FastAPI)
    └── 其他 → 返回 Vue 静态页面
    ↓
backend 容器 (8000 端口)
    ↓
mysql 容器 (3306 端口)
```

## 故障排查

**问题 1：后端提示数据库连不上**
- 检查 MySQL 是否启动完成：`docker-compose logs mysql`
- 确保 `DATABASE_URL` 里用的是 `mysql` 服务名，不是 `localhost`

**问题 2：前端提示 API 404**
- 检查 Nginx 配置是否正确反向代理到 `/api`
- 检查前端 `request.js` 里 `baseURL` 是否为 `/api`

**问题 3：修改代码后没有生效**
- 修改后端代码：需要重启 `docker-compose restart backend`
- 修改前端代码：需要重新构建 `docker-compose up -d --build frontend`
- 数据持久化：MySQL 数据在卷里，修改表结构需要手动迁移或删除卷重建

## 技术要点回顾

1. **为什么用多阶段构建前端？**
   - 第一阶段用 Node 镜像编译，第二阶段用 Nginx 镜像运行
   - 最终镜像只有 Nginx + 静态文件，没有 Node 环境，体积小、启动快、更安全

2. **为什么容器间用服务名通信？**
   - Docker 自定义网络内置 DNS，`mysql`、`backend` 自动解析为对应容器 IP
   - 不用管 IP 是多少，也不用 `localhost`（localhost 是每个容器自己）

3. **为什么需要 healthcheck？**
   - MySQL 启动需要时间建库建表，后端依赖它，等健康了再启动避免报错
   - 后端启动了不代表能响应请求，健康检查确保就绪后再让前端启动

4. **数据存在哪里？**
   - MySQL 数据在 `mysql_data` 卷，宿主机 Docker 目录下
   - 即使 `docker-compose down` 数据也不会丢，除非加 `-v` 删除卷
