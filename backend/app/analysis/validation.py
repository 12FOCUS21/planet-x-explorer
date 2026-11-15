"""Control mínimo de compatibilidad entre épocas para evitar falsos positivos."""
def validate_pair(a:dict,b:dict):
    if a['id']==b['id']:
        raise ValueError('Escoge dos observaciones distintas')
    if a['simulated']!=b['simulated']:
        raise ValueError('No es válido mezclar simulaciones con observaciones reales')
    if not a['simulated']:
        if a.get('collection')!=b.get('collection'):
            raise ValueError('Compara observaciones de la misma colección SPHEREx')
        if a['detector']!=b['detector']:
            raise ValueError('Para comparar datos reales, usa el mismo detector SPHEREx (D1...D6)')
        if a['date']==b['date'] or 'Fecha no indicada' in (a['date'], b['date']):
            raise ValueError('Necesitas épocas diferentes para buscar movimiento temporal')
        try:
            a_lo,a_hi=float(a['_em_min']),float(a['_em_max'])
            b_lo,b_hi=float(b['_em_min']),float(b['_em_max'])
        except (KeyError,TypeError,ValueError):
            raise ValueError('IRSA no proporcionó rangos espectrales verificables para este par')
        a_width,b_width=a_hi-a_lo,b_hi-b_lo
        overlap=max(0.0,min(a_hi,b_hi)-max(a_lo,b_lo))
        if min(a_width,b_width)<=0 or overlap/min(a_width,b_width)<.8:
            raise ValueError('El par tiene rangos espectrales incompatibles (se requiere al menos 80% de solapamiento)')
