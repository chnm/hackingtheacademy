---
title: "Teach the “Why” not the “How”"
authors: ["David Doria"]
weight: 41
original_url: "http://daviddoria.blogspot.com/2010/05/teach-why-not-how.html"
archive_url: "https://web.archive.org/web/20100529163931/http://daviddoria.blogspot.com/2010/05/teach-why-not-how.html"
published: 2010-05-20
captured_from: wayback
---

Let us consider a college Calculus course. The timeline of the course goes approximately like this:


Week 1 - What is a derivative?

Week 2-10 - Practice manually computing derivatives of hundreds of functions.

Week 11 - What is an integral?

Week 12-20 - Learn many methods for performing integration manually and practice this on hundreds of complex functions.


They have the missed the point completely. With todays technology, on a device as simple as a handheld calculator, one can find a derivative (10 weeks of practicing) in a single line:


diff(f(x),x)


The same goes for integration:


int(f(x),x)


What is it, then, that we humans are needed for at all? The answer is three fold


1) To be able to produce an f(x) out of a real life problem


2) To know when to type one of those lines into the calculator or computer


3) Understand how to interpret the results


Consider a typical, simplified workflow in an industrial application. You work at a marble factor. Your boss says "Dave, we need you to make a box out of this cardboard square so that we can ship the most marbles." You go back to your office and draw a sketch of an unfolded box. You come up with the equation of the volume of the resulting box in terms of a couple of parameters. You realize that what you need to do is find the maximum of this volume function. You know that by equating the derivative of a function to zero you will find the extrema! You then type


solve(diff(f(x),x)=0,x)


into the nearest computing device. It tells you that there are two solutions. You realize that one is probably a minimum and one is probably the maximum you are looking for. Another couple of lines to verify this:


v(solution1)

v(solution2)


You pick the solution that produces the highest volume. You are done! You report to you boss that you know how to make the biggest box out of the cardboard blank and he is happy with your work.


Here is a rough breakdown of the knowledge required to solve this problem:


50% - Setting up the volume function

40% - Knowing that the zeros of the derivatives are the extrema

10% - Interpret what the roots mean


Note that 0% was reserved for knowing HOW to solve for the roots. Computers can do this :)


Your boss may ask you "How did you do it?". To this you can say "I developed an equation for the volume of the box with a couple of parameters that you can see in this sketch. I then maximized this function to determine the appropritae parameters." You will NOT have to answer the question "How did you solve that equation?". This is because not only is it unimportant, it is also assumed that you have used all of the tools at your disposal to prevent human error.


Let's revisit the Calculus class. How much time did they spend teaching you how to develop functions from practical situations? Almost none. How much is this necessary? VERY! How much time did they spend teaching you HOW to solve the problems? Almost 10 weeks. How much is this necessary? NONE!


The solution here is to shift the instruction away from the "how" and focus on the "why".


A skilled team of mathemeticians and computer scientists has figured out how to handle almost any operation on almost any function you can develop. If you are not on that team, you do not need to know what happens inside the box, you only have to be intellegent about what you feed to the box, and you have to know what to do with the information the box gives you back. THIS is engineering.


Certainly we do not want these mechanics/details to become a lost art. By not teaching every student these details, we are not losing the art. There are hundreds of text books published with the mechanics/methods for these operations. If one ever does need to know the details (perhaps they've joined the team to write the next software package!), any of these books can be consulted.


I am ABSOLUTELY NOT condone the typical malpractice of students just typing equations into a calculator without knowing what they mean. In fact, many teachers have banned calculators in classrooms for this reason. Unfortunately, these teachers have missed the point. If their questions can be answered by the calculator alone, they are asking the WRONG QUESTIONS! As described above, the need to focus almost entirely on what the calculator CANNOT do, and explain that it is OK to defer the parts that the calculator CAN do to the calculator! A math teacher may tell you "No, no, look at all of these real life problems the students are doing for homework!". Look more closely. These "real life" problems are typically simply a mask over a mundane "do the computation" type of problem. Rather than just renaming variables, the empasis needs to be on "Look how many exciting things you can do now that you know these concepts!".


We have to be careful, though, to not say "Here is the theory, now you are done." This is very bad. Theory without practice is reserved for scientists and mathemeticians! But we are engineers! We must say instead "Here is the theory, now we're going to discuss and give you many examples of typical use cases". This is what will put students on the right track to becoming excellent, problem solving engineers.

## Thursday, May 20, 2010


### [Teach the "Why", Not the "How"](http://daviddoria.blogspot.com/2010/05/teach-why-not-how.html)

Posted by
David Doria
at
[1:01 PM](http://daviddoria.blogspot.com/2010/05/teach-why-not-how.html)
![](image-1.gif)


Labels:
[education](http://daviddoria.blogspot.com/search/label/education),
[Engineering education](http://daviddoria.blogspot.com/search/label/Engineering%20education)

Subscribe to:
[Post Comments (Atom)](http://daviddoria.blogspot.com/feeds/1573463594794745114/comments/default)
