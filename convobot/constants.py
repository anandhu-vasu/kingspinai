RE_UNAME = r"~uname~"

RE_ENTITY = r"~([_A-Z]+)~"
RE_VALUE = r"~([_a-z]+)~"

RE_ENTITY_DEF = r"\|[\w ,.']+\|~([_A-Z]+)~"

# RE_MEDIA = r"(\n)?(<(image|video)\|https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)>)(\n)?"
RE_MEDIA = r"(<(image|video)\|(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*))>)"

# reg_button = r"<button\|([^|\n]+)\|([^|\n]+)\|>"
RE_BUTTON = r"<buttons\|([^|\n]+)\|>"

MESSAGE_SEPARATOR = "\n\n"
