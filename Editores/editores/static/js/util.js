/**
 * Created on 27/09/2013
 * 
 * @author: Roberto Guimaraes Morati Junior
 */

	var id_tipos;//variavel utilizada para armazenar tipos de objetos (id), para montar a Biblioteca de Objetos qndo a página carregar pela primeira vez.


	/**
	 * Abre modal para criar ou atualizar "coisas" por meio da url
	 * @param url - página a ser carrega
	 * @param idDiv - div para onde será carregada a modal
	 */
	function openModal(url,idDiv) {
		$.get(url, function( data ) {
			$("#"+idDiv).html(data);
		});
	};

	/**
	 * Atualiza o conteudo da div.
	 * @param urlView - urlView a ser atualizada
	 * @param idDiv - div a ser atualizada
	 */
	function refreshDiv(urlView,idDiv) {
		$.ajax({
			  url: urlView,
			  cache: false,
			  success: function() {
				 $('#'+idDiv).load(urlView);
			  },
			  error: function() { alert("Erro ao atualizar dados...Xiiii ;)"); }
			});
	}
	
	 /**
	  * Função para criar o menu de acordo com os tipos de objetos existentes
	  * 
	  * @param urlView - url para carregar os tipos de objetos, por meio de json
	  */
	 var flag = 0;
	 function addTabs(urlView) {

		 $.ajax({
		        type: 'GET',
		        url: urlView,
		        cache: false,
		        async: false,
		        success: function(response) {
		        	var obj = $.parseJSON(response);
			        //recuperando tipo e id e montando o menu
		        	for (i=0;i<obj.length;i++){
		        		//adiciona os primeitos tipos
			    		if(i < 2){	//trabalhar de acordo com a largura da tela...maybe hahaha!
			    			$('#objetoTab').append(
			    			// id="tipo' + obj[i].fields.tipo + '" class="panel-info"
			    			$('<li id="loadObjetos' + obj[i].fields.tipo + '"><a href="#tipo' + obj[i].fields.tipo + '" data-toggle="tab">' + obj[i].fields.tipo + '</a></li>'));
			    			$('#tipo' + obj[i].fields.tipo).tab('show');
			    			
			    	    }else{
			    	    	//adiciona nome para o dropdown
			    	    	if(flag == 0){		  
			    	    		$('#objetoTab')
			    				.append(
			    						$(  "<li id='outrosObjetos' class='dropdown' >" +
			    							    "<a class='dropdown-toggle' data-toggle='dropdown' href=''>" +
			    								"  Outros <span class='caret'></span>" +
			    								"</a> <ul id='outros' class='dropdown-menu'>" +
			    								"</ul> </li>"));
			    		        $('#objetosOutros').tab('show');
			    	    	}//fim do if
			    	    	flag = 1;
			    	    	//adiciona os outros tipos de objetos
			    	    	$('#outros').append(
			    	    			//id="tipo' + obj[i].fields.tipo + '"
			    	    			$('<li id="loadObjetos' + obj[i].fields.tipo + '""><a href="#tipo' + obj[i].fields.tipo + '" data-toggle="tab">' + obj[i].fields.tipo + '</a></li>'));
			    	    			$('#tipo' + obj[i].fields.tipo).tab('show');
			    		}//fim do else
			    				
			    		//local para alocar os objetos
			    		buildTabContent(obj[i].pk,obj[i].fields.tipo);
		        	}

		        },
		        error: function() {
		        	alert("Erro ao recuperar tipos de objetos...Xiiii ;)");
		        }
		});
	 }
	

	 /**
	  * Constroi as divs para carregar os objetos
	  * @param idTipo
	  * @param tabTipoObbjeto
	  */
	 function buildTabContent(idTipo, tabTipoObbjeto) {
		
 		$('#pageTabContent').append(
 		        $('<div class="tab-pane row-fluid show-grid" id="tipo' + tabTipoObbjeto  + '">' + 
 		        	"<script type='text/javascript'> " +
 		        		'$("#loadObjetos' + tabTipoObbjeto + '").on("click", "a", function(e) { ' + 
 		        		" getObjetos(" + idTipo +"," + "'"+ tabTipoObbjeto + "'"+ "); " + 
 		        		" });" +
 		        	"</script>"+
 		        "</div>"));
 		 //getObjetos(idTipo,tabTipoObbjeto);
	 }
	 //" getObjetos(" + idTipo + "','" + tabTipoObbjeto + ");" + 
	 
	 /**
	  * Recupera objetos de acordo com o tipo
	  * @param idTipo - tipo do objeto
	  * @param tipoObjeto - nome do tipo do objeto
	  */
	 function getObjetos(idTipo,tipoObjeto){
		 //alert(idTipo + tipoObjeto);
		 var urlView = '/editor_objetos/objeto/get_lista_objetos/';
		 urlView += idTipo + '/'; //concatena url com tipo de objeto
		 
		 $.getJSON(
				    urlView, 
					function(data){	
				    	//data is empty, do something
					    if(data == ""){
					    	jQuery('div#tipo'+tipoObjeto).html('');
					    	$('#tipo'+tipoObjeto).append(
					    			'<p class="text-info">' + 'Não existem objetos do tipo ' +
									 tipoObjeto + '</p>');
					    	
					    //data no empty, load objects
					    }else{
					    	//limpa div para atualizar com novos objetos
					    	 jQuery('div#tipo'+tipoObjeto).html('');
					
							for (i=0;i<data.length;i++){	
								
								//temporario, devido ao callback do getJson e problemas com retorno de valor pelo callback
								//temporario se tornou utilizado :)
								getUrlIcone(tipoObjeto,data, i);	
							}	
					    }
					    
					}).error(function( data, textStatus, jqXHR ){ /* assign handler */
						alert("Erro ao recuperar objetos...Xiiii ;)");
			        });
	 }
	 
	 
	 /***
		* 1 - the offset of the map also must be used inside the calculation(when the map is not placed at the top left corner of the page)
		* 2 - the anchor of the marker by default is the bottom-center , but the script simply takes the position provided via the event-argument, 
		*      what may give different results, depending on the point inside the image where you grip it.
		*
		*     Função que permite o objeto ser "draggable".
		*/
		function draggableObjeto() {
			//alert("uia");
			$(".draggable_objeto").draggable({helper: 'clone',
				iframeFix: true,
				stop: function(e,ui) {
				    var mOffset=$($map.getDiv()).offset();
				    
					var scale = $map.getZoom();
				    var point=new google.maps.Point(
				        ui.offset.left-mOffset.left+(ui.helper.width()/scale),
				        ui.offset.top-mOffset.top+(ui.helper.height())
				    );									
				    
				    var loc=overlay.getProjection().fromContainerPixelToLatLng(point);
					var icon = $(this).attr('src');//jQuery(this).find('img').attr('src');
					var id = $(this).attr('id');
					var name_objeto = $(this).attr('alt');

					placeMarker(loc,icon, id, name_objeto);
				}
			
			});	

		}
		
	 /**
	  * Recupera a url do icone
	  * 
	  * @param dadosObjeto - todos dados do objeto
	  * @param i - position
	  * @param tipoObjeto - nome do tipo de objeto
	  */
	 function getUrlIcone(tipoObjeto,dadosObjeto,i){
		 var urlView = '/editor_objetos/get_url_icone/';
		 urlView += dadosObjeto[i].fields.icone_objeto; //concatena url com tipo de objeto
		 $.getJSON(
				    urlView, 
					function(data){	
				    	
				    	$('#tipo'+tipoObjeto).append( 
				    			//div com o id do objeto...		não é possivel utilizar span2		    			
				    	      '<img  class="draggable_objeto objeto img-circle" id="'+ dadosObjeto[i].pk + 
				    	      '" src="/media/' + data[0].fields.icone + '" alt="'+ dadosObjeto[i].fields.nome  +
				    	      '" title="' + dadosObjeto[i].fields.nome + '" dialogo="' + dadosObjeto[i].fields.dialogo +  
				    	      '" data-toggle="tooltip"/>');
				    	
				    		   draggableObjeto();//add drag ao objeto
				 
					}).error(function( data, textStatus, jqXHR ){ /* assign handler */
						alert("Erro ao recuperar objetos...Xiiii ;)");
			        });
		
	 }
	 
	 /**
	  * Recupera avatar do autor
	  * 
	  * @param id do autor
	  */
	 function getAvatar(idUser){
		 var urlView = '/autor/get_url_icone/';
		 urlView += idUser; //concatena url com o id do autor
		
		 $.getJSON(
				    urlView, 
					function(data){	

					   $("#autor_avatar").append( 		
					    	      '<img  class="img-rounded" id="'+ idUser + 
					    	      '"style="width: 50px; height: 50px;" src="/media/' + data[0].fields.icone_autor + '" alt="Avatar'+
					    	      '" />');
	   
					}).error(function( data, textStatus, jqXHR ){ /* assign handler */
						alert("Erro ao recuperar avatar do autor...Xiiii ;)");
			        });
	 }
	 
	 
/*=========================================================================================================================
 |  							    		Rascunhos												         			  |
 ==========================================================================================================================/
 /*
  * 
  * '<div  class="span2" id="' + dadosObjeto[i].pk +  '" data-toggle="tooltip" title="'+ dadosObjeto[i].fields.nome + '"> ' +
								'<img  id="draggable_objeto" class="img-circle" src="/media/' + data[0].fields.icone + '" alt="'+ dadosObjeto[i].fields.nome  +'"/>'
								 +
								'</div>');
  */
 	/* function addContentTab(urlView, tabTipoObbjeto) {
			
		 //getObjetos(urlView);
		 //var teste = getUrlIcone('{% url icon_get_json_url_view 1 %}');
 		$('#pageTabContent').append(
 		        $('<div class="tab-pane" id="tipo' + tabTipoObbjeto  + '">' + teste +
 		        		"</div>"));

	 }*/
	
	 function teste(urlView) {
	     //alert(urlView);
		$.getJSON(urlView, function(result) {
			return result;
		});
 }
	 
		  
 /**
	 * Remove a Tab
	 */
 $('#objetoTab').on('click', ' li a .close', function() {
 var tabId = $(this).parents('li').children('a').attr('href');
 $(this).parents('li').remove('li');	
 });

/**
 * Ativação de nav-tabs;
 * @param tab a ser ativada
 */
function activaTab(tab){
   $('.nav-tabs a[href="#' + tab + '"]').tab('show');
}

/**
 * Recuperar a "url" de um icone
 * 
 * @param urlView - urlView com id do icone

function getUrlIcone(urlView){
	 $.ajax({
	        type: 'GET',
	        url: urlView,
	        cache: false,
	        success: function(data,textStatus,jqXHR) {
	        	
	        	alert("response " + data);
	        	//var obj = $.parseJSON(response);
	        	//alert("response " + obj);
	        },
	        error: function() {
	        	alert("Erro ao recuperar tipos de objetos...Xiiii ;)");
	        }
	});
} */