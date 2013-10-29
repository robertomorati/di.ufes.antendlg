<link rel="stylesheet" href="http://code.jquery.com/ui/1.10.3/themes/smoothness/jquery-ui.css" />
<script src="http://code.jquery.com/jquery-1.9.1.js"></script>
<script src="http://code.jquery.com/ui/1.10.3/jquery-ui.js"></script>
<link rel="stylesheet" href="/resources/demos/style.css" />


function popitup(url) {
    newwindow=window.open(url,'{{title}}','height=200,width=150');
    if (window.focus) {newwindow.focus()}
    return false;
}

$(function() {
    $( "#dialog-confirm" ).dialog({
      resizable: false,
      height:140,
      modal: true,
      buttons: {
        "Deletar": function() {
          $post({
        	  url: tipo_objeto_delete_view object.pk
          }
        },
        Cancel: function() {
          $( this ).dialog( "close" );
        }
      }
    });
  });