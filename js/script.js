//siehe https://api.jquery.com/jQuery.post/
//https://api.jquery.com/jquery.ajax/

$(document).ready(function(){
    $("#getSynonyms").submit(function(){
        // Stop form from submitting normally
         event.preventDefault();
		$("#response_head").empty();
		$("#response_body").empty();
		 // Get the values from elements on the page:
        var $form = $(this),
            inputword = $form.find("input[name='w']").val(),
			sprache_wort = $("#sprache_wort").children("option:selected").val(),
            nr = $("#nr").children("option:selected").val(),
			sprache_wordemb = $("#sprache_wordemb").children("option:selected").val(),
            radioValue = $("input[name='searchType']:checked").val();
        $(document).ajaxStart(function(){
			// Adding loading GIF
			$('#animation').html('<img id="loader-img" alt="" src="https://pisys.co/wp-content/uploads/2019/01/Animated-OTS-Logo-Medium.gif" width="130" height="100" align="center" />');
		});
		$(document).ajaxComplete(function(){
			// Wir nehmen die Animation wieder raus
			$('#animation').html(' ');
		});
		jQuery.ajax({
            url: "var/www/cgi-bin/get_synonyms.py",
            type: "POST",
            //contentType: "application/json",
            data: {w: inputword,
				   sprache_wort: sprache_wort,
                   nr: nr,
				   sprache_wordemb: sprache_wordemb,
                   st: radioValue
                   },
            success: function(response){
                console.log(response);
                $("#response_head").empty().append('<br>');
                if (response.syn1 == 'Dieses Wort befindet sich nicht in der Sammlung.'){
                    $("#response_body").append(response.syn1 + '<br><br>');
                }else{
				    if (sprache_wordemb == 'd' && nr == '1') {
					    var content = "Wir haben folgendes Wordembedding für " + inputword + " auf deutsch gefunden: ";
				    }else if (sprache_wordemb == 'd'){
					    var content = "Wir haben folgende " + nr + " Wordembeddings für " + inputword + " auf deutsch gefunden: ";
				    }else if(sprache_wordemb == 'e' && nr == '1'){
					    var content = "Wir haben folgendes Wordembedding für " + inputword + " auf deutsch gefunden: ";
				    }else{
					    var content = "Wir haben folgende " + nr + " Wordembeddings für " + inputword + " auf englisch gefunden: ";
				    }
				    $("#response_head").append(content);
                    var respArr = response.syn1.split(',');
                    for (let el in respArr) {
                        $("#response_body").append(respArr[el] + '<br><br>');
                    }
                 }

                // oder:
                //alt_resp =  "<h4>Synonyme: " + resp + " </h4>";
                //return alt_resp;
            }
            //error: function(xhr, status, error){
            //    console.log(error)
            //}
        });
    });
});