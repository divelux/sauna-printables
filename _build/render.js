// Renders the jobs listed in a JSON file to PDF. One Chromium for the whole batch, closed right away.
// Run only under the shared lock:
//   NODE_PATH=/opt/carmax/node_modules flock /tmp/freebies-chromium.lock node render.js jobs.json report.json
const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const report = [];
  const browser = await chromium.launch();
  try {
    const page = await browser.newPage();
    await page.emulateMedia({ media: 'print' });
    for (const j of jobs) {
      await page.goto('file://' + j.html + (j.query ? '?' + j.query : ''), { waitUntil: 'load' });
      await page.evaluate(() => document.fonts.ready);
      // Layout checks: anything sticking out of its page, anything running into the footer,
      // any box marked .fit whose text does not fit.
      const checks = await page.evaluate(() => {
        const out = { pages: 0, problems: [] };
        let i = -1;
        document.querySelectorAll('.page').forEach((p) => {
          if (!p.getClientRects().length) return; // hidden in this paper mode
          i++; out.pages++;
          const pr = p.getBoundingClientRect();
          let worst = 0, who = '';
          p.querySelectorAll('*').forEach((el) => {
            if (el.closest('[data-bleed]')) return;
            if (el.closest('svg') && el.tagName.toLowerCase() !== 'svg') return;
            const r = el.getBoundingClientRect();
            if (!r.width && !r.height) return;
            const d = Math.max(r.right - pr.right, r.bottom - pr.bottom, pr.left - r.left, pr.top - r.top);
            if (d > worst) { worst = d; who = el.tagName + '.' + el.className; }
          });
          if (worst > 1) out.problems.push(`page ${i + 1}: ${who} sticks out ${Math.round(worst)}px`);
          // Siblings that run into each other, and boxes whose content spills out of them.
          const kids = [...p.children].filter((el) => !el.hasAttribute('data-bleed') && getComputedStyle(el).position !== 'absolute');
          for (let k = 0; k < kids.length - 1; k++) {
            const d = kids[k].getBoundingClientRect().bottom - kids[k + 1].getBoundingClientRect().top;
            if (d > 1.5) out.problems.push(`page ${i + 1}: .${kids[k].className} runs into .${kids[k + 1].className} by ${Math.round(d)}px`);
          }
          const spill = (el, depth) => {
            if (/^(h1|h2|svg)$/i.test(el.tagName) || el.hasAttribute('data-bleed')) return;
            const r = el.getBoundingClientRect();
            let worstS = 0, whoS = '';
            el.querySelectorAll('*').forEach((d) => {
              if (d.closest('h1,h2,svg,[data-bleed]')) return;
              const b = d.getBoundingClientRect();
              if (!b.height || !b.width) return;
              const o = Math.max(b.bottom - r.bottom, b.right - r.right);
              if (o > worstS) { worstS = o; whoS = d.tagName + '.' + d.className + ' "' + d.textContent.trim().slice(0, 24) + '"'; }
            });
            if (worstS > 2) out.problems.push(`page ${i + 1}: ${whoS} spills out of .${el.className} by ${Math.round(worstS)}px`);
            else if (depth < 2) [...el.children].forEach((c) => spill(c, depth + 1));
          };
          kids.forEach((k) => spill(k, 0));
          const foot = p.querySelector(':scope > .foot');
          if (foot) {
            const ft = foot.getBoundingClientRect().top;
            p.querySelectorAll(':scope > *:not(.foot)').forEach((el) => {
              if (el.hasAttribute('data-bleed')) return;
              const b = el.getBoundingClientRect().bottom;
              if (b - ft > 1) out.problems.push(`page ${i + 1}: .${el.className} overlaps footer by ${Math.round(b - ft)}px`);
            });
            if (pr.bottom - foot.getBoundingClientRect().bottom < 14) out.problems.push(`page ${i + 1}: footer too close to the edge`);
          }
        });
        document.querySelectorAll('.fit,h1,h2').forEach((el) => {
          const head = /^H[12]$/.test(el.tagName);
          if ((!head && el.scrollHeight > el.clientHeight + 1) || el.scrollWidth > el.clientWidth + 1) {
            out.problems.push(`fit: .${el.className} "${el.textContent.trim().slice(0, 40)}" ${el.scrollWidth}x${el.scrollHeight} in ${el.clientWidth}x${el.clientHeight}`);
          }
        });
        return out;
      });
      await page.pdf({ path: j.pdf + '.raw', width: j.width, height: j.height, printBackground: true,
        margin: { top: '0', right: '0', bottom: '0', left: '0' } });
      report.push({ pdf: j.pdf, pages: checks.pages, problems: checks.problems });
    }
  } finally {
    await browser.close();
  }
  fs.writeFileSync(process.argv[3], JSON.stringify(report, null, 1));
})().catch((e) => { console.error(e); process.exit(1); });
