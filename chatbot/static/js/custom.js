$(document).ready(function () {

    function counterAnimation(id){
        $("#"+id).waypoint(
            function () {
                if(this.completed==undefined)
                    this.completed = true
                else if(this.completed && this.hasOwnProperty('destroy')){
                    this.destroy()
                }else return
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
            },
            { offset: "100%"}
        );
    }

/*     $('main > *').waypoint({
        offset: '50%',
		handler: function() {
			$('main>*').each( function(index) {
				jQuery( this ).delay( index*200 ).queue(function(next){
					jQuery( this ).addClass('animated fadeIn');
					next();
				});
			});
		}
    }) */
    
    counterAnimation('ach-counter');
    counterAnimation('jou-counter');
});
