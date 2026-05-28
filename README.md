# Tacheon & Smacient — Data & AI Product Engineer Assessment


# Task 1 — Product Scoping

## The Problem

The marketing team currently answers the question
"how is our marketing performing across channels?"
by manually logging into multiple tools, pulling
numbers separately, and stitching them together
by hand.

This creates three problems:
- It takes too long
- The answer looks different every time
  depending on who does it
- If the usual person is busy, the question
  just goes unanswered

## My Approach

I scoped an internal tool that gives the team
one place to answer this question — automatically,
consistently, without changing how they currently
work.

See the full product brief here:
`task-1-scoping/product-brief.md`

## Summary of Decisions

**Primary user: Internal analyst**
I focused on the internal analyst rather than
the client because they are the ones doing the
manual work today. Solving their problem first
is the right starting point.

**v1 does one thing only**
A single dashboard showing week-on-week
performance per channel. No AI recommendations,
no client access, no custom date ranges.
I kept it small deliberately — a focused
solution that works is more valuable than
an ambitious one that doesn't.

**Fits around existing tools**
The tool pulls from APIs the team already uses
— Google Ads, Meta Ads, email platform. No one
needs to change how they work.

## What I Would Revisit With More Time

- Talk to an actual analyst before designing
  anything — I made assumptions a single
  conversation would correct
- Draw a wireframe to make layout decisions
  clearer before writing any code
- Understand data reliability — what happens
  when one channel's API fails?

---

# Task 2 — Data Pipeline

## What This Pipeline Does

Automatically fetches news articles from NewsAPI,
cleans and transforms the raw data, adds derived
analytical fields, and loads everything into
Google BigQuery for querying.

## Why NewsAPI?

I chose NewsAPI over the other options for
three reasons:

1. It is relevant to a marketing technology
   company — news monitoring is a real
   marketing use case

2. The data needs genuine transformation work
   — nested fields, nulls, inconsistent values
   — which makes it a better pipeline demo

3. It has reliable uptime and clear
   documentation
    
