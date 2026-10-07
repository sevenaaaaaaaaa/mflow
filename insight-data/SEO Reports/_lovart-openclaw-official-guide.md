# Lovart OpenClaw User Guide

Welcome to use the **Lovart** OpenClaw skill. This guide is designed to help creators quickly master.

## **Step 1: Choose Your Environment (OpenClaw & Beyond)**

To use Lovart Skills, you need a compatible agent host. We recommend the following:
- **OpenClaw Desktop (Local):** The most powerful way to run Lovart locally on your machine.
- **Discord / Telegram Integrations:** For teams using the OpenClaw Discord gateway or Telegram bot wrappers.
- **Slack Agent:** Optimized for professional workspace collaboration.

## **Step 2: Set up the Lovart OpenClaw Skill**

You can set up the Lovart OpenClaw Skill in two ways:
1. **GitHub CLI:** Run `npx skills add lovartai/lovart-skills` for an automated setup
2. **ClawHub:** Visit the https://clawhub.ai/lovart-admin/lovart-skill on ClawHub and click "Install" to sync directly to your environment.

## **Step 3: Authentication**

Lovart requires an `access_key` and `secret_key` to link your workspace and computing resources.

### **Obtaining your Key:**
Log in to your **Lovart.ai** account, navigate to "Settings" via your profile icon in the top right, and copy your unique `access_key` and `secret_key`.

### **Activation**
Message your agent "access_key: [your-key], secret_key: [your-key]", or set as global environment variables:
```
export LOVART_ACCESS_KEY="ak_xxx"
export LOVART_SECRET_KEY="sk_xxx"
```

## **Step 4: Creating with Lovart**
- **Recommended Models:** For complex "Skill" logic, use top-tier models like **GPT-5.4**, **Claude 4.6**, or **Gemini 3.1**
- **Reference Files:** Upload images or videos as style/structure references directly in the chat.
