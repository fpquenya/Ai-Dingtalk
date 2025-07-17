# AI-钉钉新闻管理系统

一个集成钉钉AI助手的基于Web的新闻管理系统。

## 功能特性

- **AI助手集成**: 嵌入式钉钉AI助手，支持智能交互
- **新闻管理**: 添加、编辑、删除和组织新闻文章
- **搜索过滤**: 新闻文章实时搜索功能
- **响应式设计**: 移动端友好界面
- **数据持久化**: 基于JSON的数据存储，支持自动备份
- **统计分析**: 查看新闻统计和分析数据

## 项目结构

```
AI-Dingtalk/
├── index.html          # 主页面（AI助手和新闻显示）
├── news_page.html      # 新闻管理界面
├── news_server.py      # Python HTTP服务器后端
├── news_manager.py     # 新闻管理工具
├── news.json          # 新闻数据存储
└── README.md          # 项目文档
```

## 快速开始

1. **克隆仓库**:
   ```bash
   git clone https://github.com/fpquenya/Ai-Dingtalk.git
   cd Ai-Dingtalk
   ```

2. **启动服务器**:
   ```bash
   python news_server.py
   ```

3. **访问应用**:
   - 主页面: http://localhost:8000
   - 新闻管理: http://localhost:8000/news_page.html

## 使用方法

### 主界面
- 通过嵌入式iframe访问钉钉AI助手
- 在底部区域查看最新新闻更新

### 新闻管理
- 添加带标题和URL的新闻文章
- 搜索现有新闻文章
- 按日期排序（最新/最旧优先）
- 编辑或删除现有新闻条目
- 导出/导入新闻数据

## API接口

- `GET /news.json` - 获取所有新闻数据
- `POST /api/news` - 保存新闻数据
- `GET /api/stats` - 获取新闻统计信息

## 技术细节

- **后端**: Python HTTP服务器，自定义请求处理器
- **前端**: 原生HTML/CSS/JavaScript
- **数据存储**: JSON文件，支持自动备份
- **跨域**: 支持跨域请求

## 系统要求

- Python 3.6+
- 现代化Web浏览器
- 互联网连接（用于钉钉AI助手）

## 开源协议

本项目采用MIT协议开源。

## 贡献指南

欢迎贡献代码！请随时提交Pull Request。
