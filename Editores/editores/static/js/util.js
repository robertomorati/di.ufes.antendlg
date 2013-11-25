/**
 * Created on 27/09/2013
 * 
 * @author: Roberto Guimaraes Morati Junior
 */

/**
 * Open a modal to create things.
 * 
 * @param url - page to load
 * @param idDiv - div  in which the modal will be loaded.
 */
function openModal(url,idDiv) {
	$.get(url, function( data ) {
		$("#"+idDiv).html(data);
	});
};


/**
 * Update the content of a div.
 * 
 * @param urlView - url with content
 * @param idDiv - div will be update
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
  * @param urlView - url para carregar os tipos de objetos
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
		        //Recupera tipo e id para montar o menu
	        	for (i=0;i<obj.length;i++){
	        		
	        		//adiciona primeiros tipos.
		    		if(i < 2){	//é interessante trabalhar com a largura da tela.
		    			//create the menu with two types
		    			$('#objetoTab').append(
		    			$('<li id="loadObjetos' + obj[i].fields.tipo + '"><a href="#tipo' + obj[i].fields.tipo + '" data-toggle="tab">' + obj[i].fields.tipo + '</a></li>'));
		    			$('#tipo' + obj[i].fields.tipo).tab('show');
		    			
		    	    }else{
		    	    	//cria a tab outrosObjetos para adicionar os outros tipos
		    	    	if(flag == 0){		  
		    	    		$('#objetoTab')
		    				.append(
		    						$(  "<li id='outrosObjetos' class='dropdown' >" +
		    							    "<a class='dropdown-toggle' data-toggle='dropdown' href=''>" +
		    								"  Outros <span class='caret'></span>" +
		    								"</a> <ul id='outros' class='dropdown-menu'>" +
		    								"</ul> </li>"));
		    		        $('#objetosOutros').tab('show');
		    	    	}
		    	    	
		    	    	flag = 1;//impede a criação de outras  tabs - outrosObjetos
		    	    	
		    	    	//adiciona os tipos de objetos
		    	    	$('#outros').append(
		    	    			//id="tipo' + obj[i].fields.tipo + '"
		    	    			$('<li id="loadObjetos' + obj[i].fields.tipo + '""><a href="#tipo' + obj[i].fields.tipo + '" data-toggle="tab">' + obj[i].fields.tipo + '</a></li>'));
		    	    			$('#tipo' + obj[i].fields.tipo).tab('show');
		    		
		    	    }//end else
		    				
		    		//construção do "espaço para alocar os tipos de objetos"
		    		buildTabContent(obj[i].pk,obj[i].fields.tipo);
	        	}
	        	flag = 0;//flag recebe 0, pois o autor pode criar novos tipos, assim, sendo necessário atualizar a estrutura da "biblioteca de objetos"

	        },
	        error: function() {
	        	alert("Erro ao recuperar tipos de objetos...Xiiii ;)");
	        }
	});
 }


 /**
  * Construção das divs para carrega os objetos.
  * 
  * @param idTipo - indentificação do tipo de objeto
  * @param tabTipoObbjeto - nome do tipo de objeto
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

 /**
  * Recupera objetos de acordo com o tipo.
  * 
  * @param idTipo - tipo do objeto
  * @param tipoObjeto - nome do tipo do objeto
  */
 function getObjetos(idTipo,tipoObjeto){
	
	
	 var urlView = '/editor_objetos/objeto/get_lista_objetos/';
	 urlView += idTipo + '/'; 
	 
	 $.getJSON(
			    urlView, //url para recuperar uma lista json contendo objetos de um dado tipo
				function(data){	
			    	
			    	//data is empty, do something.
				    if(data == ""){
				    	jQuery('div#tipo'+tipoObjeto).html('');
				    	$('#tipo'+tipoObjeto).append(
				    			'<p class="text-info">' + 'Não existem objetos do tipo ' +
								 tipoObjeto + '</p>');
				    	
				    //load objects
				    }else{
				    	 
				    	 //limpa o conteúdo da div para atualizar com os objetos
				    	 jQuery('div#tipo'+tipoObjeto).html('');
				
						for (i=0;i<data.length;i++){	
							//isso deveria ser feito qndo o objeto é recuperado.
							//recupera url do icone
							getUrlIcone(tipoObjeto,data, i);	
						}	
				    }
				    
				}).error(function( data, textStatus, jqXHR ){ /* assign handler */
					alert("Erro ao recuperar objetos...Xiiii ;)");
		        });
 }
 
 /**
  * Recupera a url do icone e carrega os objetos.
  * 
  * @param dadosObjeto - dados do objeto
  * @param i - posição para acesso aos dado
  * @param tipoObjeto - nome do tipo de objeto
  */
 function getUrlIcone(tipoObjeto,dadosObjeto,i){
	 var urlView = '/editor_objetos/get_url_icone/';
	 urlView += dadosObjeto[i].fields.icone_objeto;
	 
	 $.getJSON(
			    urlView, 
				function(data){	
			    	//carrega dados
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
    * Função que permite o objeto ser draggable.
    * 
	* 1 - the offset of the map also must be used inside the calculation(when the map is not placed at the top left corner of the page)
	* 2 - the anchor of the marker by default is the bottom-center , but the script simply takes the position provided via the event-argument, 
	*      what may give different results, depending on the point inside the image where you grip it.
	*
	**/
	function draggableObjeto() {
		
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
				var icon = $(this).attr('src');
				var id = $(this).attr('id');
				var name_objeto = $(this).attr('alt');

				//essa função delega o tipo marker ou Polygon.
				createInstance(loc,icon, id, name_objeto);
				
			}
		
		});	

	}
	

 
 /**
  * Recupera "avatar" do autor
  * 
  * @param idUser - id do autor
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
 |  							    		Rascunhos	Códigos com problema      						      			  |
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