

$("#submit").click(function(event){
    console.log("YESS")
    $("#details").remove()
    event.preventDefault()
    $.ajax({
        type: 'GET',
        url:'http://127.0.0.1:8000/info',
        data: $("#regionData").serialize(),
        success: function(res){
            $('main').append(res)
        },
        error(res){
            console.log(res)
        }
    }
    )
})