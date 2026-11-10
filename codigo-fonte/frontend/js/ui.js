// GymManager — utilitários de interface (GYM-SRC-006)

// Escapa texto vindo da API antes de inserir em HTML (proteção contra XSS).
export function esc(valor) {
  return String(valor ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

export const $ = (seletor, raiz = document) => raiz.querySelector(seletor);
export const $$ = (seletor, raiz = document) => [...raiz.querySelectorAll(seletor)];

// ---------------------------------------------------------------- mensagens
export function aviso(mensagem, tipo = "sucesso") {
  const area = $("#avisos");
  const item = document.createElement("div");
  item.className = `aviso aviso-${tipo}`;
  item.setAttribute("role", tipo === "erro" ? "alert" : "status");
  item.textContent = mensagem;
  area.appendChild(item);
  while (area.children.length > 3) area.firstElementChild.remove();
  setTimeout(() => item.remove(), 4500);
}

export function erro(e) {
  aviso(e?.message || "Erro inesperado.", "erro");
}

export function confirmar(mensagem) {
  return window.confirm(mensagem);
}

// Mostra o erro de validação junto ao campo indicado pela API, quando houver.
export function erroNoFormulario(form, e) {
  $$(".campo-erro", form).forEach((n) => n.remove());
  $$(".invalido", form).forEach((n) => n.classList.remove("invalido"));
  const campo = e?.campo && form.elements.namedItem(e.campo);
  if (campo && campo.closest) {
    campo.classList.add("invalido");
    const msg = document.createElement("small");
    msg.className = "campo-erro";
    msg.textContent = e.message;
    campo.closest("label")?.appendChild(msg);
    campo.focus();
  }
  erro(e);
}

// ---------------------------------------------------------------- formatação
export function dataBR(iso) {
  if (!iso) return "—";
  const [a, m, d] = iso.slice(0, 10).split("-");
  return `${d}/${m}/${a}`;
}

export function dataHoraBR(iso) {
  if (!iso) return "—";
  const data = new Date(iso);
  return data.toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" });
}

export function kg(valor) {
  if (valor === null || valor === undefined) return "—";
  return `${Number(valor).toLocaleString("pt-BR", { maximumFractionDigits: 2 })} kg`;
}

export function iniciais(nome) {
  return (nome || "?")
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((p) => p[0].toUpperCase())
    .join("");
}

export function hojeISO() {
  const d = new Date();
  return new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
}

export function selo(ativo, textos = ["Ativo", "Inativo"]) {
  return `<span class="selo ${ativo ? "selo-ok" : "selo-off"}">${ativo ? textos[0] : textos[1]}</span>`;
}

// ---------------------------------------------------------------- formulários
// Lê os campos do formulário; campos vazios viram null; números convertidos.
export function lerFormulario(form) {
  const dados = {};
  for (const campo of form.elements) {
    if (!campo.name || campo.disabled) continue;
    if (campo.type === "checkbox") dados[campo.name] = campo.checked;
    else if (campo.type === "number") dados[campo.name] = campo.value === "" ? null : Number(campo.value);
    else dados[campo.name] = campo.value.trim() === "" ? null : campo.value.trim();
  }
  return dados;
}

export function opcoes(lista, selecionado, rotulo = (x) => x.nome, valor = (x) => x.id) {
  return lista
    .map((x) => `<option value="${esc(valor(x))}" ${String(valor(x)) === String(selecionado) ? "selected" : ""}>${esc(rotulo(x))}</option>`)
    .join("");
}

// ---------------------------------------------------------------- gráfico
// Gráfico de linha em SVG (sem estilos inline, compatível com a CSP).
export function graficoLinha(pontos, { rotuloY = (v) => v } = {}) {
  if (!pontos.length) return `<p class="vazio">Sem registros para este exercício.</p>`;
  const L = 560, A = 220, ME = 48, MD = 16, MT = 16, MB = 34;
  const valores = pontos.map((p) => p.valor);
  let min = Math.min(...valores), max = Math.max(...valores);
  if (min === max) { min = Math.max(0, min - 5); max = max + 5; }
  const x = (i) => ME + (pontos.length === 1 ? (L - ME - MD) / 2 : (i * (L - ME - MD)) / (pontos.length - 1));
  const y = (v) => MT + (A - MT - MB) * (1 - (v - min) / (max - min));
  const linhas = [0, 0.5, 1].map((f) => {
    const v = min + (max - min) * f;
    return `<line x1="${ME}" x2="${L - MD}" y1="${y(v)}" y2="${y(v)}" class="g-grade"/>
            <text x="${ME - 8}" y="${y(v) + 4}" text-anchor="end" class="g-texto">${esc(rotuloY(Math.round(v * 10) / 10))}</text>`;
  }).join("");
  const caminho = pontos.map((p, i) => `${i ? "L" : "M"}${x(i).toFixed(1)},${y(p.valor).toFixed(1)}`).join(" ");
  const marcas = pontos.map((p, i) => `<circle cx="${x(i)}" cy="${y(p.valor)}" r="4" class="g-ponto"><title>${esc(p.rotulo)}: ${esc(rotuloY(p.valor))}</title></circle>`).join("");
  const passo = Math.max(1, Math.ceil(pontos.length / 6));
  const eixoX = pontos.map((p, i) => (i % passo === 0 || i === pontos.length - 1)
    ? `<text x="${x(i)}" y="${A - 10}" text-anchor="middle" class="g-texto">${esc(p.rotulo)}</text>` : "").join("");
  return `<svg viewBox="0 0 ${L} ${A}" class="grafico" role="img" aria-label="Evolução">
    ${linhas}<path d="${caminho}" class="g-linha"/>${marcas}${eixoX}</svg>`;
}
