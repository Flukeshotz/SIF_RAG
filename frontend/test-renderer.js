import { marked } from 'marked';

const renderer = new marked.Renderer();
renderer.table = function(token) {
  console.log("table token keys:", Object.keys(token));
  console.log("table header:", token.header);
  console.log("table rows:", token.rows);
  return `<table>...</table>`;
};
marked.use({ renderer });

const out = marked.parse("| A | B |\n|---|---|\n| 1 | 2 |");
