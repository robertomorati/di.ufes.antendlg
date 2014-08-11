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
		
		
		
		
		//apenas algumas modais v�o ter o tamanho alterado de acordo com a necessidade
			var id_form = $('#'+idDiv).find('form').attr('id');

			if(id_form == "condicoes_missao_list_view"){
				modalChange(idDiv);
			}
		
	});
};


/**
 * change dynamically size modal 
 */
function modalChange(idDiv){
	
	$("#"+idDiv).css({
		width:'auto',
        height:'auto', 
       'max-height':'100%',
      // 'margin-top': function () { //vertical centering
     //      return -($(this).height() / 2);
      // },
       'margin-left': function () { //Horizontal centering
           return -($(this).width() / 2);
       }
    	   
	});


	$("#"+idDiv).draggable({
	    handle: "."+idDiv
	});
	

	
}

/**
 * Função que trata a criação de comportamento para o agente em questão.
 * 
 * @param comportamento - tipo de comportamento
 * @param idDiv - id da div
 * @param idAgente - id do agente que terá o comportamento
 */
function openModalComportamentoAgentes(comportamento, idDiv, idAgente){
	
	  //salva os dados do agente na session, de modo a, permitir a criação do comportamento para o agente
	  msg_datas_agente = '[{"comportamento":"' + comportamento + '"' + ',"idAgente":"' + idAgente + '"}]'
	 // alert(msg_datas_agente);
	  $.ajax({
			 headers: { "X-CSRFToken": getCookie("csrftoken") },//token django
		     type:"POST",
		     url:'/editor_movimentos/agente/agente_session/'+idAgente+'/',
		     data: msg_datas_agente,
		     success: function(data,status){

		    	 	//data retorna msg em formato json se é criação ou atualização
		    	 	if(data.response == "create"){
			    	 	//cria comportamento agressivo para  agente
			    	 	if(comportamento == "Agressivo"){
			    	 		url = '/editor_movimentos/agente/criar_comportamento_agressivo/';
			    			openModal(url,idDiv);
			    	 	}else if(comportamento == "Passivo"){
			    	 		url = '/editor_movimentos/agente/criar_comportamento_passivo/';
			    			openModal(url,idDiv);
			    	 	}else if(comportamento == "Colaborativo"){
			    	 		url = '/editor_movimentos/agente/create_comportamento_colaborativo/';
			    			openModal(url,idDiv);
			    	 	}else if(comportamento == "Competidor"){
			    	 		url = '/editor_movimentos/agente/create_comportamento_competitivo/';
			    			openModal(url,idDiv);
			    	 	}
			    	 	
		    	 	}if(data.response == "update"){
			    	 	//atualização do comportamento
			    	 	if(comportamento == "Agressivo"){
			    	 		url = '/editor_movimentos/agente/update_comportamento_agressivo/'+idAgente+'/';
			    	 		openModal(url,idDiv);
			    	 	}else if(comportamento == "Passivo"){
			    	 		url = '/editor_movimentos/agente/update_comportamento_passivo/'+idAgente+'/';
			    			openModal(url,idDiv);
			    	 	}else if(comportamento == "Colaborativo"){
			    	 		url = '/editor_movimentos/agente/update_comportamento_colaborativo/'+idAgente+'/';
			    			openModal(url,idDiv);
			    	 	}else if(comportamento == "Competidor"){
			    	 		url = '/editor_movimentos/agente/update_comportamento_competitivo/'+idAgente+'/';
			    			openModal(url,idDiv);
			    	 	}
		    	 	}
		    	 	
		     },
		     error: function(xhr) {
		        	alert("Erro ao criar comportamento.");
		     }
		 });
}

/**
 * Função que trata a add de instancias para comportamentos colaborativos e competitivos
 * 
 * @param comportamento - tipo de comportamento
 * @param idDiv - id da div
 * @param idAgente - id do agente que terá o comportamento atualizado
 * @param op - tipo de operacao
 */
function addInstancesComportamento(comportamento, idDiv, idAgente,op){
	
	  //salva os dados do agente na session, de modo a, permitir a atualização do comportamento para o agente
	  msg_datas_agente = '[{"comportamento":"' + comportamento + '"' + ',"idAgente":"' + idAgente + '"}]'
	  
	  $.ajax({
			 headers: { "X-CSRFToken": getCookie("csrftoken") },//token django
		     type:"POST",
		     url:'/editor_movimentos/agente/agente_session/'+idAgente+'/',
		     data: msg_datas_agente,
		     success: function(data,status){

		     	  if(op == "create"){
		     		  url = '/editor_movimentos/agente/add_instance_agente/';
		     		  openModal(url,idDiv);
		     	  }else if(op == "list"){
			          url = '/editor_movimentos/agente/list_instance_agente/';
			          openModal(url,idDiv);
		     	  }
		    	 	
		     },
		     error: function(xhr) {
		        	alert("Erro ao criar comportamento.");
		     }
		 });
}


/**
 * Função que atualiza uma instancia e a mensagem que está sendo referenciada pelo comportamento de um dado agente
 * É válido lembrar que os dados do agente/comportamento neste momento estão armazenados na session.
 * 
 * @param urlUpdate
 * @param idDiv
 */
function updateInstanceBehavior(urlUpdate, idDiv){
	
		 $('#agente').modal('hide');
	     openModal(urlUpdate,idDiv);
	     
}


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
	        	var buffer = "";
		        //Recupera tipo e id para montar o menu
	        	for (i=0;i<obj.length;i++){
	        		
	        		//adiciona primeiros tipos.
		    		if(i < 2){	//é interessante trabalhar com a largura da tela.
		    			//create the menu with two types
		    			buffer = obj[i].fields.tipo;
			    		buffer = buffer.replace(/\s/g, '');
		    			$('#objetoTab').append(
		    			$('<li id="loadObjetos' + buffer + '"><a href="#tipo' + obj[i].fields.tipo + '" data-toggle="tab">' + buffer + '</a></li>'));
		    			$('#tipo' + buffer).tab('show');
		    			
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
		    			buffer = obj[i].fields.tipo;
			    		buffer = buffer.replace(/\s/g, '');
		    	    	//adiciona os tipos de objetos
		    	    	$('#outros').append(
		    	    			//id="tipo' + obj[i].fields.tipo + '"
		    	    			$('<li id="loadObjetos' +buffer + '""><a href="#tipo' + buffer + '" data-toggle="tab">' + obj[i].fields.tipo + '</a></li>'));
		    	    			$('#tipo' + buffer).tab('show');
		    		
		    	    }//end else
		    				
		    		//construção do "espaço para alocar os tipos de objetos"
		    		buffer = obj[i].fields.tipo;
		    		buffer = buffer.replace(/\s/g, '');
		    		buildTabContent(obj[i].pk,buffer);
		    		buffer = "";
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
 
function createPosInstanciaAtiva(json_instancias){
    var urlView = '/editor_objetos/estado_aventura/create_instances_activates/';
    
    
    //atualiza a localização da aventura
    $.ajax({
		 headers: { "X-CSRFToken": getCookie("csrftoken") },//token django
	     type:"POST",
	     url:urlView,
	     data: json_instancias,
	     success: function(data,status){	  	 
	    	 //uso da flag
	      	 
	    	
	     },
	     error: function(xhr) {

	        }
	 });
	
}

function createAvatarAtivo(json_avatars){
    var urlView = '/editor_objetos/estado_aventura/create_avatars_activates/';
    
    $.ajax({
		 headers: { "X-CSRFToken": getCookie("csrftoken") },//token django
	     type:"POST",
	     url:urlView,
	     data: json_avatars,
	     success: function(data,status){	  	 

	     },
	     error: function(xhr) {

	        }
	 });
	
}

function createMissaoAtiva(json_missoes){
    var urlView = '/editor_objetos/estado_aventura/create_missions_activates/';
    
    $.ajax({
		 headers: { "X-CSRFToken": getCookie("csrftoken") },//token django
	     type:"POST",
	     url:urlView,
	     data: json_missoes,
	     success: function(data,status){	  	 

	     },
	     error: function(xhr) {

	        }
	 });
	
}

function createCondicaoAtiva(json_condicoes){
    var urlView = '/editor_objetos/estado_aventura/create_conditions_activates/';
    
    $.ajax({
		 headers: { "X-CSRFToken": getCookie("csrftoken") },//token django
	     type:"POST",
	     url:urlView,
	     data: json_condicoes,
	     success: function(data,status){	  	 

	     },
	     error: function(xhr) {

	        }
	 });
	
}

function getCity(lat, lng,id_aventura) {

	alert("Teste");
    var newIdDiv = "locationAdventure"+id_aventura;
    document.getElementById("locationAdventure").setAttribute("id", newIdDiv);
    document.getElementById(newIdDiv).setAttribute("class", newIdDiv);
    
	var lat = lat.replace(',', '.');
	var lng = lng.replace(',', '.');
    var pos = new google.maps.LatLng(lat, lng);
    var geocoder = new google.maps.Geocoder(); 
    geocoder.geocode({'latLng': pos}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        if (results[1]) {
        //find country name
         for (var i=0; i<results[0].address_components.length; i++) {
            for (var b=0;b<results[0].address_components[i].types.length;b++) {
            	
            //there are different types that might hold a city admin_area_lvl_1 usually does in come cases looking for sublocality type will be more appropriate
                if (results[0].address_components[i].types[b] == "neighborhood") {
                    //this is the object you are looking for
                    city= results[0].address_components[i];
                    break;
                }
            }
        }
        //city data
         $( "."+newIdDiv ).empty().append( ""+city.short_name );
        } else {
        	$( "."+newIdDiv ).empty().append("Sem Localização");
        }
      } else {
    	  $( "."+newIdDiv ).empty().append("Sem Localização");
      }
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