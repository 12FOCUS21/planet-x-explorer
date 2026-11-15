"""Contenido educativo; la evaluación sucede localmente en el navegador."""
from fastapi import APIRouter
router=APIRouter(prefix='/api',tags=['education'])
LESSONS=[
 {'id':'01','tag':'Fundamentos','title':'¿Qué es el Planeta Nueve?', 'length':'3 min',
  'text':'Planeta Nueve o Planeta X es una hipótesis: un planeta distante cuya gravedad podría influir en ciertos objetos transneptunianos. No está confirmado. La búsqueda por imagen necesita observaciones repetidas y validación orbital.',
  'fact':'Una luz que se mueve NO es automáticamente un planeta.'},
 {'id':'02','tag':'Misiones NASA','title':'El universo infrarrojo', 'length':'4 min',
  'text':'SPHEREx observa el cielo en muchas longitudes de onda infrarrojas. La señal medida depende del filtro y de la posición del detector. Por eso, dos imágenes deben estar calibradas y comparadas en longitudes de onda compatibles.',
  'fact':'El infrarrojo puede revelar objetos que son difíciles de observar en luz visible.'},
 {'id':'03','tag':'Método científico','title':'Busca cambios, no certezas', 'length':'5 min',
  'text':'Alinea observaciones usando sus coordenadas celestes; resta el fondo, calcula diferencias, comprueba los errores y contrasta las fuentes con catálogos. Un objeto nuevo puede ser ruido, una estrella variable o un asteroide.',
  'fact':'Las fuentes conocidas y los artefactos deben descartarse antes de proponer candidatos.'},
]
QUESTIONS=[
 {'question':'¿Se ha confirmado científicamente la existencia del Planeta Nueve?',
  'answers':['Sí, SPHEREx lo fotografió','No, sigue siendo una hipótesis','Sí, Gaia lo descubrió'], 'correct':1,
  'explanation':'No existe una detección confirmada del Planeta Nueve.'},
 {'question':'¿Qué debemos hacer antes de restar dos imágenes del cielo?',
  'answers':['Alinear sus coordenadas y verificar bandas','Subir el contraste al máximo','Eliminar todas las estrellas'], 'correct':0,
  'explanation':'La alineación WCS y la compatibilidad espectral son esenciales.'},
 {'question':'¿Qué observa principalmente SPHEREx?',
  'answers':['Ondas de radio','Rayos gamma','Luz infrarroja'], 'correct':2,
  'explanation':'SPHEREx es un observatorio de espectroscopía infrarroja.'},
 {'question':'¿Qué demuestra un punto brillante desplazado entre dos imágenes?',
  'answers':['Un posible cambio que debemos verificar','Una órbita planetaria confirmada','La existencia del Planeta X'], 'correct':0,
  'explanation':'Un cambio tiene varias explicaciones y exige más observaciones.'},
 {'question':'¿Para qué sirve Gaia DR3 en nuestro análisis?',
  'answers':['Para inventar estrellas nuevas','Para contrastar posiciones y movimientos estelares','Para confirmar automáticamente planetas'], 'correct':1,
  'explanation':'Gaia DR3 proporciona astrometría de fuentes conocidas.'},
]
@router.get('/academy')
def academy():return {'lessons':LESSONS,'questions':QUESTIONS}
