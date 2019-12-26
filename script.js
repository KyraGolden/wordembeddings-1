//siehe https://api.jquery.com/jQuery.post/
//https://api.jquery.com/jquery.ajax/

$(document).ready(function(){
    $("#getSynonyms").submit(function(){
        //alert("Submitted");i
        // Stop form from submitting normally
         event.preventDefault();
        // Get some values from elements on the page:
        var $form = $(this),
            inputword = $form.find("input[name='s']").val(),
            nr = $form.find("input[name='nr']").val();
        jQuery.ajax({
            url: "var/www/cgi-bin/get_synonyms.py",
            type: "POST",
            //contentType: "application/json",
            data: {s: inputword,
                   nr: nr
                   },
            success: function(response){
                console.log(response);
                //alert(response.syn1);
                var content = nr + " synonyms for ";
                $("#result").empty().append(content);
                $("#result").append(inputword);
                $("#result").append(": <br>");
                $("#result").append(response.syn1);
                // oder:
                //alt_resp =  "<h5>Synonyms: " + resp + " </h5>";
                //return alt_resp;
            }
            //error: function(xhr, status, error){
            //    console.log(error)
            //}
        });
    });
});