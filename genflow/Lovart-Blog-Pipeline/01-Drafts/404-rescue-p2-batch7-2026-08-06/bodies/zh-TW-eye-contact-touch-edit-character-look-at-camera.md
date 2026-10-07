---
title: "眼神接觸修復：用 Touch Edit 讓 AI 角色看向鏡頭"
slug: eye-contact-touch-edit-character-look-at-camera
date: "2026-08-06"
language: zh-TW
page_type: Blog Post
category: How-To
author: Lovart Content Team
description: "繁中 404 修復：gaze vector、catchlight、Identity Lock、ChatCanvas thread。"
estimated_read: 9 min
difficulty: beginner
tool: ChatCanvas, Brand Kit, Touch Edit, Design Agent
focus_keyword: eye contact touch edit look at camera
keywords:
  - eye contact touch edit
  - ai gaze
  - lovart chatcanvas
  - touch edit
tags:
  - lovart
  - 404-recovery
seo_title: "AI 眼神接觸 Touch Edit — 繁中操作指南"
seo_description: "Touch Edit 修 gaze：Design Agent QA、Brand Kit series。"
seo_schema: FAQ
cover_url: https://blogs.lovart.ai/wp-content/uploads/2026/03/blogcover-038-1024x682.png
alt_text: eye-contact-touch-edit-character-look-at-camera — Lovart blog cover
status: ready
content_cluster: How-To — Eye Contact
releaseDate: "2026-08-05T20:00:00Z"
publishedAt: "2026-08-05T20:00:00Z"
---



# 眼神接觸修復：用 Touch Edit 讓 AI 角色看向鏡頭

這條繁體中文 URL 曾返回 404，但搜尋仍在問「怎麼讓 AI 人像眼神看鏡頭」。整圖重 roll 常換掉整張臉，Identity 漂移比 gaze 更糟。正確做法多半是局部：**Touch Edit** 修 gaze vector、保 catchlight、**ChatCanvas** thread 鎖同一角色，**Design Agent** 驗收 publish size 下的 iris 可讀性。

## 眼神接觸在物料裡指什麼

第一是 gaze vector 朝向 lens，不是看肩膀幽靈點。第二是 publish size 下 iris/pupil 對稱可讀。第三是 catchlight 與場景光源一致。第四是 thumbnail 120px 寬仍像「在看觀眾」，不是瞇眼或斜視 artifacts。

## 什麼時候 Touch Edit，什麼時候重出

主體 identity、髮型、服裝已對，只有眼神偏了 → **Touch Edit** 框 eye region，指令寫「gaze toward camera, keep catchlight upper-left, do not change face shape」。整張構圖、光線、pose 都錯 → 改 brief 重出，不要硬修半臉。Brand mascot 系列必須同一 thread，避免 slide 3 換成陌生人。

## ChatCanvas brief 合同

弱 brief：「讓他看鏡頭」。強 brief：「保留 Identity Lock reference，只修 gaze toward lens，catchlight match key light upper-left，publish 1080×1350，eye region Touch Edit only，禁止改 jawline」。**Design Agent** 需要 acceptance 欄位才能 QA。

## Touch Edit 操作節奏

框選過大 → 下巴與鼻型被改壞。框選過小 → gaze 改不動。三次仍不對，縮框再試，不要擴大 prompt  vagueness。每次 pass 只改一個變量：先 gaze，再 catchlight，再 lid openness。

## Brand Kit 與系列角色

若 mascot 有固定 accent 與 type role，**Brand Kit** 約束 promo stripe 不 drift；眼神修復不改 stripe geometry。carousel 同一 thread 批量修 gaze，角標位置保持一致。

## 常見翻車

整圖 regen 直到「像在看鏡頭」但 identity 換人。catchlight 與 scene light 矛盾。thumbnail 上 eyes 被 platform UI 擋。video hook 眼神對但 static hero 仍斜視。只有 clip 沒有可編輯 static companion。

## 測量什麼

記「gaze fix 分鐘」vs「full regen 分鐘」。記 publish size preview 120px pass/fail。404 修復頁給 operator stable SOP URL，內鏈到 character consistency 相關 how-to 時附 Identity Lock 欄位範例。

## 合規邊界

修 gaze 不是偽造真人代言。若素材暗示真實使用者見證，需有授權與 disclaimer。**ChatCanvas** static 先過 textual QA 再配 motion hook。


## 實操補充 1：gaze 修復與 catchlight

很多團隊第一次用 **Design Agent** 時會把 brief 寫成形容詞堆疊，結果圖「好看」但價目字小、角標擋主體。第二次只改 brief 裡的必填欄位與 safe zone，第三輪往往就能進 Brand Kit 流程。記錄每輪改 brief 花了多久、是否觸發整圖重出，比爭論模型名字更有用。gaze 修復與 catchlight 這類場景裡，**Touch Edit** 改價若能在五分鐘內完成，就證明 static-first 路線成立；若每次改價都要重 roll，說明 Brand Kit 或 brief 模板還沒設好。404 修復頁的價值是讓 SOP 有 stable URL，新人不用在群組裡問「到底用哪套流程」。內鏈到此頁時，請附帶 hex 與 disclaimer 句原文，減少 ChatCanvas thread 裡來回確認。



## 實操補充 2：gaze 修復與 catchlight

很多團隊第一次用 **Design Agent** 時會把 brief 寫成形容詞堆疊，結果圖「好看」但價目字小、角標擋主體。第二次只改 brief 裡的必填欄位與 safe zone，第三輪往往就能進 Brand Kit 流程。記錄每輪改 brief 花了多久、是否觸發整圖重出，比爭論模型名字更有用。gaze 修復與 catchlight 這類場景裡，**Touch Edit** 改價若能在五分鐘內完成，就證明 static-first 路線成立；若每次改價都要重 roll，說明 Brand Kit 或 brief 模板還沒設好。404 修復頁的價值是讓 SOP 有 stable URL，新人不用在群組裡問「到底用哪套流程」。內鏈到此頁時，請附帶 hex 與 disclaimer 句原文，減少 ChatCanvas thread 裡來回確認。



## 實操補充 3：gaze 修復與 catchlight

很多團隊第一次用 **Design Agent** 時會把 brief 寫成形容詞堆疊，結果圖「好看」但價目字小、角標擋主體。第二次只改 brief 裡的必填欄位與 safe zone，第三輪往往就能進 Brand Kit 流程。記錄每輪改 brief 花了多久、是否觸發整圖重出，比爭論模型名字更有用。gaze 修復與 catchlight 這類場景裡，**Touch Edit** 改價若能在五分鐘內完成，就證明 static-first 路線成立；若每次改價都要重 roll，說明 Brand Kit 或 brief 模板還沒設好。404 修復頁的價值是讓 SOP 有 stable URL，新人不用在群組裡問「到底用哪套流程」。內鏈到此頁時，請附帶 hex 與 disclaimer 句原文，減少 ChatCanvas thread 裡來回確認。



## 實操補充 4：gaze 修復與 catchlight

很多團隊第一次用 **Design Agent** 時會把 brief 寫成形容詞堆疊，結果圖「好看」但價目字小、角標擋主體。第二次只改 brief 裡的必填欄位與 safe zone，第三輪往往就能進 Brand Kit 流程。記錄每輪改 brief 花了多久、是否觸發整圖重出，比爭論模型名字更有用。gaze 修復與 catchlight 這類場景裡，**Touch Edit** 改價若能在五分鐘內完成，就證明 static-first 路線成立；若每次改價都要重 roll，說明 Brand Kit 或 brief 模板還沒設好。404 修復頁的價值是讓 SOP 有 stable URL，新人不用在群組裡問「到底用哪套流程」。內鏈到此頁時，請附帶 hex 與 disclaimer 句原文，減少 ChatCanvas thread 裡來回確認。



## 實操補充 5：gaze 修復與 catchlight

很多團隊第一次用 **Design Agent** 時會把 brief 寫成形容詞堆疊，結果圖「好看」但價目字小、角標擋主體。第二次只改 brief 裡的必填欄位與 safe zone，第三輪往往就能進 Brand Kit 流程。記錄每輪改 brief 花了多久、是否觸發整圖重出，比爭論模型名字更有用。gaze 修復與 catchlight 這類場景裡，**Touch Edit** 改價若能在五分鐘內完成，就證明 static-first 路線成立；若每次改價都要重 roll，說明 Brand Kit 或 brief 模板還沒設好。404 修復頁的價值是讓 SOP 有 stable URL，新人不用在群組裡問「到底用哪套流程」。內鏈到此頁時，請附帶 hex 與 disclaimer 句原文，減少 ChatCanvas thread 裡來回確認。



## 實操補充 6：gaze 修復與 catchlight

很多團隊第一次用 **Design Agent** 時會把 brief 寫成形容詞堆疊，結果圖「好看」但價目字小、角標擋主體。第二次只改 brief 裡的必填欄位與 safe zone，第三輪往往就能進 Brand Kit 流程。記錄每輪改 brief 花了多久、是否觸發整圖重出，比爭論模型名字更有用。gaze 修復與 catchlight 這類場景裡，**Touch Edit** 改價若能在五分鐘內完成，就證明 static-first 路線成立；若每次改價都要重 roll，說明 Brand Kit 或 brief 模板還沒設好。404 修復頁的價值是讓 SOP 有 stable URL，新人不用在群組裡問「到底用哪套流程」。內鏈到此頁時，請附帶 hex 與 disclaimer 句原文，減少 ChatCanvas thread 裡來回確認。



## 實操補充 7：gaze 修復與 catchlight

很多團隊第一次用 **Design Agent** 時會把 brief 寫成形容詞堆疊，結果圖「好看」但價目字小、角標擋主體。第二次只改 brief 裡的必填欄位與 safe zone，第三輪往往就能進 Brand Kit 流程。記錄每輪改 brief 花了多久、是否觸發整圖重出，比爭論模型名字更有用。gaze 修復與 catchlight 這類場景裡，**Touch Edit** 改價若能在五分鐘內完成，就證明 static-first 路線成立；若每次改價都要重 roll，說明 Brand Kit 或 brief 模板還沒設好。404 修復頁的價值是讓 SOP 有 stable URL，新人不用在群組裡問「到底用哪套流程」。內鏈到此頁時，請附帶 hex 與 disclaimer 句原文，減少 ChatCanvas thread 裡來回確認。



## 實操補充 8：gaze 修復與 catchlight

很多團隊第一次用 **Design Agent** 時會把 brief 寫成形容詞堆疊，結果圖「好看」但價目字小、角標擋主體。第二次只改 brief 裡的必填欄位與 safe zone，第三輪往往就能進 Brand Kit 流程。記錄每輪改 brief 花了多久、是否觸發整圖重出，比爭論模型名字更有用。gaze 修復與 catchlight 這類場景裡，**Touch Edit** 改價若能在五分鐘內完成，就證明 static-first 路線成立；若每次改價都要重 roll，說明 Brand Kit 或 brief 模板還沒設好。404 修復頁的價值是讓 SOP 有 stable URL，新人不用在群組裡問「到底用哪套流程」。內鏈到此頁時，請附帶 hex 與 disclaimer 句原文，減少 ChatCanvas thread 裡來回確認。



## 實操補充 9：gaze 修復與 catchlight

很多團隊第一次用 **Design Agent** 時會把 brief 寫成形容詞堆疊，結果圖「好看」但價目字小、角標擋主體。第二次只改 brief 裡的必填欄位與 safe zone，第三輪往往就能進 Brand Kit 流程。記錄每輪改 brief 花了多久、是否觸發整圖重出，比爭論模型名字更有用。gaze 修復與 catchlight 這類場景裡，**Touch Edit** 改價若能在五分鐘內完成，就證明 static-first 路線成立；若每次改價都要重 roll，說明 Brand Kit 或 brief 模板還沒設好。404 修復頁的價值是讓 SOP 有 stable URL，新人不用在群組裡問「到底用哪套流程」。內鏈到此頁時，請附帶 hex 與 disclaimer 句原文，減少 ChatCanvas thread 裡來回確認。



## 實操補充 10：gaze 修復與 catchlight

很多團隊第一次用 **Design Agent** 時會把 brief 寫成形容詞堆疊，結果圖「好看」但價目字小、角標擋主體。第二次只改 brief 裡的必填欄位與 safe zone，第三輪往往就能進 Brand Kit 流程。記錄每輪改 brief 花了多久、是否觸發整圖重出，比爭論模型名字更有用。gaze 修復與 catchlight 這類場景裡，**Touch Edit** 改價若能在五分鐘內完成，就證明 static-first 路線成立；若每次改價都要重 roll，說明 Brand Kit 或 brief 模板還沒設好。404 修復頁的價值是讓 SOP 有 stable URL，新人不用在群組裡問「到底用哪套流程」。內鏈到此頁時，請附帶 hex 與 disclaimer 句原文，減少 ChatCanvas thread 裡來回確認。



## 實操補充 11：gaze 修復與 catchlight

很多團隊第一次用 **Design Agent** 時會把 brief 寫成形容詞堆疊，結果圖「好看」但價目字小、角標擋主體。第二次只改 brief 裡的必填欄位與 safe zone，第三輪往往就能進 Brand Kit 流程。記錄每輪改 brief 花了多久、是否觸發整圖重出，比爭論模型名字更有用。gaze 修復與 catchlight 這類場景裡，**Touch Edit** 改價若能在五分鐘內完成，就證明 static-first 路線成立；若每次改價都要重 roll，說明 Brand Kit 或 brief 模板還沒設好。404 修復頁的價值是讓 SOP 有 stable URL，新人不用在群組裡問「到底用哪套流程」。內鏈到此頁時，請附帶 hex 與 disclaimer 句原文，減少 ChatCanvas thread 裡來回確認。


## FAQ

**整圖 regen 還是 Touch Edit？**  
identity 已對只修 gaze → Touch Edit eye region。

**catchlight 怎麼保？**  
brief 寫 key light 方向；框選勿過大。

**Brand Kit 要嗎？**  
mascot 系列建議，防 promo stripe drift。

**404 修復？**  
stable eye contact SOP URL。

**合規？**  
修 gaze 非偽造真人代言；disclaimer 必填。



*Article for www.lovart.ai/blog 404 recovery. Part of 404-rescue P2 batch7 content cluster.*

