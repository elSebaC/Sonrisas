document.getElementById("anio").textContent = new Date().getFullYear();

const formulario = document.getElementById("formulario-cita");
const confirmacion = document.getElementById("confirmacion");

const reglas = {
  nombre: (v) => (v.trim().length >= 2 ? "" : "Escribe tu nombre."),
  telefono: (v) =>
    /^[0-9+\s().-]{9,}$/.test(v.trim()) ? "" : "Escribe un teléfono válido.",
  motivo: (v) => (v ? "" : "Elige una opción."),
  franja: (v) => (v ? "" : "Elige una opción."),
  privacidad: (_, el) => (el.checked ? "" : "Marca la casilla para continuar."),
};

function validarCampo(nombre) {
  const el = formulario.elements[nombre];
  const mensaje = reglas[nombre](el.value, el);
  const hueco = formulario.querySelector(`[data-error-de="${nombre}"]`);
  if (hueco) hueco.textContent = mensaje;
  el.closest(".campo")?.classList.toggle("invalido", Boolean(mensaje));
  el.setAttribute("aria-invalid", mensaje ? "true" : "false");
  return !mensaje;
}

// Revalida en cuanto alguien corrige un campo ya marcado en rojo, para que
// el error desaparezca al arreglarlo y no al volver a enviar.
Object.keys(reglas).forEach((nombre) => {
  const el = formulario.elements[nombre];
  el.addEventListener("blur", () => validarCampo(nombre));
  el.addEventListener("input", () => {
    if (el.getAttribute("aria-invalid") === "true") validarCampo(nombre);
  });
});

formulario.addEventListener("submit", (evento) => {
  evento.preventDefault();

  const resultados = Object.keys(reglas).map(validarCampo);
  if (resultados.includes(false)) {
    formulario.querySelector('[aria-invalid="true"]')?.focus();
    return;
  }

  // Sin backend todavía: aquí va el envío real (Formspree, tu API, etc.).
  console.log("Solicitud de cita:", Object.fromEntries(new FormData(formulario)));

  formulario.reset();
  confirmacion.hidden = false;
  confirmacion.scrollIntoView({ block: "center", behavior: "smooth" });
});
