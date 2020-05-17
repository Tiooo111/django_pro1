$(".addHidden").click(function () {

　　if ($(".addShow").css("display") == "none") {

　　　　$(".addShow").css("display", "block");

　　　} else {

　　　　$(".addShow").css("display", "none");

　　}

})
function f1(){
var tab1=document.getElementById("tab1");
tab1.style.display=(tab1.style.display=="none"?"":"none");
}