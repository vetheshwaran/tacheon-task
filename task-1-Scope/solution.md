# Product Brief — Marketing Performance Tool

## The Problem

The team currently answers the question 
"how is our marketing performing?" by 
manually checking multiple tools and 
pulling numbers together by hand.

This takes too long, gives inconsistent 
answers depending on who does it, and 
breaks down when the usual person is 
unavailable.

I think the core issue is simple:
there is no single place to look.
This tool should fix that.

---

## Who Is This Tool For?

I think the primary user is the 
internal analyst.

My reasoning is straightforward — they 
are the ones doing the manual work today. 
If the tool saves them time, the problem 
is solved.

I considered designing for clients too, 
but decided against it for v1. I am not 
sure yet what clients actually need to 
see, and I did not want to guess wrong 
and build the wrong thing.

---

## What Does v1 Do?

One screen. One question answered.

"How is each channel performing 
this week?"

Shows per channel:
- Spend
- Clicks
- Conversions
- Is it up or down vs last week?

I kept this small deliberately. 
I am not sure what else is needed yet, 
and I would rather build something 
small that works than something big 
that doesn't.

---

## What Data Does It Need?

- Google Ads (for paid search)
- Meta Ads (for social)
- Email platform like Mailchimp

I am assuming the team already has 
access to these. I do not fully 
understand the API setup process yet, 
but I know these platforms have APIs 
and that is the direction I would 
explore first.

If APIs are too complex for v1, 
a manual CSV upload from each platform 
could work as a starting point.

---

## What Is NOT in v1?

- No client access
  (I don't know enough about what 
  clients need yet)

- No AI recommendations
  (feels premature before the basic 
  data display is working)

- No custom date ranges
  (adds complexity I want to avoid 
  in the first version)

I know these things would be useful. 
I just think trying to build everything 
at once is how projects get stuck.

---

## What Would Make Users Trust It?

Honestly this is the part I am least 
sure about, but here is my thinking:

- Show when data was last updated
  so users know if numbers are fresh

- If something fails to load, 
  say so clearly rather than showing 
  wrong numbers silently

- Keep the numbers few and accurate
  rather than showing many numbers 
  some of which might be wrong

---

## What I Would Do Differently 
## With More Time

- Talk to an actual analyst before 
  designing anything. I made a lot 
  of assumptions here that a single 
  conversation would probably correct.

- Understand how the APIs actually 
  work in practice — I have a basic 
  idea but not hands-on experience yet.

- Draw even a rough wireframe to 
  make the layout decisions clearer.

---

## Honest Reflection

This is my first time doing a scoping 
exercise like this. I tried to focus 
on the core problem rather than 
overcomplicating things.

I know there are gaps in my thinking — 
especially around data infrastructure 
and API reliability. But I believe the 
direction is right: one place, one 
question, reliable answer.

I would learn a lot more by building 
a rough version and getting feedback 
than by planning it further on paper.