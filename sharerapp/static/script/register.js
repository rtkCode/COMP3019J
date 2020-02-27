// this register.js is for register page
// here is a bug in firefox: focus event has to happened before blur, the solution is setTimeout, the method is learned from https://blog.csdn.net/weixin_30438813/article/details/95036694

// username on blur check
$("#username").blur(function () {
    checkAvailable("username");
});

// email on blur check
$("#email").blur(function () {
    checkAvailable("email");
    checkEmailFormat($("#email").val());
});

// password on blur check match
$("#password2").blur(function () {
    if($(this).val()!=$("#password").val()){ // if not match show hint
        $(".error-password").show("normal");
        window.setTimeout(function () { // see top of the register.js
           $("#password2").focus(); // focus input field
        });
    }
    else if($(this).val()==$("#password").val()) $(".error-password").hide("normal"); // if match hide hint
});

// check username or email is exist in database
function checkAvailable(input) {
    console.log("checking "+input+"..."); // test
    let dataSet={"username": "", "email": ""};

    if(input=="username"){
        let inputValue=$("#username").val(); // get username
        dataSet[input]=inputValue;
    }else if(input=="email"){
        let inputValue=$("#email").val(); // get e-mail
        dataSet[input]=inputValue;
    }

    $.ajax({
        url: "/checkavailable",
        data: dataSet,
        type: "post",
        dataType: "json",
        success: function (data) {
            // console.log(data["ucode"]);
            if(data["ucode"]!=undefined){
                if(data["ucode"]=="1"){
                    $(".error-user").show("normal"); // if exist show hint
                    $("#username").focus();
                }
                else if(data["ucode"]=="0") $(".error-user").hide("normal");
            }

            if(data["ecode"]!=undefined){
                if(data["ecode"]=="1"){
                    $(".error-email").show("normal"); // if exist show hint
                    $("#email").focus();
                }
                else if(data["ecode"]=="0") $(".error-email").hide("normal");
            }
        },
        error: function () {
            console.log("Network error");
        }
    });
}

// check e-mail format
function checkEmailFormat(val){
    let regex=/^[a-zA-Z0-9\_\-\!\#\$\%\&\'\*\+\-\=\?\^\_\`\{\|\}\~\.]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
    if(regex.test(val)){
        $(".error-email-format").hide("normal");
        console.log("email format true");
    }
    else{
        $(".error-email-format").show("normal");
        window.setTimeout(function () { // see top of the register.js
           $("#email").focus();
        });
        console.log("email format false");
    }
}