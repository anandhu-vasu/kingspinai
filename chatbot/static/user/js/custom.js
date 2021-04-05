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
    $(document).on('click','.copy-btn',function(){
        var copyE = this.querySelector("input");
        copyE.select();
        copyE.setSelectionRange(0, 99999);
        document.execCommand("copy");
        $(this).addClass("copied")
        setTimeout(()=>$(this).removeClass("copied"),3000)
    })
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

function copy(e){
    var copyText = e.querySelector("input"); 
    copyText.select();
    copyText.setSelectionRange(0, 99999); /*For mobile devices*/
    document.execCommand("copy");
    alert("Copied the text: " + copyText.value);
}