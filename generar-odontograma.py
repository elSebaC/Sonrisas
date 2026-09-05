#!/usr/bin/env python3
"""Genera odontograma.svg: el esquema dental con numeracion FDI.

La notacion FDI divide la boca en cuatro cuadrantes y numera cada diente
con dos cifras (cuadrante + posicion desde el centro). Visto de frente,
el cuadrante 1 del paciente cae a la izquierda de quien mira.

Se genera con un script y no a mano porque son 32 dientes colocados sobre
una elipse: la trigonometria es mas fiable que escribir las rutas a ojo.
"""
import math
import pathlib

ANCHO, ALTO = 640, 380
CX = ANCHO / 2

# Arcos: (centro y, radio x, radio y, hacia donde se abre)
ARCO_SUP = dict(cy=196, rx=252, ry=150, signo=-1)
ARCO_INF = dict(cy=196, rx=232, ry=136, signo=1)

# Ancho y alto de corona por posicion desde el centro (1 incisivo -> 8 cordal).
CORONAS = {
    1: (19, 27), 2: (16, 24), 3: (17, 26),
    4: (18, 22), 5: (18, 21),
    6: (23, 23), 7: (22, 22), 8: (20, 21),
}

TRAZO = "#9fb8c2"
RELLENO = "#ffffff"
ETIQUETA = "#8fa3ab"
CRUZ = "#dbe4e7"

# Izquierda a derecha segun se mira la imagen.
SUPERIORES = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28]
INFERIORES = [48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38]


def diente(fdi, cx, cy, giro):
    """Un diente: corona redondeada arriba, cuello recto, girado hacia fuera."""
    ancho, alto = CORONAS[fdi % 10]
    x, y = -ancho / 2, -alto / 2
    radio = 5 if fdi % 10 >= 6 else 7
    return (
        f'<g transform="translate({cx:.1f} {cy:.1f}) rotate({giro:.1f})">'
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{ancho}" height="{alto}" '
        f'rx="{radio}" fill="{RELLENO}" stroke="{TRAZO}" stroke-width="1.4"/>'
        f"</g>"
    )


def etiqueta(fdi, cx, cy):
    return (
        f'<text x="{cx:.1f}" y="{cy:.1f}" fill="{ETIQUETA}" font-size="10.5" '
        f'font-family="Helvetica, Arial, sans-serif" text-anchor="middle" '
        f'dominant-baseline="middle">{fdi}</text>'
    )


def arco(fdis, cy, rx, ry, signo):
    """Reparte los dientes sobre media elipse, de 180 a 0 grados."""
    piezas = []
    n = len(fdis)
    for i, fdi in enumerate(fdis):
        # Margen en los extremos para que los cordales no queden de canto.
        t = math.radians(168 - i * (156 / (n - 1)))
        x = CX + rx * math.cos(t)
        y = cy + signo * ry * math.sin(t)

        # Cada diente mira hacia fuera del arco; la tangente da el giro.
        giro = math.degrees(math.atan2(rx * math.sin(t), -signo * ry * math.cos(t)))
        giro = (giro + 90) % 180 - 90

        piezas.append(diente(fdi, x, y, giro))

        # La cifra va por fuera del arco: misma elipse, un poco mas ancha.
        ex = CX + (rx + 26) * math.cos(t)
        ey = cy + signo * (ry + 26) * math.sin(t)
        piezas.append(etiqueta(fdi, ex, ey))
    return piezas


def cruz():
    """La cruz de cuadrantes: separa 1|2 arriba y 4|3 abajo.

    No es adorno. Es lo que da sentido a la primera cifra de cada numero,
    y de paso ocupa el centro, que si no queda hueco.
    """
    medio = (ARCO_SUP["cy"] - ARCO_SUP["ry"] * 0.21 + ARCO_INF["cy"] + ARCO_INF["ry"] * 0.21) / 2
    return [
        f'<line x1="{CX}" y1="18" x2="{CX}" y2="{ALTO - 18}" '
        f'stroke="{CRUZ}" stroke-width="1.2"/>',
        f'<line x1="46" y1="{medio:.1f}" x2="{ANCHO - 46}" y2="{medio:.1f}" '
        f'stroke="{CRUZ}" stroke-width="1.2"/>',
    ]


def main():
    cuerpo = cruz() + arco(SUPERIORES, **ARCO_SUP) + arco(INFERIORES, **ARCO_INF)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ANCHO} {ALTO}" '
        f'width="{ANCHO}" height="{ALTO}" role="img" '
        f'aria-label="Odontograma con los 32 dientes numerados segun la notacion FDI">'
        f'<rect width="{ANCHO}" height="{ALTO}" fill="none"/>'
        + "".join(cuerpo)
        + "</svg>"
    )
    destino = pathlib.Path(__file__).parent / "odontograma.svg"
    destino.write_text(svg + "\n", encoding="utf-8")
    print(f"{destino.name} escrito ({len(svg)} bytes, {len(SUPERIORES) + len(INFERIORES)} dientes)")


if __name__ == "__main__":
    main()
