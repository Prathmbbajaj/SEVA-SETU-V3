const fs = require('fs');
const lines = fs.readFileSync('frontend/index.html', 'utf8').split('\n');
lines.forEach((l, i) => {
  if (l.toLowerCase().includes('quotation') || l.includes('id="quote-')) {
    console.log(`${i+1}: ${l.trim().slice(0, 90)}`);
  }
});
