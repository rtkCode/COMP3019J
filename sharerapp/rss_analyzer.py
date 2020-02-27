import xml.dom.minidom
import urllib.request
import ssl

# this class is to read rss xml and convert it into a json format

class RSSAnalyzer():
    def analyze(xml_url):

        # to ensure get request correctly, the urllib may mistake without it, this answer is learned from internet
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context

        # add browser header to prevent Atom Anti-reptile
        header = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36"}

        # if link is not valid
        try:
            request = urllib.request.Request(url=xml_url, headers=header)
        except BaseException:
            return {}

        response = urllib.request.urlopen(request)

        # store page in a xml file
        xml_data=response.read()
        file=open("rss_temp.xml","wb")

        # read from the file and convert it into DOM
        file.write(xml_data)
        file=open("rss_temp.xml")
        DOMTree = xml.dom.minidom.parse(file)
        collection = DOMTree.documentElement
        coll=DOMTree

        # init
        dict = {}

        site_title = ""
        site_icon=""
        site_subtitle=""
        site_link=""
        site_update_time=""
        site_author=""

        item_count=0
        items = []
        item_title = []
        item_link = []
        item_date = []
        item_creator = []
        item_description = []
        item_content = []

        # start analysis DOM tree
        if len(coll.getElementsByTagName("feed")) != 0:
            root=coll.getElementsByTagName("feed")

            if len(root[0].getElementsByTagName("title"))!=0:
                site_title = root[0].getElementsByTagName("title")[0].childNodes[0].data

            if len(root[0].getElementsByTagName("icon"))!=0:
                site_icon = root[0].getElementsByTagName("icon")[0].childNodes[0].data

            if len(root[0].getElementsByTagName("subtitle"))!=0:
                site_subtitle = root[0].getElementsByTagName("subtitle")[0].childNodes[0].data

            if len(root[0].getElementsByTagName("link"))!=0:
                site_link = root[0].getElementsByTagName("link")[0].getAttribute("href")

            if len(root[0].getElementsByTagName("updated"))!=0:
                site_update_time = root[0].getElementsByTagName("updated")[0].childNodes[0].data

            if len(root[0].getElementsByTagName("author")) != 0:
                if len(root[0].getElementsByTagName("author")[0].getElementsByTagName("name")) != 0:
                    site_author = root[0].getElementsByTagName("author")[0].getElementsByTagName("name")[0].childNodes[0].data

            if len(root[0].getElementsByTagName("entry")) != 0:
                items = root[0].getElementsByTagName("entry")
                item_count = root[0].getElementsByTagName("entry").length

                for item in items:
                    if len(item.getElementsByTagName("title")) != 0:
                        item_title.append(item.getElementsByTagName("title")[0].childNodes[0].data)
                    else:
                        item_title.append("")

                    if len(item.getElementsByTagName("link")) != 0:
                        item_link.append(item.getElementsByTagName("link")[0].getAttribute("href"))
                    else:
                        item_link.append("")

                    if len(item.getElementsByTagName("pubDate")) != 0:
                        item_date.append(item.getElementsByTagName("pubDate")[0].childNodes[0].data)
                    else:
                        item_date.append("")

                    item_creator.append("")

                    if len(item.getElementsByTagName("summary")) != 0:
                        item_description.append(item.getElementsByTagName("summary")[0].childNodes[0].data)
                    else:
                        item_description.append("")

                    if len(item.getElementsByTagName("content")) != 0:
                        item_content.append(item.getElementsByTagName("content")[0].childNodes[0].data)
                    else:
                        item_content.append("")

        else:
            channel=collection.getElementsByTagName("channel")[0]

            if len(channel.getElementsByTagName("title"))!=0:
                site_title = channel.getElementsByTagName("title")[0].childNodes[0].data

            if len(channel.getElementsByTagName("description"))!=0:
                site_subtitle = channel.getElementsByTagName("description")[0].childNodes[0].data

            if len(channel.getElementsByTagName("link"))!=0:
                site_link = channel.getElementsByTagName("link")[0].childNodes[0].data

            if len(channel.getElementsByTagName("lastBuildDate"))!=0:
                site_update_time = channel.getElementsByTagName("lastBuildDate")[0].childNodes[0].data

            if len(channel.getElementsByTagName("item"))!=0:
                if len(channel.getElementsByTagName("item"))!=0:
                    item_count = channel.getElementsByTagName("item").length
                    items = channel.getElementsByTagName("item")

                for item in items:
                    if len(item.getElementsByTagName("title")) != 0:
                        item_title.append(item.getElementsByTagName("title")[0].childNodes[0].data)
                    else:
                        item_title.append("")

                    if len(item.getElementsByTagName("link")) != 0:
                        item_link.append(item.getElementsByTagName("link")[0].childNodes[0].data)
                    else:
                        item_link.append("")

                    if len(item.getElementsByTagName("pubDate")) != 0:
                        item_date.append(item.getElementsByTagName("pubDate")[0].childNodes[0].data)
                    else:
                        item_date.append("")

                    if len(item.getElementsByTagName("dc:creator")) != 0:
                        item_creator.append(item.getElementsByTagName("dc:creator")[0].childNodes[0].data)
                    else:
                        item_creator.append("")

                    if len(item.getElementsByTagName("description")) != 0:
                        item_description.append(item.getElementsByTagName("description")[0].childNodes[0].data)
                    else:
                        item_description.append("")

                    if len(item.getElementsByTagName("content:encoded")) != 0:
                        item_content.append(item.getElementsByTagName("content:encoded")[0].childNodes[0].data)
                    else:
                        item_content.append("")

        dict["title"]=site_title
        dict["subtitle"]=site_subtitle
        dict["link"]=site_link
        dict["author"]=site_author
        dict["update"]=site_update_time
        dict["icon"]=site_icon
        dict["count"]=item_count

        entries=[]
        for i in range(item_count):
            inner_dict={}
            inner_dict["title"]=item_title[i]
            inner_dict["summary"] = item_description[i]
            inner_dict["link"]=item_link[i]
            inner_dict["date"]=item_date[i]
            inner_dict["creator"]=item_creator[i]
            inner_dict["content"]=item_content[i]
            entries.append(inner_dict)

        dict["entries"] = entries

        # test
        # print(site_title)
        # print(site_subtitle)
        # print(site_link)
        #
        # print(item_count)
        # print(item_title)
        # print(item_link)
        # print(item_date)
        # print(item_creator)
        # print(item_description)
        # print(item_content)
        #
        # print(dict)

        return dict


