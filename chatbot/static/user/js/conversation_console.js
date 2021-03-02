function conversationConsole(){
    return {
        stories:[],
        transmit:{
            from:null,
            lift:false   
        },
        cached:"",
        isDirty(){
            return this.cached.replaceAll('\"','\\\"') != this.setCorpus();
        },
        addCategory(i){
            this.stories[i].categories.push("Category");
        },
        removeCategory(i,j){
            this.stories[i].categories.splice(j,1);
        },
        addConversation(e,i,k){
            if(k != null){
                this.stories[i].conversations.splice(k,0,{"statements":["Statement"],"responses":["Response"]});
            }else{
                this.stories[i].conversations.push({"statements":["Statement"],"responses":["Response"]});
            }
            this.notifyNiceScroll(e);
        },
        removeConversation(e,i,k){
            this.stories[i].conversations.splice(k,1);
            this.notifyNiceScroll(e);
        },
        cloneConversation(e,i,k){
            this.stories[i].conversations.splice(k+1,0,this.stories[i].conversations[k]);
            this.notifyNiceScroll(e);
        },
        moveConversation(i,k){
            this.transmit.from=[i,k];
            this.transmit.lift=true;
        },
        placeConversation(i,k){
            if(this.transmit.lift && this.transmit.from!=null){
                let con = this.stories[this.transmit.from[0]].conversations[this.transmit.from[1]];
                if(k != null){
                    this.stories[i].conversations.splice(k,0,con);
                }else{
                    this.stories[i].conversations.push(con);
                }
                this.stories[this.transmit.from[0]].conversations.splice(this.transmit.from[1],1);
                this.cancelTransmit();
            }
            this.notifyNiceScroll(null,true);
        },
        cancelTransmit(){
            this.transmit.from=null;
            this.transmit.lift=false;
        },
        notifyNiceScroll(e,bool){
            if(e==null){
                setTimeout(()=>{
                    $(".stories").getNiceScroll().resize();
                    if(bool){
                        $(".story").getNiceScroll().resize();
                    }
                },1000);
            }
            else{
                setTimeout(()=>{
                    $(e.target).parents(".story").getNiceScroll().resize();
                },1000);
            }
            
            $('[data-toggle="tooltip"]').tooltip('dispose');
            $('[data-toggle="tooltip"]').tooltip();
        },
        addStory(){
            this.stories.push({name:"Story "+(this.stories.length+1),categories:["Category"],conversations:[{"statements":["Statement"],"responses":["Response"]}]});
            setTimeout(()=>{$(".story").niceScroll(".scroll-wrapper");},100)
            this.notifyNiceScroll()
        },
        removeStory(i){
            this.stories.splice(i,1);
            this.notifyNiceScroll()
        },
        addStatement(e,i,k){
            this.stories[i].conversations[k].statements.push("Statement");
            this.notifyNiceScroll(e);
        },
        removeStatement(e,i,k,l){
            this.stories[i].conversations[k].statements.splice(l,1);
            this.notifyNiceScroll(e);
        },
        addResponse(e,i,k){
            this.stories[i].conversations[k].responses.push("Response");
            this.notifyNiceScroll(e);
        },
        removeResponse(e,i,k,m){
            this.stories[i].conversations[k].responses.splice(m,1);
            this.notifyNiceScroll(e);
        },
        setCorpus(){
            return JSON.stringify(this.stories).replaceAll('\"','\\\"');
        }
    }
}

function textareaResize(el){
    $(el).height(5);$(el).height($(el).prop('scrollHeight'));
}  

$(function(){
    $(window).on('load', function() {
        $('.conversation textarea').each(function(_,e){textareaResize(e)});
    });
});

function successToast(title,message){
    iziToast.success({
        title: title,
        message: message,
        position: 'topRight'
    });
}
function refreshConsole(corpus){
    document.querySelector('[x-data]').__x.$data.cached=corpus;
    document.querySelector('[x-data]').__x.$data.$refresh();
}