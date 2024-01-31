
  function colset(){
                 if ("{{ qry.third_term }}" == '1st Term'){
		if ("{{ qry.second_term }}" == '2nd Term'){
			document.getElementById("tena").colSpan = "9";
			document.getElementById("tenb").colSpan = '9';
			document.getElementById("fifteen").colSpan = '14';}
                else{
			document.getElementById("tena").colSpan = "8";
			document.getElementById("tenb").colSpan = '8';
			document.getElementById("fifteen").colSpan = '13';}
}};
                colset();
        function edith(i){
	$(".raw_"+""+i).hide(); 
	$(".edith_"+""+i).show();
        $("#show_ed"+""+i).hide();
        $("#show_sa"+""+i).show();
	
}

        function save(i){
	  var test = $("#edith_test_"+""+i).val();
	  var agn = $("#edith_agn_"+""+i).val();
	  var atd = $("#edith_atd_"+""+i).val();
	  var exam = $("#edith_exam_"+""+i).val();
            $("#total_0").html(eval([Number(test), Number(atd), Number(agn)].join('+')));
           $("#fagr_0").html(eval([Number(test), Number(atd), Number(agn), Number(exam)].join('+')));
	  var request  = $.ajax({
 	  url: "{% url 'responsive_updates' pk=0 %}",
	  data: {
        'flow':'fromHtml', 'tutor_id':"{{ qry.id }}", 'id':'none', 'sn':""+i, 
        'student_id': 'XX/S/19/'+$("#edith_name_id_"+""+i).val(),
        'student_name': "AMINU ISMAIL",
        'test': Number(test),
	 	    'agn': Number(agn),
	 	    'atd': Number(atd), 
	 	    'total': eval([Number(test), Number(atd), Number(agn)].join('+')),
	 	    'exam': Number(exam),
	 	    'agr': eval([Number(test), Number(atd), Number(agn), Number(exam)].join('+')),
	 	    'grade': 'D7', 
	 	    'posi': 'th'
	 	    },
	 dataType: 'json',
	 
	});
	 request.done(function(data) {
          $("#id_"+""+i).html(data.id);
            $("#id_"+""+i).css('color', '#670A53');
     });
      request.fail(function( jqXHR, textStatus) {
          alert(textStatus)
	});
 
}

        var grades = dim.reduce(function(prev, cur){prev[cur] = (prev[cur] || 0) + 1; return prev;},{});
          $("#A").html(grades.A);$("#C").html(grades.C);$("#P").html(grades.P);$("#F").html(grades.F);
          $("#F9").html(grades.F9);$("#E8").html(grades.E8);$("#D7").html(grades.D7);$("#C6").html(grades.C6);$("#C5").html(grades.C5);$("#C4").html(grades.C4);$("#B3").html(grades.B3);$("#B2").html(grades.B2);$("#A1").html(grades.A1);
          $(".oneBox").show();
          function showOnly(x){$("."+x).hide();$(".oneBox").toggle();};
          if ("{{qry.Class}}"[0] == 'J'){
            $("#Junior").show()
          }
          else{
            $("#Senior").show()
          }
          {% block scripts %}
          <script src="{{ STATIC_URL }}/static/result/js/desktops.js"></script>
        {% endblock %}