/**
 *
 * You can write your JS code here, DO NOT touch the default style file
 * because it will make it harder for you to update.
 * 
 */

"use strict";

$(document).ready(function(){
    $(window).on('load', function() {
        setInterval(()=>{
            $(".stories").niceScroll();
            $(".story").niceScroll(".scroll-wrapper");
        },100)
    });
    document.documentElement.className += 
    (("ontouchstart" in document.documentElement) ? ' touch' : ' no-touch');
});

function Toast(title,message="",type="info",position="topRight"){
    let types=["info","question","success","error","warning"]
    if(types.includes(type)){
        iziToast[type]({
            title: title,
            message: message,
            position: position
        });
    }else{
        console.log(`[${title}] ${message}`)
    }
}