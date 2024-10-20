function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: -34.9827900, lng: -71.2394300 },  // Coordenadas iniciales
        zoom: 8
    });

    fetch('/api/obtener_profesionales')
        .then(response => response.json())
        .then(profesional => {
            profesional.forEach(prof => {
                const marker = new google.maps.Marker({
                    position: { lat: parseFloat(prof.latitud), lng: parseFloat(prof.longitud) },
                    map: map,
                    title: prof.nombre
                });

                const infoWindow = new google.maps.InfoWindow({
                    content: `<h3>${prof.nombre}</h3>
                    <p>${prof.especializacion}</p>
                    <p>${prof.telefono}</p> 
                     <button onclick="openModal()" class="btn btn-primary">Agendar Cita</button>`
                });

                marker.addListener('click', function() {
                    infoWindow.open(map, marker);
                });
            });
        })
        .catch(error => {
            console.error('Error al cargar los profesionales:', error);
        });   
}

function openModal() {
    var agendarCitaModal = new bootstrap.Modal(document.getElementById('agendarCitaModal'));
    agendarCitaModal.show();
}