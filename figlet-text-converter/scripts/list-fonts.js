import figlet from 'figlet';

// Ensure dependencies are installed
async function ensureDependencies() {
  try {
    await import('figlet');
  } catch (error) {
    console.error('Dependencies not installed. Please run: npm install');
    process.exit(1);
  }
}

// Main function
async function main() {
  await ensureDependencies();

  try {
    const fonts = await figlet.fonts();

    console.log(`\n📋 Available Figlet Fonts (${fonts.length} total):\n`);
    console.log('='.repeat(60));

    // Show first 10 fonts with examples
    const previewCount = Math.min(10, fonts.length);

    for (let i = 0; i < previewCount; i++) {
      const font = fonts[i];
      console.log(`\n🔤 ${font}`);
      console.log('-'.repeat(40));

      try {
        const preview = figlet.textSync('Sample', { font });
        console.log(preview);
      } catch (error) {
        console.log('(Preview not available)');
      }
    }

    console.log('\n' + '='.repeat(60));
    console.log(`\n📝 All Available Fonts (${fonts.length} total):\n`);

    fonts.forEach((font, index) => {
      console.log(`  ${(index + 1).toString().padStart(3)}. ${font}`);
    });

    console.log('\n💡 Tip: Use font="font-name" in figlet tags');
    console.log('   Default font: "DOS Rebel"\n');
  } catch (err) {
    console.error('Error retrieving fonts:', err.message);
    process.exit(1);
  }
}

main();
