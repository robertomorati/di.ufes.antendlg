/**
 * Created on --/10/2013
 * 
 * @author: Roberto Guimaraes Morati Junior
 */		


//flags criadas para tratar cados especificos. 
var flagloadInstancias = false; //flag para evitar chamada do "ajax" que cria a POS da instância do objeto.
var flagloadBackupInstances = false;//flag para controlar "pesistência" de instâncias.	 

var intancias_objetos_json; //armazena backup das instâncias para evitar requisições desnecessárias. 


/**
 * Atualiza posição para o google maps, caso a aventura tenha uma posicao
 */
var $latlng;
function carregaPos (){
	
    //var $latlng = new google.maps.LatLng(-20.274636854719642, -40.304203033447266);
	var id = aventuraAtiva()
	if(id != '-1'){
		 
		 var urlView = '/editor_objetos/get_json_aventura/' + id +'/';
		 $.ajax({
		        type: 'GET',
		        url: urlView,
		        cache: false,
		        async: false,
		        success: function(response) {
		        	var obj = $.parseJSON(response);
		    		$latlng = new google.maps.LatLng(obj[0].fields.latitude, obj[0].fields.longitude);
		    		initialize();
	        },
	        error: function() {
	        	alert("Erro ao recuperar tipos de objetos...Xiiii ;)");
	        }
		});	
	}else{
		$latlng = new google.maps.LatLng(-30.068637, -51.120404);
		initialize();
	}

}

/**
 * Função que inicializa o google maps -v3
 * 
 */
var $map;//google maps
var overlay;
var markers = [];
function initialize() {
	
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

    // This is needed to set the zoom after fitbounds, 
    //Localiza novo local para aventura e faz ajuste do zoom
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

    
     // Create the search box and link it to the UI element.
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
            //Com o intuito de limitar a mensagem para que parecer somente uma vez, criei a flagCount.
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
		       var urlView = '/editor_objetos/set_json_aventura/';
		       urlView += id_aventura + '/'; 
		       
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
		loadInstancias();
} 
	
/**
 * Cria a instância de um objeto.
 * 
 * @param location - localização da instância
 * @param icon - imagem para add ao marcador
 * @param id - id do objeto a qual a instância pertence
 * @param name_objeto  - nome da instância
 * @param quantidade - quandidade permitida de instâncias
 */
function createInstance(location,icon, id, name_objeto) {


  //json para criação da instância do objeto
  var json_instancia_objeto = '[{"nome":"' + name_objeto + '"' + ',"id_objeto":"' + id +'"}]';
  urlView = '/editor_objetos/instancia_objeto/create_instancia/';
  
  $.ajax({
		 headers: { "X-CSRFToken": getCookie("csrftoken") },//token django
	     type:"POST",
	     url:urlView,
	     data: json_instancia_objeto,
	     success: function(data,status){
	    	 if(data.pk == 0){
	    		 alert("Impossível criar mais instâncias do objeto " + name_objeto + ". Quantidade de isntâncias no limite.");
	    	 }else{
	    		    //cria uma nova instância, e atualiza o backup de instâncias
	    		    flagloadBackupInstances = false;
	    		    flagloadInstancias = false;
	    		    loadInstancias();
	    		 	placeInstancesGoogleMaps(location,icon, data.pk, name_objeto);
			    	
	    	 	}//fim do else
	     },
	     error: function(xhr) {
	        	alert("Erro criar instância do objeto.");
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
	    	  					flagloadBackupInstances = false;//set flag to upadte instances
	    	  					loadInstancias();//update isntances
	    	  					
	    	  				}else if (ct.indexOf('json') > -1) {
	    	  					 info.close();//após atualizar fecha a infowindow
	    	  				}
	    	  			}
	    	  			
	    	  			function showsomething(){
	    	  				alert("Ocorreu um erro ao recuperar o conteúdo da instância. Por gentileza, tente a operação novamente!");
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
	  
	  markers.push(marker);
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
		   		    	 //pos salva
		   		     },
				     error: function(xhr) {
				        	alert("Erro ao salvar posicao geografica do objeto.");
				     }
			});
			
	   }//fim do if
	
	 //Quando o marcador/instância é arrastado, é feito o update da sua POS
     google.maps.event.addListener(marker, 'dragend', function() {
     
    	 var curLatLng = marker.getPosition();
    	 
        //json contendo nova pos
  		json_pos = '[{"latitude":"' + curLatLng.lat() + '"' + ',"longitude":"' + curLatLng.lng() + '"' + ',"altitude":"' + '0.0' + '"}]';
  			$.ajax({
	   			 headers: { "X-CSRFToken": getCookie("csrftoken") },
	   		     type:"POST",
	   		     url:'/editor_objetos/posicao_geografica/update_pos/'+marker.metadata.id+'/',
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
      });// fim da  google.maps.event.addListener
         
}//fim da função

/**
 * Carrega instâncias do objeto.
 * 
 */
function loadInstancias(){
	
	//verifica se a aventura está ativa
	var aventura_id = aventuraAtiva();
	if(aventura_id != '-1'){
		urlView = '/editor_objetos/instancia_objeto/get_instancia/' + aventura_id  + '/';
    		
    	if(flagloadBackupInstances == false){
 
			//ajax to get all instances by aventura_id
			$.ajax({
	   		     type:"GET",
	   		     url:urlView,
	   		     success: function(data,status){
	   		    	 
	   		    	flagloadBackupInstances = true;//altera flag
	   		    	intancias_objetos_json = data;//backup das instâncias atualizado
	   		     },
			     error: function(xhr) {
			        	alert("Erro ao recuperar lista de instâncias de objetios.");
			     }
			});
			
		}else{
			//carrega instancias
			var instancias = $.parseJSON(intancias_objetos_json);
			for (i=0;i<instancias.length;i++){  	
				var loc = new google.maps.LatLng(instancias[i].lat, instancias[i].lng);
				placeInstancesGoogleMaps(loc,instancias[i].url_icone, instancias[i].id, instancias[i].nome );
			}
			
		}
	}else{
		intancias_objetos_json = "";//limpa backup
	}
	
}
	
/**
 * Função para verificar se uma aventura está ativa
 */
function aventuraAtiva(){
	
	//verifica se existe alguma aventura ativa na barra do usuário
	var aventura_id = '-1';
	if($('body').find('aventura_ativa_id').attr('id')>0)
		aventura_id = $('body').find('aventura_ativa_id').attr('id');
	
	return aventura_id;
}





/**
 * Ao clicar em uma instância, está função posiciona o mapa no centro da instancia.
 * @param myPoint
 *
function gotoPoint(myPoint){
    map.setCenter(new google.maps.LatLng(marker[myPoint-1].position.lat(), marker[myPoint-1].position.lng()));
    marker[myPoint-1]['infowindow'].open(map, marker[myPoint-1]);
}/

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
/*********************************************************************************************
 *                                  Código Antigo											 *
 ********************************************************************************************/	    
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