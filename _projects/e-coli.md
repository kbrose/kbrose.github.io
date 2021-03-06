---
title: "Predicting Chicago's Beach Water Quality"
img: "/assets/imgs/e-coli/do-not-feed-the-birds.JPG"
---

# The Context

In the 1909 Plan of Chicago, architect Daniel Burnham wrote “The Lakefront by right belongs to the people, not a foot of its shores should be appropriated to the exclusion of the people.” Because of his vision, Chicagoans now benefit from the over thirty public beaches on Lake Michigan. If you take a trip down Lakeshore Drive on a warm summer Saturday, you’ll see crowds of beachgoers from Rogers Park to South Shore.

What Burnham did not write about is the host of dangerous microorganisms that also stake a claim to the Lakefront.

The City of Chicago has taken on the challenge of protecting beachgoers from illness caused by poor water quality. For a long time, state of the art water quality testing meant throwing water in a petri dish and checking back 24 hours later to see what grew. The problem is that the *Escherichia coli* levels at Chicago’s beaches change drastically day-to-day. If you’re a Chicago Parks District employee trying to decide if you’re going to issue a swim advisory today and all that is available is yesterday’s *E. coli* results, you may as well flip a coin.

Trying to improve the situation, the City of Chicago partnered with the United States Geological Survey (USGS) to develop a predictive model. This model would take in yesterday’s *E. coli* reading along with some other information (water temperature, choppiness, etc.) and would try to predict today’s *E. coli* reading. While better than nothing, this predictive model correctly issued swim advisories only **4%** of the time. The Chief Data Officer for the City of Chicago, Tom Schenk, knew that there had to be a better solution. He brought the problem to Chi Hack Night, a weekly gathering of civic technologists and allies in downtown Chicago.

# The Work

Tantalized by the idea of working on a project that could have a tangible effect on city operation, I worked along with several other volunteers at Chi Hack Night trying to improve the predictive model. We [visualized the data](https://github.com/Chicago/clear-water/pull/46) in different ways trying to find exploitable patterns. We [read the relevant academic literature](https://github.com/Chicago/clear-water/wiki/Research-Notes). We tried [including new data](https://github.com/Chicago/clear-water/pull/80) like weather, day of the week, and including historical _E. coli_ readings. We tried [different regression algorithms](https://github.com/kbrose/e-coli-beach-predictions/branches/stale). Comparing performance [on a held-out test set of 2015](https://github.com/Chicago/clear-water/issues/15), we found that nothing we were doing really changed performance significantly. There was just too much unexplained variance. It's possible if we had a better idea of animal behavior or water currents we could have done better, but the data was simply not available. Ultimately, none of these attempts turned out to be useful.

However, two important facts _did_ surface as part of this work. First, during initial data exploration and visualizations, it became clear that while there was very little correlation between _E. coli_ samples at a beach from one day to the next, there was substantial correlation between the _E. coli_ readings of beaches taken on the same day. Second, we discovered that there was a new method of measuring _E. coli_ levels which delivered results in one hour instead of one day, albeit at a higher cost.

If the Chicago Parks District had the budget for it, they could simply have used the new sampling method to get perfect readings. Unfortunately this was not in the budget. But we knew that there was some link between the _E. coli_ readings across beaches. If this pattern held true, the Chicago Parks District could collect samples using the new method at a subset of the beaches and use those results to predict _E. coli_ at the remaining beaches that were not measured. Instead of using the complete but out-of-date information about yesterday’s readings, we could use incomplete but timely information.

![](/assets/imgs/e-coli/corr.png)

_Correlation matrix demonstrating the abundance of correlations between beaches' E. coli levels taken on the same day (left matrix), and the lack of correlation between samples from the same beach taken one day apart (right). Brighter colors indicate higher correlation values._

In addition to having more all-around accuracy, this method has another nice side effect. While exploring the data we found that 5 beaches out of the ~20 or so were responsible for about 56% of the _E. coli_ exceedances. By sampling these beaches directly with the newer, faster method we no longer need to try and _predict_ them. This means even if the predictive model did not change, we would still increase the number of correct swim advisories by an order of magnitude.

This model was developed prior to Summer 2017, and was run as a pilot program while the beaches were open. **The new proposed model would have issued 90 correct swim advisories and 71 incorrect swim advisories. In 2016, the old model issued 12 correct and 184 incorrect swim advisories and in 2015 it issued 14 correct and 184 incorrect swim advisories.** In other words, the new model issues 6 times more correct advisories while decreasing the number of incorrect advisories by more than half. These results include the beaches that were directly sampled using the same-day. Removing these beaches and only looking at those which were _precicted_, the sensitivity still increases threefold from 4% to 12% with no significant change in specificity.

![roc curve](/assets/imgs/e-coli/roc.png)

_ROC curve comparing performances. Prior-day Model is the older model developed by USGS, Hybrid Model is the new model described here but **only** on those beaches that were predicted, not measured directly. From the pre-print publication._

The new method hugely increases the sensitivity while simultaneously decreasing the number of false positives, without added cost for the Chicago Parks District.

# The Lesson

In the end, we had to return to the original goals of the project to rethink our approach. The strategy with the most impact turned out to be deploying a new measurement approach in a manner optimized by machine learning. We had become too focused on improving the model using yesterday’s measurements and were continually being frustrated by the inability to move the needle. By stepping back and actually listening to what the data was telling us, we realized that using same-day readings were a much more effective use of time, effort, and money.

# See Also

[Code and data on GitHub](https://github.com/Chicago/clear-water)

[Pre-print published on BioRXiv](https://www.biorxiv.org/content/early/2018/01/29/250480)

[Official project description from the City of Chicago](http://chicago.github.io/clear-water/)

[[Video] Presentation at Chi Hack Night](https://youtu.be/svMEO9wrud4?t=10m2s)
