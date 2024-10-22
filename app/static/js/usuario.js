function initMap() {
    const map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: -34.9827900, lng: -71.2394300 }, // Coordenadas iniciales
        zoom: 8
    });

    // Llamada para obtener los profesionales
    fetch('/api/obtener_profesionales', {
        method: 'POST', 
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return response.json();
    })
    .then(profesionales => {
        console.log("Profesionales cargados:", profesionales);

        profesionales.forEach(prof => {
            console.log("Datos del profesional:", prof);

            const marker = new google.maps.Marker({
                position: { lat: parseFloat(prof.latitud), lng: parseFloat(prof.longitud) },
                map: map,
                title: prof.nombre
            });

            const infoWindow = new google.maps.InfoWindow({
                content: `
                    <h3>${prof.nombre}</h3>
                    <p>${prof.especializacion}</p>
                    <p>${prof.telefono}</p>
                    <button class="btn btn-primary" type="button" 
                    onclick="cargarProfesionalEnOffCanvas('${prof.nombre}', '${prof.especializacion}', '${prof.telefono}', '${prof.latitud}', '${prof.longitud}', '${prof.hora_inicio}', '${prof.hora_fin}')">
                        Agendar Cita
                    </button>`
            });

            marker.addListener('click', () => {
                infoWindow.open(map, marker);
            });
        });
    })
    .catch(error => {
        console.error('Error al cargar los profesionales:', error);
    });
}

// Función para cargar los datos del profesional en el OffCanvas
function cargarProfesionalEnOffCanvas(nombre, especializacion, telefono, latitud, longitud, hora_inicio, hora_fin) {
    const offCanvasContent = document.getElementById("offCanvasContent");

    // Formatear las horas de inicio y fin, manejando casos de datos faltantes
    const inicio = hora_inicio ? formatearHora(hora_inicio) : 'No disponible';
    const fin = hora_fin ? formatearHora(hora_fin) : 'No disponible';

    // Actualiza el contenido del off-canvas con la información del profesional
    offCanvasContent.innerHTML = `
        <div class="info-panel text-center">
            <h5>Nombre: ${nombre}</h5>
            <p>Especialización: ${especializacion}</p>
            <p>Teléfono: ${telefono}</p>
            <h6>Disponibilidad:</h6>
            <p>Hora de Inicio: ${inicio}</p>
            <p>Hora de Fin: ${fin}</p>
        </div>
        <hr>
    `;

    const offcanvasRight = new bootstrap.Offcanvas(document.getElementById('offcanvasRight'));
    offcanvasRight.show();
}

// Función para formatear la hora en un formato más amigable (ej. 14:30 -> 2:30 PM)
function formatearHora(hora) {
    const [horas, minutos] = hora.split(':');
    let horasInt = parseInt(horas);
    const periodo = horasInt >= 12 ? 'PM' : 'AM';
    horasInt = horasInt % 12 || 12; // Convierte a formato de 12 horas
    return `${horasInt}:${minutos} ${periodo}`;
}
