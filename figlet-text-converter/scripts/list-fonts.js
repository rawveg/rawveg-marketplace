import { execSync } from 'child_process';

// Get available fonts via npx figlet
function getAvailableFonts() {
  try {
    const output = execSync('npx figlet --list', { encoding: 'utf-8' });
    // Skip the "Available fonts:" header and filter out empty lines
    return output.trim().split('\n').slice(1).map(line => line.trim()).filter(line => line);
  } catch (error) {
    console.error('Error retrieving fonts:', error.message);
    process.exit(1);
  }
}

// Generate ASCII art via npx figlet
function generateAsciiArt(text, font) {
  try {
    const output = execSync(`npx figlet -f "${font}" "${text}"`, { encoding: 'utf-8' });
    return output;
  } catch (error) {
    return '(Preview not available)';
  }
}

// Main function
function main() {
  const fonts = getAvailableFonts();

  console.log(`\n📋 Available Figlet Fonts (${fonts.length} total):\n`);
  console.log('='.repeat(60));

  // Show first 10 fonts with examples
  const previewCount = Math.min(10, fonts.length);

  for (let i = 0; i < previewCount; i++) {
    const font = fonts[i];
    console.log(`\n🔤 ${font}`);
    console.log('-'.repeat(40));
    const preview = generateAsciiArt('Sample', font);
    console.log(preview);
  }

  console.log('\n' + '='.repeat(60));
  console.log(`\n📝 All Available Fonts (${fonts.length} total):\n`);

  fonts.forEach((font, index) => {
    console.log(`  ${(index + 1).toString().padStart(3)}. ${font}`);
  });

  console.log('\n💡 Tip: Use font="font-name" in figlet tags');
  console.log('   Default font: "DOS Rebel"\n');
}

main();
