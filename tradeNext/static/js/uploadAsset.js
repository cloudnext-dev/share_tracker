// variable that keeps all the filter information

var send_data = {}

$(document).ready(function () {
    getBrokers();
    getStrategies();
})
function getBrokers() {
    let url = $("#brokers").attr("url");
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {

            brokers_option = "<option value='all' selected>All Brokers</option>";
            $.each(result["brokers"], function (a, b) {
                brokers_option += "<option>" + b + "</option>"
            });
            $("#brokers").html(brokers_option)
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