"""
Playwright: intercept navigation requests on liblib.tv.
Also try to get the actual page URLs for video detail pages.
"""
import json, time, sys, re
from urllib.parse import urljoin, urlparse
from playwright.sync_api import sync_playwright

BASE = "https://www.liblib.tv/"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )
        context = browser.new_context(viewport={"width": 1920, "height": 1080})
        page = context.new_page()

        # Track all navigations and significant API calls
        navigations = []
        api_calls = []

        def on_request(request):
            url = request.url
            if any(x in url for x in ['liblib.tv', 'liblib.art', 'liblib.cloud']):
                if '/_next/' not in url and '.js' not in url and '.css' not in url and '.png' not in url and '.webp' not in url:
                    api_calls.append({
                        'url': url,
                        'method': request.method,
                        'resource_type': request.resource_type
                    })

        def on_navigation(request):
            if request.is_navigation_request() and not request.url.startswith('chrome-'):
                navigations.append({
                    'url': request.url,
                    'method': request.method,
                    'headers': dict(request.headers)
                })

        page.on('request', on_request)
        page.on('request', on_navigation)

        page.goto(BASE, timeout=20000, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)

        print(f"Loaded: {page.title()} | {page.url}")

        # Remove login overlay
        page.evaluate("""
        () => {
            document.querySelectorAll('iframe[src*="login"]').forEach(f => {
                const p = f.closest('[class*="modal"]') || f.parentElement;
                if (p) p.remove(); else f.remove();
            });
        }
        """)
        page.wait_for_timeout(1000)

        # Click each major button and watch for navigations/API calls
        click_targets = [
            "开始创作",
            "快速体验", 
            "注册/登录",
            "会员超市",
            "创作者挑战赛",
        ]

        for text in click_targets:
            api_calls_before = len(api_calls)
            navs_before = len(navigations)
            
            try:
                # Try JS click
                page.evaluate(f"""
                () => {{
                    const els = document.querySelectorAll('button, [onclick], [role="button"]');
                    for (const el of els) {{
                        if (el.textContent.includes('{text}') || el.textContent.trim() === '{text}') {{
                            el.click();
                            return true;
                        }}
                    }}
                    return false;
                }}
                """)
                page.wait_for_timeout(2000)
                
                new_api = api_calls[api_calls_before:]
                new_navs = navigations[navs_before:]
                
                print(f"\n[{text}] clicked")
                for n in new_navs:
                    print(f"  NAV: {n['url']}")
                for a in new_api:
                    print(f"  API: {a['method']} {a['url'][:120]}")
                    
                # Go back if URL changed
                if new_navs:
                    page.go_back()
                    page.wait_for_timeout(1000)
                    
            except Exception as e:
                print(f"[{text}] error: {e}")

        # Now try clicking video items in the grid
        print("\n=== Clicking video grid items ===")
        grid_navs_before = len(navigations)
        
        # Find grid item containers
        page.evaluate("""
        () => {
            const items = document.querySelectorAll('[class*="grid"] [class*="cursor-pointer"], [onclick]');
            let count = 0;
            items.forEach(el => {
                if (count < 5 && (el.textContent || '').trim().length > 2) {
                    try { el.click(); count++; } catch(e) {}
                }
            });
            return count;
        }
        """)
        page.wait_for_timeout(3000)
        
        new_navs = navigations[grid_navs_before:]
        new_api = api_calls[len(api_calls) - 5:]
        for n in new_navs:
            print(f"  NAV: {n['url']}")
        for a in new_api:
            print(f"  API: {a['method']} {a['url'][:120]}")
        
        current_url = page.url
        if current_url != BASE:
            print(f"  CURRENT PAGE: {current_url}")
            title = page.title()
            print(f"  TITLE: {title}")

        # Summary
        print(f"\n{'='*60}")
        print(f"TOTAL NAVIGATIONS: {len(navigations)}")
        print(f"TOTAL API CALLS: {len(api_calls)}")
        print("\nAll navigations:")
        for n in navigations:
            print(f"  {n['method']} {n['url']}")
        print("\nAll API calls:")
        seen = set()
        for a in api_calls:
            url = a['url']
            if url not in seen:
                seen.add(url)
                print(f"  {a['method']} {url}")

        # Extract route patterns from page scripts
        print("\n=== Route patterns in page scripts ===")
        routes = page.evaluate("""
        () => {
            const all = new Set();
            document.querySelectorAll('script').forEach(s => {
                const text = s.textContent || '';
                // Match route-like strings
                const matches = [...text.matchAll(/["'](\/[a-z][\w\/-]*)["']/g)];
                matches.forEach(m => {
                    const route = m[1];
                    if (route.length > 1 && route.length < 80 &&
                        !route.includes('_next') && !route.includes('//') &&
                        !route.startsWith('/chunks/') && !route.startsWith('/liblib')) {
                        all.add(route);
                    }
                });
            });
            return Array.from(all).sort();
        }
        """)
        for r in routes:
            print(f"  {r}")

        browser.close()

if __name__ == "__main__":
    main()
