# Figlet Text Converter - Usage Guide

## Overview

The Figlet Text Converter skill converts marked text in files to ASCII art. It uses a universal `<figlet>` tag syntax that works across all file types and intelligently preserves comment formatting.

## Getting Started

### Installation

The skill automatically manages Node.js dependencies on first use. When invoked:

1. Verifies Node.js v14+ is installed
2. Installs the figlet package via npm if needed
3. Processes your file

### Basic Usage

Insert `<figlet>` tags in any file to mark text for conversion:

```
<figlet>Text to Convert</figlet>
```

Then ask Claude to process the file:

```
"Convert all figlet tags in this markdown file to ASCII art"
```

## Tag Syntax

### Simple Tag (Uses Default Font)

```
<figlet>Welcome</figlet>
```

Uses 'standard' font (default).

### Tag with Custom Font

```
<figlet font="3-D">Welcome</figlet>
```

Uses the specified font. Font names are case-sensitive and must exactly match figlet's font list.

## Usage Examples

### Markdown Document

**Input:**
```markdown
# My Documentation

<figlet font="Standard">Getting Started</figlet>

Follow these steps...

<figlet>Important Note</figlet>

This is critical...
```

**Output:**
```markdown
# My Documentation

 ____     _   _     _               _____   _             _   _           _
/ ___| ___| |_| |_(_)_ __   __ _  / ____| | |_  __ _ _ _| |_| |___  __| |
| |  _/ -_|  _|  _| | '_ \ / _` | / __| _ | __| / _` | | | |  _| / _ \/ _` |
| |_| \__ \  _|  _| | | | | (_| |/ /____| | |_| (_| | | | | | |_|  __/ (_| |
 \____|___/\__|\__|_|_| |_|\__, |\_______|  \__|\_\__,_\_/_|_|\__|\___|\_\__,
                             |___/
Follow these steps...

 ___                       _
|_ _|_ __ ___  _ __   ___| |_  __ _  _ _  | |_
 | | '_ ` _ \| '_ \ / _ \|  _| / _` || | | |  _|
 | | | | | | | |_) |  __/ | |_| (_| || | | | | |
|___|_| |_| |_| .__/ \___|_|\__|\_\__|\__,_|_| |
              |_|

This is critical...
```

### Python Script

**Input:**
```python
# <figlet>Configuration</figlet>

DEBUG = True
LOG_LEVEL = "INFO"
```

**Output:**
```python
# ____              ___                                            _
# / ___|__ _   _   / __| ___   _ _   ___   ___  _ _  __ _  __  __| | __
# | |__/ _ \ | | | / /__ / _ \ | | | / _ \ / _ \| | | / _` | \ \/ /| |/ /
# |  __| | | || | |  ___| | | || |_|| (_) ||  __/ (_| |(  _ |  >  < |  __\
# |_|  |_| |_| \_\  \___|_| |_| \__,_|\___/ \___|\__,_| \_/ |_/_/\_\ |_|

DEBUG = True
LOG_LEVEL = "INFO"
```

### Shell Script

**Input:**
```bash
#!/bin/bash

echo '<figlet font="Block">Starting Deployment</figlet>'

# Deploy code...
```

**Output:**
```bash
#!/bin/bash

echo '  ___   _         _   _          _            ___   _             _
 / __|_| |_ __ _ | |_| | ___  _ | | __ _   / ___| |___  _ __  | |
 \__ \_   _/ _` ||  __| |/ _ \| | |/ _` | / /  | | _ \| '_ \ | |_
 |___/ |_| \__,_| \__|_| \___/|_|_|\__, | \_\__| | |_) | |_) ||___|
                                    |___/          |_.__/ | .__/|___|
                                                         |_|'

# Deploy code...
```

### PHP Code

**Input:**
```php
<?php

// <figlet>Database Connection</figlet>

$conn = new PDO($dsn);
```

**Output:**
```php
<?php

// ___   __  _          _                _     ___
// |  \ /  \| |_ __ _ | |__   __ _ ___ ___  / __|
// | | ||  ()| / _` ||  _ \ / _` | -_) -_) \__ \
// |__/ \_/\_|\__,_||_|_|_|\__,_|\___|___|  |___/
//
// ____  ___   _ _  _ _   _    ___   __  _
// / ___| / _ \ | | | | | | |  / _ \ /  \| |_
// |  ___| | | || | | | | | _ | | | ||  ()| / _|
// |  \__| |_| | \_/ | |_|_||_| \__/  \_/|\__\
// \____|___/

$conn = new PDO($dsn);
```

### Configuration File

**Input:**
```ini
[database]
<figlet>Database Settings</figlet>
host=localhost
port=5432
```

**Output:**
```ini
[database]
 ___   __  _          _                ___   __  _   _   _
|  \ /  \| |_ __ _ | |__   __ _ ___ / __| |_ _| | | | | |_ __  __ _ ___
| | ||  ()| / _` ||  _ \ / _` | -_) \__ \|  _| |_| |_|  _| / _` | / _ \
|__/ \_/\_|\__,_||_|_|_|\__,_|\___|  |___/ |_| \___/ |_| \__, | \___/
                                                         |___/
host=localhost
port=5432
```

## Comment Style Detection

The skill automatically detects and preserves comment styles:

| Language | Comment Style | Example |
|----------|---------------|---------|
| C/C++/Java/PHP/JavaScript | `//` | `// <figlet>Section</figlet>` |
| Python/Bash | `#` | `# <figlet>Section</figlet>` |
| SQL | `--` | `-- <figlet>Section</figlet>` |
| C/Java (Block) | `/*` | `/* <figlet>Section</figlet>` |
| Plain text | None | `<figlet>Section</figlet>` |

When a tag is on a line with a comment marker, output is formatted with that comment style:

```
// <figlet>Header</figlet>
```

Becomes:

```
// ___                 _            _
// | | | |___  ___  __| |__ _ ___  __
// | |_| // -_)/ _ \/ _` / _` / -_) / _ \
//  \___/ \___|\___/\__,_\__,_|\___|  __/
//                                  |_|
```

## Finding Fonts

To see all available fonts, ask Claude to list them:

```
"List all available figlet fonts"
```

This will show:
- Previews of popular fonts
- Complete alphabetical listing of 400+ available fonts
- Font names to use in tags

### Popular Fonts

- **standard** - Default, traditional figlet style
- **3-D** - 3D effect with shading
- **Block** - Large, blocky characters
- **Big** - Large and simple
- **Shadow** - Shadowed appearance
- **Slant** - Slanted characters
- **Graffiti** - Artistic style
- **Doom** - Heavy, bold style
- **Isometric1/2** - Isometric projection

## Troubleshooting

### Invalid Font Error

```
❌ Error: Invalid font "MyFont" in tag: <figlet font="MyFont">Text</figlet>
   Run 'node list-fonts.js' to see available fonts.
```

**Solution:** Use a valid font name from the list. Font names are case-sensitive.

### File Not Found

```
❌ Error: File not found: /path/to/file.txt
```

**Solution:** Verify the file path is correct.

### Node.js Not Installed

```
❌ Dependencies not installed. Please run: npm install
```

**Solution:** Install Node.js v14+ from https://nodejs.org/

## Advanced Usage

### Multiple Tags in One File

You can use multiple figlet tags in a single file:

```markdown
<figlet font="Block">Section One</figlet>

Content here...

<figlet font="3-D">Section Two</figlet>

More content...
```

Each tag is processed independently with its own font and style.

### Mixing Comment Styles

Different parts of a file can have different comment styles:

```
// <figlet>JavaScript Section</figlet>

const x = 10;

# <figlet>Python Section</figlet>

x = 10
```

Each is formatted appropriately for its comment context.

### Large Text Conversion

ASCII art can be quite large. For long text strings:

```
<figlet font="Standard">A</figlet>  <!-- Smaller -->
<figlet font="Big">A</figlet>        <!-- Larger -->
```

Use shorter fonts for longer text to keep output manageable.

## Tips & Tricks

1. **Preview Before Converting**: Ask Claude to show you the ASCII art for your text before inserting it
2. **Consistent Styling**: Use the same font throughout a file for visual consistency
3. **Comment the Conversion**: Leave a comment explaining what the ASCII art represents
4. **Test Display**: Verify the output displays correctly in your target environment (editor, terminal, web)
5. **Reserve for Impact**: Use ASCII art sparingly for section headers, not inline text

## Limitations

- Font names must match figlet's font list exactly (case-sensitive)
- Each tag is processed independently; multi-line ASCII art expands proportionally
- Comment detection is line-based (tag must be on same line as comment marker)
- Very long text may produce large ASCII art output
