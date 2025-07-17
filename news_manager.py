import json
import os

NEWS_FILE = 'news.json'

class NewsManager:
    def __init__(self):
        self.news = []
        self.load_news()

    def load_news(self):
        """加载新闻数据"""
        if os.path.exists(NEWS_FILE):
            try:
                with open(NEWS_FILE, 'r', encoding='utf-8') as f:
                    self.news = json.load(f)
            except Exception as e:
                print(f"加载新闻失败: {e}")
                self.news = []
        else:
            self.news = []

    def save_news(self):
        """保存新闻数据"""
        try:
            with open(NEWS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.news, f, ensure_ascii=False, indent=4)
            print("新闻保存成功!")
        except Exception as e:
            print(f"保存新闻失败: {e}")

    def add_news(self, title, url):
        """添加新闻"""
        # 检查是否已存在相同标题或URL
        for item in self.news:
            if item['title'] == title or item['url'] == url:
                print("错误: 新闻标题或URL已存在!")
                return False
        
        self.news.append({
            'title': title,
            'url': url
        })
        self.save_news()
        return True

    def delete_news(self, index):
        """删除新闻"""
        if 0 <= index < len(self.news):
            del self.news[index]
            self.save_news()
            return True
        return False

    def list_news(self):
        """列出所有新闻"""
        if not self.news:
            print("暂无新闻数据")
            return
        
        print("===== 新闻列表 =====")
        for i, item in enumerate(self.news):
            print(f"[{i+1}] {item['title']}")
            print(f"   URL: {item['url']}")
        print("====================")

    def run(self):
        """运行管理程序"""
        print("===== 新闻管理程序 =====")
        while True:
            print("\n操作菜单:")
            print("1. 查看所有新闻")
            print("2. 添加新闻")
            print("3. 删除新闻")
            print("4. 退出")
            
            choice = input("请选择操作 (1-4): ")
            
            if choice == '1':
                self.list_news()
            elif choice == '2':
                title = input("请输入新闻标题: ")
                url = input("请输入新闻链接: ")
                if self.add_news(title, url):
                    print("新闻添加成功!")
            elif choice == '3':
                self.list_news()
                if self.news:
                    index = input("请输入要删除的新闻序号: ")
                    try:
                        index = int(index) - 1
                        if self.delete_news(index):
                            print("新闻删除成功!")
                        else:
                            print("无效的序号!")
                    except ValueError:
                        print("请输入有效的数字!")
            elif choice == '4':
                print("谢谢使用，再见!")
                break
            else:
                print("无效的选择，请重试!")

if __name__ == '__main__':
    manager = NewsManager()
    manager.run()