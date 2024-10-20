function cargarProfesionales() {
    console.log("Cargando profesionales...");  // Esto debería aparecer en la consola al hacer clic
    fetch('/api/obtener_profesionales')
      .then(response => response.json())
      .then(data => {
        console.log(data);
        const offCanvasContent = document.getElementById("offCanvasContent");
        offCanvasContent.innerHTML = '';
        if (data.length === 0) {
          offCanvasContent.innerHTML = '<p>No hay profesionales disponibles.</p>';
          return;
        }
        data.forEach(profesional => {
          const profesionalHTML = `
            <div class="info-panel text-center">
              <h5>Nombre: ${profesional.nombre}</h5>
              <p>Especialización: ${profesional.especializacion}</p>
              <p>Teléfono: ${profesional.telefono}</p>
              <h6>Ubicación</h6>
              <p>Latitud: ${profesional.latitud}, Longitud: ${profesional.longitud}</p>
            </div>
            <hr>
          `;
          offCanvasContent.innerHTML += profesionalHTML;
        });
      })
      .catch(error => {
        console.error('Error al cargar los profesionales:', error);
      });
  }
  