
def agruparPorTimestamp(fotos):
    tandaFotos = []
    fotosAgrupadas = []
    grupos = 0
    tamGrupo = 0    
    tandaFotos.append(fotos[0])
    for foto in fotos[1:]:
        if (foto[:26] == tandaFotos[0][:26]):
            tandaFotos.append(foto)
        else:
            fotosAgrupadas.append(tandaFotos)
            tandaFotos = []
            tandaFotos.append(foto)
    [print(len(fotos), "de 7 fotos\n", fotos, "\n\n") for fotos in np.array(fotosAgrupadas)]
    return fotosAgrupadas

#Se realiza el solapamiento

def solaparFotos(fotos):
    for grupoFotos in fotosAgrupadas:
        fotosSolapadas = Image.new('RGB',(len(grupoFotos)*1080, 1920), (250,250,250))
        for iteracion,foto in enumerate(fotosAgrupadas):    
            with Image.open("./dirFotos/"+foto) as ficheroFoto:
                fotosSolapadas.paste(ficheroFoto, (1080*int(foto[33]),0))
        return fotosSolapadas

