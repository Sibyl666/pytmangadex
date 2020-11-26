from .chapter import Chapter

class Group():

    __slots__ = (
        "session", "id", "name", "altNames", "language", "leader", "members", "description", "website", "discord",
        "ircServer", "ircChannel", "email", "founded", "likes", "follows", "views", "chapters", "threadId",
        "threadPosts", "isLocked", "isInactive", "delay", "lastUpdated", "banner"
    )

    def __init__(self, session, data):
        self.session = session

        self.id = data["group"]["id"]
        self.name = data["group"]["name"]
        self.altNames = data["group"]["altNames"]
        self.language = data["group"]["language"]
        self.leader = data["group"]["leader"]
        self.members = data["group"]["members"]
        self.description = data["group"]["description"]
        self.website = data["group"]["website"]
        self.discord = data["group"]["discord"]
        self.ircServer = data["group"]["ircServer"]
        self.ircChannel = data["group"]["ircChannel"]
        self.email = data["group"]["email"]
        self.founded = data["group"]["founded"]
        self.likes = data["group"]["likes"]
        self.follows = data["group"]["follows"]
        self.views = data["group"]["views"]
        self.chapters = data["group"]["chapters"]
        self.threadId = data["group"]["threadId"]
        self.threadPosts = data["group"]["threadPosts"]
        self.isLocked = data["group"]["isLocked"]
        self.isInactive = data["group"]["isInactive"]
        self.delay = data["group"]["delay"]
        self.lastUpdated = data["group"]["lastUpdated"]
        self.banner = data["group"]["banner"]

        self.chapters = [Chapter(self.session, chapter) for chapter in data["chapters"] if chapter["id"]]
        