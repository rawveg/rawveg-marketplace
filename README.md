# 🎯 SkillsForge Marketplace

> A curated collection of Claude Code skills and plugins to supercharge your development workflow

Welcome to SkillsForge! This marketplace provides a centralized hub for discovering and installing powerful Claude Code extensions that enhance your productivity, streamline your workflows, and integrate with your favorite tools and services.

## 📚 Table of Contents

- [Quick Start](#-quick-start)
- [Available Skills](#-available-skills)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage Examples](#-usage-examples)
- [Contributing](#-contributing)
- [Support](#-support)

---

## 🚀 Quick Start

Get started with SkillsForge in just two commands:

```bash
# Add the SkillsForge marketplace to Claude Code
/plugin marketplace add rawveg/skillsforge-marketplace

# Browse and install skills interactively
/plugin
```

That's it! You now have access to all the skills in the SkillsForge collection.

---

## 🎨 Available Skills

SkillsForge currently offers **23 curated skills** across focused categories. Only skills included in `.claude-plugin/marketplace.json` are listed below.

### 📝 Content & Publishing

| Skill | Purpose |
|-------|---------|
| **[apify-js-sdk](./apify-js-sdk)** | Interacts with the Apify JS SDK. Allows you to work with Actors and other Apify features. |
| **[article-title-optimizer](./article-title-optimizer)** | Optimize article titles for SEO. |
| **[forem-api](./forem-api)** | Create, update, and delete articles and manage your Forem profile. |
| **[hashnode-api](./hashnode-api)** | Manage articles and profile on Hashnode. |
| **[writeas](./writeas)** | Work with Write.as/WriteFreely for simple publishing. |
| **[snapas](./snapas)** | Upload and manage images via Snap.as. |
| **[tumblr](./tumblr)** | Manage articles and profile on Tumblr. |
| **[word-count-checker](./word-count-checker)** | Accurately count words in documents (avoids token-based estimates). |

### 🛠️ Development Tools

| Skill | Purpose |
|-------|---------|
| **[figlet-text-converter](./figlet-text-converter)** | Convert tagged text to ASCII art using figlet. |
| **[github-issue-fetcher](./github-issue-fetcher)** | Fetch GitHub issues for a repository. |
| **[tdd-methodology-expert](./tdd-methodology-expert)** | Guidance and helpers for TDD methodology and best practices. |

### 🔧 Laravel Ecosystem

| Skill | Purpose |
|-------|---------|
| **[laravel](./laravel)** | Core Laravel integration for Claude Code. |
| **[laravel-cashier-paddle](./laravel-cashier-paddle)** | Work with Laravel Cashier (Paddle). |
| **[laravel-cashier-stripe](./laravel-cashier-stripe)** | Work with Laravel Cashier (Stripe). |
| **[laravel-dusk](./laravel-dusk)** | Browser testing with Laravel Dusk. |
| **[laravel-mcp](./laravel-mcp)** | Integrate Laravel with MCP. |
| **[laravel-prompts](./laravel-prompts)** | Use Laravel Prompts for interactive CLIs. |

### 🤖 AI & Model APIs

| Skill | Purpose |
|-------|---------|
| **[openrouter](./openrouter)** | Connect to the OpenRouter API for multi-model access. |
| **[ollama](./ollama)** | Interact with local models via the Ollama API. |
| **[midjourney-replicate-flux](./midjourney-replicate-flux)** | Generate Midjourney-style prompts/images via Replicate (Flux 1.1 Pro). |

### ☁️ Cloud & Infra

| Skill | Purpose |
|-------|---------|
| **[vercel](./vercel)** | Manage deployments and resources via the Vercel API. |
| **[linode-api](./linode-api)** | Manage Linode resources via API. |
| **[linode-cli](./linode-cli)** | Run Linode CLI operations. |
| **[frankenphp](./frankenphp)** | Integrate with the FrankenPHP app server. |
| **[vastai-api](./vastai-api)** | Access GPU instances via the VastAI API. |\

### 🛡️ Security

| Skill | Purpose |
|-------|---------|
| **[haveibeenpwned](./haveibeenpwned)** | Check if your email/password has been compromised in data breaches. |

### 📱 Social Media

| Skill | Purpose |
|-------|---------|
| **[threads-api](./threads-api)** | Interact with the Threads API. |
| **[pinterest-api](./pinterest-api)** | Interact with the Pinterest API. |

---

## 💻 Installation

### Method 1: Install the Entire Marketplace (Recommended)

Add the SkillsForge marketplace to access all skills:

```bash
/plugin marketplace add rawveg/skillsforge-marketplace
```

Once added, you can:
- Browse all available skills with `/plugin`
- Install specific skills: `/plugin install skill-name@skillsforge-marketplace`
- Update skills automatically when new versions are released

### Method 2: Install Individual Skills

If you prefer to install specific skills without adding the marketplace:

```bash
# Install directly from GitHub
/plugin install https://github.com/rawveg/skillsforge-marketplace/tree/main/skill-name
```

### Method 3: Local Development

For testing or development:

```bash
# Clone the repository
git clone https://github.com/rawveg/skillsforge-marketplace.git

# Add as local marketplace
/plugin marketplace add ./skillsforge-marketplace

# Or install individual skills locally
/plugin install ./skillsforge-marketplace/skill-name
```

---

## ⚙️ Configuration

### Automatic Team Setup

To ensure your entire team has access to SkillsForge, add this to your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "skillsforge-marketplace": {
      "source": {
        "source": "github",
        "repo": "rawveg/skillsforge-marketplace"
      }
    }
  },
  "enabledPlugins": {
    "figlet-text-converter@skillsforge-marketplace": {},
    "word-count-checker@skillsforge-marketplace": {},
    "forem-api@skillsforge-marketplace": {}
  }
}
```

When team members trust the repository folder, Claude Code will automatically:
1. Install the SkillsForge marketplace
2. Enable the specified skills
3. Keep everything synchronized

### Verify Installation

Check that the marketplace is properly configured:

```bash
# List all marketplaces
/plugin marketplace list

# Verify SkillsForge appears in the list
# Should show: skillsforge-marketplace (GitHub: rawveg/skillsforge-marketplace)
```

---

## 📖 Usage Examples

### Example 1: Publishing to DEV.to

```bash
# Install the Forem API skill
/plugin install forem-api@skillsforge-marketplace

# Create a new article
Hey Claude, can you publish my article in article.md to DEV.to?
```

### Example 2: ASCII Art Headers

```bash
# Install the Figlet converter
/plugin install figlet-text-converter@skillsforge-marketplace

# Convert text to ASCII art
Please convert the title "SkillsForge" to ASCII art using the 'banner' font
```

### Example 3: Word Count Accuracy

```bash
# Install the word count checker
/plugin install word-count-checker@skillsforge-marketplace

# Get accurate word counts
What's the word count of my manuscript.md file?
```

### Example 4: Laravel Development

```bash
# Install Laravel skills
/plugin install laravel@skillsforge-marketplace
/plugin install laravel-prompts@skillsforge-marketplace

# Use Laravel-specific features
Help me create a new Artisan command with interactive prompts
```

---

## 🤝 Contributing

We welcome contributions to SkillsForge! Here's how you can help:

### Adding New Skills

1. Fork the repository
2. Create a new directory for your skill: `./your-skill-name/`
3. Add your skill files and a `SKILL.md` documentation file
4. Update `.claude-plugin/marketplace.json` with your skill entry
5. Submit a pull request with a clear description

### Skill Submission Checklist

- [ ] Skill follows the [Claude Code plugin structure](https://docs.claude.com/docs/claude-code/plugins)
- [ ] Includes clear documentation in `SKILL.md`
- [ ] Tested locally with `/plugin install ./your-skill-name`
- [ ] Added to marketplace.json with appropriate metadata
- [ ] Follows semantic versioning (e.g., 1.0.0)

### Reporting Issues

Found a bug or have a feature request?

1. Check existing [GitHub Issues](https://github.com/rawveg/skillsforge-marketplace/issues)
2. Create a new issue with:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs. actual behavior
   - Claude Code version and environment details

---

## 🔍 Managing the Marketplace

### Update Skills

Refresh the marketplace to get the latest skill versions:

```bash
/plugin marketplace update skillsforge-marketplace
```

### List Installed Skills

See which skills you have installed:

```bash
/plugin list
```

### Remove Skills

Uninstall skills you no longer need:

```bash
/plugin uninstall skill-name
```

### Remove Marketplace

To completely remove SkillsForge:

```bash
/plugin marketplace remove skillsforge-marketplace
```

> **Note:** Removing the marketplace will also uninstall all skills installed from it.

---

## 📋 Troubleshooting

### Marketplace Won't Load

**Problem:** Can't add the marketplace or see any skills

**Solutions:**
- Verify you have internet access
- Ensure you're using the correct repository name: `rawveg/skillsforge-marketplace`
- Try updating Claude Code to the latest version
- Check GitHub isn't experiencing downtime

### Skill Installation Fails

**Problem:** Skill appears in the list but won't install

**Solutions:**
- Run `/plugin marketplace update skillsforge-marketplace` to refresh
- Try installing with the full path: `/plugin install skill-name@skillsforge-marketplace`
- Check the skill's individual documentation for specific requirements
- Ensure you have proper file system permissions

### Skill Not Working After Installation

**Problem:** Skill installed but Claude doesn't recognize it

**Solutions:**
- Restart Claude Code
- Verify the skill is enabled: `/plugin list`
- Check for any error messages in the Claude Code logs
- Try reinstalling: `/plugin uninstall skill-name` then `/plugin install skill-name@skillsforge-marketplace`

---

## 💬 Support

Need help or have questions?

- **Documentation:** [Claude Code Plugins Guide](https://docs.claude.com/docs/claude-code/plugins)
- **Issues:** [GitHub Issues](https://github.com/rawveg/skillsforge-marketplace/issues)
- **Discussions:** [GitHub Discussions](https://github.com/rawveg/skillsforge-marketplace/discussions)

---

## 📄 License

All skills in this marketplace are released under the MIT License unless otherwise specified in individual skill directories.

```
MIT License

Copyright (c) 2025 Tim Green

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🌟 Star History

If you find SkillsForge useful, please consider giving it a star on GitHub! It helps others discover these tools.

---

## 🎯 Roadmap

Upcoming skills and features:

- [ ] GitHub Actions integration skill
- [ ] Database query and management tools
- [ ] API testing and documentation generators
- [ ] Cloud deployment helpers (AWS, Azure, GCP)
- [ ] Code quality and security scanning tools

Have ideas for new skills? [Open an issue](https://github.com/rawveg/skillsforge-marketplace/issues) with the "enhancement" label!

---

<div align="center">

**Built with ❤️ by [Tim Green](https://github.com/rawveg)**

[⬆ Back to Top](#-skillsforge-marketplace)

</div>
