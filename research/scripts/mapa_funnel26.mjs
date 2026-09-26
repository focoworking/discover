/* Genera producto/funnel26/mapa.js: geometria del Sur de Florida (condados, Census via
   us-atlas 10m) proyectada en Mercator a coordenadas SVG, un recuadro con todo el estado
   y la proyeccion para ubicar ciudades en el navegador. Correr desde una carpeta con
   us-atlas, topojson-client y d3-geo instalados:
     node mapa_funnel26.mjs <FOCO>/producto/funnel26/mapa.js */
import { readFileSync, writeFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import { feature } from 'topojson-client'
import { geoMercator, geoPath, geoCentroid } from 'd3-geo'
const require = createRequire(process.cwd() + '/')
const us = JSON.parse(readFileSync(require.resolve('us-atlas/counties-10m.json'), 'utf8'))
const fl = feature(us, us.objects.counties).features.filter((f) => String(f.id).startsWith('12'))
const estado = feature(us, us.objects.states).features.find((f) => f.id === '12')
const FOCO = { '12086': 'Miami-Dade', '12011': 'Broward' }
const VECINOS = { '12099': 'Palm Beach', '12087': 'Monroe', '12021': 'Collier', '12051': 'Hendry' }
const W = 640, H = 820
const foco = { type: 'FeatureCollection', features: fl.filter((f) => FOCO[f.id]) }
// Se encuadra el corredor urbano (donde estan las ciudades), no el condado entero:
// al oeste solo hay Everglades y los puntos quedarian amontonados en la costa.
const corredor = { type: 'MultiPoint', coordinates: [[-80.52, 25.42], [-80.06, 26.35]] }
const proj = geoMercator().fitExtent([[30, 30], [W - 30, H - 30]], corredor)
const path = geoPath(proj).digits(1)
const condados = fl.filter((f) => FOCO[f.id] || VECINOS[f.id]).map((f) => ({
  id: f.id, nombre: FOCO[f.id] || VECINOS[f.id], foco: !!FOCO[f.id], d: path(f), c: proj(geoCentroid(f)).map((v) => Math.round(v)),
}))
// Recuadro: todo Florida, con el marco de la zona ampliada
const IW = 150, IH = 150
const pi = geoMercator().fitExtent([[6, 6], [IW - 6, IH - 6]], estado)
const pathI = geoPath(pi).digits(1)
const [[x0, y0], [x1, y1]] = geoPath(pi).bounds(foco)
const salida = {
  fuente: 'U.S. Census Bureau cartographic boundaries via us-atlas 10m (dominio público)',
  vista: { w: W, h: H, escala: proj.scale(), traslado: proj.translate() },
  condados,
  florida: { w: IW, h: IH, d: pathI(estado), marco: [x0, y0, x1 - x0, y1 - y0].map((v) => Math.round(v * 10) / 10) },
}
writeFileSync(process.argv[2], '/* Generado por discover/research/scripts/mapa_funnel26.mjs. No editar a mano. */\nexport const MAPA = ' + JSON.stringify(salida) + '\n')
console.log(process.argv[2], JSON.stringify(salida).length, 'bytes', condados.map((c) => c.nombre).join(', '))
