
$(document).ready(function() {
    $('#dp1').select2({
        closeOnSelect: false,
        placeholder: "All Regions",

    });

});

regions = []

$("#fetchData").click(function(event){
    event.preventDefault()
    
    getRegionData()
    region = $("#regionData").serialize()
    region+='&Sentiment=0'
    $("#Neu").prop('checked', true);
    $("#numWords").val('10');
    $("#Mentions_count").val('100');
    getWordCloud(region)
    getTopNTerms(region)
    getTopMentions(region)
    getHistogram(region)

})

let plotData = function(res){
    let data = res
    ctr = -2
    for(i of data){
        i.type = "bar"
        // i.type =  "scatter",
        // i.mode =  "lines",
        console.log(i)
    }

    var layout = {
        
        title: 'Tweets over time',
        xaxis: {
            //autorange: true,
            range: ['2020-01-01', '2020-12-31'],
            rangeselector: {buttons: [
                {
                count: 1,
                label: '1m',
                step: 'month',
                stepmode: 'backward'
                },
                {
                count: 6,
                label: '6m',
                step: 'month',
                stepmode: 'backward'
                },
                {step: 'all'}
            ]},
            rangeslider: {range: ['2020-01-01', '2020-12-31']},
            type: 'date'
        },
        
          
        // barmode: 'stack'
        barmode: 'group'
    };
    //console.log(data)
    Plotly.newPlot("TimeGraph", data,layout)
}

$('input[name="barmode"]').on('click change',function(){
    if(this.value == 'line'){
        var update = {
            type:'scatter',
            mode:'lines'
        }
        Plotly.restyle("TimeGraph",update)
    }
    else{
        // var update_type = {type:[['bar'],['bar'],['bar'],['bar'],['bar']]}
        var update = {
            type:'bar',
            
        }
        var layout = {
            barmode : this.value
        }
        Plotly.update("TimeGraph",update,layout)
        
    }
    
})

$('input[name="Sentiment_h"]').on('click change',function(){
    region = $("#regionData").serialize()
    region = region + '&Sentiment=' + this.value
    console.log("***Region")
    console.log(region)
    getHistogram(region)

    
})

$('input[name="Sentiment"]').on('click change',function(){
    region = $("#regionData").serialize()
    region = region + '&Sentiment=' + this.value
    console.log("***Region")
    console.log(region)
    $("#numWords").val('10');
    getWordCloud(region)
    getTopNTerms(region)

    
})

$('select[name="numWords"]').on('click change',function(){
    region = $("#regionData").serialize()
    sentiment = $('input[name="Sentiment"]:checked').val()
    region = region + '&Sentiment=' + sentiment
    numWords = this.value
    region = region + "&numWords=" + numWords
    console.log("***Region")
    console.log(region)
    getTopNTerms(region)

    
})


$('select[name="Mentions_count"]').on('click change',function(){
    region = $("#regionData").serialize()
    
    numMentions = this.value
    region = region + "&Mentions_count=" + numMentions
    console.log("***Region")
    console.log(region)
    getTopMentions(region)

    
})


getRegionData = function(){
    regions = $("#regionData").serialize()
    $.ajax({
        type: 'POST',
        url:'http://127.0.0.1:8000/getRegionData',
        data: regions,
        success: function(res){
            plotData(res)
        },
        error(res){
            console.log("Error")
            console.log(res)
        }
    })
    $("#grouped-bar").prop('checked', true);
}

getWordCloud = function(region){

    $.ajax({
        type:'POST',
        data: region,
        url:'http://127.0.0.1:8000/getWordCloud',
        success:function(res){
            $('#WordCloud>img').prop("src", res._link)
        },
        error(res){
            console.log("Error")
            console.log(res)
        }
    })

}

getTopNTerms = function(region){
    $.ajax({
        type:'POST',
        data: region,
        url:'http://127.0.0.1:8000/getWordFrequencies',
        success:function(res){
            var data = [{
                type: 'bar',
                x: res.x,
                y: res.y,
                
              }];
              
              Plotly.newPlot('word_frequency', data);
        },
        error(res){
            console.log("Error")
            console.log(res)
        }
    })
}

getTopMentions = function(region){
    $.ajax({
        type:'POST',
        data: region,
        url:'http://127.0.0.1:8000/getTopMentions',
        success:function(res){
            var data = [{
                type: 'bar',
                x: res.x,
                y: res.y,
                orientation:'h'
              }];

            var layout = {
                autosize: false,
                width: 1500,
                height: 700,
            }


              
              Plotly.newPlot('mentions_frequency', data,layout);
        },
        error(res){
            console.log("Error")
            console.log(res)
        }
    })
}

getHistogram = function(region){
    $.ajax({
        type:'POST',
        data: region,
        url:'http://127.0.0.1:8000/getHistograms',
        success:function(res){
            var trace = {
                x: res.tweet_lengths,
                type: 'histogram',
                histnorm: 'probability density'
              };
            var data = [trace];
            var layout = {
                bargap: 0.00000005, 
                
            };
            Plotly.newPlot('tweet_length_histograms', data,layout);
        },
        error(res){
            console.log("Error")
            console.log(res)
        }
    })
}


$(() => {
    getRegionData()
    getWordCloud({})
    getTopNTerms()
    getTopMentions()
    getHistogram()
})


