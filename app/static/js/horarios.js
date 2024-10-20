function cargarHorasDisponibles(profesionalId) {
    console.log("Cargando horas disponibles para el profesional:", profesionalId);

    fetch(`/api/obtener_horas/${profesionalId}`)
        .then(response => response.json())
        .then(horas => {
            const horasContainer = document.getElementById("horasDisponibles");
            horasContainer.innerHTML = "";  // Limpiar el contenido anterior

            if (Object.keys(horas).length === 0) {
                horasContainer.innerHTML = "<p>No hay horas disponibles</p>";
                return;
            }

            for (let dia in horas) {
                const diaElement = document.createElement("h5");
                diaElement.textContent = dia;
                horasContainer.appendChild(diaElement);

                const ul = document.createElement("ul");
                horas[dia].forEach(hora => {
                    const li = document.createElement("li");
                    li.textContent = hora;
                    ul.appendChild(li);
                });
                horasContainer.appendChild(ul);
            }
        })
        .catch(error => {
            console.error('Error al cargar las horas disponibles:', error);
            document.getElementById("horasDisponibles").innerHTML = "<p>Error al cargar las horas disponibles</p>";
        });
}