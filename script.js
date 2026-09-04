document.getElementById("year").textContent = new Date().getFullYear();

const form = document.getElementById("booking-form");
const success = document.getElementById("form-success");

const rules = {
  nombre: (v) => (v.trim().length >= 2 ? "" : "Escribe tu nombre."),
  telefono: (v) =>
    /^[0-9+\s().-]{9,}$/.test(v.trim()) ? "" : "Escribe un teléfono válido.",
  email: (v) =>
    v.trim() === "" || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v.trim())
      ? ""
      : "Escribe un email válido.",
  motivo: (v) => (v ? "" : "Elige un motivo."),
  franja: (v) => (v ? "" : "Elige una franja."),
  privacidad: (_, el) => (el.checked ? "" : "Necesitamos tu consentimiento."),
};

function validateField(name) {
  const el = form.elements[name];
  const message = rules[name](el.value, el);
  const slot = form.querySelector(`[data-error-for="${name}"]`);
  if (slot) slot.textContent = message;
  el.closest(".field")?.classList.toggle("invalid", Boolean(message));
  el.setAttribute("aria-invalid", message ? "true" : "false");
  return !message;
}

// Revalidar en cuanto el usuario corrige un campo ya marcado como erróneo.
Object.keys(rules).forEach((name) => {
  const el = form.elements[name];
  el.addEventListener("blur", () => validateField(name));
  el.addEventListener("input", () => {
    if (el.getAttribute("aria-invalid") === "true") validateField(name);
  });
});

form.addEventListener("submit", (event) => {
  event.preventDefault();

  const results = Object.keys(rules).map(validateField);
  if (results.includes(false)) {
    form.querySelector('[aria-invalid="true"]')?.focus();
    return;
  }

  // Sin backend: aquí iría el envío real (fetch a tu API, Formspree, etc.).
  console.log("Solicitud de cita:", Object.fromEntries(new FormData(form)));

  form.reset();
  success.hidden = false;
  success.scrollIntoView({ block: "center", behavior: "smooth" });
});
