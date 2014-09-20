##Fusion - Tool to Manage BFH Servers

Released this tool as open source in case anyone finds it useful. This is a rewrite of the tool I've been using for a while which I'd thought I release. It is currently
still in the stages of being rewritten, so is missing A LOT of essential features. It's not a priority of mine to add all of these features, I don't have a server
on a regular basis anymore so it's not in my interests to add them. Main reason for originally developing this was so I had a Linux compatible tool as all the other
publically available tools are Windows only. It's also why I share this, in case anyone needs a tool to run on Linux. 


###Prerequisites
*Python 3
*This makes uf of my BFHRCONPython repository. I have included this however in the "bfhrcon" directory.
*Add your server details in confg/config.xml

###How to Run?

There are 2 versions of the program:
GUI - run MainWindow.py
CLI - run cli.py (currently not included - will be soon)

###Staff.txt
Just a txt file containing staff. Each line must contain a player ID and a permission level. Like follows:
12084824,1337

Different staff levels are,
Owner: 1337
Admin: 2
Moderator: 1




