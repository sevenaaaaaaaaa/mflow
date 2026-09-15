---
title: "New Features Demo Webinar: What Is New in Lovart 3.5 — Full Script and Talking Points"
page_type: Webinar
category: Product
keywords: lovart webinar demo, lovart new features, lovart 3.5 update, lovart product demo
date: 2027-08-02
status: Draft
---

<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebPage",
  "name": "New Features Demo Webinar: What Is New in Lovart 3.5 — Full Script and Talking Points",
  "description": "--- title: "New Features Demo Webinar: What Is New in Lovart 3.5 — Full Script and Talking Points" page_type: Webinar category: Product keywords: lovart we",
  "url": "https://www.lovart.ai/01-webinar-new-features-demo",
  "datePublished": "2026-05-12",
  "publisher": {
    "@type": "Organization",
    "name": "Lovart",
    "url": "https://www.lovart.ai"
  }
}
</script>

# New Features Demo Webinar: What Is New in Lovart 3.5 — Full Script and Talking Points

## Webinar Metadata

- **Title**: Lovart 3.5: The Collaboration and Scale Update
- **Date**: August 26, 2027
- **Duration**: 45 minutes presentation + 15 minutes Q&A
- **Presenters**: Alex Kim (VP of Product), Sarah Okonkwo (Product Designer)
- **Target Audience**: Existing Lovart users on Pro, Agency, and Enterprise plans; prospective users evaluating team design solutions
- **Registration Link**: lovart.ai/webinar/august-2027

## Webinar Description

Lovart 3.5 is the biggest update to team collaboration and production scale in our history. Join VP of Product Alex Kim and Product Designer Sarah Okonkwo for a live walkthrough of every new feature, including real-time co-editing for teams, the redesigned Brand Kit inheritance system, Custom Skills version 2.0, and our new enterprise security controls. This session is designed for current Lovart users who want to maximize their workflow and for teams evaluating Lovart as their primary design platform.

## Full Script

### 0:00 — 3:00 | Welcome and Agenda

**Alex**: Welcome to the Lovart 3.5 launch webinar. I am Alex Kim, VP of Product at Lovart, and I am joined by Sarah Okonkwo from our product design team. Over the next forty-five minutes, we will walk you through everything new in Lovart 3.5. If you are watching live, drop your questions in the Q&A panel. We will answer as many as we can in the final fifteen minutes. If you are watching the recording, the Q&A will be published as a follow-up post on our blog.

**Sarah**: Here is our agenda. First, Alex will walk through the collaboration features: real-time co-editing, the new workspace permissions model, and approval workflows. Then I will cover the Brand Kit updates: inheritance, multi-kit management, and the new color system. After that, we will dive into Custom Skills 2.0 and the new API endpoints. Finally, Alex will wrap up with enterprise security features and our updated pricing. Let us jump in.

### 3:00 — 12:00 | Real-Time Co-Editing

**Alex**: Lovart 3.5 introduces real-time co-editing for teams. Let me show you what that looks like.

[Screen share: Lovart workspace with three collaborators active]

You can see three avatars in the top-right corner. Maya is editing the hero text. Jordan is adjusting the color palette in the Brand Kit panel. Priya is working on a different artboard in the same project. Each person's cursor appears in their assigned color, and changes propagate instantly.

[Demo: Sarah joins the project from a second browser window]

Sarah just joined the project. You can see her avatar appear, and her cursor is now visible on my screen. Sarah, can you edit the headline?

**Sarah**: Sure. I am changing "Summer Collection" to "Autumn Preview." Alex, do you see the update?

**Alex**: I see it live. Now watch what happens when two people try to edit the same element. Sarah and I will both click on the subheading.

[Demo: Both click. Element highlights with lock indicator on Sarah's screen]

Sarah grabbed the lock first. On my screen, the element highlights in yellow with a small lock icon. I can see that Sarah is editing, and I will be able to edit as soon as she moves to a different element. No overwrites, no conflicts, no lost work.

[Transition to slide showing collaboration benchmarks]

Real-time co-editing supports up to twenty-five simultaneous collaborators per project. In our beta test with forty agencies, we measured a thirty-eight percent reduction in time from concept to final delivery, driven primarily by the elimination of asynchronous review cycles.

### 12:00 — 20:00 | Workspace Permissions and Approval Workflows

**Alex**: Alongside co-editing, we are launching a redesigned permissions system. Let me walk you through the new roles.

[Demo: Workspace settings panel]

Every workspace member now has one of five roles. Viewer can see projects but cannot edit. Contributor can edit assigned projects but cannot create new ones or access Brand Kit settings. Designer has full creative access but cannot manage team members or billing. Brand Manager can create and edit Brand Kits and approve brand-related changes. Workspace Admin has full control.

[Demo: Approval workflow configuration]

Approval workflows are new in 3.5. A designer finishes a project and clicks "Submit for Review." The system routes it to the designated reviewers, who can be specific people or anyone with a particular role. Reviewers see a clean viewing mode with pinned comment capability. They can approve, request changes, or reject with notes.

[Talking point card]

For agencies, you can configure multi-stage approvals. A creative director approves concept direction, a brand manager approves compliance, and a client approver gives final sign-off. Each stage can be sequential or parallel. The approval dashboard shows every project's status across your entire workspace.

### 20:00 — 28:00 | Brand Kit Inheritance and Multi-Kit Management

**Sarah**: Now let me show you the biggest update to Brand Kits since we launched them.

[Screen share: Brand Kit dashboard showing parent-child hierarchy tree]

Brand Kits now support inheritance. You define a master brand kit with your foundational rules: color palette, typography, logo system, image styles. Then you create child kits for sub-brands, regional markets, or product lines.

[Demo: Creating a child kit]

I am creating a child kit called "European Market." It inherits everything from the master: colors, fonts, logos. But I can override specific settings. Let me change the color palette to meet European accessibility guidelines. I will also add a translated tagline to the logo.

[Demo: Master kit change propagation]

Now watch. Alex, can you change the primary font in the master kit?

**Alex**: Done. Changed from Inter to Satoshi.

**Sarah**: I see the change reflected in my European child kit. The font updated, but my overridden color palette and logo tagline remained intact. You control which properties cascade down and which stay locked.

[Demo: Multi-kit switching]

For agencies managing multiple clients, you can switch between Brand Kits with one click. The entire interface context updates: available templates, team members with access, recent projects, all scoped to the selected client.

### 28:00 — 36:00 | Custom Skills 2.0

**Sarah**: Custom Skills are getting a major upgrade in 3.5.

[Screen share: New Skill Builder interface]

The Skill Builder has been redesigned with a visual action sequencer. Instead of writing skill definitions in a text editor, you drag action blocks onto a canvas and connect them with arrows. This makes skills easier to build, easier to debug, and easier to share with your team.

[Demo: Building a skill]

Let me build a skill live. I am creating an "Amazon Listing Generator" skill. I drag in a Template Loader block and select our Amazon listing template. I add an Image Source block pointing to a product photo folder. I add a Text Generator block with a prompt to write five bullet points based on a product description. I connect them in sequence.

[Demo: Testing the skill]

I click "Test" in the right panel. The skill runs on a sample product, and I can see the output at each step. The text generator just produced five bullet points that perfectly match the tone of our template.

[Demo: Publishing and sharing]

When the skill is ready, I can publish it to my team's skill library. Anyone on the team can now type "Create Amazon A+ Content for this product" and the skill runs automatically. Skills can also be published to the Lovart Skill Marketplace for the broader community.

**Alex**: Custom Skills 2.0 also supports conditional logic, loops for batch processing, and external API calls. A skill can pull product data from your PIM system, generate designs, and push finished assets to your DAM, all from a single ChatCanvas command.

### 36:00 — 42:00 | Enterprise Security and API

**Alex**: For our enterprise users, 3.5 introduces several security and governance features.

[Slide: Enterprise feature overview]

Single Sign-On is now available with SAML and OIDC provider support. Audit logging captures every significant action in your workspace for SOC 2 and ISO 27001 compliance. Data residency options let you choose which cloud region stores your brand assets. Custom retention policies define how long version history is preserved.

[Demo: API dashboard]

The Lovart API, previously in limited beta, is now generally available. You can programmatically manage workspaces, provision users, update Brand Kits, trigger batch generations, and query activity logs. Full documentation is at docs.lovart.ai/api with interactive examples.

[Code snippet shown on screen: API call to trigger batch generation]

### 42:00 — 45:00 | Pricing Updates and Roadmap

**Alex**: A quick note on pricing. Lovart 3.5 does not change our existing plan prices. All new collaboration features are included in Pro, Agency, and Enterprise plans. The Custom Skills limit increases from five to twenty on the Pro plan. Agency and Enterprise retain unlimited Custom Skills.

[Slide: Upcoming roadmap preview]

Looking ahead, here is what is coming in the next quarter. Visual similarity detection to flag potential IP conflicts in AI-generated outputs. Enhanced video template support for TikTok and Reels. A Brand Kit analytics dashboard showing which brand elements are used most frequently across your projects. And we are exploring a Lovart-reviewed freelance marketplace that connects brands with designers who specialize in Lovart-powered workflows.

**Sarah**: That brings us to Q&A. We have collected your questions from the panel and will work through as many as we can in the remaining time. For questions we cannot get to live, we will publish answers on our blog within the week.

## Speaker Bio Cards

**Alex Kim**, VP of Product at Lovart. Previously led product at two design-tool startups acquired by Adobe and Canva. Based in San Francisco.

**Sarah Okonkwo**, Product Designer at Lovart. Seven years of experience in design tools and creative platforms. Based in London.

## Follow-Up Assets

- Blog post: "Lovart 3.5: Complete Feature Guide"
- Video: Individual feature deep-dives (Real-Time Co-Editing, Brand Kit Inheritance, Custom Skills 2.0)
- Documentation: Updated docs.lovart.ai for all 3.5 features
- Email: Feature announcement to all plan subscribers
- Social: 60-second highlight reel for Instagram, TikTok, LinkedIn

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
