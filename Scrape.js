const fs = require('fs');
const fetch = require('node-fetch');

(async () => {
  const keywordsFile = 'config/keywords.txt';
  if (!fs.existsSync(keywordsFile)) {
    console.error(' No keywords file found.');
    process.exit(1);
  }

  const keywords = fs.readFileSync(keywordsFile, 'utf-8').split(/\r?\n/).filter(Boolean);
  if (!keywords.length) {
    console.log('⚠No keywords to process.');
    process.exit(0);
  }

  const results = [];

  for (const keyword of keywords) {
    console.log(`Searching: ${keyword}`);
    const res = await fetch(`https://api.duckduckgo.com/?q=${encodeURIComponent(keyword)}&format=json`);
    const data = await res.json();

    const entry = {
      keyword,
      result: data.AbstractText || data.RelatedTopics?.[0]?.Text || 'No summary found'
    };
    results.push(entry);
  }

  const output = results.map(r => `# ${r.keyword}\n${r.result}\n\n`).join('');
  fs.mkdirSync('results', { recursive: true });
  fs.writeFileSync(`results/scrape_output.md`, output);

  console.log(' Scraping complete. Results saved to results/scrape_output.md');
})();
