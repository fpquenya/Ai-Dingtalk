# Docker 部署指南

本指南将详细介绍如何使用 Docker 部署 AI-钉钉新闻管理系统。

## 前置条件

1. **安装 Docker**
   - Windows: 下载并安装 [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
   - macOS: 下载并安装 [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
   - Linux: 参考 [Docker 官方安装指南](https://docs.docker.com/engine/install/)

2. **验证 Docker 安装**
   ```bash
   docker --version
   docker-compose --version
   ```

## 部署步骤

### 方法一：使用 Docker Compose（推荐）

1. **克隆项目到服务器**
   ```bash
   git clone https://github.com/fpquenya/Ai-Dingtalk.git
   cd Ai-Dingtalk
   ```

2. **构建并启动容器**
   ```bash
   docker-compose up -d
   ```

3. **查看容器状态**
   ```bash
   docker-compose ps
   ```

4. **查看日志**
   ```bash
   docker-compose logs -f
   ```

5. **访问应用**
   - 打开浏览器访问: `http://localhost:8000`
   - 或者访问服务器IP: `http://your-server-ip:8000`

### 方法二：使用 Docker 命令

1. **构建镜像**
   ```bash
   docker build -t dingtalk-news .
   ```

2. **运行容器**
   ```bash
   docker run -d \
     --name dingtalk-news-app \
     -p 8000:8000 \
     -v $(pwd)/news.json:/app/news.json \
     --restart unless-stopped \
     dingtalk-news
   ```

3. **查看容器状态**
   ```bash
   docker ps
   ```

4. **查看日志**
   ```bash
   docker logs -f dingtalk-news-app
   ```

## 常用管理命令

### Docker Compose 命令

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看日志
docker-compose logs -f

# 进入容器
docker-compose exec dingtalk-news bash

# 重新构建镜像
docker-compose build --no-cache

# 更新并重启
docker-compose pull && docker-compose up -d
```

### Docker 命令

```bash
# 停止容器
docker stop dingtalk-news-app

# 启动容器
docker start dingtalk-news-app

# 重启容器
docker restart dingtalk-news-app

# 删除容器
docker rm dingtalk-news-app

# 删除镜像
docker rmi dingtalk-news

# 进入容器
docker exec -it dingtalk-news-app bash

# 查看容器资源使用情况
docker stats dingtalk-news-app
```

## 数据持久化

新闻数据存储在 `news.json` 文件中，通过 Docker 卷映射确保数据持久化：

```bash
# 备份数据
docker cp dingtalk-news-app:/app/news.json ./news_backup.json

# 恢复数据
docker cp ./news_backup.json dingtalk-news-app:/app/news.json
```

## 环境配置

### 端口配置

如需修改端口，编辑 `docker-compose.yml`：

```yaml
ports:
  - "9000:8000"  # 将本地9000端口映射到容器8000端口
```

### 环境变量

可以通过环境变量配置应用：

```yaml
environment:
  - PYTHONUNBUFFERED=1
  - DEBUG=false
  - PORT=8000
```

## 生产环境部署

### 1. 使用 Nginx 反向代理

创建 `nginx.conf`：

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 2. 添加 SSL 证书

```bash
# 使用 Let's Encrypt
sudo certbot --nginx -d your-domain.com
```

### 3. 设置自动重启

```yaml
# docker-compose.yml
restart: unless-stopped
```

## 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   # 查看端口占用
   netstat -tulpn | grep 8000
   # 或者修改端口
   ```

2. **权限问题**
   ```bash
   # 检查文件权限
   ls -la news.json
   # 修改权限
   chmod 644 news.json
   ```

3. **容器无法启动**
   ```bash
   # 查看详细日志
   docker-compose logs
   # 检查配置文件
   docker-compose config
   ```

4. **网络问题**
   ```bash
   # 检查网络
   docker network ls
   # 重建网络
   docker-compose down && docker-compose up -d
   ```

### 性能优化

1. **限制资源使用**
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '0.5'
         memory: 512M
   ```

2. **健康检查**
   ```yaml
   healthcheck:
     test: ["CMD", "curl", "-f", "http://localhost:8000"]
     interval: 30s
     timeout: 10s
     retries: 3
   ```

## 更新部署

```bash
# 1. 拉取最新代码
git pull origin main

# 2. 重新构建并部署
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# 3. 验证部署
docker-compose ps
docker-compose logs -f
```

## 监控和日志

### 日志管理

```bash
# 查看实时日志
docker-compose logs -f --tail=100

# 日志轮转配置
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

### 监控指标

```bash
# 查看资源使用
docker stats

# 查看容器信息
docker inspect dingtalk-news-app
```

---

**注意事项：**
- 确保防火墙开放8000端口
- 定期备份 `news.json` 数据文件
- 生产环境建议使用 HTTPS
- 监控容器资源使用情况