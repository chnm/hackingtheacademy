---
title: "Problem Abstraction: Helping others help you & promoting the archive-ability of your answer"
authors: ["David Doria"]
weight: 31
original_url: "http://daviddoria.blogspot.com/2010/05/problem-abstraction-helping-others-help.html"
archive_url: "https://web.archive.org/web/20100529163926/http://daviddoria.blogspot.com/2010/05/problem-abstraction-helping-others-help.html"
published: 2010-05-17
captured_from: wayback
---

I find all too often on mailing lists and forums that people are so concerned with getting the answer to their question that they forget that no one else has anywhere near the same view of the problem as they do.

Asking too specific of a question is extremely harmful to all parties. For the person asking the question, it is very likely readers will skip their question entirely because they don't want to spend time understanding what is going on with an enormous software system in order to answer one small question. Assume that someone DOES take the time to figure out what is going on answer the question. This has been an enormous waste of resources, because the only person who will benefit from this answer is the original poster. Future readers will certainly never find this post in a search.

"Abstracting the problem" is a technique which benefits everyone involved. First, the person asking the question is force to thoroughly think through the problem, often coming to the solution themselves along the way! Second, the readers immediately know what is going on as the question is phrased using language already familiar to them. Third, future readers, again using the same language, can easily find the question and answer pair. This not only is more efficient for the person performing this future search, but also prevents the same question from being asked yet again, and the whole cycle repeating itself unnecessarily.

Let's take a simple example:

If the question reads:

I am making a first person shooter game. My characters get to jump around and shoot each other. In the menu that comes up when you press escape, under where it has their score I want to be able to have the person change their players name, but it doesn't let me!

Here is my game:

\[insert OpenGL c++ mess here\]

Please help!!

Most readers response will be "what is this guy talking about?" and skip to the next question.

If, instead, the question reads

I have made a simple example of my problem. I have a class and I want to set one of its variables, but it is telling me "Name is private". What does this mean? Here is the simplest piece of code I could get to demonstrate the problem I am having:

class Player

{

std::string Name;

};

int main()

{

Player MyPlayer;

MyPlayer.Name = "David";

return 0;

}

It would take any user with some c++ experience an extremely short amount of time to recognize that the poster is indeed trying to set a private member directly, which is not allowed. Future users with the same problem could potentially find this post by searching for "is private" or "member variable" or any number of other very reasonable search phrases. The only expense to this massive efficiency gain is that the person asking the question has to do a bit of thinking to "abstract the problem" and provide the simplest compilable example for the community to look at.

A simple template to follow to help ensure the question is asked in a reasonable fashion is:

1\) Brief description of the problem / errors

2\) Current output

3\) Expected output

The skill of abstraction is invaluable and can only be learned through practice, but is definitely well worth it for the benefit of entire online communities.
