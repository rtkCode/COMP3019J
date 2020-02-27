// this home.js is for home page

// on delete feed link
$(".delete").click(function () {

    // get id hidden in html
    let id=$(this).siblings(".feed-i-id").html();
    let dataSet={"id": id};

    let thisElement=$(this).parent().parent();

    // send a request to rear-end
    $.ajax({
        url: "/deletefeed",
        data: dataSet,
        type: "post",
        dataType: "json",
        success: function (data) {
            // console.log(data); // use this to test

            if(data["code"]==1){
                thisElement.remove(); // remove the element
            }
        },
        error: function () {
            console.log("Network error");
        }
    });

});

// load first feed firstly
let firstLi=$(".feed-list .feed-i-feed-link a i").first();
let firstLink=firstLi.html(); // find first link
loadContent(firstLink);

// load other feed when their link is clicked
$(".feed-list-li-title").click(function () {
    let link=$(this).siblings(".feed-detail").children(".feed-i-feed-link").children("a").children("i").html();
    $("section div").first().empty();
    loadContent(link);
});

// this method is to get feed details from rear-end
function loadContent(feedLink){

    // before data is load, show animation
    $(".loading").show("normal");
    $(".loading-text").show("normal");

    let dataSet={"feed_link": feedLink};

    // sent request to rear-end
    $.ajax({
        url: "/feeddetail",
        data: dataSet,
        type: "post",
        dataType: "json",
        success: function (data) {
            console.log(data);
            if(data["code"]==1) makeContent(data["data"]); // build content
        },
        error: function () {
            console.log("Network error");
        }
    });
}

// build content
function makeContent(data){

    for(let i=0;i<data["entries"].length;i++){

        let feedListI=$("<div class=\"feed-list-i\">");
        let listTitle=$("<h3 class=\"list-title\"></h3>");
        let listTitleA=$("<a></a>");
        listTitleA.text(data["entries"][i]["title"]);

        let listSummary=$("<blockquote class=\"list-summary\"></blockquote>");
        let listSummaryP=$("<p></p>");
        listSummaryP.html(data["entries"][i]["summary"]);


        let listHidden=$("<div class=\"list-hidden\"></div>");
        let listHidden1=$("<div></div>");

        let small1=$("<small></small>");
        small1.text(data["entries"][i]["date"]);

        let small2=$("<small></small>");
        small2.text("Link: ");
        small2.append($("<a href=\""+data["entries"][i]["link"]+"\" target=\"_blank\">"+data["entries"][i]["link"]+"</a>"));

        let listContent=$("<div class=\"list-content\">");
        listContent.html(data["entries"][i]["content"]);

        listHidden1.append(small1);
        listHidden1.append(small2);

        listHidden.append(listHidden1);
        listHidden.append(listContent);

        listTitle.append(listTitleA);
        listSummary.append(listSummaryP);

        feedListI.append(listTitle);
        feedListI.append(listSummary);
        feedListI.append(listHidden);

        $("section div").first().append(feedListI);

        // click feed title to show/hide content
        listTitle.click(function () {
            if(listHidden.is(":hidden")){
                listHidden.show("normal");
                listSummary.hide("normal");
            }else{
                listHidden.hide("normal");
                listSummary.show("normal");
            }
        });

    }

    // after data is load, hide animation
    $(".loading").hide("normal");
    $(".loading-text").hide("normal");

}

// on click hide feed details
$(".top-arrow").click(function () {
    $(this).parent().hide("normal");
});

$(".hide").click(function () {
    $(this).parent().hide("normal");
});