// variable that keeps all the filter information

var send_data = {}

$(document).ready(function () {
    getAccounts();
    getStrategies();
})
function getAccounts() {
    let url = $("#accounts").attr("url");
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {

            accounts_option = "<option value='all' selected>All Accounts</option>";
            $.each(result["accounts"], function (a, b) {
                accounts_option += "<option>" + b + "</option>"
            });
            $("#accounts").html(accounts_option)
        },
        error: function(response){
            console.log(response)
        }
    });
}

function getStrategies() {
    let url = $("#strategies").attr("url");

    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
            strategy_options = "<option value='all' selected>All Strategies</option>";
            $.each(result["strategies"], function (a, b) {
                strategy_options += "<option>" + b + "</option>"
            });
            $("#strategies").html(strategy_options)
        },
        error: function(response){
            console.log(response)
        }
    });
}