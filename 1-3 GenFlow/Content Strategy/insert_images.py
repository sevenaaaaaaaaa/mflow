#!/usr/bin/env python3
"""
批量插入已生产图片到博客文章中
用法: python3 insert_images.py
前提: 设计师已将图片保存到 已生产图片/ 目录，命名格式 {filename}__IMAGE_{N}.png
"""

import os, re, shutil

BASE = "/Users/seveno/Library/Mobile Documents/iCloud~md~obsidian/Documents/LifeOS Pro PARA Vault/1-Project/Content Marketing/Content Calendar/已生产内容"
ARTICLES_DIR = os.path.join(BASE, "博客文章")
IMAGES_DIR = os.path.join(BASE, "已生产图片")

def scan_produced_images():
    """Scan images directory and return {article_filename: {image_num: image_path}}"""
    if not os.path.isdir(IMAGES_DIR):
        print(f"❌ 图片目录不存在: {IMAGES_DIR}")
        print("   请创建此目录并将生产的图片放入其中")
        return {}
    
    image_map = {}
    for fn in os.listdir(IMAGES_DIR):
        if not fn.endswith(('.png', '.jpg', '.jpeg', '.webp', '.gif')):
            continue
        
        # Parse filename: {article}__IMAGE_{N}.png
        parts = fn.rsplit('__IMAGE_', 1)
        if len(parts) != 2:
            print(f"  ⚠️  跳过(格式不符): {fn}")
            continue
        
        article_fn = parts[0]
        img_num = parts[1].rsplit('.', 1)[0]
        
        if article_fn not in image_map:
            image_map[article_fn] = {}
        image_map[article_fn][img_num] = fn
    
    return image_map

def insert_images(article_path, images, dry_run=False):
    """Replace IMAGE placeholders with actual image references"""
    with open(article_path, 'r') as f:
        content = f.read()
    
    original = content
    replacements = 0
    
    for img_num, img_fn in images.items():
        placeholder_pattern = f'[IMAGE {img_num} PLACEHOLDER'
        if placeholder_pattern in content:
            # Replace the full placeholder line
            lines = content.split('\n')
            new_lines = []
            for line in lines:
                if placeholder_pattern in line:
                    # Extract alt text from placeholder
                    alt = line.replace('[', '').replace(']', '').strip()
                    new_lines.append(f'![{alt}]({img_fn})')
                    replacements += 1
                else:
                    new_lines.append(line)
            content = '\n'.join(new_lines)
    
    if replacements > 0 and not dry_run:
        with open(article_path, 'w') as f:
            f.write(content)
    
    return replacements

def main():
    import sys
    dry_run = '--dry-run' in sys.argv or '-n' in sys.argv
    
    print("🔍 扫描已生产图片...")
    image_map = scan_produced_images()
    
    if not image_map:
        print("\n📂 请将图片放入: " + IMAGES_DIR)
        print("   命名格式: {文章文件名}__IMAGE_{N}.png")
        print("   例如: how-to-create-logos-with-ai.md__IMAGE_1.png")
        print("\n💡 提示: 可先运行 --dry-run 预览匹配结果")
        return
    
    print(f"   找到 {sum(len(v) for v in image_map.values())} 张图片")
    print(f"   覆盖 {len(image_map)} 篇文章\n")
    
    total_inserted = 0
    matched = 0
    unmatched = []
    
    for article_fn, images in image_map.items():
        article_path = os.path.join(ARTICLES_DIR, article_fn)
        
        if not os.path.isfile(article_path):
            unmatched.append(article_fn)
            continue
        
        matched += 1
        inserted = insert_images(article_path, images, dry_run=dry_run)
        total_inserted += inserted
        
        if inserted > 0:
            imgs = ', '.join(f'IMAGE_{n}' for n in images)
            print(f"  ✅ {article_fn[:60]} ← {imgs}")
    
    print(f"\n{'[DRY RUN] ' if dry_run else ''}📊 结果:")
    print(f"   匹配文章: {matched}/{len(image_map)}")
    print(f"   插入图片: {total_inserted} 张")
    
    if unmatched:
        print(f"\n   ⚠️  {len(unmatched)} 篇文章未找到(文件名不匹配):")
        for fn in unmatched[:5]:
            print(f"     - {fn}")
    
    pending_total = 2115 - total_inserted
    if pending_total > 0:
        print(f"\n   ⏳ 还有 {pending_total} 张待生产 (见插图生产/IMAGE_PROMPTS_ALL_2115.csv)")

if __name__ == '__main__':
    main()
