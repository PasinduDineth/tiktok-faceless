const fs2 = require('fs');
const path2 = require('path');

const imagesDir2 = path2.join(process.cwd(), 'public', 'assets', 'images');
const audioDir2 = path2.join(process.cwd(), 'public', 'assets', 'audio');

if (!fs2.existsSync(imagesDir2)) {
  console.error('No images dir.');
  process.exit(2);
}
if (!fs2.existsSync(audioDir2)) {
  console.error('No audio dir.');
  process.exit(2);
}

const imgs = fs2.readdirSync(imagesDir2).filter((f) => /\.(jpg|jpeg|png|webp)$/i.test(f));
const auds = fs2.readdirSync(audioDir2).filter((f) => /\.(mp3|wav|m4a|aac)$/i.test(f));

if (imgs.length === 0) {
  console.error('No images found.');
  process.exit(2);
}
if (auds.length === 0) {
  console.error('No audio found.');
  process.exit(2);
}

console.log('Assets OK:', imgs.length, 'images, audio:', auds[0]);
process.exit(0);