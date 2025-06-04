-- Cargar el CSV limpio
eventos = LOAD 'data/eventos_limpios.csv'
    USING PigStorage(',')
    AS (tipo:chararray, comuna:chararray, timestamp:chararray, descripcion:chararray);

-- Filtrar encabezado
eventos_filtrados = FILTER eventos BY tipo != 'tipo';

-- Agrupar por nombre de clase (campo tipo = clase Waze)
por_clase = GROUP eventos_filtrados BY tipo;

-- Contar cuántos hay de cada clase
conteo_clase = FOREACH por_clase GENERATE group AS clase, COUNT(eventos_filtrados) AS cantidad;

-- Guardar resultado
STORE conteo_clase INTO 'resultados/conteo_por_clase' USING PigStorage(',');
