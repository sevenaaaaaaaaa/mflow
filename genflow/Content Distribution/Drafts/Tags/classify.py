#!/usr/bin/env python3
import os
import re
import shutil
from pathlib import Path

# 定义分类和对应的标签
CATEGORIES = {
    "01-AI-Agent生态": ["AI", "Claude Code", "AI Agent", "Codex", "Cursor", "Skills", "MCP", "ChatGPT", "DeepSeek", "Agent", "OpenCode", "LLM", "GPT"],
    "02-内容创作媒体": ["字幕", "视频编辑", "视频翻译", "AI短剧", "配音", "音乐", "视频剪辑", "视频", "音频", "字幕生成", "视频制作"],
    "03-效率生产力": ["Obsidian", "搜索", "自动化", "翻译", "剪贴板", "OCR", "飞书", "效率", "生产力", "笔记", "任务管理", "日历"],
    "04-操作系统平台": ["macOS", "浏览器", "Chrome", "跨平台", "Windows", "Android", "iOS", "Linux", "平台", "操作系统"],
    "05-开发技术栈": ["Whisper", "Tauri", "隐私", "Electron", "Rust", "npm", "API", "开发", "编程", "代码", "终端", "Git", "Docker"],
    "06-设计视觉": ["设计", "可视化", "3D", "绘图", "图片", "图像", "UI", "UX", "动画", "图形"]
}

def extract_tags(file_path):
    """从markdown文件中提取tags字段"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 查找tags字段
        tags_match = re.search(r'tags:\s*\[([^\]]+)\]', content)
        if tags_match:
            tags_str = tags_match.group(1)
            # 分割标签并清理空格
            tags = [tag.strip().strip('"').strip("'") for tag in tags_str.split(',')]
            return tags
        
        # 尝试匹配其他格式的tags
        tags_match = re.search(r'tags:\s*"([^"]+)"', content)
        if tags_match:
            tags_str = tags_match.group(1)
            tags = [tag.strip() for tag in tags_str.split(',')]
            return tags
            
        return []
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def classify_file(tags):
    """根据tags判断文件属于哪个分类"""
    # 计算每个分类的匹配分数
    scores = {}
    for category, category_tags in CATEGORIES.items():
        score = 0
        for tag in tags:
            if tag in category_tags:
                score += 1
        if score > 0:
            scores[category] = score
    
    # 返回匹配分数最高的分类
    if scores:
        return max(scores, key=scores.get)
    return None

def main():
    tags_dir = Path("/Users/seveno/Knowledge/Obsidian/MindRe/1-Project/PSPI/genflow/Article Pipeline/Tags")
    
    # 统计信息
    total_files = 0
    classified_files = 0
    unclassified_files = 0
    category_counts = {cat: 0 for cat in CATEGORIES.keys()}
    unclassified_list = []
    
    # 遍历所有md文件
    for file_path in tags_dir.glob("*.md"):
        if file_path.is_file():
            total_files += 1
            
            # 提取tags
            tags = extract_tags(file_path)
            
            # 分类
            category = classify_file(tags)
            
            if category:
                # 移动文件到对应分类文件夹
                dest_dir = tags_dir / category
                dest_path = dest_dir / file_path.name
                
                # 如果文件已存在，添加数字后缀
                if dest_path.exists():
                    counter = 1
                    while dest_path.exists():
                        stem = file_path.stem
                        suffix = file_path.suffix
                        dest_path = dest_dir / f"{stem}_{counter}{suffix}"
                        counter += 1
                
                shutil.move(str(file_path), str(dest_path))
                classified_files += 1
                category_counts[category] += 1
                print(f"✓ {file_path.name} -> {category}")
            else:
                unclassified_files += 1
                unclassified_list.append(file_path.name)
                print(f"✗ {file_path.name} (未匹配分类)")
    
    # 输出统计信息
    print("\n" + "="*50)
    print("分类完成统计")
    print("="*50)
    print(f"总文件数: {total_files}")
    print(f"已分类: {classified_files}")
    print(f"未分类: {unclassified_files}")
    print("\n各分类文件数:")
    for category, count in category_counts.items():
        print(f"  {category}: {count}")
    
    if unclassified_list:
        print(f"\n未分类文件列表 (共{len(unclassified_list)}个):")
        for filename in unclassified_list[:10]:  # 只显示前10个
            print(f"  - {filename}")
        if len(unclassified_list) > 10:
            print(f"  ... 还有{len(unclassified_list) - 10}个文件")

if __name__ == "__main__":
    main()