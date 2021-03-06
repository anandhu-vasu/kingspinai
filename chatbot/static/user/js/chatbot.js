function removeChatbot(event,name,id){
    swal({
        title: `Are you sure to delete chatbot?`,
        text: `Once deleted, All models and data of your "${name}" chatbot will be deleted permanently!`,
        icon: 'warning',
        buttons: true,
        dangerMode: true,
        })
        .then((willDelete) => {
        if (willDelete) {
            $('.chatbot-btns .btn').prop('disabled', true)
            $(event.target).find("i.far").removeClass('fa-trash-alt').addClass('loading-icon fa-spinner fa-pulse')
            Unicorn.call('chatbot', 'delete',id);
        }
    });
}
function removeChatbotFinished(){
    $('.chatbot-btns .btn').prop('disabled', false)
    $("i.loading-icon").removeClass('loading-icon fa-spinner fa-pulse').addClass('fa-trash-alt')
    
}

function notifyUI(){
    $('[data-toggle="tooltip"]').tooltip('dispose');
    $('[data-toggle="tooltip"]').tooltip();
}

function showChatbotSettings(event,id){
    document.getElementById("chatbot-settings").__x.$data.open=false
    $('.chatbot-btns .btn').prop('disabled', true)
    $(event.target).find("i.fas").removeClass('fa-tools').addClass('loading-icon fa-spinner fa-pulse')
    Unicorn.call("chatbot-settings","set_chatbot",id)
    event.stopPropagation();
    event.preventDefault()
}
function openChatbotSettings(){
    $('.chatbot-btns .btn').prop('disabled', false)
    $("i.loading-icon").removeClass('loading-icon fa-spinner fa-pulse').addClass('fa-tools')
    document.getElementById("chatbot-settings").__x.$data.open=true
    bindDirtyObserver()
}
function showErrors(){
    $('.unicorn-errors:not(.error-shown)').addClass("error-shown").find(".error").slideDown();
    /* $('.has-error').removeClass("has-error").addClass("no-error")
    for ( field in Unicorn.getComponent("chatbot-settings").errors){
        $("#"+field).addClass("has-error").removeClass("no-error");
    } */
}

function bindDirtyObserver(){
    var observer = new MutationObserver(function (event) {
        if( $(".line-loader").hasClass("loading") ){
            if( $(".dirtable.dirtied").length == 0 ){
                $(".line-loader").removeClass("loading")
            }
        }else{
            if( $(".dirtable.dirtied").length > 0 ){
                $(".line-loader").addClass("loading")
            }
        }
    })

    $(".dirtable").each(function(){
        observer.observe(this, {
            attributes: true, 
            attributeFilter: ['class'],
            childList: false, 
            characterData: false
        })
    })
}

function refreshChatbotComponent(){
    Unicorn.call("chatbot","$refresh")
}
function refreshChatbotSettingsComponent(){
    Unicorn.call("chatbot-settings","$refresh")
}