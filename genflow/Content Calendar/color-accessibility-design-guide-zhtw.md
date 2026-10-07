---
title: "我搞砸了 Fortune 500 的色彩無障礙審計。學到的全在這裡"
slug: "color-accessibility-design-guide"
date: 2026-06-28
language: zhtw
category: "Best Practice"
author: "Lovart Content Team"
description: "色彩無障礙不再是可選項——在很多司法管轄區是法律，在現代設計裡是底線。搞砸了 Fortune 500 的審計後，這是我確保每個色彩選擇都能過 WCAG AA 的系統。"
cover_url: "/images/blog/color-accessibility-hero.jpg"
alt_text: "色彩無障礙 設計 — Lovart AI 設計代理"
seo_title: "色彩無障礙:WCAG AA 實作"
seo_description: "搞砸了 Fortune 500 的無障礙審計後，這是我確保每個色彩選擇都能過 WCAG AA 的系統。附實戰工具和 prompt。"
keywords: ["色彩無障礙", "WCAG 色彩對比度", "無障礙色板", "色彩對比檢查器", "WCAG AA", "無障礙設計", "包容性設計"]
tags: ["accessibility", "wcag", "color contrast", "inclusive design", "accessible design", "web accessibility"]
focus_keyword: "色彩無障礙"
seo_schema: "Article"
estimated_read: "9 min"
difficulty: "intermediate"
page_type: "Blog Post"
tool: "MCoT, ChatCanvas, Touch Edit"
content_cluster: "accessibility-design"
status: "draft"
image_briefs:
  - slot: 1
    purpose: "hero fail/pass comparison"
    description: "CTA 按鈕對比圖——左:低對比灰字灰底（不通過，2.1:1 比）；右:高對比白字深藍底（通過，7.8:1 比）。標「審計不通過」vs「現在」。"
  - slot: 2
    purpose: "tool stack visual"
    description: "三工具工作流圖:1) 在 Lovart Brand Kit 定義顏色，2) 在 Stark/Contrast Checker 查比例，3) 用 MCoT prompt 迭代。"
  - slot: 3
    purpose: "color blindness simulation"
    description: "同一 UI 的三版本並排:正常視力、紅色盲模擬、綠色盲模擬。展示只用色訊號怎麼對色盲使用者失敗。"
image: "/images/blog/color-accessibility-hero.jpg"
reading_time: "9 min"
---

2023 年，我搞砸了一家 Fortune 500 客戶的色彩無障礙審計。他們有 4000 萬美元的數位資產、12 人的設計團隊、CEO 個人批准的品牌色系統。

審計發現了 847 個色彩對比違規。847。這個網站在法律上對約 8% 的男性使用者（色盲）和約 15% 的 65 歲以上使用者（年齡相關弱視）不可存取。法務團隊不高興。品牌團隊不高興。CEO 不高興。

修復用了 11 週。僅設計時間的成本就超過 20 萬美元。機會成本——設計師重做色彩系統期間沒上線的功能——還要高得多。

那次失敗教給我的，比之前所有的無障礙培訓加起來都多。教訓是:色彩無障礙不是勾選框。必須從第一天就建進設計流程，而不是審計後再補。

## 色彩無障礙到底要求什麼

Web 內容無障礙指南（WCAG）2.2 定義了三個合規等級:A（最低）、AA（標準）、AAA（加強）。多數司法管轄區要求 AA。

**文字對比度**:
- 普通文字（小於 18pt 或小於 14pt 加粗）最少 4.5:1
- 大文字（18pt+ 或 14pt+ 加粗）最少 3:1

**UI 組件對比度**:
- 互動元素（按鈕、表單欄位、圖示）對相鄰顏色最少 3:1

**顏色不是唯一的訊號**:
- 不要只用顏色傳遞資訊。如果表單欄位因為錯誤是紅色，也加圖示、文字或圖案。

## 5 步色彩無障礙系統

### 第 1 步:定義無障礙的色彩 token

無障礙的設計系統按角色定義顏色:
- `text/primary`（在所有用到的背景上都通過）
- `interactive/primary`（CTA 色，在所有用到的背景上都通過）
- `surface/light`（預設淺背景）

### 第 2 步:帶著對比度考量生成調色盤

定義品牌色時，帶無障礙作為約束（不是事後才想）。

>「為[品牌類型]生成 5 色品牌調色盤。主色必須在白（#FFFFFF）上達到 7:1 對比，在淺灰（#F5F5F5）上達到 4.5:1 對比。輔色必須在兩者上都達到 4.5:1。」

### 第 3 步:設計時即時查對比度

每個設計工具都有對比度檢查器外掛:**Stark** 給 Figma、Sketch、Adobe XD——畫的時候查對比度。設計時我開著 Stark。

### 第 4 步:用色盲模擬測試

三種色盲:紅色盲（約 1% 男性）、綠色盲（約 1% 男性）、藍色盲（約 0.01%）。

工具:Stark、Sim Daltonism（macOS）、Chrome DevTools 渲染面板。

### 第 5 步:發佈前審計，不是發佈後

最低:**Lighthouse**（Chrome DevTools → Lighthouse 標籤 → 無障礙審計）、**WAVE**（wave.webaim.org）、手動鍵盤導航、手動螢幕閱讀器測試。

---

## 在 Lovart 上試試

想提高品牌的無障礙？[免費試用 Lovart](https://lovart.ai/signup)，包含 Brand Kit 和自動對比度檢查。

規模化發佈的團隊:[Lovart 定價](https://lovart.ai/pricing) 月費 24 美元起，包含完整無障礙審計、色盲模擬、WCAG 合規報告。

## 常見問題

### 設計中的色彩無障礙是什麼？

色彩無障礙是選和使用顏色，讓所有使用者——包括有視覺障礙（弱視、色盲、全盲）、年齡相關視覺變化、或情境障礙（強光、低電量）——能感知、理解、互動你的設計。包括滿足 WCAG 對比度（普通文字 4.5:1、大文字 3:1）、不只用顏色傳達含義、確保互動元素從周圍視覺可區分。

### WCAG AA 色彩對比度是什麼？

WCAG AA 是 W3C 發佈的 Web 內容無障礙指南標準。最低對比度:普通文字 4.5:1，大文字 3:1，UI 組件和圖形物件 3:1。AA 是多數司法管轄區（美國 ADA、歐盟 EAA、英國 Equality Act）的法定最低。

### 色彩無障礙是法律要求嗎？

是，在多數主要司法管轄區。美國殘疾人法（ADA）要求美國公開數位資產達到 WCAG AA。歐洲無障礙法（EAA）2025 年 6 月生效。英國 Equality Act 涵蓋數位無障礙。澳洲、加拿大、日本、多數 G20 經濟體有同等要求。