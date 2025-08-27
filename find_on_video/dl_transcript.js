(() => {
  const rows = [...document.querySelectorAll('ytd-transcript-segment-renderer')];
  if (!rows.length) { alert("No transcript found!"); return; }

  const lines = rows.map(r => {
    const time = r.querySelector('.segment-timestamp')?.textContent.trim() || '';
    const text = r.querySelector('.segment-text')?.textContent.trim() || '';
    return `${time} ${text}`.trim();
  });

  const out = lines.join('\n');
  const blob = new Blob([out], { type: 'text/plain' });
  const url = URL.createObjectURL(blob);

  const a = document.createElement('a');
  a.href = url;
  a.download = "transcript.txt";
  a.click();
  URL.revokeObjectURL(url);
})();

