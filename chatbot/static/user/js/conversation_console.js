function conversationConsole() {
    return {
        stories: [],
        transmit: {
            from: null,
            lift: false,
        },
        help: false,
        cached: "",
        init() {
            this.notifyUI();
        },
        isDirty() {
            return (
                this.cached.replaceAll('"', '\\"').replaceAll("\\n", "\\\\n") !=
                this.setCorpus()
            );
        },
        addCategory(i) {
            this.stories[i].categories.push("Category");
        },
        removeCategory(i, j) {
            this.stories[i].categories.splice(j, 1);
        },
        addConversation(e, i, k) {
            let conversation = {
                intent: "intent_" + Math.floor(Date.now()).toString(36),
                auth: false,
                data_fetch: false,
                entities: "",
                statements: ["Statement"],
                responses: ["Response"],
            };
            if (k != null) {
                this.stories[i].conversations.splice(k, 0, conversation); //insert to k'th position
            } else {
                this.stories[i].conversations.push(conversation); //push to bottom
            }
            this.notifyUI(e);
        },
        removeConversation(e, i, k) {
            this.stories[i].conversations.splice(k, 1);
            this.notifyUI(e);
        },
        cloneConversation(e, i, k) {
            this.stories[i].conversations.splice(
                k + 1,
                0,
                this.stories[i].conversations[k]
            );
            this.notifyUI(e);
        },
        moveConversation(i, k) {
            this.transmit.from = [i, k];
            this.transmit.lift = true;
        },
        placeConversation(i, k) {
            if (this.transmit.lift && this.transmit.from != null) {
                let con =
                    this.stories[this.transmit.from[0]].conversations[
                        this.transmit.from[1]
                    ];
                if (this.transmit.from[0] == i && k != null) {
                    this.stories[this.transmit.from[0]].conversations[
                        this.transmit.from[1]
                    ] = this.stories[i].conversations[k];
                    this.stories[i].conversations[k] = con;
                } else {
                    if (k != null) {
                        this.stories[i].conversations.splice(k, 0, con);
                    } else {
                        this.stories[i].conversations.push(con);
                    }
                    this.stories[this.transmit.from[0]].conversations.splice(
                        this.transmit.from[1],
                        1
                    );
                }
                this.cancelTransmit();
            }
            this.notifyUI(null, true);
        },
        cancelTransmit() {
            this.transmit.from = null;
            this.transmit.lift = false;
        },
        notifyUI(e, bool) {
            $(".tooltip.show").remove();
            if (e == null) {
                setTimeout(() => {
                    $(".stories").getNiceScroll().resize();
                    if (bool) {
                        $(".story").getNiceScroll().resize();
                    }
                    $('[data-toggle="tooltip"]').tooltip("dispose");
                    $('[data-toggle="tooltip"]').tooltip();
                }, 1000);
            } else {
                setTimeout(() => {
                    $(e.target).parents(".story").getNiceScroll().resize();
                    $('[data-toggle="tooltip"]').tooltip("dispose");
                    $('[data-toggle="tooltip"]').tooltip();
                }, 1000);
            }
        },
        addStory() {
            this.stories.push({
                name: "Story " + (this.stories.length + 1),
                categories: ["Category"],
                conversations: [
                    {
                        intent: "intent_" + Math.floor(Date.now()).toString(36),
                        auth: false,
                        data_fetch: false,
                        entities: [],
                        statements: ["Statement"],
                        responses: ["Response"],
                    },
                ],
            });
            setTimeout(() => {
                $(".story").niceScroll(".scroll-wrapper");
            }, 100);
            this.notifyUI();
        },
        removeStory(i) {
            this.stories.splice(i, 1);
            this.notifyUI();
        },
        addIntent(e, i, k) {
            this.stories[i].conversations[k].intent =
                "intent_" + Math.floor(Date.now()).toString(36);
            this.notifyUI(e);
        },
        removeIntent(e, i, k) {
            this.stories[i].conversations[k].intent = "";
            this.notifyUI(e);
        },
        addStatement(e, i, k) {
            this.stories[i].conversations[k].statements.push("Statement");
            this.notifyUI(e);
        },
        removeStatement(e, i, k, l) {
            this.stories[i].conversations[k].statements.splice(l, 1);
            this.extractEntities(i, k);
            this.notifyUI(e);
        },
        addResponse(e, i, k) {
            this.stories[i].conversations[k].responses.push("Response");
            this.notifyUI(e);
        },
        removeResponse(e, i, k, m) {
            this.stories[i].conversations[k].responses.splice(m, 1);
            this.notifyUI(e);
        },
        setCorpus() {
            return JSON.stringify(this.stories, null, 0)
                .replaceAll('"', '\\"')
                .replaceAll("\\n", "\\\\n");
        },
        validateUniqueIntent(ai, ak) {
            if (!this.stories[ai].conversations[ak].intent) {
                setTimeout(() => {
                    if (!this.stories[ai].conversations[ak].intent) {
                        this.stories[ai].conversations[ak].intent =
                            "intent_" + Math.floor(Date.now()).toString(36);
                    }
                }, 1000);
            }
            this.stories[ai].conversations[ak].intent = this.stories[
                ai
            ].conversations[ak].intent.replace(/[\s]+/g, "_");
            this.stories[ai].conversations[ak].intent = this.stories[
                ai
            ].conversations[ak].intent.replace(/[^_a-zA-Z0-9]+/g, "");
            for (i in this.stories) {
                for (k in this.stories[i].conversations) {
                    if ("" + i + k != "" + ai + ak) {
                        if (
                            this.stories[i].conversations[k].intent ==
                            this.stories[ai].conversations[ak].intent
                        ) {
                            this.stories[ai].conversations[ak].intent +=
                                "_" +
                                Math.floor(Date.now() / 1000).toString(36);
                        }
                    }
                }
            }
        },
        extractEntities(i, k) {
            let entities = new Set();

            let regexp = /\w+\|~([_A-Z]+)~/g;
            for (statement of this.stories[i].conversations[k].statements) {
                let matches = statement.matchAll(regexp);
                for (let match of matches) {
                    entities.add(match[1]);
                }
            }
            this.stories[i].conversations[k].entities = [...entities];
        },
    };
}

function textareaResize(el) {
    $(el).height(5);
    $(el).height($(el).prop("scrollHeight"));
}

$(function () {
    $(window).on("load", function () {
        $(".conversation textarea").each(function (_, e) {
            textareaResize(e);
        });
    });
});

function refreshConsole(corpus) {
    document.querySelector("[x-data]").__x.$data.cached = corpus;
    document.querySelector("[x-data]").__x.$data.$refresh();
}
