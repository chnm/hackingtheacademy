---
title: "Creating a Common Research Language"
authors: ["David Doria"]
weight: 20
original_url: "http://daviddoria.blogspot.com/2010/05/creating-common-research-language.html"
archive_url: "https://web.archive.org/web/20110814084811/http://daviddoria.blogspot.com/2010/05/creating-common-research-language.html"
published: 2010-05-14
captured_from: wayback
---

As a research engineer, the sharing and dissemination of ideas throughout the field is absolutely critical. These ideas are tightly coupled to their implementations. As a explanatory example, consider a very simple invention, the pencil. Once can explain the concept of a pencil in a single sentence : \`\`A pencil is a writing implement usually constructed of a narrow, solid pigment core inside a protective casing.'' Now, consider that you have an incremental improvement to the pencil - you want to make it one color for the first half of the pigment, and a second color for the second half! It is a very simple new concept. If you were the creator of the original pencil, this small change would be extremely fast and easy to produce - simply use two different pigments in your pencil core production process. If you are NOT the creator of the original pencil, this is now an extremely complex task - you must address questions like \`\`How do I compact graphite?'', \`\`How do I get the core to not slip inside of the casing?'', and \`\`What kind of wood do I use for the casing?''. These questions have already been addressed, and likely studied in detail by the original creator of the pencil. That is of no use to you, though. Unless you are personal friends with this person, it is not likely that he will let you use his pencil factory to try out your new idea, so you must start from scratch.


This contrived example of an improvement to the pencil is shockingly similar to the daily situations encountered by engineering researchers. The major difference is that in software there is a simple solution! The situation is all too frequent: someone develops an algorithm and spends years perfecting its implementation. Now I want to use that algorithm as a step in my research. The path rarely strays from: 1) look online and find that there is no publicly available implementation of the algorithm published by the author. 2) email the author asking them to share their implementation with you. 3a) The author has agreed! Now you realize the code has been written without a single regard for future users - there are no comments and no standardized workflow, basically rendering the code useless to anyone but the original author. 3b) More commonly, the author will not respond, or will give you a \`\`sorry, I can't share that code'' type of response. Either way, you must now move forward with nothing. 4) Decide whether to take your research in a different direction, or stay and fight by implementing the alrogithm yourself. 5) spend countless hours and days fighting with the nuances that were left out of the publication of the algorithm, all of which the author has surely already addressed in their implementation. (Note that step 5 is where the majority of graduate students time is spent - REdoing past work!).


Having experienced the above path on countless occasions, I have seen three major problems that arise when implementations are not shared:


1) Massive time expense for newcomers to a field.


Consider that you are a new PhD student. There are two options; 1) No students in your lab have worked in the area you plan to work. In this case, you must start absolutely from scratch. 2) Your research interests have been shared by previous students in your lab. The good news: you get to start with implementations of several important algorithms! The bad news: each algorithm has been implemented by a different student, in a different language. If you are lucky enough that the language is common, it certainly was not using the same libraries. If you are extremely lucky and they did use the same libraries, the code is likely written in a way that does not encourage reuse- either no comments or no reasonable API. You might as well be in case 1 :(


2) Clique-ish research groups.


In the very rare case a lab has multiple studedents working together on parts of a unified problem, the effects of the Pencil analogy are intensely amplified. After a few years of multiple people working together on a code base, incremental changes are extremely easy to pump out quickly. This leads to an even more intimidating barrier to a newcomer to the field. This, in turn, leads to a less diversified outlook on problems, as the same people are almost exclusive continually working on certain problems.


3) \`\`Bad'' re-implementations.


When it has been determined that the way to proceed is to re-implement an existing algorithm, many things start to go wrong. Besides spending massive amounts to time that should be spent elsewhere, one must also consider the quality of the re-implementation. The original researcher spent months or years of his time completely dedicated to this particular algorithm. You intend to simply use it as a small piece in a much larger puzzle. The implementation you create in a week will absolutely not compare to the original implementation in speed, correctness, and reusability. This leads to inaccurate comparisons in research results, as well as overall lower quality and speed of future research.


Scientific computing/programming languages are no different than oral languages. Several oral languages developed thousands of years ago, and regionally societies accepted a particular language so that they could all communicate with one another. This was likely all done unintentionally. Here, the people are the researchers, and the regions are the fields of research. If laypeople could come to these conclusions without even intentional consideration, why can researchers not come to the same conclusions in the face of a very serious problem?


My field is computer vision and scientific data analysis. The languages of choice are Matlab and c++. The libraries (sub-languages) of choice are CGAL, VTK, ITK, and VXL. This exposition is not intended to claim a particular solution (though many of you know which way I lean :) ). If one of these is chosen as the \`\`accepted'' language for this type of research, the field would be able to accelerate at an amazing rate. 


If a researcher is able to say "I have implemented all of my research as VTK filters", the next researcher can simply use his work as a building block for the next year's research. If, instead, the researcher says \`\`I wrote all of my classes from scratch by myself 20 years ago and my students and I have used them ever since'', there is a serious problem.

## Friday, May 14, 2010


### Creating a Common Research Language

Posted by
David Doria
at
[7:39 AM](http://daviddoria.blogspot.com/2010/05/creating-common-research-language.html)



Subscribe to:
[Post Comments (Atom)](http://daviddoria.blogspot.com/feeds/2236281093671603114/comments/default)
