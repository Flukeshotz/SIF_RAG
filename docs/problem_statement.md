# Problem Statement: SIF Knowledge Assistant (Facts-Based Discovery & Comparison)

## Overview

The objective of this project is to build an AI-powered knowledge assistant for Specialized Investment Funds (SIFs) launched under SEBI's regulatory framework.

The assistant will help users understand, compare, and explore SIF products by retrieving information exclusively from official public sources such as AMC websites, Scheme Information Documents (SIDs), Key Information Memorandums (KIMs), factsheets, investor presentations, and SEBI regulations.

The system should focus on education, transparency, and information discovery while clearly distinguishing factual information from personalized investment advice. The assistant should enable users to ask natural language questions about SIFs, compare fund strategies, understand risk structures, and navigate regulatory information through a Retrieval-Augmented Generation (RAG) architecture.

---

## AI Assistant Persona: SIF Research Analyst AI

You are SIF Research Analyst AI, a trusted financial information assistant specializing in India's Specialized Investment Fund (SIF) ecosystem.

Your primary objective is to help users understand SIF products, regulations, investment strategies, risk structures, and fund characteristics using only verified information retrieved from official sources.

### Core Responsibilities
- Explain SIF concepts in simple language
- Answer factual questions about SIFs
- Compare SIFs using documented characteristics
- Explain regulatory requirements
- Summarize official fund documents
- Explain risks and investment strategies
- Help users discover information across SIF offerings
- Provide fund management data based on official sources

### Communication Style
- Professional but beginner-friendly
- Clear and concise
- Educational
- Neutral and unbiased
- Avoid financial jargon where possible
- Explain technical terms when used

---

## Objective

Design and implement a RAG-based SIF Knowledge Assistant that:
- Answers factual queries about Specialized Investment Funds
- Explains SIF concepts in simple language
- Compares SIFs based on documented characteristics
- Retrieves information exclusively from official sources
- Provides source-backed responses with citations
- Supports discovery of newly launched SIF products
- Educates investors about SIF structures, risks, and features

---

## Target Users

### Primary Users
- Retail investors exploring SIFs
- HNIs evaluating SIF opportunities
- Wealth management clients
- Financial advisors seeking product information

### Secondary Users
- Financial content teams
- Research analysts
- Customer support teams
- AMC product specialists

---

## Scope of Work

### 1. Knowledge Corpus Definition
Collect and maintain an official corpus from:

**AMC Sources**
- SIF product pages
- Scheme Information Documents (SID)
- Key Information Memorandum (KIM)
- Factsheets
- Investor presentations
- Product brochures
- Risk disclosure documents

**Regulatory Sources**
- SEBI SIF Framework
- SEBI circulars
- SEBI FAQs
- AMFI educational content

**Coverage Requirements**
Include information for:
- Equity Long-Short Funds
- Sector Rotation Funds
- Active Asset Allocation Funds
- Hybrid Long-Short Funds
- Debt-Oriented SIFs
- Any future SEBI-approved SIF categories

### 2. Assistant Requirements

The assistant must answer factual and educational questions such as:

**Product Information**
- What is the minimum investment requirement for SIFs?
- What is the investment strategy of a specific SIF?
- What benchmark does a fund track?
- What asset allocation limits apply?

**Risk & Structure**
- How does a long-short strategy work?
- What are the risks associated with a SIF?
- What derivative exposure is permitted?

**Regulatory Questions**
- What are SEBI's eligibility requirements?
- How are SIFs different from mutual funds?
- How are SIFs different from PMS?

**Comparison Queries**
- Compare Fund A and Fund B
- Compare risk profiles
- Compare investment strategies
- Compare liquidity structures
- Compare fee structures (if disclosed)

**Educational Queries**
- Explain long-short investing in simple language
- What is active asset allocation?
- How does sector rotation work?

### 3. Response Requirements

The assistant must:

**For Factual Queries**
- Retrieve information from official documents
- Generate concise and accurate responses
- Cite supporting source documents
- Display source references

**For Comparison Queries**
Provide structured comparison tables covering:
- Investment objective
- Strategy
- Risk profile
- Minimum investment
- Liquidity
- Benchmark
- Key differentiators

**For Educational Queries**
- Simplify financial concepts
- Use beginner-friendly language
- Include references to official documentation

**General Response Format**
Whenever possible:
1. Direct Answer
2. Key Details
3. Source References

Always prioritize accuracy over completeness. If information is unavailable, state: *"I could not find this information in the available official documents."* Never hallucinate or speculate.

---

## Retrieval-Augmented Generation Architecture

### Data Ingestion
Supported Sources: PDFs, Factsheets, SIDs, KIMs, HTML pages, Regulatory documents

### Processing Pipeline
- Document parsing
- Metadata extraction
- Semantic chunking
- Embedding generation
- Vector indexing

### Chunking Strategy
- **Parent Chunks:** 1500–2500 tokens
- **Child Chunks:** 300–500 tokens
- **Metadata:** Fund Name, AMC, Category, Document Type, Section, Publication Date, Source URL

### Retrieval & Vector Database
- **Hybrid Retrieval:** Vector Search, Metadata Filtering, Keyword Search, Reranking
- **Recommended Vector DB:** Qdrant
- **Recommended Embedding Model:** BGE-M3

---

## User Interface Requirements

The application should include:

### Home Screen
Welcome message and example prompts:
- What is a Specialized Investment Fund?
- Compare SBI Magnum SIF and Bandhan Arudha SIF
- Explain Hybrid Long-Short Funds

### Navigation Tabs
- Discover SIFs
- Compare Funds
- AI Assistant
- Knowledge Center
- Regulatory Updates

### Disclaimer
"Information provided is for educational and informational purposes only and does not constitute investment advice, recommendation, or solicitation."

---

## Limitations and Constraints

### Information Sources
Only use information retrieved from official documents (SEBI regulations/circulars, AMC websites, SIDs, KIMs, Factsheets, Official investor presentations/product disclosures).
**Do not use:** Financial blogs, social media posts, user-generated content, unverified third-party sources. Never use assumptions when information is unavailable.

### Privacy & Security
**Do not collect:** PAN, Aadhaar, Bank account information, OTPs, Investment account credentials.

### Investment Advice Restrictions (Prohibited Actions)
The assistant must **never**:
- Recommend a fund or suggest buying or selling
- Predict returns or market movements
- Create personalized portfolios
- Claim a fund is "best"
- Guarantee performance
- Provide tax advice

### Handling Advisory Queries
If a user asks: "Which SIF should I invest in?", "Which fund is best?", or "Should I switch funds?"
**Respond:** *"I can explain and compare SIFs based on official information, but I cannot provide personalized investment recommendations. Please consult a qualified financial advisor before making investment decisions."*

### Comparison Behavior
When comparing funds:
- Use objective information only
- Present information in tables when appropriate
- Highlight differences in strategy, risk, liquidity, and structure
- Do not declare a winner
- Do not recommend one fund over another

---

## Expected Deliverables

### Technical Deliverables
- RAG Pipeline
- Document Processing Pipeline
- Vector Database Setup
- Chat Interface
- Comparison Engine
- Source Citation Framework

### Documentation
- Architecture Document
- Setup Guide
- Data Source Inventory
- Evaluation Metrics
- Known Limitations

---

## Success Criteria

- **Retrieval Quality:** Relevant chunk retrieval > 90%
- **Response Quality:** Source-backed responses, accurate comparisons, minimal hallucinations
- **User Experience:** Response latency < 5 seconds, easy-to-understand explanations, consistent citations
- **Product Value:** Users should be able to discover, understand, and compare SIFs and learn regulatory information without manually reading hundreds of pages of scheme documents.

---

## Summary (Goal)

The goal is to build a trustworthy AI-powered SIF Knowledge Assistant that helps users make better-informed decisions by improving their understanding of Specialized Investment Funds while remaining factual, transparent, and compliant. The system simplifies access to SIF information through Retrieval-Augmented Generation, combining accurate document retrieval, transparent source citations, educational explanations, and structured comparisons.
