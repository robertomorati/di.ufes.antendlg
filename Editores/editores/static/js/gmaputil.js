		
		var intancias_objetos_json;//backup das instâncias do servidor para evitar requisições desnecessárias. 
 	   
		/**
		 * Função que inicializa o google maps v3
		 * 
		 */
		var $map;
        var $latlng;
        var overlay;
        var markers = [];
        //flag para evitar a chamada desnecessária do "ajax" que cria a POS da instância do objeto. Por exemplo, no momento que o objeto é arrastado.
        var flagloadInstancias = false; 
        var flagloadBackupInstances = false;
        function initialize() {
        
        	//ponto inicial do mapa
	        var $latlng = new google.maps.LatLng(-30.068637, -51.120404);
	        //var $latlng = new google.maps.LatLng(-20.274636854719642, -40.304203033447266);
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
	        //após localizar um novo local para a aventura, este "código" faz o "ajuste" do zoom
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
		            
		            //Algumas cidades apresentam problemas ao serem localizadas, retornando mais de um POS.
		            //Desta forma desencadeia uma quantidade absurdade de mensagens para o usuário, devido a requisição de salva POS estar dentro do for.
		            //Com o intuito de limitar a mensagem a aparecer somente uma vez, criamos a flagCount.
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
						    	 //matém o zoom 15...
						      	 if(flagCount == 0){  
						      		 	//recupera instâncias de objeto para aventura
						      		 	flagloadInstancias = true;
						      		 	flagloadBackupInstances = true;
						      		 	loadInstancias();
						      		    $map.setZoom(15);
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
           // [END region_getplaces]

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
	 * Cria a instância do objeto
	 * 
	 * @param location
	 * @param icon
	 * @param id
	 * @param name_objeto
	 * @param quantidade
	 */
	function placeMarker(location,icon, id, name_objeto) {

    
	  //json para criação da instância do objeto
	  var json_instancia_objeto = '[{"nome":"' + name_objeto + '"' + ',"id_objeto":"' + id +'"}]';
	  urlView = '/editor_objetos/instancia_objeto/create_instancia/';
	  
      $.ajax({
			 headers: { "X-CSRFToken": getCookie("csrftoken") },
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
		    		 	placeInstancesGoogleMap(location,icon, data.pk, name_objeto);
				    	
		    	 	}//fim do else
		     },
		     error: function(xhr) {
		        	alert("Erro criar instância do objeto.");
		     }
		 });

	}
	
	/**
	 * 
	 * 
	 */
	/*function atualizaPosicaoAventura(urlView) {
		 $.ajax({
		        type: 'GET',
		        url: urlView,
		        cache: false,
		        async: false,
		        success: function(response) {
		        	var obj = $.parseJSON(response);
		        	
		        }
		
	        },
	        error: function() {
	        	alert("Erro ao recuperar tipos de objetos...Xiiii ;)");
	        }
		});
	 }*/

	
	/**
	 * Função para adicionar instância no mapa
	 * @param location
	 * @param icon
	 * @param id_instancia
	 * @param name_objeto
	 * @param interacoes
	 */
	function placeInstancesGoogleMap(location,icon, id_instancia, name_objeto){
		
		  //cria uma instância do objeto, quando o mesmo é arrastado para o mapa
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
		  //http://jsfiddle.net/kjy112/3CvaD/
		  var nameInfo = 'infoWindow' + name_objeto;
		  marker[nameInfo] = new google.maps.InfoWindow({ 
			    maxWidth: 600,
	      });
		  
		  var info;
		  google.maps.event.addListener(marker, 'click', function() {
	
		       urlIO = '/editor_objetos/instancia_objeto/update_instancia/' +  marker.metadata.id + '/';
		       
		       this[nameInfo].open($map, this);
		       info = this[nameInfo];
		       var rmMaker = marker;
		       //De acordo com "fontes" no stackoverflow, a forma mais eficiente para carregar o conteúdo na infowindow é por meio de ajax.
		       $.ajax({	
		    	    type: 'GET',
		    	    url: urlIO,
		    	    success: function(data){

		    	  
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
		    	  					flagloadBackupInstances = false;//atualizar backup de instâncias que estão sendo editadas
		    	  					loadInstancias();
		    	  				}else if (ct.indexOf('json') > -1) {
		    	  					 info.close();//após atualizar fecha a infowindow
		    	  				}
		    	  			}
		    	  			
		    	  			function showsomething(){
		    	  				alert("Ocorreu um erro ao recuperar o conteúdo da instância. Por gentileza, tente a operação novamente!");
		    	  			}

		    	  			$('#instancia_objeto_update_view').ajaxForm(options);
		    	  			$('#instancia_objeto_delete_view').ajaxForm(options);
		    	    	  
		    	      });//fim do script para tratar o json
		    	    	
		    	       info.setContent(data);
		    	       
		    	    },
				     error: function(xhr) {
				        	alert("Ocorreu um erro ao carregar os dados da instância!");
				     }
		    	});
		       
		  });
		  
		  markers.push(marker);
	     //add id da instância no marcado
		  marker.metadata = {id: id_instancia};
		
		   //só cria posição caso for uma nova instância
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
				});//fim fo ajax
		   }//fim do if
		
			 //qndo o marcador é largado novamente é feito o update.
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
	         
	}//fim da funcion
	
	/**
	 * Carrega instâncias do objeto
	 * 
	 * Momentos em que está função ocorre: 
	 * -ativação de aventura;
	 * -sair e voltar para o google maps;
	 * -criar nova instância, atualiza o backup
	 */
	function loadInstancias(){
		
		//verifica se existe alguma aventura ativa na barra do usuário
		var aventura_id = '-1';
		if($('body').find('aventura_ativa_id').attr('id')>0)
			aventura_id = $('body').find('aventura_ativa_id').attr('id');

		if(aventura_id != '-1'){
    		urlView = '/editor_objetos/instancia_objeto/get_instancia/' + aventura_id  + '/';
    		
    		if(flagloadBackupInstances == false){
 
				//ajax to get all instances by aventura_id
				$.ajax({
		   		     type:"GET",
		   		     url:urlView,
		   		     success: function(data,status){
		   		    	 
		   		    	flagloadBackupInstances = true;
		   		    	intancias_objetos_json = data;//backup das instâncias
		   		    
		   		     
		   		     },
				     error: function(xhr) {
				        	alert("Erro ao recuperar lista de instâncias de objetios.");
				     }
				});
    		}//fim do if flagloadBackupInstances
    		else{
    			
    			var instancias = $.parseJSON(intancias_objetos_json);
    			for (i=0;i<instancias.length;i++){  	
    				var loc = new google.maps.LatLng(instancias[i].lat, instancias[i].lng);
    				placeInstancesGoogleMap(loc,instancias[i].url_icone, instancias[i].id, instancias[i].nome );
    			}
    			
    		}
		}else{
			intancias_objetos_json = "";//limpa backup
		}
		
	}
	
	
	
	
	
	/**
	 * Ao clicar na instâ, está função posiciona o mapa, o centro do mapa na instancia.
	 * @param myPoint
	 */
	function gotoPoint(myPoint){
	    map.setCenter(new google.maps.LatLng(marker[myPoint-1].position.lat(), marker[myPoint-1].position.lng()));
	    marker[myPoint-1]['infowindow'].open(map, marker[myPoint-1]);
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