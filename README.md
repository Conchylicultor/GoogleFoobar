# Google Foobar

I've got the chance to receive an invitation for [Google Foobar](https://foobar.withgoogle.com/) few month ago. I'll probably never been contacted anymore so I share the code I submitted back then. After completing the challenges, here are some thought about it.

![Interface](imgs/GoogleFoobar.png)

The challenges have an increasing difficulty, but the last level is definitely one step above all others, maybe because it is more about math than algorithm. They let you 22 days to solve this challenge. Each solution can be done using either Java or Python. In my opinion, people who choose Python have a big advantage over those who keep Java. In addition to the fact that prototyping is much faster with Python due to the less verbose (and more permissive) syntax, Java would require to re-program features otherwise available in the Python standard library (the fact that the `itertools` or `fractions` modules were allowed was quite convenient).

Usually, the solution can be found by starting from a brute-force algorithm and optimizing on top of that (sometimes require refactoring). The brute-force implementation help to better understand the problem and generate some data to find a pattern. For some problems, doing some data visualization really helped to discover patterns and made the challenge much easier.

![Fractal](imgs/fractal.png)![Spiral](imgs/spiral.png)

While I was completing level 5, I triggered Foobar again. It doesn't change anything but gives you the possibility to launch two challenges at the same time. If you want to try, here are the keywords which can trigger the challenge. Being located in the US and more specifically in the bay area probably helps:
 * `python list comprehension`
 * `dependency injection`

Those are the two which worked for me. There are other queries which works too (From what I've heard, queries related to `hashmap`, `pthread` or `try catch`). When typing the query, be careful and wait a few second (something like 2s) to gives enough time for the message to appear. I think I missed another opportunity one year ago when I closed the page while the message was appearing.

After completing the last level, you get some message encrypted in base64, maybe with PGP. I'm not sure if everyone get the same message though.

![End](imgs/end.png)
