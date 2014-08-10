/**
 * Created on --/10/2013
 * 
 * Arquivo que habilita:
 * 			1 - A inicialização da API - Google Maps V3;
 * 			2 - Persistência de dados de uma dada aventura quando ativa;
 * 			3 - Operações (CRUD) nas instancias por json;
 * 
 * @author: Roberto Guimaraes Morati Junior <robertomorati@gmail.com>
 */		

/**
 * Flags criadas para tratar casos especificos relacionados com as instâncias.
 **/
var flagloadInstancias = false; //Flag para evitar a execução do "ajax" que cria a primeira posição geográfica do objeto.
var flagloadBackupInstances = false;//Flag para controlar o backup de instâncias. Assim, evita requisições desnecessárias.	 

var flagLoadBackupInstancesMoreOfPos = false;//Flag para tratar o backup de instâncias que possuem mais de uma posição geográfica.

var intancias_objetos_json;//buffer para armazenar instâncias de objetos.
var singleClickMouse = false;//Flag para tratar o click simples e duplo em marcadores do Polygon. Uso somente em instâncias com mais de uma POS.



/**
 * carregaPos()
 * 
 * Função que verifica se a aventura está ativa. 
 * Caso a mesma esteja ativa, a posição do mapa é direcionado para a localização da aventura, caso exista.
 */
var $latlng;//posição do mapa
function carregaPos (){
	
	var id = aventuraAtiva();
	
	if(id != '-1'){
		 var urlView = '/editor_aventuras/get_json_aventura/' + id +'/';
		 $.ajax({
		        type: 'GET',
		        url: urlView,
		        cache: false,
		        async: false,
		        success: function(response) {
		        	var obj = $.parseJSON(response);
		        	if(obj[0].fields.latitude != '' && obj[0].fields.longitude != ''){
		        		$latlng = new google.maps.LatLng(obj[0].fields.latitude, obj[0].fields.longitude);
		        	}else{
		        		$latlng = new google.maps.LatLng(32.6381461, -16.9332489);
		        	}
		        	initialize();//inicializa o google maps
	        },
	        error: function() {
	        	alert("Erro ao recuperar tipos de objetos...Xiiii ;)");
	        }
		});	
	}else{
		//32,6381461 -16,9332489   -30.068637, -51.120404
		$latlng = new google.maps.LatLng(32.6381461, -16.9332489);//posição padrão caso a aventura não possua.
		initialize();//inicializa o google maps em uma posição padrão
	}

}

/**
 * Função que inicializa o google maps. 
 * 
 */
var $map;//google maps
var overlay;
function initialize() {

	//opções iniciais de configuração do mapa ao para ser iniciado
    var myOptions = {
      zoom: 16,
      center: $latlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP,
      mapTypeControlOptions: {
            style: google.maps.MapTypeControlStyle.DROPDOWN_MENU,
            position: google.maps.ControlPosition.TOP_LEFT },
            mapTypeControl: true,
            mapTypeControlOptions: {
                    style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
            },
            zoomControl: true,
            scaleControl: true,
            scaleControlOptions: {
                    position: google.maps.ControlPosition.TOP_LEFT
            },
            streetViewControl: true,

    };
    
    $map = new google.maps.Map(document.getElementById("map-canvas"),myOptions);

    //ajusta o zoom após o local da aventura ser localizado
    google.maps.event.addListener($map, 'zoom_changed', function() {
            zoomChangeBoundsListener = google.maps.event.addListener($map, 'bounds_changed', function(event) {
                            if (this.getZoom() >= 15 && this.initialZoom == true) {
                                    // Change max/min zoom here
                                    this.setZoom(15);
                                    this.initialZoom = false;
                            }
                    google.maps.event.removeListener(zoomChangeBoundsListener);
            });
    });

    var defaultBounds = new google.maps.LatLngBounds($latlng);
    $map.initialZoom = true;//position start
    $map.fitBounds(defaultBounds);

     //Create the search box and link it to the UI element.
     var input = document.getElementById('target');
     var searchBox = new google.maps.places.SearchBox(input);
       // [START region_getplaces]
      // Listen for the event fired when the user selects an item from the
      // pick list. Retrieve the matching places for that item.
      google.maps.event.addListener(searchBox, 'places_changed', function() {
	            var places = searchBox.getPlaces();
	
	            /*for (var i = 0, marker; marker = markers[i]; i++) {
	              marker.setMap(null);
	            }*/

            // For each place, get the icon, place name, and location.
            //markers = [];
            
            //Algumas cidades apresentam problemas ao serem localizadas, retornando mais de uma POS.
            //Desta forma desencadeia uma quantidade absurda de mensagens para o usuário, devido a requisição de salva POS estar dentro do for/loop.
            //Com o intuito de limitar a mensagem para que parecer somente uma vez, fora criada a flagCount.
            var flagCount = 0;
            var bounds = new google.maps.LatLngBounds();
            for (var i = 0, place; place = places[i]; i++) {
              /*var image = {
                url: place.icon,
                size: new google.maps.Size(71, 71),
                origin: new google.maps.Point(0, 0),
                anchor: new google.maps.Point(17, 34),
                scaledSize: new google.maps.Size(25, 25)
              };*/
              
              // Create a marker for each place.
              // Removido, pois ao localizar um lugar está função atribui um marker desnecessário para o autor da aventura.
             /* var marker = new google.maps.Marker({
                map: map,
                icon: image,
                title: place.name,
                position: place.geometry.location
              });

              markers.push(marker);*/

              bounds.extend(place.geometry.location);
              
              //Atualiza a posição da aventura que estiver ativa
              
		       jsonObj = '[{"latitude":"' + place.geometry.location.lat() + '"' + ',"longitude":"' + place.geometry.location.lng() + '"}]';
		      //Getting id aventura from bar user
		       id_aventura = $('body').find('aventura_ativa_id').attr('id');
		       
		      //create url "to" update aventura
		       var urlView = '/editor_aventuras/set_json_aventura/';
		       urlView += id_aventura + '/'; 
		       
		       //atualiza a localização da aventura
		       $.ajax({
					 headers: { "X-CSRFToken": getCookie("csrftoken") },//token django
				     type:"POST",
				     url:urlView,
				     data: jsonObj,
				     success: function(data,status){	  	 
				    	 //uso da flag
				      	 if(flagCount == 0){  
				      		 	//recupera instâncias de objeto para aventura
				      		 	flagloadInstancias = true;
				      		 	flagloadBackupInstances = true;
				      		 	loadInstancias();
				      		    $map.setZoom(15);//matém o zoom 15...
				      		    //show user msg, says: "aventura com posição atualizada"
					            openModal('/editor_objetos/gmap/msg/','msg');
					            $('#msg').modal('show');
					            flagCount += 1;
					      }
				    	
				     },
				     error: function(xhr) {
				    	  if(flagCount == 0){
				        	alert("Erro ao atualizar posição geográfica da aventura. Certifique-se de que existe alguma aventura em modo de auntoria." +
				        		  " Ou vá para o meno Configurações Aventura -> Editar Aventura e ative uma aventura para ser 'autorada'!");
				        	flagCount += 1;
				     		}
				        }
				 });
              
            }
            $map.fitBounds(bounds);
      });
      //[END region_getplaces]

	  // Bias the SearchBox results towards places that are within the bounds of the
	  // current map's viewport.
	  google.maps.event.addListener($map, 'bounds_changed', function() {
	    var bounds = $map.getBounds();
	    searchBox.setBounds(bounds);
	  });
  
		overlay = new google.maps.OverlayView();
		overlay.draw = function() {};
		overlay.setMap($map);
		
		flagloadInstancias = true;
		flagLoadBackupInstancesMoreOfPos = true;
		loadInstancias();
} 

	
/**
 * Cria a instância de um objeto.
 * 
 * @param location - localização da instância
 * @param icon - imagem para add no marcador
 * @param id - id do objeto instanciado
 * @param name_objeto  - nome da instância
 * @param quantidade - quandidade permitida de instâncias
 */
function createInstance(location,icon, id, name_objeto) {

  //json para criação da instância do objeto
  var json_instancia_objeto = '[{"nome":"' + name_objeto + '"' + ',"id_objeto":"' + id +'"}]';
  urlView = '/editor_objetos/instancia_objeto/create_instancia/';
  
  //criação da instância
  $.ajax({
		 headers: { "X-CSRFToken": getCookie("csrftoken") },//token django
	     type:"POST",
	     url:urlView,
	     data: json_instancia_objeto,
	     success: function(data,status){
	    	 if(data.pk == 0){
	    		 alert("Impossível criar mais instâncias do objeto " + name_objeto + ". Quantidade de isntâncias no limite.");
	    	 }else{
	    		    //cria uma nova instância, e atualiza o buffer de instâncias
	    		    flagloadBackupInstances = false;
	    		    flagLoadBackupInstancesMoreOfPos = false;
	    		    flagloadInstancias = false;
	    		    loadInstancias();
	    		    
	    		    if(data.qntde_pos == 1){
	    		    	placeInstancesGoogleMaps(location,icon, data.pk, name_objeto);
	    		    }else{
	    		    	placeInstancesPolygonGoogleMaps(location,icon, data.pk, name_objeto,data.qntde_pos,"");
	    		    }
			    	
	    	 	}//fim do else
	     },
	     error: function(xhr) {
	        	alert("Erro criar instância do objeto.");
	     }
	 });

}


/**
 * Função para adicionar instância que possui POS > 1
 * 
 * @param location - localização de onde a instãncia foi largada
 * @param icon - imagem da instância
 * @param id_instancia
 * @param name_objeto
 * @param qntde_pos - quantidade de posições geográficas que a instância pode assumir.
 */
function placeInstancesPolygonGoogleMaps(location,icon, id_instancia, name_objeto,qntde_pos,pos){
	  
	/**
	 * Explicação do MVCArray, utilizado para o marker Polygon.
	 * https://developers.google.com/maps/articles/mvcfun?hl=pt-BR&csw=1
	 **/
	var path = new google.maps.MVCArray;
	//makers da instância
	var markers = [];

	//create Polygon
   var poly = new google.maps.Polygon({
      strokeWeight: 2,//expessura da aresta
      fillColor: "#FFFFFF",//cor da aresta
	  fillOpacity: .01, //This changes throughout the program 
	  //zIndex: 5,
    });
	
    poly.setMap($map);
    poly.setPaths(new google.maps.MVCArray([path]));

    //metadata para a instância
    poly.set("id", "qnt_pos_limite","qnt_pos_inicial","icone","nome");
    poly.set("id", id_instancia);
    poly.set("qnt_pos_limite", qntde_pos);
    poly.set("qnt_pos_inicial", 0);
    poly.set("icone", icon);
    poly.set("nome", name_objeto);
    
    
    if(pos.length > 0){//processo de carregamento de instâncias
    
		//quantidade de pos indica a quantidade de marcadores que aquele Polygon possui
		for (var j=0;j<pos.length;j++){
			
			   poly.set("qnt_pos_inicial", (poly.get("qnt_pos_inicial")+1));
			   var loc = new google.maps.LatLng(pos[j].lat, pos[j].lng);
			   
			   path.insertAt(path.length, loc);
			   
			   createMakerLoaded(poly,loc,id_instancia,path,j,markers,pos);
				
	
		}//fim do for de pos
    		
    }else{//processo de autoria 
    	     
	    //cria marcador inicial
	    poly.set("qnt_pos_inicial", (poly.get("qnt_pos_inicial")+1));
	    
	    path.insertAt(path.length, location);
	    
		var marker = new google.maps.Marker({
			  position: location,
			  map: $map,
			  draggable: true,
			  icon: poly.get("icone"),
			  zIndex: 5,
		});
		
		marker.set("id_instancia","id_pos");
	    marker.set("id_instancia", id_instancia);
		markers.push(marker);
		
		marker.setTitle("POS #" + path.length);
		createPosMarkerPolygon(marker);

		google.maps.event.addListener(marker, 'click', function() {
			singleClickMouse = true;
			//setTimeout("runIfNotDblClick()",300);
			setTimeout(function(){
				 if(singleClickMouse==true)
				   infoWindowMarkersPolygon(poly,marker,iconTime,markers,path,marker.getTitle());
			 }, 400);  
		});
		
	    //adicionar pontos no marcador/instância/Polygon
		google.maps.event.addListener(marker, 'dblclick', function(event){
			 singleClickMouse = false;
			 createMarkerToPolygon(poly,event,path,markers); 
	    });
		
		//Se marcador da instância do tipo Polygon é arrastado, então atualiza POS.
		google.maps.event.addListener(marker, 'dragend', function() {
			updataPosMarkerPolygon(marker,markers,path);
		});
		
		//deleção do marcador
		google.maps.event.addListener(marker, 'rightclick', function() {	  
			deleteMarkerPolygon(marker,markers,path,poly );
		});
	
    }
	
 }
    
/**
 * 
 * @param marker - marcador a ser deletado
 * @param markers - lista de marcadores da instância Polygon
 * @param path - path do MVCArray
 * @param poly - Polygon que representa instâncias com mais de uma POS
 */
 function deleteMarkerPolygon(marker,markers,path,poly ){
	 
	 var urlIO = '/editor_objetos/posicao_geografica/delete_pos/' +  marker.get("id_pos") + '/';
	 var urlInstance = '/editor_objetos/instancia_objeto/delete_instancia/'+marker.get('id_instancia')+'/';
	 $.ajax({
			headers: { "X-CSRFToken": getCookie("csrftoken") },//token django
	        type: 'POST',
	        url: urlIO,
	        cache: false,
	        async: false,
	        success: function(responseText) {
	        	
				if(responseText.response == 1){
				
					 $.ajax({
							headers: { "X-CSRFToken": getCookie("csrftoken") },//token django
					        type: 'POST',
					        url: urlInstance,
					        cache: false,
					        async: false,
					        success: function(responseText) {
					        		//instancia deletada
							},error: function() {
								alert("Erro ao deletar instância...Xiiii ;)");
							}
						});
				}
				
				marker.setMap(null);
				poly.set("qnt_pos_inicial", (poly.get("qnt_pos_inicial")-1));
				for (var i = 0, I = markers.length; i < I && markers[i] != marker; ++i);
				markers.splice(i, 1);
				path.removeAt(i);
				
	    	 	//pos atualizada
	    	    //atualiza backup de instâncias
	    	 	flagloadBackupInstances = false;
	    	 	loadInstancias();
				
			},error: function() {
				alert("Erro ao deletar marcador...Xiiii ;)");
			}
		});

 }

 /**
  * 
  * @param poly - Polygon que representa instâncias com mais de uma POS
  * @param loc - posição geográfica
  * @param id_instancia - identificação da instância.
  * @param path - MVCArray
  * @param j - interação do loop que chama createMakerLoaded
  * @param markers - lista de marcadores da instância Polygon
  * @param pos - posicoes para carregar o marcador
  *  
  */
function createMakerLoaded(poly,loc,id_instancia,path,j,markers,pos){
	
	 var marker = new google.maps.Marker({
			  position: loc,
			  map: $map,
			  draggable: true,
			  icon: poly.get("icone"),
			  zIndex: 5,
	  });
		
	  marker.set("id_instancia","id_pos");
	  marker.set("id_instancia", id_instancia);
	  marker.set("id_pos", pos[j].id_pos);
		
	  marker.setTitle("POS #" + path.length);
	  
	  markers.push(marker);
	  path.setAt(j, marker.getPosition());

	google.maps.event.addListener(marker, 'click', function() {
		 singleClickMouse = true;
		 
		 //setTimeout("runIfNotDblClick()", 300);
		 setTimeout(function(){
			 if(singleClickMouse==true)
			   infoWindowMarkersPolygon(poly,marker,iconTime,markers,path,marker.getTitle());
		 }, 400);  
	
	});
	
    //adicionar pontos no marcador/instância/Polygon
	google.maps.event.addListener(marker, 'dblclick', function(event){
		 singleClickMouse = false;
		 createMarkerToPolygon(poly,event,path,markers); 
    });
	
	//Se marcador da instância do tipo Polygon é arrastado, então atualiza POS.
	google.maps.event.addListener(marker, 'dragend', function() {
		updataPosMarkerPolygon(marker,markers,path);
	});
	
	//deleção do marcador
	google.maps.event.addListener(marker, 'rightclick', function() {
		deleteMarkerPolygon(marker,markers,path,poly );
	});



	
}

/**
 * Função que cria marcador para a instância do tipo Polygon
 * 
 * @param poly - referência ao marker do tipo Polygon
 * @param event - evento dispado no dlclick
 * @param path - path do MVCArray
 * @param markers - array de makers do poly
 */
function createMarkerToPolygon(poly,event,path,markers){
	
  //verifica a quantidade de posições geográficas
  if(poly.get("qnt_pos_inicial") < poly.get("qnt_pos_limite")){
		
	    poly.set("qnt_pos_inicial", (poly.get("qnt_pos_inicial")+1));
		
	    path.insertAt(path.length, event.latLng);
	    
		var marker = new google.maps.Marker({
		  position: event.latLng,
		  map: $map,
		  draggable: true,
		  icon: poly.get("icone"),
		  zIndex: 5,
		});
		
		
		marker.set("id_instancia","id_pos");
		marker.set("id_instancia", poly.get("id"));
		
		//flag Polygon criado?
		createPosMarkerPolygon(marker);
		
		//alert(poly.get("qnt_pos_inicial") + " Posição do marcador: " + marker.getPosition() );
		markers.push(marker);
		marker.setTitle("POS #" + path.length);//o path deve ser unico para cada marcador.

		google.maps.event.addListener(marker, 'click', function() {
			 singleClickMouse = true;

			 setTimeout(function(){
				 if(singleClickMouse==true)
				   infoWindowMarkersPolygon(poly,marker,iconTime,markers,path,marker.getTitle());
			 }, 400);  
		
		});
		
	    //adicionar pontos no marcador/instância/Polygon
		google.maps.event.addListener(marker, 'dblclick', function(event){
			 singleClickMouse = false;
			 createMarkerToPolygon(poly,event,path,markers); 
	    });
	
		
		//Se marcador da instância do tipo Polygon é arrastado, então atualiza POS.
		google.maps.event.addListener(marker, 'dragend', function() {	 
			updataPosMarkerPolygon(marker,markers,path);
		});
		
		//deleção do marcador
		google.maps.event.addListener(marker, 'rightclick', function() {
			deleteMarkerPolygon(marker,markers,path,poly );
		});

		
		flagLoadBackupInstancesMoreOfPos = false;
		loadInstancias();

	}else{
		alert("Essa instância de objeto já está utilizando o máximo de posições geográficas permitidas.");
	}
}

/**
 * Função que lida com a atualização dos dados de uma instância,
 * com mais de 1 posição geográfica.
 * 
 * @param poly - Instância Polygon 
 * @param marker - marcador que receve a infowindow
 * @param iconTime - ícone de tempo para carregamento dos dados da instância
 * @param markers - lista de marcadores
 * @param path - MVCArray
 * @param nome_marker - nome do marcador
 */
function infoWindowMarkersPolygon(poly,marker,iconTime,markers,path,nome_marker){
	
	//Icone para fornecer feedback ao usuário de que os dados da instância estão sendo carregados
	iconTime = "" + '<i class=" icon-download-alt"></i>';
	  
	 
	 //Criação da infoWindows, 
	 //fonte:http://jsfiddle.net/kjy112/3CvaD/
	 var nameInfo = 'infoWindow' + nome_marker;
	 marker[nameInfo] = new google.maps.InfoWindow({ 
		    maxWidth: 600,
		    content: iconTime,
     });
   
   //Url para recuperar dados da instância que será atualizada
   var urlIO = '/editor_objetos/instancia_objeto/update_instancia/' +  marker.get("id_instancia") + '/';
  
   marker[nameInfo].open($map, marker);
   info = marker[nameInfo];
   
   var rmMaker = marker;
   
   //Carregando conteúdo da infoWindow por meio de uma requisição Ajax
   $.ajax({	
	    type: 'GET',
	    url: urlIO,
	    success: function(data){
	    	
	    	//Adiciona um evento ao conteúdo da infowindo relacionado ao DOM.
	    	google.maps.event.addListener(info, 'domready', function(event) {
	    	  
	    	var options = {
  				target : '#contentInstance', 
  				success : showResponse,
  				error: showsomething, 
  				async: false 
  			};
    	  
  			// post-submit callback 
  			function showResponse(responseText, statusText, xhr, $form) {
				var ct = xhr.getResponseHeader("content-type") || "";
				
				if(responseText.response == "delete"){
				    
					//Fecha a infoWindow se a instância for deletada
					info.close();
					//atualiza flag para atualizar buffer de instâncias
					flagLoadBackupInstancesMoreOfPos = false;
					//atualiza instâncias
					loadInstancias();
					
					for (var i = 0; i <= markers.length; i++){
						var delMarker = markers[i];
						//markers.splice(i, (i+1));
						delMarker.setMap(null);
						poly.setMap(null);
					}
					
				}else if (ct.indexOf('json') > -1) {
					 //instância atualizada com sucesso, fecha infowindow
					 info.close();
				}
  			}
  			
  			function showsomething(){
  				alert("Ocorreu um erro ao recuperar o conteúdo da instância. Por gentileza, tente a operação novamente!");
  			}
  			
  			//add evento nos forms
  			$('#instancia_objeto_update_view').ajaxForm(options);
  			$('#instancia_objeto_delete_view').ajaxForm(options);
	    	  
	      });//fim do script para tratar o json e domready
	      //atualiza conteúdo
	      info.setContent(data); 
	    },
	     error: function(xhr) {
	        	alert("Ocorreu um erro ao carregar os dados da instância!");
	    }
	});
   info.setContent(iconTime);
}

/**
 * Atualiza a posição de um marcador do Polygon
 * @param marker - marcador
 * @param markers - lista de marcadores
 * @param path - path do MVCArray
 */
function updataPosMarkerPolygon(marker,markers,path) {
	
	//atualiza a aresta que liga os marcadores
	for (var i = 0, I = markers.length; i < I && markers[i] != marker; ++i);
	path.setAt(i, marker.getPosition());
	
	 var pos = "" + marker.getPosition();
	 var res = pos.split(",");
	 var lat = res[0].replace('(', '');
	 var lng = res[1].replace(')', '');
	 
	json_pos = '[{"latitude":"' + lat + '"' + ',"longitude":"' + lng + '"' + ',"altitude":"' + '0.0' + '"}]';
	
	//atualiza posicao daquela instancia
    $.ajax({
		 headers: { "X-CSRFToken": getCookie("csrftoken") },
	     type:"POST",
	     url:'/editor_objetos/posicao_geografica/update_pos/'+ marker.get("id_pos")+'/',
	     data: json_pos,
	     success: function(data,status){
	    	 	//pos atualizada
	    	    //atualiza backup de instâncias
 				flagLoadBackupInstancesMoreOfPos = false;
 				loadInstancias();
	     },
	     error: function(xhr) {
	        	alert("Erro ao salvar posicao geografica do objeto.");
	     }
	}); 
}

/**
 *  Função que atualiza a posição geográfica de um marcador de um Polygon
 *  O marker do Polygon possui uma estrutura de representação de dados diferente do Maker que representa uma instância com uma POS
 *  
 * @param marker - marcador do Polygon
 */
function createPosMarkerPolygon(marker){
	
	 var pos = "" + marker.getPosition();
	 var res = pos.split(",");
	 var lat = res[0].replace('(', '');
	 var lng = res[1].replace(')', '');
	 
	
	json_pos = '[{"latitude":"' + lat + '"' + ',"longitude":"' + lng + '"' + ',"altitude":"' + '0.0' + '"' + ',"instancia_objeto_id":"' + marker.get("id_instancia") + '"}]';
	
	//cria posicao para a instância do objeto
	$.ajax({
   			 headers: { "X-CSRFToken": getCookie("csrftoken") },
   		     type:"POST",
   		     url:'/editor_objetos/posicao_geografica/create_pos/',
   		     data: json_pos,
   		     success: function(data,status){
   		    	marker.set("id_pos", data.pk);
   				flagLoadBackupInstancesMoreOfPos = false;
   				loadInstancias();
   		     },
		     error: function(xhr) {
		        	alert("Erro ao salvar posicao geografica do objeto.");
		     }
	});
	
}


/**
 * Função para adicionar instância no mapa, bem como outros eventos que acotnecem com a instância.
 * 
 * @param location - localização 
 * @param icon - ícone para a instância
 * @param id_instancia - id da instância
 * @param name_objeto - nome do objeto
 */
function placeInstancesGoogleMaps(location,icon, id_instancia, name_objeto){
	
	  //obtendo log e latitude
	  var pos = "" + location;
	  var res = pos.split(",");
	  var lat = res[0].replace('(', '');
	  var lng = res[1].replace(')', '');
	  
	  //cria um novo marcador para a instância do objeto
	  var marker = new google.maps.Marker({		
		  map: $map,
		  position: location,
		  draggable:true,	
		  icon:	icon,
		  zIndex: 5,
	  });
	  
	  //<TESTE>
	  /**var circle = new google.maps.Circle({
		  map: $map,
		  radius: 20,    // 10 miles in metres
		  fillColor: '#AA0000'
		});
	  
	  circle.bindTo('center', marker, 'position');
	  **/
	  iconTime = "" + '<i class=" icon-download-alt"></i>';
	  
	  //getting of following link:
	  //http://jsfiddle.net/kjy112/3CvaD/
	  var nameInfo = 'infoWindow' + name_objeto;
	  marker[nameInfo] = new google.maps.InfoWindow({ 
		    maxWidth: 600,
		    content: iconTime,
      });
	  
	 
	  var info;
	  //adiciona evento de click para abrir a infowindo da instância.
	  //Função também responsavel por carregar o conteúdo na infowindow.
	  google.maps.event.addListener(marker, 'click', function() {

	       var urlIO = '/editor_objetos/instancia_objeto/update_instancia/' +  marker.metadata.id + '/';
	       
	       
	       this[nameInfo].open($map, this);
	       info = this[nameInfo];
	       var rmMaker = marker;
	       //De acordo com "fontes" no stackoverflow, a forma mais eficiente para carregar o conteúdo na infowindow é por meio de ajax.
	       $.ajax({	
	    	    type: 'GET',
	    	    url: urlIO,
	    	    success: function(data){
	    	    	
	    	    	//adiciona um evento ao conteúdo da infowindo relacionado ao DOM.
	    	    	google.maps.event.addListener(info, 'domready', function(event) {
	    	    	  
	    	    	  var options = {
	    	  				target : '#contentInstance',
	    	  				success : showResponse,
	    	  				error: showsomething,
	    	  				async: false 
	    	  			};
	    	    	  
	    	  			// post-submit callback 
	    	  			function showResponse(responseText, statusText, xhr, $form) {
	    	  				
	    	  				var ct = xhr.getResponseHeader("content-type") || "";
	    	  				
	    	  				if(responseText.response == "delete"){
	    	  					info.close();//fecha infowindow
	    	  					rmMaker.setMap(null);//remove marcador
	    	  					flagloadBackupInstances = false;//set flag to update instances
	    	  					loadInstancias();//update isntances
	    	  					
	    	  				}else if (ct.indexOf('json') > -1) {
	    	  					info.close();//após atualizar fecha a infowindow
	    	  					
	    	  					info.setContent(data);//atualiza conteúdo
	    	  				}else{
	    	  					//alert("Dados?" + responseText.response + " " + ct);
	    	  				}
	    	  				
	    	  				
	    	  			}
	    	  			
	    	  			function showsomething(){
	    	  				alert("Ocorreu um erro ao recuperar o conteúdo da instância ou durante a atualização da mesma. Por gentileza, tente a operação novamente!");
	    	  			}
	    	  			
	    	  			//add evento nos forms
	    	  			$('#instancia_objeto_update_view').ajaxForm(options);
	    	  			$('#instancia_objeto_delete_view').ajaxForm(options);
	    	    	  
	    	      });//fim do script para tratar o json e domready
	    	    	
	    	       info.setContent(data);//atualiza conteúdo;
	    	       
	    	    },
			     error: function(xhr) {
			        	alert("Ocorreu um erro ao carregar os dados da instância!");
			     }
	    	});
	       
	       info.setContent(iconTime);
	       
	  });
	  
	  //markers.push(marker);
	  marker.metadata = {id: id_instancia};//add id da instância no marcado para atualizar a POS da instância
	
	   //Flag que só permite criar a posição, caso seja uma nova instância.
	   if(flagloadInstancias == false){
			
		    //cria posicao para a instância do objeto
			json_pos = '[{"latitude":"' + lat + '"' + ',"longitude":"' + lng + '"' + ',"altitude":"' + '0.0' + '"' + ',"instancia_objeto_id":"' + id_instancia + '"}]';
			$.ajax({
		   			 headers: { "X-CSRFToken": getCookie("csrftoken") },
		   		     type:"POST",
		   		     url:'/editor_objetos/posicao_geografica/create_pos/',
		   		     data: json_pos,
		   		     success: function(data,status){
		   		    	 
		   		     },
				     error: function(xhr) {
				        	alert("Erro ao salvar posicao geografica do objeto.");
				     }
			});
			
	   }//fim do if
	
	 //Quando uma instância de objeto é arrastada, sua posiçào geográfica é atualizada
     google.maps.event.addListener(marker, 'dragend', function() {
     
    	 var curLatLng = marker.getPosition();
    	
        //json para atualização da pos
  		json_pos = '[{"latitude":"' + curLatLng.lat() + '"' + ',"longitude":"' + curLatLng.lng() + '"' + ',"altitude":"' + '0.0' + '"}]';
  	
  		updatePosMarker(json_pos,marker);
  		
     });//fim da  google.maps.event.addListener

}//end function


/**
 * Função que atualiza a posição de uma instância que possua POS igual a 1.
 * 
 * @param json_pos - nova posicao do marcador
 * @param - marcador a ter sua POS atualizada
 */
function updatePosMarker(json_pos,marker){
		
		$.ajax({
			 headers: { "X-CSRFToken": getCookie("csrftoken") },
		     type:"GET",
		     url:'/editor_objetos/posicao_geografica/get_json_pos/'+marker.metadata.id+'/',
		     success: function(data,status){
		    	
		    	 var pos = $.parseJSON(data);//recupera id da posicao daquela instância
		    	 
		    	    //atualiza posicao daquela instancia
		  		    $.ajax({
			   			 headers: { "X-CSRFToken": getCookie("csrftoken") },
			   		     type:"POST",
			   		     url:'/editor_objetos/posicao_geografica/update_pos/'+pos[0].pk+'/',
			   		     data: json_pos,
			   		     success: function(data,status){
			   		    	 	//pos atualizada
			   		    	    //atualiza backup de instâncias
			   		    	 	flagloadBackupInstances = false;
			   		    	 	loadInstancias();
			   		     },
					     error: function(xhr) {
					        	alert("Erro ao salvar posicao geografica do objeto.");
					     }
		  			});
		    },
	     error: function(xhr) {
	    	 alert("Erro ao salvar posicao geografica do objeto.");
	     }
		});


}

/**
 * Carrega instâncias do objeto.
 * 
 */
function loadInstancias(){
	
	//verifica se a aventura está ativa
	var aventura_id = aventuraAtiva();
	
	if(aventura_id != '-1'){
		urlView = '/editor_objetos/instancia_objeto/get_instancia/' + aventura_id  + '/';
		   
    	if(flagloadBackupInstances == false || flagLoadBackupInstancesMoreOfPos == false){
 
    		if(flagloadBackupInstances == false) flagloadBackupInstances = true
    		if(flagLoadBackupInstancesMoreOfPos == false) flagLoadBackupInstancesMoreOfPos = true
			
    		//ajax to get all types of instances by aventura_id
			$.ajax({
	   		     type:"GET",
	   		     url:urlView,
	   		     success: function(data,status){
	   		    	intancias_objetos_json = data;//backup das instâncias atualizado
	   		     },
			     error: function(xhr) {
			        	alert("Erro ao recuperar lista de instâncias de objetos.");
			     }
			});
			
		}else{
			
			var instancias = $.parseJSON(intancias_objetos_json);
			
			for (var i=0;i<instancias.length;i++){
				if(instancias[i].posicoes_geograficas > 1){
					placeInstancesPolygonGoogleMaps("", instancias[i].url_icone, instancias[i].id, instancias[i].nome, instancias[i].posicoes_geograficas, instancias[i].pos);
				
				}else{
					var loc = new google.maps.LatLng(instancias[i].pos[0].lat, instancias[i].pos[0].lng);
					placeInstancesGoogleMaps(loc,instancias[i].url_icone, instancias[i].id, instancias[i].nome);
				}
			}
			
		}
	}else{
		intancias_objetos_json = "";//limpa backup
	}
	
}
	
/**
 * Função para verificar se existe aventura ativa para o usuário logado
 */
function aventuraAtiva(){
	
	//verifica se existe alguma aventura ativa na barra do usuário
	var aventura_id = '-1';
	if($('body').find('aventura_ativa_id').attr('id')>0)
		aventura_id = $('body').find('aventura_ativa_id').attr('id');
	
	return aventura_id;
}

/**
 * Esta função ajusta o centro do mapa. Qual a necessidade disso? Veja a estrutura de camadas do google maps para melhor entender.
 * Com o mapa é deslocado para outra posição na pagina, ocorre um problema com a camada de coordenadas, afetando o dragdrop.
 * Assim, esta função corrige este problema.
 * 
 * @param latlng
 * @param offsetx
 * @param offsety
 */
function map_recenter(latlng,offsetx,offsety) {
    var point1 = $map.getProjection().fromLatLngToPoint(
        (latlng instanceof google.maps.LatLng) ? latlng : map.getCenter()
    );
    var point2 = new google.maps.Point(
        ( (typeof(offsetx) == 'number' ? offsetx : 0) / Math.pow(2, $map.getZoom()) ) || 0,
        ( (typeof(offsety) == 'number' ? offsety : 0) / Math.pow(2, $map.getZoom()) ) || 0
    );  
    $map.setCenter($map.getProjection().fromPointToLatLng(new google.maps.Point(
        point1.x - point2.x,
        point1.y + point2.y
    )));
}

/**
 * A mesma coisa da funcao map_recenter()
 * @param latlng
 * @param offsetx
 * @param offsety
 */
function offsetCenter(latlng,offsetx,offsety) {

	// latlng is the apparent centre-point
	// offsetx is the distance you want that point to move to the right, in pixels
	// offsety is the distance you want that point to move upwards, in pixels
	// offset can be negative
	// offsetx and offsety are both optional

	var scale = Math.pow(2, map.getZoom());
	var nw = new google.maps.LatLng(
	    map.getBounds().getNorthEast().lat(),
	    map.getBounds().getSouthWest().lng()
	);

	var worldCoordinateCenter = map.getProjection().fromLatLngToPoint(latlng);
	var pixelOffset = new google.maps.Point((offsetx/scale) || 0,(offsety/scale) ||0)

	var worldCoordinateNewCenter = new google.maps.Point(
	    worldCoordinateCenter.x - pixelOffset.x,
	    worldCoordinateCenter.y + pixelOffset.y
	);

	var newCenter = map.getProjection().fromPointToLatLng(worldCoordinateNewCenter);

	map.setCenter(newCenter);

}
    
/**
 * Django
 * @param c_name
 * @returns
 */
function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }


//http://gmaps-samples-v3.googlecode.com/svn/trunk/poly/poly_edit.html
//http://stackoverflow.com/questions/3394961/google-maps-api-v3-how-to-draw-dynamic-polygons-polylines


function getCity(lat, lng,id_aventura) {

	alert("Teste");
    var newIdDiv = "locationAdventure"+id_aventura;
    document.getElementById("locationAdventure").setAttribute("id", newIdDiv);
    document.getElementById(newIdDiv).setAttribute("class", newIdDiv);
    
	var lat = lat.replace(',', '.');
	var lng = lng.replace(',', '.');
    var latlng = new google.maps.LatLng(lat, lng);
    var geocoder = new google.maps.Geocoder(); 
    geocoder.geocode({'latLng': latlng}, function(results, status) {
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


/*********************************************************************************************
 *                                  Código Antigo											 *
 ********************************************************************************************/	    



/**
 *Não está sendo utilizada.
 * @param address
 */
function codeAddress(address) {
    geocoder = new google.maps.Geocoder();
    geocoder.geocode({
        'address': address
    }, function(results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            var myOptions = {
                zoom: 8,
                center: results[0].geometry.location,
                mapTypeId: google.maps.MapTypeId.ROADMAP
            }
            map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

            var marker = new google.maps.Marker({
                map: map,
                position: results[0].geometry.location
            });
        }
    });
}

/**
 * Ao clicar em uma instância, está função posiciona o mapa no centro da instancia.
 * @param myPoint
 *//*
function gotoPoint(myPoint){
    map.setCenter(new google.maps.LatLng(marker[myPoint-1].position.lat(), marker[myPoint-1].position.lng()));
    marker[myPoint-1]['infowindow'].open($map, marker[myPoint-1]);
}*/

//google.maps.event.addDomListener(window, 'load', initialize);

/*
$(document).ready(function() {
	$(".drag").draggable({helper: 'clone',
	iframeFix: true,
    start: function () {
        $("div#map-canvas").css('z-index', '-1');
    },
	stop: function(e,ui) {
		$("div#map-canvas").css('z-index', '0');
		window.createMarker(ui.position);
	    }
	});
});


function createMarker(position) {
	//Adjust Offset
	var offset = {
		left : 10,
		top : -5
	}

	//Create a new GPoint
	var myGPoint = new google.maps.Point(position.left + offset.left, position.top
			+ offset.top);

	//Calculate the LatLng for this point
	var overlay = new google.maps.OverlayView();
	overlay.setMap(map);
	
	var myLatLng = overlay.getProjection().fromLatLngToContainerPixel(myGPoint);

	//Create the Marker and add it to the Map
	var marker = new google.maps.GMarker(myLatLng);
	map.addOverlay(marker);
}*/
	
   /**
	 * Recebe ums lista de instâncias de objetos com respectivas urls dos icones de seus objetos e aplica no google maps
	 * Função não está mais sendo utilizada.
	 * @param intancias_objetos_json
	 
	function placeListMakers(instancias){
		
			
			//loop para ler intancias_objetos_json
			for (i=0;i<instancias.length;i++){
				//alert(instancias[i].id + " " + instancias[i].nome + " " + instancias[i].url_icone + " " + instancias[i].lat + " " + instancias[i].lng + " " + instancias[i].altd);
				//cria um novo marcador para a instância do objeto
				 var location = new google.maps.LatLng(instancias[i].lat, instancias[i].lng);
				 
				 var marker = new google.maps.Marker({		
					  map: $map,
					  position: location, 
					  draggable:true,	
					  icon:	 instancias[i].url_icone,
					  zIndex: 5
				  });
				  
				  //http://jsfiddle.net/kjy112/3CvaD/
				  marker['infowindow'] = new google.maps.InfoWindow({
			            content: "<div id='instancia"+instancias[i].nome+"' class='form-actions'> Instância de " + instancias[i].nome  +" </div>"
			            //construir dados 
			      });
				  
				  google.maps.event.addListener(marker, 'click', function() {
				       this['infowindow'].open($map, this);
				  });
				  
				  markers.push(marker);
				  marker.metadata = {id: instancias[i].id};
		  	       
				 google.maps.event.addListener(marker, 'dragend', function() {
			            var curLatLng = marker.getPosition();
			          
			            //atualiza a posicao para novo drag drop
			    		json_pos = '[{"latitude":"' + curLatLng.lat() + '"' + ',"longitude":"' + curLatLng.lng() + '"' + ',"altitude":"' + '0.0' + '"' + ',"instancia_objeto_id":"' + marker.metadata.id + '"}]';
			    		$.ajax({
					   			 headers: { "X-CSRFToken": getCookie("csrftoken") },
					   		     type:"POST",
					   		     url:'/editor_objetos/posicao_geografica/update_pos/',
					   		     data: json_pos,
					   		     success: function(data,status){
					   		    	 	alert("eita");
					   		     },
							     error: function(xhr) {
							        	alert("Erro ao salvar posicao geografica do objeto.");
							     }
			    		});
			        });
			}
		
	}//fim da placeListMakers
	*/