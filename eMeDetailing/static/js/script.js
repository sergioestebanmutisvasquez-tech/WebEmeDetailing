// ======================================================
// IA: ChatGPT ayudó a mejorar:
// - Sanitización contra XSS
// - Validaciones con regex
// - Codificación segura del mensaje para WhatsApp
// - Modularización de funciones
// - Manipulación segura del DOM con createElement y textContent
// - Sistema de reserva tipo carrito
// ======================================================

// ======================================================
// VARIABLES PRINCIPALES
// ======================================================

let consultas = [];
let reservas = [];
let servicioSeleccionado = null;

// ======================================================
// SANITIZACIÓN
// ======================================================

function sanitizar(texto) {
    return texto
        .replace(/[<>"'`]/g, "")
        .replace(/\s+/g, " ")
        .trim();
}

// ======================================================
// VALIDACIONES GENERALES
// ======================================================

function validarEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

function validarNombre(nombre) {
    const regex = /^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$/;
    return regex.test(nombre);
}

function validarVehiculo(vehiculo) {
    const vehiculosPermitidos = ["Citycar", "Sedan", "SUV"];
    return vehiculosPermitidos.includes(vehiculo);
}

function validarTelefono(telefono) {
    const regex = /^[0-9]{9}$/;
    return regex.test(telefono);
}



function validarFechaReserva(fecha) {
    const fechaSeleccionada = new Date(fecha + "T00:00:00");
    const hoy = new Date();

    hoy.setHours(0, 0, 0, 0);

    return fechaSeleccionada >= hoy;
}

function validarHoraReserva(hora) {
    return hora >= "09:00" && hora <= "19:00";
}

// ======================================================
// FORMATO PRECIO
// ======================================================

function formatearPrecio(valor) {
    return Number(valor).toLocaleString("es-CL", {
        style: "currency",
        currency: "CLP"
    });
}

// ======================================================
// SISTEMA DE CARRITO / RESERVA
// ======================================================

function seleccionarServicio(boton) {
    servicioSeleccionado = {
        nombre: boton.dataset.servicio,
        precios: {
            Citycar: Number(boton.dataset.citycar),
            Sedan: Number(boton.dataset.sedan),
            SUV: Number(boton.dataset.suv)
        }
    };

    actualizarCarrito();

    document.getElementById("reserva").scrollIntoView({
        behavior: "smooth"
    });
}


function actualizarCarrito() {
    const carritoServicio = document.getElementById("carritoServicio");
    const carritoTotal = document.getElementById("carritoTotal");
    const vehiculo = document.getElementById("vehiculo").value;
    const campoServicio = document.getElementById("servicioReserva");

    if (!servicioSeleccionado) {
        carritoServicio.textContent =
            "Aún no has seleccionado un servicio.";

        carritoTotal.textContent = "";
        campoServicio.value = "";
        return;
    }

    campoServicio.value = servicioSeleccionado.nombre;

    carritoServicio.textContent =
        `Servicio: ${servicioSeleccionado.nombre}`;

    if (vehiculo && servicioSeleccionado.precios[vehiculo]) {
        carritoTotal.textContent =
            `Total: ${formatearPrecio(servicioSeleccionado.precios[vehiculo])}`;
    } else {
        carritoTotal.textContent =
            "Selecciona el tipo de vehículo para calcular el total.";
    }
}


function validarFormularioReserva(datos) {
    if (!servicioSeleccionado) {
        return "Debes seleccionar un servicio antes de reservar";
    }

    if (
        !datos.nombre ||
        !datos.email ||
        !datos.telefono ||
        !datos.vehiculo ||
        !datos.direccion ||
        !datos.fecha ||
        !datos.hora
    ) {
        return "Todos los campos de reserva son obligatorios";
    }

    if (datos.nombre.length < 3 || datos.nombre.length > 50) {
        return "El nombre debe tener entre 3 y 50 caracteres";
    }

    if (!validarNombre(datos.nombre)) {
        return "El nombre solo puede contener letras y espacios";
    }

    if (datos.email.length > 50) {
        return "El email no puede superar los 50 caracteres";
    }

    if (!validarEmail(datos.email)) {
        return "El Email ingresado no es válido";
    }

    if (!validarTelefono(datos.telefono)) {
        return "El teléfono debe contener solo números y tener 9 dígitos";
    }

    if (!validarVehiculo(datos.vehiculo)) {
        return "Debes seleccionar un vehículo válido";
    }

    if (datos.direccion.length < 8 || datos.direccion.length > 60) {
        return "La dirección debe tener entre 8 y  60 caracteres";
    }

    if (!validarFechaReserva(datos.fecha)) {
        return "La fecha de reserva no puede ser anterior al día actual";
    }

    if (!validarHoraReserva(datos.hora)) {
        return "La hora debe estar entre las 09:00 y las 19:00";
    }

    return null;
}

function mostrarMensajeReserva() {
    const mensajeReserva = document.getElementById("mensajeReserva");

    mensajeReserva.textContent =
        "Se abrirá WhatsApp para solicitar tu reserva. Aún no se guarda en la base de datos.";
}

function limpiarMensajeReserva() {
    const mensajeReserva = document.getElementById("mensajeReserva");
    mensajeReserva.textContent = "";
}


function enviarReserva(evento) {
    limpiarMensajeReserva();

    if (!servicioSeleccionado) {
        evento.preventDefault();
        alert("Debes seleccionar un servicio.");
        return;
    }

    const datos = {
        nombre: document.getElementById("nombre").value,
        email: document.getElementById("email").value,
        telefono: document.getElementById("telefono").value,
        vehiculo: document.getElementById("vehiculo").value,
        direccion: document.getElementById("direccion").value,
        fecha: document.getElementById("fechaReserva").value,
        hora: document.getElementById("horaReserva").value
    };

    const error = validarFormularioReserva(datos);

    if (error) {
        evento.preventDefault();
        alert(error);
        return;
    }

    document.getElementById("servicioReserva").value =
        servicioSeleccionado.nombre;
}

// ======================================================
// GALERÍA CON FLECHAS
// ======================================================

function activarGaleria() {
    const galeriaScroll = document.getElementById("galeriaScroll");
    const flechaIzquierda = document.getElementById("flechaIzquierda");
    const flechaDerecha = document.getElementById("flechaDerecha");

    flechaIzquierda.addEventListener("click", () => {
        galeriaScroll.scrollBy({
            left: -300,
            behavior: "smooth"
        });
    });

    flechaDerecha.addEventListener("click", () => {
        galeriaScroll.scrollBy({
            left: 300,
            behavior: "smooth"
        });
    });
}

// ======================================================
// INIT
// ======================================================

document.addEventListener("DOMContentLoaded", () => {

    document.getElementById("servicioReserva").value =
    servicioSeleccionado ? servicioSeleccionado.nombre : "";
    
    document
        .getElementById("reservaForm")
        .addEventListener("submit", enviarReserva);

    document
        .getElementById("vehiculo")
        .addEventListener("change", actualizarCarrito);

    document.querySelectorAll(".btn-servicio").forEach((boton) => {
        boton.addEventListener("click", () => {
            seleccionarServicio(boton);
        });
    });

    activarGaleria();
});


const fotoVehiculo = document.getElementById("fotoVehiculo");
const quitarImagen = document.getElementById("quitarImagen");

if (fotoVehiculo && quitarImagen) {
    fotoVehiculo.addEventListener("change", function () {
        quitarImagen.style.display = this.files.length > 0
            ? "inline-block"
            : "none";
    });

    quitarImagen.addEventListener("click", function () {
        fotoVehiculo.value = "";
        quitarImagen.style.display = "none";
    });
}

