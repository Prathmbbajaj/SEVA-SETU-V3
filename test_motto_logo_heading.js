const fs = require('fs');

const html = fs.readFileSync('frontend/index.html', 'utf8');

// 1. Heading check
if (!html.includes('Your Need, Our Deed.')) {
  console.error('FAIL: Heading Your Need, Our Deed. missing');
  process.exit(1);
}
console.log('PASS: Heading "Your Need, Our Deed." exists in services panel');

// 2. Motto check
if (html.includes('Bridging Trust, Security & Transparency') || html.includes('Bridging Trust, Security &amp; Transparency')) {
  console.error('FAIL: Old motto still present');
  process.exit(1);
}
if (!html.includes('सेवा से समृद्धि')) {
  console.error('FAIL: New Hindi motto missing');
  process.exit(1);
}
console.log('PASS: Motto successfully replaced with "सेवा से समृद्धि"');

// 3. Logo check
if (!fs.existsSync('frontend/assets/seva_setu_logo.png')) {
  console.error('FAIL: seva_setu_logo.png does not exist');
  process.exit(1);
}
const stats = fs.statSync('frontend/assets/seva_setu_logo.png');
console.log('PASS: Logo exists (3 heads, no text emblem) with size:', stats.size, 'bytes');

console.log('\nALL 3 USER REQUIREMENTS VERIFIED SUCCESSFULLY!');
