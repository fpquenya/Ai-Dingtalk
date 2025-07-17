import http.server
import socketserver
import json
import os
from urllib.parse import urlparse, parse_qs
from datetime import datetime
from http.server import HTTPServer

class NewsHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 如果请求的是根路径，则将其指向 index.html
        if self.path == '/':
            self.path = '/index.html'

        # 将API请求与文件服务分离开
        if self.path == '/news.json':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                with open('news.json', 'r', encoding='utf-8') as f:
                    content = f.read()
                news_data = json.loads(content)
                standardized_data = self.standardize_news_data(news_data)
                self.wfile.write(json.dumps(standardized_data, ensure_ascii=False).encode('utf-8'))
            except (FileNotFoundError, json.JSONDecodeError):
                # 如果文件不存在或损坏，返回空列表
                self.wfile.write(b'[]')

        elif self.path == '/api/stats':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            try:
                with open('news.json', 'r', encoding='utf-8') as f:
                    news_data = json.loads(f.read())
                stats = self.calculate_stats(news_data)
                self.wfile.write(json.dumps(stats, ensure_ascii=False).encode('utf-8'))
            except Exception:
                self.wfile.write(b'{"total": 0, "today": 0}')
        else:
            # 对于所有其他路径，使用默认的文件服务处理器
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/api/news':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                news_data = json.loads(post_data.decode('utf-8'))
                
                # 验证和标准化数据
                validated_data = self.validate_and_standardize(news_data)
                
                # 备份原文件
                if os.path.exists('news.json'):
                    backup_name = f'news_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
                    try:
                        with open('news.json', 'r', encoding='utf-8') as src:
                            with open(backup_name, 'w', encoding='utf-8') as dst:
                                dst.write(src.read())
                    except:
                        pass  # 备份失败不影响主要功能
                
                # 保存新数据
                with open('news.json', 'w', encoding='utf-8') as f:
                    json.dump(validated_data, f, ensure_ascii=False, indent=4)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "success",
                    "message": "新闻数据保存成功",
                    "count": len(validated_data)
                }, ensure_ascii=False).encode('utf-8'))
                
            except json.JSONDecodeError as e:
                self.send_error_response(400, f"JSON格式错误: {str(e)}")
            except ValueError as e:
                self.send_error_response(400, f"数据验证失败: {str(e)}")
            except PermissionError:
                self.send_error_response(403, "没有写入权限，请检查文件权限")
            except Exception as e:
                self.send_error_response(500, f"服务器内部错误: {str(e)}")
        else:
            self.send_response(404)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write('{"error": "接口不存在"}'.encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def send_error_response(self, code, message):
        """发送错误响应"""
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        error_data = {
            "status": "error",
            "message": message,
            "code": code
        }
        self.wfile.write(json.dumps(error_data, ensure_ascii=False).encode('utf-8'))
    
    def standardize_news_data(self, news_data):
        """标准化新闻数据格式"""
        if not isinstance(news_data, list):
            return []
        
        standardized = []
        for i, item in enumerate(news_data):
            if not isinstance(item, dict):
                continue
                
            # 确保必要字段存在
            standardized_item = {
                "id": item.get("id", int(datetime.now().timestamp() * 1000) + i),
                "title": str(item.get("title", "")).strip(),
                "url": str(item.get("url", "")).strip(),
                "createTime": item.get("createTime", datetime.now().isoformat()),
                "updateTime": item.get("updateTime", datetime.now().isoformat())
            }
            
            # 只保留有效的新闻项
            if standardized_item["title"] and standardized_item["url"]:
                standardized.append(standardized_item)
        
        return standardized
    
    def validate_and_standardize(self, news_data):
        """验证并标准化新闻数据"""
        if not isinstance(news_data, list):
            raise ValueError("新闻数据必须是数组格式")
        
        validated = []
        seen_titles = set()
        seen_urls = set()
        
        for item in news_data:
            if not isinstance(item, dict):
                continue
            
            title = str(item.get("title", "")).strip()
            url = str(item.get("url", "")).strip()
            
            if not title or not url:
                continue
            
            # 检查重复
            if title in seen_titles or url in seen_urls:
                continue
            
            seen_titles.add(title)
            seen_urls.add(url)
            
            # 验证URL格式
            if not (url.startswith('http://') or url.startswith('https://')):
                continue
            
            validated_item = {
                "id": item.get("id", int(datetime.now().timestamp() * 1000)),
                "title": title,
                "url": url,
                "createTime": item.get("createTime", datetime.now().isoformat()),
                "updateTime": item.get("updateTime", datetime.now().isoformat())
            }
            
            validated.append(validated_item)
        
        return validated
    
    def calculate_stats(self, news_data):
        """计算新闻统计信息"""
        if not isinstance(news_data, list):
            return {"total": 0, "today": 0}
        
        total = len(news_data)
        today = datetime.now().date()
        today_count = 0
        
        for item in news_data:
            if not isinstance(item, dict):
                continue
            
            # 统计今日新增
            create_time = item.get("createTime", "")
            try:
                if create_time:
                    create_date = datetime.fromisoformat(create_time.replace('Z', '+00:00')).date()
                    if create_date == today:
                        today_count += 1
            except:
                pass
        
        return {
            "total": total,
            "today": today_count
        }
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == '__main__':
    # 在Docker容器中使用0.0.0.0以允许外部访问
    host = '0.0.0.0'
    port = 8000
    server = HTTPServer((host, port), NewsHandler)
    print(f'启动服务器在 http://{host}:{port}')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\n服务器已停止')
        server.shutdown()