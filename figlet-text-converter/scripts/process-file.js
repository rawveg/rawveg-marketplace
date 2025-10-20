import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

// Get available fonts via npx figlet
function getAvailableFonts() {
  try {
    const output = execSync('npx figlet --list', { encoding: 'utf-8' });
    // Skip the "Available fonts:" header and filter out empty lines
    return output.trim().split('\n').slice(1).map(line => line.trim()).filter(line => line);
  } catch (error) {
    throw new Error(`Failed to fetch available fonts: ${error.message}`);
  }
}

// Generate ASCII art via npx figlet
function generateAsciiArt(text, font) {
  try {
    const output = execSync(`npx figlet -f "${font}" "${text}"`, { encoding: 'utf-8' });
    return output;
  } catch (error) {
    throw new Error(`Failed to generate ASCII art: ${error.message}`);
  }
}

// Parse command line arguments
function parseArguments() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: node process-file.js <file-path>');
    console.error('');
    console.error('This script processes <figlet> tags in files and replaces them with ASCII art.');
    console.error('');
    console.error('Syntax: <figlet font="font-name">Text to convert</figlet>');
    console.error('        <figlet>Text to convert</figlet>  (uses DOS Rebel font by default)');
    process.exit(1);
  }
  return args[0];
}

// Detect comment style from the line
function detectCommentStyle(line) {
  const trimmed = line.trimStart();

  if (trimmed.startsWith('//')) {
    return '//';
  } else if (trimmed.startsWith('#')) {
    return '#';
  } else if (trimmed.startsWith('--')) {
    return '--';
  } else if (trimmed.startsWith('/*')) {
    return '/*';
  }

  return null; // plain text, no comment style
}

// Format ASCII art with comment prefixes
function formatWithComments(asciiArt, commentStyle) {
  // Remove trailing empty lines
  const lines = asciiArt.split('\n').filter((line, index, arr) => {
    // Keep the line if it's not empty, or if it's not the last line
    return line.trim().length > 0 || index < arr.length - 1;
  });

  if (!commentStyle) {
    return asciiArt.trimEnd();
  }

  switch (commentStyle) {
    case '//':
      return lines.map(line => `// ${line}`).join('\n');

    case '#':
      return lines.map(line => `# ${line}`).join('\n');

    case '--':
      return lines.map(line => `-- ${line}`).join('\n');

    case '/*':
      // For block comments, each line gets " * " prefix
      return lines.map(line => ` * ${line}`).join('\n');

    default:
      return asciiArt.trimEnd();
  }
}

// Main function
function main() {
  const filePath = parseArguments();

  // Verify file exists
  if (!fs.existsSync(filePath)) {
    console.error(`❌ Error: File not found: ${filePath}`);
    process.exit(1);
  }

  // Read file content
  let content = fs.readFileSync(filePath, 'utf-8');

  // Get available fonts for validation
  let availableFonts;
  try {
    availableFonts = getAvailableFonts();
  } catch (err) {
    console.error(`❌ Error fetching available fonts: ${err.message}`);
    process.exit(1);
  }

  // Find all figlet tags: <figlet font="...">text</figlet> or <figlet>text</figlet>
  const tagRegex = /<figlet(?:\s+font="([^"]+)")?>(.+?)<\/figlet>/g;
  let match;
  const replacements = [];

  while ((match = tagRegex.exec(content)) !== null) {
    const fullTag = match[0];
    const fontName = match[1] || 'DOS Rebel';
    const textToConvert = match[2];
    const tagIndex = match.index;

    // Validate font
    if (!availableFonts.includes(fontName)) {
      console.error(`❌ Error: Invalid font "${fontName}" in tag: ${fullTag}`);
      console.error(`   Run 'node list-fonts.js' to see available fonts.`);
      process.exit(1);
    }

    // Detect comment style from the line containing the tag
    const lineStart = content.lastIndexOf('\n', tagIndex) + 1;
    const lineEnd = content.indexOf('\n', tagIndex);
    const endPos = lineEnd === -1 ? content.length : lineEnd;
    const line = content.substring(lineStart, endPos);
    const commentStyle = detectCommentStyle(line);

    replacements.push({
      tag: fullTag,
      font: fontName,
      text: textToConvert,
      commentStyle
    });
  }

  // If no tags found, inform user
  if (replacements.length === 0) {
    console.log(`ℹ️  No figlet tags found in: ${filePath}`);
    return;
  }

  // Process each replacement
  for (const replacement of replacements) {
    try {
      const asciiArt = generateAsciiArt(replacement.text, replacement.font);
      const formatted = formatWithComments(asciiArt, replacement.commentStyle);
      content = content.replace(replacement.tag, formatted);
    } catch (err) {
      console.error(`❌ Error generating ASCII art for "${replacement.text}": ${err.message}`);
      process.exit(1);
    }
  }

  // Write modified content back to file
  fs.writeFileSync(filePath, content, 'utf-8');

  console.log(`✅ Successfully processed ${replacements.length} figlet tag(s) in: ${filePath}`);
}

main();
