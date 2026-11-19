---
title: "thoughts on omeka-fied cv"
authors: ["Patrick Murray-John"]
weight: 25
original_url: "http://www.patrickgmj.net/node/185"
archive_url: "https://web.archive.org/web/20100614190352/http://www.patrickgmj.net/node/185"
published: 2010-05-15
captured_from: wayback
---

"Any medium powerful enough to extend man's reach is powerful enough to topple his world.  To get the medium's magic to work for one's aims rather than against them is to attain literacy."

-- Alan Kay, "Computer Software", Scientific American, September 1984

# Thoughts on Omeka-fied CV

0The last few posts have been about my experiment to use [Omeka](http://omeka.org) to create [my online CV](http://cv.patrickgmj.net). Many thanks to the folks who left comments and thoughts on them -- they've been really helpful. The end of the school year is always a good time to update the CV, and given the amount of work I've been doing with Omeka lately it seemed like now was the time to do some pushing on that experiment. I've linked to it before in [previous posts](http://www.patrickgmj.net/taxonomy/term/129), but it's only recently that I tweeted a link to it. I guess that's the new version of officially launching a site. So here's some reflection on the process, decisions, and difficulties I've encountered.

0
{{< missing-image alt=`` src=`http://www.patrickgmj.net/images/omekacv/header.png` >}}


0The first real exhibit I tackled was "Becoming a Digital Academic". Overall, writing the first exhibit was an odd mix of writing a blog post and writing an objective narrative. In some ways, it might be more like a blog post than blog posts are in the depth of reflection on where I am and where I have been, focused by attention to the particular items that I added to the Omeka site. I think that some pages lean more toward reflection, and some lean more toward historical account. I suppose that result should have been obvious from the premise of the experiment. But it was funny to encounter through the writing process.

0
{{< missing-image alt=`` src=`http://www.patrickgmj.net/images/omekacv/exhibit-switch.png` >}}


### Structure

0
The first thing that I wanted to make sure I did was to take very seriously the *online* part of online CV. At the most basic level, that meant not simply creating a page and slapping in something that looks close to the print version of the CV. (And I just realized that, in concentrating on that, I completely forgot to add a link to a PDF version of the CV. I'm tempted to leave it out altogether.) If I'm really going to rethink the textuality and function of a CV in the online environment, I need to forget the print version.

0 One obvious thing that going online offers is infinite space. I don't have to try to cram everything into a reasonably small number of pages. And, to emphasize the online-ness, I get to put in a link to any and (almost) every online account that I have, something that would probably be out of balance in a print CV.

{{< missing-image alt=`` src=`http://www.patrickgmj.net/images/omekacv/google.png` >}}

{{< missing-image alt=`` src=`http://www.patrickgmj.net/images/omekacv/twitter.png` >}} />/>

0 Moreover, since it's an online CV, and part of the implicit point about the kind of work that I do is that it builds up an online presence, I wanted to emphasize the online-ness not just by giving links to my online accounts, but to show real-time evidence of me online. And so one essential part of the online CV is including a "Google Me" link, which opens up Google's search page with my name filled in inside an iframe in the site. That's the real evidence of and perspective on me online. Maybe one better -- and I'm conscious that this might be risky -- I put a similar "Recent Mentions On Twitter" link, again with an iframe of the Twitter search page on "@patrickgmj".

0 Those two components strike me as essential to the translation from print to online CV's, and reflect the broader translation of traditional scholarship to the online environment. A traditional CV would of course list the various publications and other contributions to scholarship under one's name. And, traditionally, that's a list of printed items, intended to reflect and demonstrate your place and, hopefully, influence in the intellectual community. Digital academia, at least in part, calls for an analogous online element to show one's place in the online intellectual community. "Google Me" and "Recent Mentions on Twitter" are an effort to implement that translation from print academia to digital academia.

{{< missing-image alt=`` src=`http://www.patrickgmj.net/images/omekacv/cvproper.png` >}}

{{< missing-image alt=`` src=`http://www.patrickgmj.net/images/omekacv/details.png` >}} 

0 But I didn't feel like I could entirely omit the bullet-pointish quick overview of the print CV. And so, I've been trying to divide items up into collections that reflect the traditional print CV, and provide a page that moves toward that view. I used some of the techniques elsewhere in Omeka for tabbed display to treat the collections as tabs to show the list of Items in those collections. Then, I added in some javascript to show some of the item information on mouseover. Unfortunately, that makes for a pretty long load time for the page, since so much about all the items has to get loaded up before the javascript can do it's thing. A future version might switch that over to some AJAX. The advantage is that, like the print CV, you can get a very quick overview, but go one step further. In the print CV, the bulleted item is the end of the information. Online, rolling over the bulleted item immediately pulls up a little bit more information about that bullet-point. That's especially happy with anything, like a conference, that has a handy image to go along with it.

### Item Types

0Item types got to be stickier than I thought. On one hand, I could have gone all-out and created new item types and item type metadata as needed to reflect the implicit types in a traditional CV. That is, create a "Degee" item type, a "Conference Paper" item type, a "Job" item type, etc.I might still do that, at least for some of types. But I also wanted to stay as close as I could to out-of-the-box Omeka, and follow where those constraints led me -- like a poetic form, constraints can push creativity and rethinking. And so, I'm thinking a lot about event-based modelling. So I'm putting in conferences as events. That does an odd reversal to the structure of a print CV, where the *paper* gets the emphasis. Here, I'm letting the conference have the emphasis as the item. If I were to go all-out, I'd make both the conference and the paper items, use use the "Relation" element to tie them together. That'd be the better information modelling, I think, but it would make a decent display in an Exhibit harder to do -- I'd have to pull both items into whatever Exhibit page I was building, and in the item-based navigation it would visually split them apart more than I'd like. In a later version, that might be the way to go, but I'm hesitant.

### People and Groups as Items

0When I started to think about building up real exhibits in Omeka to give perspective to the items -- which was really the entire point of the experiment -- I realized something kinda startling. There is little to no place in a print CV for the *people* who have been essential parts of one's "Course of Life" ("Curriculum Vitæ"). The one exception is listing one's dissertation director, and maybe the entire committee. That seems like a huge gap in the traditional CV. I suspect, though cannot know with any certainty, that search committees will try to fill in that information from what they know of the "feel" of particular conferences and their knowledge of what scholars are also at institutions listed in the job history. The mode of exhibit-building, where you are creating a story and an interpretation, seemed to require adding people and groups as items.

0But, I have really mixed feelings about making some of my friends and colleages items in an Omeka collection. In general, I'm pretty sure that they won't have too many objections. But, it makes me extra-conscious that I am creating an online representation of them, so how do I approach putting in a description for them? I started out with a description that put them into a perspective relative to me (e.g., "Gardner was the director of DTLT who hired me."). I started rethinking that as I went along, and am now leaning toward something more objective, copying what they put into the Twitter bios where I can. I'll have to go back through them all to make sure I'm consistent about that.

0What if I make one of the people in my online CV a featured item?

0I also added a few more elements to the Person item type, and I expanded it to "People and Groups". ("People and Groups" is really a reflection of thinking in terms of FOAF, where people and groups are subsets of a general "Agent" class.) The elements that I added are "URL" to link to their web page, and "Twitter" to link to their Twitter accounts. Again, I have a few misgivings about creating web pages about other people.

### Representative Images for Items

0You really can't get away from the strength of the web being visually-oriented. So for items, and especially how they appear when added to an exhibit page, I found some real difficulty in representative images. One bonus of treating conferences as events is that I could mine Flickr for images, at least for some of them. But the absense of images for others stands out. And what do I do about a representative image for a dissertation or a degree? Especially for someone with little to no graphic design skill, that's going to be a tricky thing to get around.

0On the other side, for some events I have several images, and I'm getting a little stuck in how to select the one I want for a particular exhibit page. I might just be missing something in working with exhibits. It made a funny realization that I've spent relatively little time in the work of actually building exhibits in Omeka during all that time I spent in the code of Omeka!

### Completeness of Item Metadata

0As a general principle, I always want metadata to be as complete as possible. Here, though, I've found myself dealing with practicalities of prioritizing what metadata to spend the time on. Do I want to think about Subjects? I'm leaning toward getting myself to a position of declaring to myself a limited set, and just trying to be consistent about including that limited set where I can. Here again, the issue of making people I know Omeka items is tricky. I don't think that I should include birthdays. But gender? Occupation? Online accounts? Images? Especially if the image is a group or crowd shot from a conference, and I'm picking them out in an annotation that they might not even know exists? I suppose it's not too different from Flickr's feature to say who is depicted in an image, but it still strikes me as a funny thing to create data on the web about a person without them really knowing about it. Here again, I find myself considering some ethical questions about representing others online that I hadn't anticipated.

0Another practical twist to adding people is that the default display mode counts on Dublin Core metadata. Though I'm not sure that any technical declarations have been made saying that Dublin Core should not apply to people, it still strikes me as a mismatch. I've fired up the FOAF Element Set, but haven't really made much use of it so far because I'm not yet ready to make meaningful use of it (or any other Element Set) within Omeka exhibits. I'd like to be find an easy way to branch metadata display of an item in an exhibit based on its item type, but that might be a pretty complicated task.

### Future work

0I've submerged some typical Omeka features, like browsing items and collections (though if you get to an item page, the link to its collection is still there). I think that's right, since I'm working on presenting my history as I want to represent it. But, once again, that raises the fact that I'm also creating and publishing information about others. That happens often enough in blog posts, too, I suppose. Is there a different import to doing it in an Omeka installation? What difference does the structure of Omeka make? How different is this from creating a Wikipedia entry about someone? (Note to self, I should check Wikipedia's policies about writing about living people.)

0One interesting practical place where I might have to consider this is if I start to build up some tag-based navigation. I mostly avoided tags so far, but found myself wanting to put on some basic tags, like "CHNM" and "DTLT". Those could apply to both people and atifacts. Those examples of tags are fairly objective, though. What about tags that have a greater personal interpretation weight. I doubt that I'd go here, but some extreme examples of tags in the context of my history might be "Influence", "Mentor", "Nemesis", "Friend", "Fail", "Owes A Beer To". More in a middle ground might be tags like "Digital Humanities", "Coding", "Research", "Alt-Ac", "THATCamp". Those could apply to both people and artifacts, and amount to publishing an interpretation of them. Something about doing so in the medium of a CV feels different from doing so in the medium of a blog post.
