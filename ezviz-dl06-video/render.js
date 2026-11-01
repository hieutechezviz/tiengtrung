// Render video.html -> EZVIZ_DL06.mp4
// Cách dùng:  node render.js            (render toàn bộ)
//             node render.js --preview  (xuất vài ảnh PNG xem trước)
// Ảnh tuỳ chọn trong thư mục anh/: slot1.jpg, slot2.jpg, slot3.jpg (ảnh lắp đặt), logo.png (logo EZVIZ gốc)
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { spawn, execFileSync } = require('child_process');

const DIR = __dirname;
const OUT = path.join(DIR, 'EZVIZ_DL06.mp4');
const preview = process.argv.includes('--preview');

function assets() {
  const res = {};
  const dir = path.join(DIR, 'anh');
  if (!fs.existsSync(dir)) return res;
  for (const f of fs.readdirSync(dir)) {
    const m = f.match(/^(slot[123]|logo|dl06_front|dl06_back)\.(jpe?g|png|webp)$/i);
    if (!m) continue;
    const mime = m[2].toLowerCase() === 'png' ? 'image/png' : m[2].toLowerCase() === 'webp' ? 'image/webp' : 'image/jpeg';
    res[m[1].toLowerCase().replace('dl06_', '')] = `data:${mime};base64,` + fs.readFileSync(path.join(dir, f)).toString('base64');
  }
  return res;
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 540, height: 960 } });
  await page.addInitScript(() => Object.defineProperty(navigator, 'webdriver', { get: () => true }));
  await page.goto('file://' + path.join(DIR, 'video.html'));
  await page.evaluate(async () => {
    for (const w of [400, 500, 600, 700, 800, 900]) await document.fonts.load(`${w} 40px Inter`, 'Khoá ổ ặ');
  });
  const a = assets();
  console.log('Ảnh nạp vào:', Object.keys(a).join(', ') || '(không có — dùng khung trống)');
  await page.evaluate(x => window.loadAssets(x), a);
  const { FPS, DURATION } = await page.evaluate(() => window.VIDEO_META);

  if (preview) {
    fs.mkdirSync(path.join(DIR, 'preview'), { recursive: true });
    const times = process.argv.slice(3).map(Number).filter(n => !isNaN(n));
    for (const t of (times.length ? times : [2, 3.6, 6, 8.5, 10, 14.5, 17, 23, 29, 33, 38])) {
      const d = await page.evaluate(t => window.grab(t, .9), t);
      fs.writeFileSync(path.join(DIR, 'preview', `t${String(t).padStart(5, '0')}.jpg`), Buffer.from(d.split(',')[1], 'base64'));
    }
    await browser.close(); return;
  }

  const total = Math.round(FPS * DURATION);
  const tmp = path.join(DIR, '_video_noaudio.mp4');
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', String(FPS), tmp], { stdio: ['pipe', 'ignore', 'inherit'] });
  for (let f = 0; f < total; f++) {
    const d = await page.evaluate(t => window.grab(t), f / FPS);
    const buf = Buffer.from(d.split(',')[1], 'base64');
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 90 === 0) process.stdout.write(`\rKhung ${f}/${total}`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  await browser.close();
  console.log('\nGhép nhạc...');
  const music = path.join(DIR, 'nhac_nen.wav');
  if (fs.existsSync(music)) {
    execFileSync('ffmpeg', ['-y', '-i', tmp, '-i', music, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', OUT], { stdio: 'ignore' });
    fs.unlinkSync(tmp);
  } else fs.renameSync(tmp, OUT);
  console.log('Xong:', OUT);
})();
