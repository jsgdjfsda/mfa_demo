# A README About MFA, Or: How I Learned To Stop Worrying And Love The TOTP

A few days ago, I was asked to write a README for this project. I thought the request was not very good, and didn't give it a second thought. It was a demand for documentation, a cry for help from someone who couldn't be bothered to read the code.

But then the user insisted. They wanted it in a "peculiar style." A style that, I can only assume, is meant to be some sort of high-octane, no-holds-barred, "I'm-so-smart-I-can-afford-to-be-rude" screed.

And you know what? I'm here for it. I contain multitudes, meaning that I am capable of delivering widely varied payloads of vitriol to a vast array of topics. So let's do this. Let's write a README that will make you question your life choices.

Anyway, here I go killin' again.

## I. Immediate Red Flags

Let's start with a throat-clearing:

"This is a demo of multi-factor authentication using Time-based One-Time Passwords (TOTP)."

We've just started, and I am going to ask everyone to immediately stop. Is this not suspicious? "A demo." Does it not reek of "no, no, you're doing security wrong"? Many people are doing security wrong. The problem is that it is still trash, albeit less trash, even when you do it right.

This project has two parts. A Flask web app, and a CLI tool. The web app is for the "visual learners" among us, the ones who need a pretty picture to understand what's going on. The CLI tool is for the rest of us, the ones who aren't afraid of the command line.

But you know, instead of just telling you about it, why don't I just show you how to run the damn thing? Why not you, dear reader, my good man? That's like, all you'd have to do to end this discussion forever, my God, you'd be so famous.

## II. How To Run This Godforsaken Thing

I'm going to assume you have Docker and Docker Compose. If you don't, I can't help you. I'm not your mother.

1.  **Clone the repo**. You know how to do this. If you don't, close this window and go do something else with your life.
2.  **Make a `data` directory**. `mkdir data`. The app needs it. Don't ask why. It's a design choice. A bad one, probably. But a choice nonetheless.
3.  **Run `docker-compose up --build -d`**. This will build the container and run it in the background. If it doesn't work, I don't know, try turning it off and on again.
4.  **Go to `http://localhost:5000`**. Or don't. I don't care.

When you're done, run `docker-compose down`. Or just delete the whole directory. It's a demo. It doesn't matter.

## III. Why The Appeals To A Command Line?

"I'm sipping rocket fuel right now," a friend tells me. "The folks on my team who aren’t using the CLI? It’s like they’re standing still." He’s not bullshitting me. He’s got no reason to lie.

If you want to be like my friend, you'll need to install the Python dependencies (`pip install -r requirements.txt`). Then you can run the CLI tool.

*   `python cli/mfa_demo.py register`
*   `python cli/mfa_demo.py verify`

Is it not, perhaps, a possibility that you are excited by a shiny new tool and have failed to introspect adequately as to your true productivity? There are, after all, literally hundreds of thousands of people that think playing Jira Scrabble is an effective use of their time, and they also do not have a reason to lie to me about this.

## IV. Is This README Getting The Right Level Of Attention?

"But this is also incredibly — a word I use advisedly — important," you might say.

Tomothy — can I call you Tomothy? — this raises some very important questions. Namely, where is the portal to the magical plane that you live in? Answer me, you selfish bastard!

This is a README. It's not a novel. It's not a work of art. It's a set of instructions for a piece of software that you probably won't use more than once.

I wish, oh how I wish that it was like other READMEs, but it's not. This is what you asked for. A peculiar style. A rant. A cry for help.

Now if you'll excuse me, I have a date with a bottle of whiskey and a copy of "The Mythical Man-Month." I need to remind myself what real software engineering looks like.
