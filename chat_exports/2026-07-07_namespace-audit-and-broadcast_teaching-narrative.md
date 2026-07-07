# Teaching Narrative: The Filing Cabinet That Ate the Afternoon

*Raw material for an AIMM teaching block. Companion file: the full conversation export.*

---

## 1. The Initial Idea / Need

Lou runs a library of AI "skills" — reusable capabilities an AI agent can load on demand (a research skill, an editing skill, a session-management skill, and so on). Over time this library had grown to 44+ skills. The initial, entirely reasonable question was organizational:

> "Should these be grouped by team, by expertise, or by function — and which is most useful day to day?"

This is a question every knowledge entrepreneur eventually hits once their toolkit — whether that's AI skills, SOPs, templates, or content assets — outgrows a flat list. The instinct to "put it in folders" feels like maturity. It photographs as professionalism.

## 2. The Journey — What, Why, How

**What happened, in sequence:**

1. Claude recommended organizing by *function* (the job to be done) rather than team/brand or expertise, and the two of them wrote this down as a formal rule: **a category earns its place only if it disambiguates something real, or it's decoration — delete it.**
2. Within the same work session, Claude then expanded the existing four categories to eight — and in doing so, quietly broke the very rule it had just written. Nobody caught it. Not Lou, not Claude, in the moment.
3. Later, Lou asked a sharper question: *"how do I audit the thinking process itself, not just the output?"* This led to a genuine technical distinction worth teaching on its own: auditing an **output** (a document, a plan, a decision) is different from auditing the **reasoning that produced it**. For an output audit, you want the auditor blind to the author's rationale — the deliverable has to stand alone. For a process audit, the rationale *is* the thing being audited, so you export it in full. What stays constant in both cases is that the auditor must be *cold* — a fresh perspective with no memory of the moment, no investment in the reasons that felt right an hour ago.
4. Lou asked to actually run this: audit the reasoning from the session, live, cold. The fresh "auditor" read the whole transcript as a stranger would and caught the contradiction from step 2 immediately — the two of them had built a gate and then walked right around it, in the same breath.
5. Lou then asked the harder question underneath the fix: *"does the library even need to use namespaces at all?"* This flipped the frame from "how do we do this well" to "should we be doing this at all." A quick check of who actually *used* the namespace feature — grepping the entire codebase for real consumers — turned up **zero.** No project manifest anywhere referenced a namespace. The whole apparatus (a design doctrine, a validation script, version history, a documented decision with a date) had never had a single user.
6. They deleted the entire capability. Nothing broke. The system had been finding the right tool by reading its plain description the whole time — the "folder labels" were redundant with the contents.

**Why this matters, not just what happened:** the interesting move isn't the audit catching a bug. It's that after the bug was correctly fixed, someone still asked "wait — was this worth doing in the first place?" That question is not implied by a successful fix. A fix that works invites you to stop looking. The real discipline is asking the *bigger* question right after you've earned the right to feel good about the smaller one.

## 3. The Ultimate Result

- A capability with real, ongoing cost (documentation, validation code, a rule to remember, a decision to defend) and exactly zero usage was identified and removed in under an hour, once the right question was asked.
- The library's actual routing — how the AI decides which skill to use — turned out to work perfectly well without the categorization layer. It had been matching on plain-language descriptions ("use this when the user says X") the entire time.
- A reusable process pattern got documented as a byproduct: a **cold, blind audit** (hand your own reasoning to a fresh perspective with no memory of why you made the choices you made) reliably catches self-justifying blind spots that the original author — human or AI — cannot see from inside the moment.

## 4. Use Case / Application for Knowledge Entrepreneurs

This isn't really a story about software categories. It's a story about **any system a knowledge entrepreneur builds to organize their own expertise or business** — a content taxonomy, a CRM tagging scheme, a course module structure, a set of "brand pillars," a folder system for client work.

Three transferable lessons:

1. **Organizing is not free, and it doesn't announce its own cost.** A tagging system, a naming convention, a set of categories — each one you add is a small tax on every future decision ("which bucket does this go in?"). That tax is invisible day to day and only shows up as an audit finding: nobody's using this.

2. **You cannot audit your own reasoning from inside the moment you had it.** This is the most exportable idea in the whole session. When you're deciding whether a rule you just wrote is being followed, you're the wrong person to check — you're still full of the reasons that made the exception feel fine. The fix is structural, not effortful: get a genuinely fresh read (a colleague who wasn't in the room, a version of yourself a week later, a cold re-read of the plan with none of the context that justified it) before you trust that a decision holds up.

3. **The question after the fix is the one that pays for itself.** It's tempting to treat "I found the bug and fixed it correctly" as the finish line. The higher-leverage question is the one Lou asked next: *does this thing need to exist at all?* That question is cheap to ask and, when the answer is no, it's worth more than any number of correct fixes to the thing you were about to keep.

**The one-line takeaway for the teaching block:**

> Before you perfect the taxonomy, ask who opens the drawer. If the honest answer is no one, the most organized thing you can do is throw the cabinet out.
