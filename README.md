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
/plugin marketplace add rawveg/rawveg-marketplace

# Browse and install skills interactively
/plugin
```

That's it! You now have access to all the skills in the SkillsForge collection.

---

## 🎨 Available Skills

SkillsForge currently offers **12 powerful skills** across various categories:

### 📝 Content & Publishing

| Skill | Description | Version |
|-------|-------------|---------|
| **[forem-api](./forem-api)** | Create, update, and delete articles on Forem platforms (DEV.to, etc.) | 1.0.0 |
| **[hashnode-api](./hashnode-api)** | Manage your Hashnode blog articles and profile directly from Claude Code | 1.0.0 |
| **[word-count-checker](./word-count-checker)** | Accurately count words in documents without token-based estimation | 1.0.0 |

### 🛠️ Development Tools

| Skill | Description | Version |
|-------|-------------|---------|
| **[figlet-text-converter](./figlet-text-converter)** | Transform text into ASCII art using figlet tags with 400+ fonts | 1.0.1 |
| **[github-issue-checker](./github-issue-checker)** | Create, update, and manage GitHub issues seamlessly | 1.0.0 |

### 🔧 Laravel Ecosystem

| Skill | Description | Version |
|-------|-------------|---------|
| **[laravel](./laravel)** | Core Laravel framework integration and helper tools | 1.0.0 |
| **[laravel-cashier-paddle](./laravel-cashier-paddle)** | Work with Laravel Cashier Paddle for subscription billing | 1.0.0 |
| **[laravel-cashier-stripe](./laravel-cashier-stripe)** | Integrate Laravel Cashier Stripe payment processing | 1.0.0 |
| **[laravel-dusk](./laravel-dusk)** | Browser automation and testing with Laravel Dusk | 1.0.0 |
| **[laravel-mcp](./laravel-mcp)** | Laravel Model Context Protocol integration | 1.0.0 |
| **[laravel-prompts](./laravel-prompts)** | Beautiful command-line prompts for Laravel applications | 1.0.0 |

### 🤖 AI & API Integration

| Skill | Description | Version |
|-------|-------------|---------|
| **[openrouter](./openrouter)** | Connect to OpenRouter API for multi-model AI access | 1.0.0 |

---

## 💻 Installation

### Method 1: Install the Entire Marketplace (Recommended)

Add the SkillsForge marketplace to access all skills:

```bash
/plugin marketplace add rawveg/rawveg-marketplace
```

Once added, you can:
- Browse all available skills with `/plugin`
- Install specific skills: `/plugin install skill-name@rawveg-marketplace`
- Update skills automatically when new versions are released

### Method 2: Install Individual Skills

If you prefer to install specific skills without adding the marketplace:

```bash
# Install directly from GitHub
/plugin install https://github.com/rawveg/rawveg-marketplace/tree/main/skill-name
```

### Method 3: Local Development

For testing or development:

```bash
# Clone the repository
git clone https://github.com/rawveg/rawveg-marketplace.git

# Add as local marketplace
/plugin marketplace add ./rawveg-marketplace

# Or install individual skills locally
/plugin install ./rawveg-marketplace/skill-name
```

---

## ⚙️ Configuration

### Automatic Team Setup

To ensure your entire team has access to SkillsForge, add this to your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "rawveg-marketplace": {
      "source": {
        "source": "github",
        "repo": "rawveg/rawveg-marketplace"
      }
    }
  },
  "enabledPlugins": {
    "figlet-text-converter@rawveg-marketplace": {},
    "word-count-checker@rawveg-marketplace": {},
    "forem-api@rawveg-marketplace": {}
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
# Should show: rawveg-marketplace (GitHub: rawveg/rawveg-marketplace)
```

---

## 📖 Usage Examples

### Example 1: Publishing to DEV.to

```bash
# Install the Forem API skill
/plugin install forem-api@rawveg-marketplace

# Create a new article
Hey Claude, can you publish my article in article.md to DEV.to?
```

### Example 2: ASCII Art Headers

```bash
# Install the Figlet converter
/plugin install figlet-text-converter@rawveg-marketplace

# Convert text to ASCII art
Please convert the title "SkillsForge" to ASCII art using the 'banner' font
```

### Example 3: Word Count Accuracy

```bash
# Install the word count checker
/plugin install word-count-checker@rawveg-marketplace

# Get accurate word counts
What's the word count of my manuscript.md file?
```

### Example 4: Laravel Development

```bash
# Install Laravel skills
/plugin install laravel@rawveg-marketplace
/plugin install laravel-prompts@rawveg-marketplace

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

1. Check existing [GitHub Issues](https://github.com/rawveg/rawveg-marketplace/issues)
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
/plugin marketplace update rawveg-marketplace
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
/plugin marketplace remove rawveg-marketplace
```

> **Note:** Removing the marketplace will also uninstall all skills installed from it.

---

## 📋 Troubleshooting

### Marketplace Won't Load

**Problem:** Can't add the marketplace or see any skills

**Solutions:**
- Verify you have internet access
- Ensure you're using the correct repository name: `rawveg/rawveg-marketplace`
- Try updating Claude Code to the latest version
- Check GitHub isn't experiencing downtime

### Skill Installation Fails

**Problem:** Skill appears in the list but won't install

**Solutions:**
- Run `/plugin marketplace update rawveg-marketplace` to refresh
- Try installing with the full path: `/plugin install skill-name@rawveg-marketplace`
- Check the skill's individual documentation for specific requirements
- Ensure you have proper file system permissions

### Skill Not Working After Installation

**Problem:** Skill installed but Claude doesn't recognize it

**Solutions:**
- Restart Claude Code
- Verify the skill is enabled: `/plugin list`
- Check for any error messages in the Claude Code logs
- Try reinstalling: `/plugin uninstall skill-name` then `/plugin install skill-name@rawveg-marketplace`

---

## 💬 Support

Need help or have questions?

- **Documentation:** [Claude Code Plugins Guide](https://docs.claude.com/docs/claude-code/plugins)
- **Issues:** [GitHub Issues](https://github.com/rawveg/rawveg-marketplace/issues)
- **Discussions:** [GitHub Discussions](https://github.com/rawveg/rawveg-marketplace/discussions)

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

Have ideas for new skills? [Open an issue](https://github.com/rawveg/rawveg-marketplace/issues) with the "enhancement" label!

---

<div align="center">

**Built with ❤️ by [Tim Green](https://github.com/rawveg)**

[⬆ Back to Top](#-skillsforge-marketplace)

</div>
