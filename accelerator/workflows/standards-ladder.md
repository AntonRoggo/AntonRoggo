# The Standards Ladder play

When to run it: every time the operator corrects Claude, and every time the same mistake comes back. This is the executor for [[Standards Ladder]].

## The loop
1. Claude produces something.
2. The operator reacts: yes, no, not like that.
3. BANK the reaction so it never has to fire again. In the moment, that is /remember-this. End of session, /reflect sweeps for anything missed.

Banking means writing the rule where Claude always reads it, at the right altitude:

| The rule is | It goes in |
|---|---|
| Universal and creative (voice, taste) | brand/voice.md |
| Client-specific and creative | clients/{name}.md |
| Universal and operational (how we work) | CLAUDE.md, Rules that bite |
| Pipeline- or style-specific and operational | that skill's rubric or systems/ folder |

Four buckets, two questions: creative or operational, universal or specific. A rule for one style must never leak into another and break it. That is how a rulebook scales without rotting.

## When a rule is not enough, build a tool
A recurring failure is not a reason to nag harder. It is a signal to build a check in code. Build one the second any of these is true:
- The same mistake keeps coming back after the rule was written.
- The standard is non-negotiable: right most of the time is not good enough.
- A computer can check it: pass or fail, a banned word, a format, a file location. Taste that needs a human eye stays a rule.
- The operator keeps doing the same manual step by hand.

The operator does not ask for a tool. They describe the problem: "how do we make sure this never happens again?" Claude decides it should be a tool, builds it, and wires it in.

## The two-brain pattern
One model writes, a sharper one grades against the rubric and bounces failures back before the operator ever sees the draft. This vault already has the judge move: /adversarial-review. The live-feedback upgrade: when the operator reacts to a draft, write the reaction into the rubric on the spot, then keep working.

## What a banked rubric looks like (Mario's examples, not our rules)
The format to copy: dated raw reaction, then the permanent rule it hardened into.

- 05-30 "I'm not vulgar, that's just how I talk" became: do not neuter the profanity, it is texture.
- 05-31 "I really hate how often you say it" became: no vague pronouns, name the actual noun.
- 06-01 "break up all triplets, that's a strong AI tell" became: doublet is the default, a survivor earns its own line.
- 06-02 "what the fuck does that mean" became: never leave the WHY vague, cash every claim into a concrete reader payoff.

Those are Mario's taste, kept here only as format examples. Ours get banked the same way, into brand/voice.md and the client files.

Related: [[Standards Ladder]] [[Promotion]] [[Memory Loop]] [[voice]]
