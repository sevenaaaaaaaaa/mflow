---
title: "Lovart Podcast #8: 2028 Vision Special — What We Are Building and Why"
date: 2027-12-17
week: W3
category: Podcast
tags: [lovart 2028 vision, lovart podcast, AI design future, lovart product roadmap, design tool vision, AI design 2028]
seo_keywords: lovart 2028 vision, lovart podcast episode 8, AI design future, lovart product roadmap, design tools 2028, AI design predictions, Lovart vision special
description: "Lovart Podcast Episode #8: CEO Amara Osei and the product leadership team unveil the 2028 vision — component extraction, design tokens, community marketplace, and the future of agentic design. A special extended episode."
author: Lovart Podcast Team
featured_image: /images/podcast-episode-8.jpg
reading_time: 8 min
word_count: 1500
slug: podcast-episode-8-2028-vision
platform: [Blog, Spotify, Apple Podcasts, YouTube]
status: published

---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "Lovart Podcast #8: 2028 Vision Special — What We Are Building and Why",
  "description": "--- title: "Lovart Podcast 8: 2028 Vision Special — What We Are Building and Why" date: 2027-12-17 week: W3 category: Podcast tags: lovart 2028 vision, lov",
  "url": "https://www.lovart.ai/01-podcast-episode-8",
  "datePublished": "2026-05-12",
  "publisher": {
    "@type": "Organization",
    "name": "Lovart",
    "url": "https://www.lovart.ai"
  }
}
</script>

# Lovart Podcast #8: 2028 Vision Special — What We Are Building and Why

**Episode 8 · December 17, 2027 · 68 minutes**

*Final episode of 2027. Available on [Spotify](https://spotify.com), [Apple Podcasts](https://apple.com/podcasts), and [YouTube](https://youtube.com/@lovart).*

---

## Episode Summary

For the final episode of 2027, we break format. No guest interview. No industry roundtable. Instead, CEO Amara Osei and the entire Lovart product leadership team — Daniel Kessler (Head of Product), Mei-Lin Zhao (Head of Community), and Dr. Samir Patel (Head of Research) — sit down for an extended, unfiltered conversation about the year ahead.

What is on the 2028 roadmap? What did we learn in 2027 that changed our plans? What are we building that we have not talked about publicly yet? And what are we most worried about?

This is the 2028 Vision Special. Here is what is coming.

## Key Discussion Points

### The 2028 Roadmap: Four Big Bets

**Amara Osei:** In 2027, we shipped 14 major features. In 2028, we are going deeper on fewer things. Four big bets. Each one could be a company on its own. Together, they are the next version of what Lovart becomes.

### Bet 1: Component Extraction — From Generation to Design Systems

**Daniel Kessler:** The most requested feature from our professional users — and the one Maya Chen called out in Episode 5 as the missing piece — is the ability to extract structured components from generated designs.

Here is the problem: when you generate a design in Lovart today, the output is a flat composition. A beautiful image. But if you want to reuse the button from that design, or the card layout, or the hero section structure, you have to rebuild it. The design exists as pixels, not as a system.

Component Extraction changes that. When you generate a design, Lovart's vision model analyzes the composition and identifies structural components — the button, the card, the navigation bar, the hero layout, the pricing table. You can extract any component, name it, give it variants and states, and save it to your component library. The extracted component is editable, responsive, and reusable across future designs.

Under the hood, this is technically hard. It requires the AI to understand design semantics — "this group of elements functions as a button" — not just visual arrangement. But the team has been prototyping it since August, and the early results are promising. We are targeting a Q1 2028 beta.

This feature bridges the gap between AI generation and design systems. It means a team can generate 100 layout variations, extract the best components from those variations, and build a design system from AI output rather than from scratch. The AI becomes a design system accelerator, not just a design generator.

### Bet 2: Design Token Export — AI to Code, Actually

**Daniel:** The second big bet is design token export. Our API users have been asking for this since day one. They want to generate a color palette and typography scale in Lovart and export it as a structured design token file — JSON, YAML, or CSS custom properties — that drops directly into their Tailwind config, their Style Dictionary pipeline, or their component library.

In 2028, we are building exactly that. Generate a brand identity in Lovart. Export the tokens. Drop them into your codebase. The design and the code speak the same language — literally.

We are targeting the W3C Design Tokens specification, which is approaching community group report status. This means Lovart-exported tokens will be compatible with any tool that supports the spec — Figma, Tokens Studio, Style Dictionary, and an ecosystem of token-aware design and development tools.

Combined with Component Extraction, this gives you AI-generated design that is production-ready — not as a flat image, but as structured, tokenized, component-based assets that integrate directly into development workflows. That is the vision. Q1 2028 is when we start shipping it.

### Bet 3: Community Marketplace — Creators Earn From Their Templates

**Mei-Lin Zhao:** The community built 12,800 templates in 2027. They did it for free — for the love of the tool, for the satisfaction of helping other creators, for the reputation. And that is beautiful. But love does not pay rent.

In 2028, we are launching the Lovart Community Marketplace — a platform where template creators can sell their work. Creators set their own prices. Lovart takes a 15% platform fee (industry standard is 30%, and we are trying to do better). Buyers get high-quality, community-vetted templates that solve real design problems. Creators get paid for the value they create.

We are also introducing free tier options: creators can offer templates for free (building audience and reputation), "pay what you want," or fixed price. Revenue sharing applies only to paid templates.

The marketplace launches in Q1 2028 with an initial cohort of 50 invited creators — including Rafael Costa, Amina Noor, Park Joon-woo, and other top template builders from 2027. It opens to all creators by Q2.

This is not just a feature. It is an economic engine for the Lovart ecosystem. If we get it right, the best designers in the world will build templates for Lovart — not because we pay them, but because the marketplace lets them capture the value they create. And the best templates will attract more users, who will create more demand for templates, which will attract more creators. The flywheel.

### Bet 4: Agentic Campaigns — The AI That Builds Entire Campaigns

**Amara:** The fourth bet is the most ambitious and the most uncertain. We are calling it Agentic Campaigns internally.

Here is the idea: you describe a campaign — "a Q2 product launch for a DTC skincare brand targeting millennial women, launching April 15, primary channels Instagram and email, secondary channel TikTok, brand aesthetic is clean minimal premium" — and the AI designs the entire campaign.

Not one design. The entire campaign. Social posts for all platforms, in all formats, on a content calendar. Email sequence headers. Web assets. Ad creative. All brand-consistent. All platform-optimized. All produced autonomously.

This is not prompt-to-design. It is brief-to-campaign. The AI makes hundreds of design decisions — which template to use for the announcement post, how to adapt it for Instagram vs. TikTok, what email header style fits the campaign tone, how many posts in the teaser sequence, what the countdown graphics look like — within the constraints of your Brand Kit and campaign parameters.

The human's role: define the brief. Review the output at key milestones. Approve or refine. Not design anything. Direct everything.

This is the logical endpoint of the agentic trajectory we have been on all year. Adaptive Color Intelligence led to Multi-Platform Auto-Adapt. Auto-Adapt led to One-Click Campaign Export. One-Click Campaign Export leads to Agentic Campaigns. Each step reduces the number of explicit decisions the human must make.

Will it be ready in 2028? Honest answer: we do not know. The technical challenges are significant — particularly around maintaining quality and brand coherence across dozens of autonomously generated assets. We are targeting a beta in Q2 2028, but this is genuinely research-forward work. It might slip. It might need to be scoped down. It might not work at all.

But if it does work — if we can go from brief to campaign with the same reliability we can currently go from prompt to design — it changes what Lovart is. It stops being a design tool and becomes a creative operations platform. That is the ambition.

### What We Learned in 2027 That Changed the Roadmap

**Amara:** Three lessons from 2027 that directly shaped the 2028 plan:

**Lesson 1: Governance is the unlock for adoption.** We thought the API would be our biggest enterprise adoption driver. It mattered. But Brand Kit Locking mattered more. When we gave brand teams the ability to say "the AI shall not deviate from our brand standards," the Fortune 500 conversation changed from "interesting technology" to "when can we roll this out?" Our 2028 roadmap reflects this: governance features are not an afterthought. They are the foundation.

**Lesson 2: The community is our R&D department.** The template marketplace, the component extraction feature, the design token export — all of these were community requests before they were roadmap items. The community is not just our user base. It is our product strategy think tank. The best 2028 features are the ones the community already asked for.

**Lesson 3: Speed of iteration matters more than perfection of output.** The features that won in 2027 were not the most polished. They were the fastest to ship and iterate. Batch Generation shipped with rough edges and got better every week based on usage data. Brand Kit Locking was a feature flag for a month before it was a product. The lesson: ship the thing. Learn from usage. Ship the next thing. The market moves too fast for perfectionism.

### What We Are Worried About

**Jordan Park:** Let us talk about the fears. What keeps each of you up at night about 2028?

**Amara:** Platform dependency. We are building on top of foundation models we do not control. If a model provider changes their API, raises their prices, or deprecates a model we depend on, we have a problem. We are investing in model redundancy — the ability to run on multiple foundation models so no single provider is a dependency. But it is expensive and complex and never quite done.

**Daniel:** Feature bloat. Every feature we ship adds weight to the product. Weight slows everything down — the interface, the learning curve, the support burden, the engineering velocity. The discipline of saying no to good ideas to protect the simplicity of the core experience is the hardest product discipline there is. I worry about losing it.

**Mei-Lin:** Community scaling. A 97,000-member Discord is a very different thing from a 28,000-member Discord. At some size, the intimacy breaks. The `#help` channel where you knew everyone's username becomes an anonymous firehose. Preserving community culture through hypergrowth — while also monetizing the marketplace in a way that feels fair to creators — is the challenge I think about most.

**Samir:** Research velocity vs. product velocity. Good research takes time. Controlled experiments. Peer review. Statistical rigor. Product moves fast. Ship it. Measure it. Ship it again. The tension between those paces is constant. I worry about shipping features informed by shallow research that later turns out to be wrong — and about research that is so slow it is irrelevant by the time it lands.

### What Success Looks Like in 2028

**Jordan:** Final question. December 2028. What does success look like?

**Amara:** Three things. One: a designer — a real, trained, professional designer — tells us Lovart is part of their daily workflow, not a tool they tried once. Two: a brand we have never heard of builds something extraordinary on our API — and we only find out about it when we see it in the wild. Three: the community marketplace has made at least ten creators enough money that designing Lovart templates is their full-time job.

If all three of those things are true in December 2028, we will have had a very good year.

**Daniel:** From the product side: Component Extraction is out of beta and used by at least 30% of active users. Design token export is integrated into at least two major frontend frameworks. And Agentic Campaigns — even if it is scoped down from the full vision — is in the hands of users and making their lives easier.

**Mei-Lin:** The marketplace has 500+ active creators. The top creator has earned $50,000+. And the community feels like a community — not a user base — even at 5 million members. Culture scales. We just have to figure out how.

**Samir:** We publish a 2028 Design Trend Report that is better than the 2027 report. We have a year of API data, a year of component extraction data, a year of marketplace data. The insights we can generate from that corpus — about how design is actually practiced, not just talked about — will be unlike anything the design industry has had access to before. If we do the research right, we will not just be reporting on design trends. We will be defining them.

## Episode Links

- [Lovart 2028 Public Roadmap](https://lovart.ai/roadmap)
- [Component Extraction Beta — Join the Waitlist](https://lovart.ai/features/component-extraction)
- [Community Marketplace — Creator Applications Open](https://lovart.ai/marketplace/apply)
- [Lovart API — Design Token Export Spec](https://docs.lovart.ai/design-tokens)

## Subscribe

The Lovart Podcast returns in January 2028 with Episode 9. Subscribe now to catch it when it drops. Until then: thank you for listening. Thank you for creating. See you in the new year.

*This transcript has been edited for clarity and length. The full 68-minute episode includes deeper technical discussion of Component Extraction architecture, a preview of the design token export format, and the team's candid conversation about pricing strategy for 2028.*

**[Start Creating Free — No Credit Card Required](https://www.lovart.ai/)**

## Frequently Asked Questions

### Can I use the designs commercially?
Yes. Every design, image, and video you create with Lovart is yours to use commercially — for ads, products, client work, social media, print, or anything else. No attribution required.

### Do I need design experience to use this?
No. Lovart is built for non-designers. You describe what you want in plain language, and the AI design agent handles the rest. The Touch Edit feature lets you refine results by tapping, not by learning complex software.

### How is Lovart different from other AI design tools?
Unlike Midjourney, DALL-E, or Canva — which generate images or use templates — Lovart is an AI Design Agent. It understands your business context through MCoT (Mind Chain of Thought), lets you edit specific parts without regenerating (Touch Edit), keeps your brand consistent automatically (Brand Kit), and exports in professional formats (PSD, SVG, PDF).

### Can I try it for free?
Yes. Lovart's Free plan gives you 50 image generations per month, access to 5 AI models, Touch Edit (10 edits/month), and Brand Kit setup. No credit card required.

---

**[Start Creating — Free, No Credit Card Required](https://www.lovart.ai/)**
