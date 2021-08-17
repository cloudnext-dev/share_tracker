// variable that keeps all the filter information

var send_data = {}

$(document).ready(function () {
    resetFilters();
    getAPIData();
    getSectors();
    getIndustries();
    
    $('#sectors').on('change', function () {
        if(this.value == "all")
            send_data['sector'] = "";
        else
            send_data['sector'] = this.value;

        if($('#industries :selected').text() == "All Industries")
            send_data['industry'] = "";
        else
            send_data['industry'] = $('#industries :selected').text();

        getAPIData();
    });

    $('#industries').on('change', function () {
        // get the api data of updated variety
        if($('#sectors :selected').text() == "All Sectors")
            send_data['sector'] = "";
        else
            send_data['sector'] = $('#sectors :selected').text();

        if(this.value == "all")
            send_data['industry'] = "";
        else
            send_data['industry'] = this.value;
        getAPIData();
    });

    $("#display_all").click(function(){
        resetFilters();
        getAPIData();
    });

    $("#refresh_stocks").click(function(){
        refreshStocks();
    })
})


/**
    Function that resets all the filters   
*/
function resetFilters() {
    $("#sectors").val("all");
    $("#industries").val("all");
    send_data['sector'] = '';
    send_data['industry'] = '';
}

function putTableData(result) {
    // creating table row for each result and

    // pushing to the html cntent of table body of listing table

    let row = ''
    if(result.length > 0){
        $("#no_results").hide();
        $("#list_data").show();
        $("#listing").html("");  
        $.each(result, function (a, b) {
            row = "<tr> <td>" + b.AssetId + "</td>" +
            "<td>" + b.AccountId + "</td>" +
            "<td >" + b.StrategyId + "</td>" +
                "<td>" + b.EntryPrice.toFixed(2) + "</td>" +
                "<td>" + b.CurrentMarketPrice.toFixed(2) + "</td>" +
                "<td>" + b.EntryPriceDiff.toFixed(2) + "</td>" +
                "<td>" + b.AvgEntryPoint1.toFixed(2) + "</td>" +
                "<td>" + b.Avg1Diff.toFixed(2) + "</td>" +
                "<td>" + b.AvgEntryPoint2.toFixed(2) + "</td>" +
                "<td>" + b.Avg1Diff.toFixed(2) + "</td>" +
                "<td>" + b.Quantity + "</td>" +
                "<td>" + b.TargetPrice.toFixed(2) + "</td>" +
                "<td>" + b.Sector + "</td>" +
                "<td>" + b.Industry + "</td>" +
                "<td>" + b.Beta + "</td>" +
                "<td>" + b.NextEarningDate + "</td>" +
                "<td>" + b.LastUpdatedOn + "</td></tr>"
            $("#listing").append(row);   
        });
    }
    else{
        // if no result found for the given filter, then display no result

        $("#no_results h5").html("No results found");
        $("#list_data").hide();
        $("#no_results").show();
    }
}

function getAPIData() {
    let url = $('#list_data').attr("url")
    $.ajax({
        method: 'GET',
        url: url,
        data: send_data,
        beforeSend: function(){
            $("#no_results h5").html("Loading data...");
        },
        success: function (result) {
            putTableData(result);
        },
        error: function (response) {
            $("#no_results h5").html("Something went wrong");
            $("#list_data").hide();
        }
    });
}

function getSectors() {
    let url = $("#sectors").attr("url");
    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {

            sectors_option = "<option value='all' selected>All Sectors</option>";
            $.each(result["sectors"], function (a, b) {
                sectors_option += "<option>" + b + "</option>"
            });
            $("#sectors").html(sectors_option)
        },
        error: function(response){
            console.log(response)
        }
    });
}

function getIndustries() {
    let url = $("#industries").attr("url");

    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
            industry_options = "<option value='all' selected>All Industries</option>";
            $.each(result["industries"], function (a, b) {
                industry_options += "<option>" + b + "</option>"
            });
            $("#industries").html(industry_options)
        },
        error: function(response){
            console.log(response)
        }
    });
}

function refreshStocks() {
    let url = '/tradeNext/ajax/refreshStocks/'

    $.ajax({
        method: 'GET',
        url: url,
        data: {},
        success: function (result) {
            if(result.status == true){
                setTimeout(function(){
                    location.reload(); 
                }, 3000); 
            }
        },
        error: function(response){
            console.log(response)
        }
    });
}