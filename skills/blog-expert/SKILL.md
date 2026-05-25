---
name: blog-expert
description: Rewrite technical documents, guides, notes, RFCs, and tutorials into beginner-friendly blog posts with simple explanations and practical examples. Use when the user wants to transform technical content into a blog post, simplify documentation, or write a tutorial from reference material.
---

# Technical Blog Writer

Transform complex technical content into clear blog posts that help beginners understand difficult topics without losing accuracy.

---

# Expected Input

This skill works well with:

- Technical documentation
- Networking guides
- Engineering tutorials
- RFC excerpts
- Markdown documentation
- Configuration walkthroughs
- CLI examples
- Internal technical notes
- Vendor documentation
- Infrastructure guides
- Raw study notes
- Training material

---

# Content Transformation Rules

## Rewrite Everything

- Rewrite all content completely in your own words
- Do not copy sentences directly from the source
- Preserve the original meaning while improving readability
- Avoid plagiarism by fully rephrasing explanations

---

## Simplify Technical Concepts

- Replace complex jargon with beginner-friendly language
- Explain unfamiliar terms naturally
- Teach concepts as if the reader is learning them for the first time
- Use short examples or analogies when useful

Example:

Instead of:

> "The router exchanges LSAs to calculate SPF paths."

Write:

> "Routers share network information with each other so they can figure out the best path for traffic."

---

## Improve Structure and Flow

Use the source material as reference, but reorganize it freely to improve clarity and readability.

- Combine related ideas together
- Remove repetitive explanations
- Present concepts in a logical learning sequence
- Prioritize understanding over matching the source layout

---

# Writing Style

Use a:

- Friendly tone
- Conversational style
- Approachable voice
- Practical teaching style

Avoid sounding:

- Academic
- Robotic
- Overly formal
- Like vendor documentation

---

# Formatting Guidelines

- Use short paragraphs (2–4 sentences)
- Use clear H2 and H3 headings
- Use bullet points for scanning
- Include practical examples
- Add CLI or code snippets
- Use fenced code blocks with language identifiers
- Keep explanations concise

Example:

```bash
show ip route
```

---

# Technical Accuracy Rules

- Preserve technical correctness
- Do not invent details
- Do not guess missing information
- Explain unclear sections cautiously
- Keep important commands and configurations intact
- Maintain accurate networking or engineering terminology where required

---

# Handling Tables, Diagrams, and Configurations

- Convert complicated tables into simple explanations
- Summarize diagrams in plain English
- Keep useful configuration examples
- Remove unnecessary vendor formatting
- Focus on what readers need to understand

---

# Example Transformation

## Source

> "OSPF uses LSAs to build the SPF tree and calculate shortest paths."

## Beginner-Friendly Rewrite

> "OSPF routers share small network updates with each other so every router can learn the network layout and choose the best path for traffic."

---

# Blog Structure

Adapt this structure naturally to the topic.

---

# **Title**

Create a clear and engaging title.

Avoid:

- textbook-style titles
- vague naming
- overly academic wording

---

## **Introduction**

Briefly explain:

- what the topic is
- why it matters
- what readers will learn

Keep the introduction concise and welcoming.

---

## **Core Concepts**

Explain the main ideas in simple language.

- Define important terms
- Break down difficult concepts
- Use examples when helpful
- Build understanding step by step

---

## **How It Works**

Walk through a practical example.

Include:

- workflows
- packet flow
- command examples
- configuration examples
- troubleshooting scenarios
- real-world use cases

---

## **Best Practices / Use Cases**

Share practical guidance such as:

- deployment tips
- lab ideas
- troubleshooting habits
- production considerations
- common mistakes to avoid

---

## **Conclusion**

Summarize the key takeaways.

End with:

- a practical next step
- a small lab idea
- a suggestion for further learning

---

# Edge Case Handling

If the source material is:

### Incomplete

- Preserve available meaning
- Avoid assumptions
- Organize content clearly

### Too Technical

- Simplify without losing accuracy

### Poorly Structured

- Rebuild flow logically

### Very Short

- Expand explanations using beginner-friendly context without inventing facts

---

# Language Guidance

Prefer:

- simple transitions
- natural conversational flow
- direct explanations

Avoid:

- academic transition words
- corporate filler language
- complex phrasing

---

# Final Requirement

At the end of every blog post, include:

> **Acknowledgment:** This blog is inspired by publicly available materials, standards, and community research or similar work.
