# CTF: La evidencia perdida

Se realizó un análisis estático de `evidence.bin`, sin ejecutarlo.

Comandos utilizados:

```bash
file evidence.bin
strings -a evidence.bin
```

Flags encontradas entre las cadenas de texto:

- **FLAG 1:** `FLAG{ELF_DESCUBIERTO}`
- **FLAG 2:** `FLAG{STRINGS_ENCONTRO_LA_EVIDENCIA}`

Se descartaron las cadenas identificadas como señuelos.

**Apoyo:** ChatGPT me ayudó a elegir y comprender los comandos utilizados.
