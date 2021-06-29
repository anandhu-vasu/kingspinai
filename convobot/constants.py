RE_WEBHOOK_URL = r"webhook/{webhook_name}/(?P<bot_token>.+?)/$"

RE_UNAME = r"~uname~"

RE_ENTITY = r"~([_A-Z]+)~"
RE_VALUE = r"~([_a-z]+)~"

RE_ENTITY_DEF = r"\|[\w ,.']+\|~([_A-Z]+)~"

RE_MEDIA = r"(?:\n)?(<(image|video)\|(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*))>)(?:\n)?"

# reg_button = r"<button\|([^|\n]+)\|([^|\n]+)\|>"
RE_BUTTON = r"<buttons\|([^|\n]+)\|>"

MESSAGE_SEPARATOR = r'\n{2,}'


