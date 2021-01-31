$(document).ready(function () {
    $("#ach-counter").waypoint(
        function (_ide) {
            $(this).find(".counter-ls-value").each(function () {
                $(this)
                    .prop("Counter", 0)
                    .animate(
                        {
                            Counter: $(this).text(),
                        },
                        {
                            duration: 3500,
                            easing: "swing",
                            step: function (now) {
                                $(this).text(Math.ceil(now));
                            },
                        }
                    );
            });
            this.destroy();
        },
        { offset: "100%",continuous: false}
    );

    $("#count").waypoint(
        function (_ide) {
            $(this).find(".counter-ls-value").each(function () {
                $(this)
                    .prop("Counter", 0)
                    .animate(
                        {
                            Counter: $(this).text(),
                        },
                        {
                            duration: 3500,
                            easing: "swing",
                            step: function (now) {
                                $(this).text(Math.ceil(now));
                            },
                        }
                    );
            });
            this.destroy();
        },
        { offset: "100%",continuous: false}
    );
});
