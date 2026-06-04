import { marked } from 'marked';
const out = marked.parse("| Benchmark |\n| NIFTY 500 |");
console.log(out);
