import threading
from queue import SimpleQueue as Queue
import requests
import os
import json
from pyquery import PyQuery

class Worker(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.s = requests.Session()
        self.s.post("https://www.ptt.cc/ask/over18",{
            "from" : "/bbs/Beauty/index.html",
            "yes" : "yes"
        })

    def getTopics(self, tocLink):
        topics = []

        toc = PyQuery(self.s.get(tocLink).text)
        for item in toc("div .r-ent").items():
            pageLink = item(".title a").attr.href
            if not pageLink:
                continue

            push = item(".nrec").text()
            if push == "爆":
                push = 99
            elif "X" in push:
                if push == "XX":
                    push = -99
                else:
                    push = int(push.replace("X", "-"))
            elif not push:
                push = 0
            else:
                push = int(push)

            title = item(".title a").text()

            topics.append((push, title, pageLink))
        return topics

    def getPics(self, topic):
        index = topic[2].split("/")[-1].replace(".html", "")
        if os.path.isdir(os.getcwd() + f"\\pics\\{index}"):
            return
        os.mkdir(os.getcwd() + f"\\pics\\{index}")
        with open(f"pics\\{index}\\inf.json", "w") as f:
            json.dump({
            "push" : topic[0],
            "title" : topic[1],
            "link" : topic[2]
            },f)

        page = PyQuery(self.s.get("https://www.ptt.cc" + topic[2]).text)
        i = 1
        for item in page("a[href]").items():
            imgurLink = item.attr.href
            if "imgur" not in imgurLink or "https" in imgurLink:
                continue
            imgLink = PyQuery(self.s.get(f"https:{imgurLink}").text)("link[rel=image_src]").attr.href
            if imgLink == None:
                continue
            format = ""
            if "jpg" in imgLink or "jpeg" in imgLink:
                format = "jpg"
            elif "png" in imgLink:
                format = "png"
            else:
                continue

            with open(f"pics\\{index}\\{i}.{format}", "wb") as p:
                for chunk in self.s.get(imgLink):
                    p.write(chunk)
            i += 1

    def run(self):
        while not self.queue.empty():
            topics = self.getTopics(self.queue.get())
            for topic in topics:
                self.getPics(topic)
