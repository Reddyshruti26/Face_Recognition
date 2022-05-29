$("#signUpButton").on('click', function (e) {
    e.preventDefault();
    console.log("Button", $('#signUpButton'))
    const data = {
        name: $('#name').val(),
        email: $('#email').val(),
        password: $('#password').val()
    };
    console.log("Data", data)

    $.ajax({
        url: "/signup",
        type: "POST",
        data: data,
        dataType: "json"
    }).done(function (data) {
        console.log("success")
        location.href = "/image";
    }).fail(function (data) {
        alert("Signup Failed! Email already exist");
        location.href = "/";
    })
});

$("#loginButton").on('click', function (e) {
    e.preventDefault();
    console.log("Button", $('#loginButton'))
    const data = {
        email: $('#email').val(),
        password: $('#password').val()
    };
    console.log("Data", data)

    $.ajax({
        url: "/login",
        type: "POST",
        data: data,
        dataType: "json"
    }).done(function (data) {
        console.log("success: ", data);
        location.href = "/dashboard";
    }).fail(function (data) {
        alert("Wrong Credentials");
        location.href = "/";
    })
});
$("#image").on("click", function (e) {
    console.log("button")
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: "/image",
        success: function (result) {
            window.location.href = "/dashboard";
        },
        error: function (result) {
            alert('error');
        }
    });
});
$("#qr").on("click", function (e) {
    console.log("button")
    e.preventDefault();
    alert("QR scan will open up shortly")
    $.ajax({
        type: "POST",
        url: "/capture",
        success: function (result) {

            window.location.href = "/details";
        },
        error: function (result) {
            alert('error');
        }
    })
});
$("#accountsub").on("click", function (e) {
    console.log("button")
    e.preventDefault();
    var account = $("#account").val();
    $.ajax({
        type: "POST",
        url: "/data",
        data: account,
        dataType: "html",
        success: function (result) {
            window.location.href = "/details";
        },
        error: function (result) {
            alert('error');
        }
    });
});
$("#phonesub").on("click", function (e) {
    console.log("button")
    e.preventDefault();
    var phone = $("#phone").val();
    $.ajax({
        type: "POST",
        url: "/data",
        data: phone,
        dataType: "html",
        success: function (result) {
            location.href = "/details";
        },
        error: function (result) {
            alert('error');
        }
    });
});
$("#paysub").on("click", function (e) {
    console.log("button")
    e.preventDefault();
    var pay = $("#pay").val();
    alert("Face verification will start shortly.")
    $.ajax({
        type: "POST",
        url: "/compare",
        data: pay,
        dataType: "html",
        success: function (result) {
            alert('Face verified');
            window.location.href = "/payment";
        },
        error: function (result) {
            alert('Face not Verified');
            window.location.href = "/failedpayment";
        }
    });
});

$(".payBill").on("click", function (e) {
    console.log("button clicked")
    window.location.href = "/bill";
});
$("#bill-button").on("click", function (e) {
    console.log("button")
    e.preventDefault();
    var bill = $("#bill").val();
    $.ajax({
        type: "POST",
        url: "/data",
        data: bill,
        dataType: "html",
        success: function (result) {
            location.href = "/details";
        },
        error: function (result) {
            alert('error');
        }
    });
});

