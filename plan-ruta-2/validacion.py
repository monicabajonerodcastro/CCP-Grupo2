import pandas as pd


def check_registro(row):
    try:
        float(row['latitud'])
        float(row['longitud'])
        if float(row['latitud'])>=4.51360957443485 and float(row['latitud'])<=4.778211501715016 and float(row['longitud'])>=-74.23457623538577 \
           and float(row['longitud'])<=-74.02618417788635 and len(row['nombre_cliente'].strip())>0 and not pd.isna(row['fecha_entrega']):
            return "valido"
        else:
            return "invalido"
    except:
        return "invalido"
    

def validacion(dictData):
    dictOrdenes = dictData['message']
    df = pd.DataFrame(dictOrdenes)
    df['fecha_entrega'] = pd.to_datetime(df['fecha_entrega'], errors='coerce', infer_datetime_format=True)
    df['latitud'] = df['direccion'].apply(lambda x: x['latitud'])
    df['longitud'] = df['direccion'].apply(lambda x: x['longitud'])
    df['check_registro'] = df.apply(check_registro, axis=1)
    if len(df[df['check_registro']=='invalido']) > 0:
        return 'invalido'
    else:
        return 'valido'
    