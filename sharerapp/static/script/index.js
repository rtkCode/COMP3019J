// this index.js is for index page

// the animation to show/hide feed content & summary
$(".list-title").click(function () {
    if($(this).siblings(".list-hidden").is(":hidden")){
        $(this).siblings(".list-summary").hide("normal");
        $(this).siblings(".list-hidden").show("normal");
    }else{
        $(this).siblings(".list-summary").show("normal");
        $(this).siblings(".list-hidden").hide("normal");
    }
});

// the animation to show/hide feed details
$(".feed-list-li-title").click(function () {
    if($(this).siblings(".feed-detail").is(":hidden")){
        $(this).siblings(".feed-detail").show("normal");
    }else{
        $(this).siblings(".feed-detail").hide("normal");
    }
});

// the animation of right-top arrow, to show/hide logout
$(".left-arrow").click(function () {
    if($(".logout").is(":hidden")){
        $(".logout").css("display","inline");
        $(this).css("transform","rotate(135deg)");
    }else{
        $(".logout").css("display","none");
        $(this).css("transform","rotate(-45deg)");
    }
});

// use regex to check url
function checkUrl(url){
    let regex=/^(http(s?):\/\/)/;
    if(regex.test(url)){ // if true hide error hint
        $(".error-url").hide("normal");
        console.log("url format true");
    }else{// if false show hint
        $(".error-url").show("normal");
        console.log("url format false");
    }
}

// when click submit check url
$("#submit").click(function () {
   checkUrl($("#link").val());
});