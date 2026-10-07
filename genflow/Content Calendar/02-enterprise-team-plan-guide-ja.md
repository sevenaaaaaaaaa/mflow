---
slug: 02-enterprise-team-plan-guide

title: "【日本語】 Lovart Team Plan: Seats, Credits & Permission Management Explained"
page_type: "Detail Page"
category: "Industry Solution"
target_keywords:
  - lovart team plan
  - design team management
  - team design tool
date: 2026-07-01
status: Draft
language: ja
---

# Lovart Team Plan: Seats, Credits & Permission Management Explained

[IMAGE 1 PLACEHOLDER — Persona Scenario]

Design doesn't happen in isolation. It happens in Slack threads, Figma comments, and the dreaded "can you make the logo bigger" email chain that's been going since Tuesday. The organizations that get design right aren't the ones with the most talented individual designers — they're the ones that figured out how to coordinate creative work across a team.

Lovart's Team Plan is built for that reality. It's a collaborative design operating system where seats, credits, and permissions work together so your team moves fast without stepping on each other's work. Here's exactly how it works.

---

## The Team Plan Structure

[IMAGE 2 PLACEHOLDER — Conceptual Diagram]

The Team Plan is built around three concepts that map directly to how real design organizations operate:

| Component | What It Controls |
|-----------|-----------------|
| **Seats** | Who's on the team and what they can do |
| **Credits** | How much AI generation capacity the team shares |
| **Permissions** | Who can create, approve, export, and manage |

A seat is a named user slot tied to an email address. A credit is a unit of compute — one credit buys roughly one AI image generation or a segment of video generation, with exact consumption varying by model and resolution. Permissions define the boundaries around every action in the workspace.

These three levers let you configure the plan for anything from a two-person startup to a 50-person creative department.

---

## Seat Types: Admin, Member, Viewer

Lovart Team Plan offers three seat tiers, each with distinct capabilities.

### Admin

Admins own the workspace. They manage billing, add and remove members, configure the Brand Kit, and set organization-wide defaults like output resolution and watermark settings.

Every workspace needs at least one Admin. You can have multiple — common practice is to give Admin to your creative director, your operations lead, and one backup person who won't leave without telling you.

**What Admins can do that others can't:**
- Purchase and allocate credit pools
- Invite and remove team members
- Change member seat types
- View organization-wide usage analytics
- Configure security settings and SSO
- Lock the Brand Kit to prevent unauthorized edits

### Member

Members are your active creators. They get full access to ChatCanvas, touch editing, Brand Kit (with configurable edit rights), all AI models, and export capabilities.

This is the seat for designers, marketers, and anyone who regularly generates visual assets. Members consume credits from the team's shared pool and can create their own projects within the workspace.

**What Members can do:**
- Generate images and videos across all available models
- Use ChatCanvas and touch editing
- Create and manage personal projects
- View their own usage statistics
- Apply the Brand Kit to their designs
- Export assets in all available formats

### Viewer

Viewers are review-only. They can see completed designs, leave comments, and download approved assets — but they can't generate anything or modify the Brand Kit.

This seat exists for stakeholders who need visibility without creation rights: clients reviewing agency work, executives approving campaign assets, compliance teams checking designs against brand guidelines. Viewers don't consume AI generation credits.

---

## Credit Pooling and Allocation

Here's where the Team Plan diverges from individual subscriptions — and why it matters for your budget.

### How Credit Pooling Works

In the Team Plan, credits live in a shared pool that all Members draw from. This is fundamentally different from individual plans where each user gets a fixed monthly allocation.

When a Member generates an image, the credit cost is deducted from the team pool. When a Viewer looks at that image, nothing is deducted. The pool refills monthly based on your plan tier.

**Why pooling matters:**

Suppose you have five Members each generating 200 images per month on average. That's 1,000 total. But one Member is working on a product launch and needs 500 images this month while another is on vacation. With pooled credits, the busy designer isn't throttled and the idle credits don't go to waste. The team's total capacity is 1,000 — how you distribute it is up to you.

### Credit Allocation Controls

Admins can optionally set per-Member credit caps. This is useful when:

- You're onboarding a junior designer and want to prevent accidental overuse
- You're working with an external contractor who needs guardrails
- You have a monthly budget per department and want to enforce it

Caps are soft limits that trigger a notification, not hard cutoffs that block work. The Member and Admin both get an alert when 80% is consumed, with the option to raise or remove the cap.

### Tracking Usage

The Usage Analytics dashboard shows:
- Total pool consumption by day, week, and month
- Per-member breakdown
- Per-model breakdown (which AI models are consuming the most credits)
- Project-level analysis (which campaigns or product lines drive the most generation)

This data helps you forecast future credit needs and identify efficiency opportunities. If one Member is spending 40% of credits on a single model that could be swapped for a cheaper option, you'll see it.

---

## Permission Levels

[IMAGE 3 PLACEHOLDER — Real UI Screenshot]

Permission management in Lovart follows the principle of least privilege — every role starts with only the access it genuinely needs.

### Brand Kit Permissions

| Permission | Admin | Member | Viewer |
|-----------|-------|--------|--------|
| View Brand Kit | Yes | Yes | Yes |
| Edit Brand Kit | Configurable | Configurable | No |
| Lock Brand Kit | Yes | No | No |
| Create new Brand Kit | Configurable | Configurable | No |

The Brand Kit is typically locked for Members once it's established. This prevents the marketing intern from accidentally turning the corporate blue into teal. If your workflow requires collaborative brand development, Admins can toggle edit access per Member.

### Project Permissions

Projects can be private (visible only to the creator), shared (visible to selected Members), or workspace-wide (visible to everyone). This matters when:

- A designer is working on a confidential rebrand that shouldn't leak
- A marketing team is preparing a campaign that's internal until launch
- An agency is serving multiple clients and needs strict separation

### Export Permissions

Admins control who can export assets and at what resolution. Common configurations:

- **Full export rights** for Members who generate final deliverables
- **Preview-only** for Viewers who need to see but not download
- **Watermarked export** for external collaborators on trial projects

---

## Team Plan vs Individual Plan: Pricing Comparison

| | Free | Individual ($19/mo) | Team ($49/mo) | Pro ($99/mo) | Max ($149/mo) |
|---|---|---|---|---|---|
| Seats | 1 | 1 | 5+ | 10+ | 25+ |
| Credit pool | 50/mo | 500/mo | 1,000/mo shared | 2,500/mo shared | 5,000/mo shared |
| Models | 9 image + 6 video | All | All | All | All |
| Brand Kit | 1 | 3 | Unlimited | Unlimited | Unlimited |
| ChatCanvas | ✓ | ✓ | ✓ | ✓ | ✓ |
| Touch Edit | ✓ | ✓ | ✓ | ✓ | ✓ |
| Credit pooling | — | — | ✓ | ✓ | ✓ |
| Usage analytics | — | Basic | Advanced | Advanced | Enterprise |
| Priority support | — | — | — | ✓ | ✓ |
| SSO | — | — | — | — | ✓ |

The Team Plan at $49/mo hits the sweet spot for most small-to-mid creative teams. You get credit pooling, multi-seat management, and advanced analytics without the enterprise price tag.

---

## Frequently Asked Questions

**Can I mix seat types?**

Yes. A typical 8-person setup might be 1 Admin, 5 Members, and 2 Viewers. You're charged per seat based on type, not a flat per-person rate.

**What happens if we hit the credit cap mid-month?**

You get an alert at 80% and 95%. At 100%, Members can still use the platform but generation pauses until the next billing cycle — or the Admin purchases a top-up credit pack. Top-ups are charged at a flat rate and don't change your monthly renewal.

**Can we bring our own AI model keys?**

The Pro and Max plans support BYOK (Bring Your Own Key) for select models. This lets you use your own API credits from OpenAI, Stability AI, or other providers instead of consuming Lovart credits. Contact sales for the current BYOK-supported model list.

**Is there a free trial for the Team Plan?**

Yes. You get 14 days with full Team Plan features and 500 trial credits shared across your team. No credit card required to start.

**How does SSO work?**

SAML-based SSO (Okta, Azure AD, Google Workspace) is available on the Max plan. Setup typically takes under 30 minutes and is guided by a Lovart onboarding engineer.

---

## Is the Team Plan Right for You?

If any of these sound familiar, the answer is probably yes:

- "I spend more time chasing down the right logo file than actually designing."
- "We keep generating images that don't match our brand because nobody knows the hex codes."

[IMAGE 4 PLACEHOLDER — Brand CTA]

- "I have no visibility into who's using what in our design tools."
- "Our freelance designers need access but I can't give them full run of the account."
- "We pay for five individual subscriptions and half the credits go unused every month."

The Team Plan solves the coordination problem that individual subscriptions can't. It gives you one workspace, one credit pool, one source of truth for brand assets — and the permission controls to keep everything safe while letting your team move fast.

[Contact Sales to discuss your team setup →](https://lovart.ai/contact)

For more on how Lovart fits into your organization's design workflow, see our [[Pillar 2 — Brand Identity & Visual Consistency|Brand Identity pillar]].

### Appendix: Image Prompts

**Image 1 — The Persona Scenario**:
A professional yet approachable person sitting at their desk, looking slightly frustrated at their computer screen while trying to create a design — warm natural lighting, candid documentary style

**Image 2 — The Conceptual Diagram**:
A hand-drawn sketch diagram showing the step-by-step workflow for creating designs with AI — clean line art on grid paper, arrows connecting each step, minimalist style

**Image 3 — Real UI Screenshot**:
[REAL SCREENSHOT REQUIRED: Lovart ChatCanvas interface showing the key feature described in this article — clean UI, uncluttered, with a visible result]

**Image 4 — Brand CTA**:
Professional brand visual for Lovart AI Design Agent — showing the final beautiful design result described in Lovart Team Plan: Seats, Credits & Permission Mana — modern, aspirational, cinematic lighting

