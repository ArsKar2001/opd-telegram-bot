class Faculty:
    name: str
    id: int

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class Curator:
    link_sdo: str
    name: str
    id: int

    def __init__(self, id, name, link_sdo):
        self.id = id
        self.name = name
        self.link_sdo = link_sdo


class Group:
    id: int
    name: str
    faculty_id: int

    def __init__(self, id, name, faculty_id):
        self.id = id
        self.name = name
        self.faculty_id = faculty_id


class Student:
    group_id: int
    curator_id: int
    full_name: str
    id: int

    def __init__(self, id, full_name, curator_id, group_id):
        self.id = id
        self.full_name = full_name
        self.curator_id = curator_id
        self.group_id = group_id


class User:
    id: int
    chat_id: int
    group_id: int

    def __init__(self, chat_id):
        self.chat_id = chat_id
