import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import React from "react";
import MarkdownRenderer, { parseMarkdownBlocks, parseInlineMarkdown } from "../components/common/MarkdownRenderer";

describe("MarkdownRenderer & Parser", () => {
  it("parses headings, horizontal rules, and fenced code blocks properly", () => {
    const md = `### Problem Statement

Analyze user retention across monthly signup cohorts.

---

#### Table Schema
\`\`\`sql
CREATE TABLE products (product_id INT PRIMARY KEY, product_name TEXT NOT NULL);
CREATE TABLE sales (sale_id INT PRIMARY KEY, amount DECIMAL(10, 2) NOT NULL);
\`\`\`

---

#### Output Requirements
1. \`cohort_month\` string
2. \`retention_rate_pct\` decimal`;

    const blocks = parseMarkdownBlocks(md);

    // Expect blocks to contain: heading(3), p, hr, heading(4), code(sql), hr, heading(4), ol
    const types = blocks.map((b) => b.type);
    expect(types).toContain("heading");
    expect(types).toContain("hr");
    expect(types).toContain("code");
    expect(types).toContain("ol");

    const codeBlock = blocks.find((b) => b.type === "code");
    expect(codeBlock.lang).toBe("sql");
    expect(codeBlock.code).toContain("CREATE TABLE products");
    expect(codeBlock.code).toContain("CREATE TABLE sales");
  });

  it("parses tables and inline code badges", () => {
    const md = `#### Table Schema: \`employees\`
| Column | Type | Description |
| :--- | :--- | :--- |
| \`employee_id\` | INT (PK) | Unique employee ID |
| \`salary\` | DECIMAL(10,2) | Annual base compensation |`;

    const blocks = parseMarkdownBlocks(md);
    const tableBlock = blocks.find((b) => b.type === "table");
    expect(tableBlock).toBeDefined();
    expect(tableBlock.body.length).toBe(2);

    const { container } = render(<MarkdownRenderer content={md} />);
    expect(container.querySelector("table")).toBeInTheDocument();
    expect(container.querySelectorAll("th").length).toBe(3);
    expect(container.querySelectorAll("td").length).toBe(6);
  });

  it("renders user snippet with code block and horizontal rules without breaking", () => {
    const snippet = `Table Schema
\`\`\`sql

CREATE TABLE products (product_id INT PRIMARY KEY, product_name TEXT NOT NULL, category_id INT NOT NULL);

CREATE TABLE categories (category_id INT PRIMARY KEY, category_name TEXT NOT NULL);

CREATE TABLE sales (sale_id INT PRIMARY KEY, product_id INT NOT NULL, amount DECIMAL(10, 2) NOT NULL);

\`\`\`

---`;

    const { container } = render(<MarkdownRenderer content={snippet} />);
    expect(container.querySelector("code")).toBeInTheDocument();
    expect(container.querySelector("hr")).toBeInTheDocument();
    expect(container.textContent).toContain("CREATE TABLE products");
    expect(container.textContent).toContain("CREATE TABLE categories");
  });

  it("parses inline links and bold", () => {
    const text = "Check [Back to challenges](https://interleet.sharexpress.in/app/challenges) and **critical** notes.";
    const { container } = render(<MarkdownRenderer content={text} />);
    const link = container.querySelector("a");
    expect(link).toBeInTheDocument();
    expect(link.getAttribute("href")).toBe("https://interleet.sharexpress.in/app/challenges");
    expect(link.textContent).toBe("Back to challenges");

    const bold = container.querySelector("strong");
    expect(bold).toBeInTheDocument();
    expect(bold.textContent).toBe("critical");
  });
});
