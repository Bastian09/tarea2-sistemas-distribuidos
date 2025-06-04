-- Cargar archivo CSV
eventos = LOAD 'data/eventos_limpios.csv'
  USING PigStorage(',')
  AS (tipo:chararray, comuna:chararray, timestamp:chararray, descripcion:chararray);

-- Filtrar encabezado
limpios = FILTER eventos BY tipo != 'tipo';

-- Extraer hora desde el timestamp (formato: 2025-06-03T06:34:12Z o similar)
horas = FOREACH limpios GENERATE
    FLATTEN(STRSPLIT(timestamp, 'T')) AS (fecha:chararray, hora_completa:chararray),
    tipo;

horas_solo = FOREACH horas GENERATE
    SUBSTRING(hora_completa, 0, 2) AS hora,
    tipo;

-- Agrupar por hora
agrupado_por_hora = GROUP horas_solo BY hora;

-- Contar eventos por hora
conteo_horas = FOREACH agrupado_por_hora GENERATE
    group AS hora,
    COUNT(horas_solo) AS cantidad;

-- Guardar resultados
STORE conteo_horas INTO 'resultados/conteo_por_hora' USING PigStorage(',');
