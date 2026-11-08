from engine.core import *
from engine.templates import *
EP = 59; TITLE = "The_GST_Council"; NAME = "The GST Council"
GOLD = hx('9C7A3C')
BEATS = [
 ("hook", "Before 2017, a product could face a tangle of taxes: central excise, state VAT, entry tax and more. GST replaced all that with one tax, shared by the Centre and the states. And a new body, the GST Council, decides the rules.", HOOK(EP, NAME)),
 ("a", "The Goods and Services Tax came through the 101st Amendment in 2016. It inserted Article 279A, which created the GST Council, and gave both Parliament and state legislatures the power to make laws on GST. GST came into force on the first of July, 2017.",
   scene('paper', TL([("2016", "101st Amendment", "came through"), ("2017", "GST in force", "came into force")], y=215, x0=600, x1=1320), LIST(None, ["Article 279A: the GST Council", "Parliament and state legislatures can both legislate on GST"], y=420, w=1700, size=36))),
 ("b", "GST has several parts. CGST is levied by the Centre on sales within a state. SGST is levied by the state on the same sale. IGST is levied by the Centre on sales between states, and shared afterwards. And UTGST covers Union Territories without legislatures.",
   GRID("Four parts of GST", [("CGST", ["Centre, on sales within a state"], C['pine']), ("SGST", ["the state, on the same sale"], C['navyl']), ("IGST", ["Centre, on sales between states; shared afterwards"], C['berry']), ("UTGST", ["Union Territories without legislatures"], GOLD)], cols=4, maxh=340, cues=["CGST is", "SGST is", "IGST is", "UTGST covers"])),
 ("c", "The GST Council is chaired by the Union Finance Minister. Its members are the Union Minister of State for Finance, and the finance or taxation ministers of every state and Union Territory with a legislature. It decides tax rates, exemptions, thresholds and rules.",
   GRID("The GST Council", [("Chair", ["Union Finance Minister"], C['pine']), ("Members", ["Union Minister of State for Finance", "finance or taxation ministers of the states and Union Territories with legislatures"], C['navyl']), ("Decides", ["rates, exemptions, thresholds, rules"], C['berry'])], cols=3, maxh=380, cues=["chaired by", "Its members are", "It decides"])),
 ("d", "The voting rules are unusual. The Centre has one-third of the votes, and all the states together have two-thirds. A decision needs three-fourths of the weighted votes present and voting. So the Centre cannot pass anything without some states, and the states cannot pass anything without the Centre.",
   scene('paper', ST("VOTING", "3/4 majority", "Centre: 1/3 of the votes · all states together: 2/3", C['berry'], "The voting rules", y=420, scale=.9), LIST(None, ["The Centre cannot pass anything without states", "The states cannot pass anything without the Centre"], y=700, w=1700, size=34))),
 ("e", "To help states during the switch, the Centre promised compensation for revenue loss for five years, funded by a cess on luxury and sin goods. The compensation period ended in June 2022, though the cess was extended to repay related borrowings.",
   LIST("Compensation to the states", ["Promised for five years", "Funded by a cess on luxury and sin goods", "Ended in June 2022", "Cess extended to repay related borrowings"], y=280, w=1700, size=34)),
 ("f", "GST has brought one national market, fewer checkpoints, and a unified tax base. But critics raise concerns. States have given up much of their power to set taxes. Items like petroleum and alcohol remain outside GST. And disputes in the Council have sometimes exposed tensions between the Centre and the states. In the Mohit Minerals case of 2022, the Supreme Court held that the Council's recommendations are persuasive, not binding.",
   GRID("Gains and concerns", [("Gains", ["one national market", "fewer checkpoints", "unified tax base"], C['pine']), ("Concerns", ["states gave up tax powers", "petroleum and alcohol outside GST", "Centre-state tensions"], C['berry']), ("Mohit Minerals, 2022", ["recommendations are persuasive, not binding"], C['navyl'])], cols=3, maxh=400, cues=["GST has brought", "But critics", "In the Mohit"])),
 ("tip", "Here is the memory tip. One-third, two-thirds, three-fourths. The Centre has one-third. The states have two-thirds. A decision needs three-fourths.",
   TIPS([[("1/3", "Centre's votes"), ("2/3", "States' votes"), ("3/4", "needed to decide")]], head_="1/3 · 2/3 · 3/4")),
 ("prelims", "In Prelims, UPSC asks about Article 279A, the voting weights, and the 101st Amendment. Remember: the states together cannot pass a decision without the Centre, since the Centre holds one-third of the votes.",
   PRELIMS(stmt="The states together can pass a GST Council decision without the Centre", ans=False, ans_cue="cannot pass a decision without the Centre")),
 ("mains", "In Mains, discuss GST as a test of cooperative federalism. Cover the shared sovereignty over taxes, the voting structure, the compensation issue, and how disputes have been handled.",
   MAINS("Is GST a test of cooperative federalism?", "Shared sovereignty, voting, compensation.", chips=[("Shared sovereignty", C['pine']), ("Voting structure", C['navyl']), ("Compensation", C['berry'])], cues=spread(3, .4, .9), spacing=500)),
 ("end", "So: one tax, one Council, and a voting rule that makes the Centre and the states depend on each other. Next time: when states disagree.", END(EP)),
]
CAPTIONS = {}
