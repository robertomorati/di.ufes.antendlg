		
 	    //Inicializa o Google Maps
		var $map;
        var $latlng;
        var overlay;
        var markers = [];
        var flagPosAventura = false;
       
        function initialize() {
        
	        var $latlng = new google.maps.LatLng(-20.274636854719642, -40.304203033447266);
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
	        google.maps.event.addListener($map, 'zoom_changed', function() {
	                zoomChangeBoundsListener = google.maps.event.addListener($map, 'bounds_changed', function(event) {
	                                if (this.getZoom() > 10 && this.initialZoom == true) {
	                                        // Change max/min zoom here
	                                        this.setZoom(15);
	                                        this.initialZoom = true;
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
			
			            for (var i = 0, marker; marker = markers[i]; i++) {
			              marker.setMap(null);
			            }
		
		            // For each place, get the icon, place name, and location.
		            //markers = [];
		            
		            //Algumas cidades apresentam problemas ao serem localizadas, retornando mais de um POS.
		            //Desta forma desencadeia uma quantidade absurdade de mensagens para o usuário, devido a requisição de salva POS estar dentro do for.
		            //Com o intuito de limitar a mensagem a aparecer somente uma vez, criamos a flagCount.
		            var flagCount = 0;
		            var bounds = new google.maps.LatLngBounds();
		            for (var i = 0, place; place = places[i]; i++) {
		              var image = {
		                url: place.icon,
		                size: new google.maps.Size(71, 71),
		                origin: new google.maps.Point(0, 0),
		                anchor: new google.maps.Point(17, 34),
		                scaledSize: new google.maps.Size(25, 25)
		              };
		
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
		              
		              //atualizar posicao da aventura que estiver ativa
				       jsonObj = '[{"latitude":"' + place.geometry.location.lat() + '"' + ',"longitude":"' + place.geometry.location.lng() + '"}]';
				      //get id aventura ativa
				       id_aventura = $('body').find('aventura_ativa_id').attr('id');
				       
				       var urlView = '/editor_objetos/set_json_aventura/';
				       urlView += id_aventura + '/'; //concatena url com id da aventura
				       
				       $.ajax({
							 headers: { "X-CSRFToken": getCookie("csrftoken") },
						     type:"POST",
						     url:urlView,
						     data: jsonObj,
						     success: function(data,status){	 
						    	 //alert("Data: " + data + "\nStatus: " + status + "   "); 
						    	 flagPosAventura = false;
						     },
						     error: function(xhr) {
						    	  if(flagCount == 0){
						        	alert("Erro ao atualizar posição geográfica da aventura. Certifique-se de que existe alguma aventura em modo de auntoria." +
						        		  " Ou vá para o meno Configurações Aventura -> Editar Aventura e ative uma aaventura para ser autorada!");
						        	flagCount += 1;
						     		}
						        }
						 });
		              
		            }
		
		
		            $map.fitBounds(bounds);
		            
		      		if(flagPosAventura == true && flagCount == 0){  
			            alert("A posição geográfica da aventura foi alterada com sucesso!");
			            flagPosAventura = false; 
			            flagCount += 1;
			      	}
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
        
        
        var infowindow = new google.maps.InfoWindow({
              content: "InstanciaObjeto"
          });
        


        
        } 
	
	/**
	 * Cria a instância do objeto
	 * 
	 * @param location
	 * @param icon
	 * @param id
	 * @param name_objeto
	 */
	function placeMarker(location,icon, id, name_objeto) {
	  //alert(location + icon + "   " + id  + "   " + name_objeto );
	  var marker = new google.maps.Marker({		
		  map: $map,
		  position: location, 
		  draggable:true,	
		  icon:	icon,
		  zIndex: 5
	  });
	  
	  //http://jsfiddle.net/kjy112/3CvaD/
	  marker['infowindow'] = new google.maps.InfoWindow({
            content: "<div id='instancia"+name_objeto+"' class='form-actions'> Instância de " + name_objeto  +" </div>"
      });
	  
	  google.maps.event.addListener(marker, 'click', function() {
	       this['infowindow'].open($map, this);
	  });
	  
	  markers.push(marker);
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
	 * Esta função ajusta o centro do mapa. Qual a necessidade disso?
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