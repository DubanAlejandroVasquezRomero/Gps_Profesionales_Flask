document.getElementById("repetir_horario").addEventListener("change", function() {
    const diasRepetir = document.getElementById("dias_repetir");
    if (this.checked) {
        diasRepetir.style.display = "block";
    } else {
        diasRepetir.style.display = "none";
    }
});