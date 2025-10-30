"""
COMPUTAÇÃO GRÁFICA E PROCESSAMENTO DE IMAGENS
"""

import cairo
import numpy as np
from PIL import Image

print('Início da Prática - CGPI')
print('=' * 50)

def criaImagemVetorial():
    """
    Cria uma imagem vetorial SVG com dois segmentos de reta e um círculo.
    Retorna a superfície SVG criada.
    """
    # Inicializa a imagem vetorial SVG (400x400 pixels)
    v = cairo.SVGSurface('cgpi1.svg', 400, 400)
    context = cairo.Context(v)
    
    # Configura escala para trabalhar com coordenadas de 0 a 1
    context.scale(400, 400)
    context.set_line_width(0.01)
    
    # Adiciona segmento de reta PRETO (0.2,0.3) até (0.8,0.7)
    context.set_source_rgb(0, 0, 0)  # Preto
    context.move_to(0.2, 0.3)
    context.line_to(0.8, 0.7)
    context.stroke()
    
    # Adiciona segmento de reta CINZA ESCURO (0.8,0.3) até (0.2,0.7)
    context.set_source_rgb(0.3, 0.3, 0.3)  # Cinza escuro
    context.move_to(0.8, 0.3)
    context.line_to(0.2, 0.7)
    context.stroke()
    
    # Adiciona círculo CINZA CLARO - centro (0.5,0.5) e raio 0.3
    context.set_source_rgb(0.9, 0.9, 0.9)  # Cinza claro
    context.arc(0.5, 0.5, 0.3, 0, 2 * 3.14159)
    context.stroke()
    
    # Salva a imagem
    context.stroke()
    v.finish()
    
    return v


def desenhaCirculo(f, c, r, g):
    """
    Desenha um círculo em uma imagem matricial usando o algoritmo do ponto médio.
    
    Parâmetros:
    f: imagem (NumPy array)
    c: centro do círculo (xc, yc)
    r: raio em pixels
    g: nível de cinza (0-255)
    """
    xc, yc = c
    x = 0
    y = r
    d = 1 - r
    
    # Função auxiliar para desenhar os 8 pontos simétricos
    def desenha8pontos(xc, yc, x, y, g):
        pontos = [
            (xc + x, yc + y), (xc - x, yc + y),
            (xc + x, yc - y), (xc - x, yc - y),
            (xc + y, yc + x), (xc - y, yc + x),
            (xc + y, yc - x), (xc - y, yc - x)
        ]
        for px, py in pontos:
            if 0 <= px < f.shape[1] and 0 <= py < f.shape[0]:
                f[py, px] = g
    
    # Desenha o círculo usando o algoritmo do ponto médio
    desenha8pontos(xc, yc, x, y, g)
    
    while x < y:
        if d < 0:
            d += 2 * x + 3
        else:
            d += 2 * (x - y) + 5
            y -= 1
        x += 1
        desenha8pontos(xc, yc, x, y, g)


def desenhaReta(f, p, q, g):
    """
    Desenha um segmento de reta em uma imagem matricial usando o algoritmo de Bresenham.
    
    Parâmetros:
    f: imagem (NumPy array)
    p: ponto inicial (x0, y0)
    q: ponto final (x1, y1)
    g: nível de cinza (0-255)
    """
    x0, y0 = p
    x1, y1 = q
    
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    
    err = dx - dy
    
    x, y = x0, y0
    
    while True:
        # Desenha o pixel se estiver dentro dos limites
        if 0 <= x < f.shape[1] and 0 <= y < f.shape[0]:
            f[y, x] = g
        
        # Verifica se chegou ao ponto final
        if x == x1 and y == y1:
            break
        
        e2 = 2 * err
        
        if e2 > -dy:
            err -= dy
            x += sx
        
        if e2 < dx:
            err += dx
            y += sy

# PASSO 1: CRIAR IMAGEM VETORIAL

def passo1():
    """
    Cria uma imagem vetorial e salva em formato PNG.
    """
    print('\n--- PASSO 1: Criando imagem vetorial ---')
    
    # Cria a imagem vetorial
    v = criaImagemVetorial()
    print('✓ Imagem vetorial criada: cgpi1.svg')
    
    # Converte SVG para PNG usando cairo
    surface = cairo.SVGSurface('cgpi1.svg', 400, 400)
    surface_png = cairo.ImageSurface(cairo.FORMAT_ARGB32, 400, 400)
    context = cairo.Context(surface_png)
    
    # Redesenha a imagem em PNG
    context.scale(400, 400)
    context.set_line_width(0.01)
    
    # Reta preta
    context.set_source_rgb(0, 0, 0)
    context.move_to(0.2, 0.3)
    context.line_to(0.8, 0.7)
    context.stroke()
    
    # Reta cinza escuro
    context.set_source_rgb(0.3, 0.3, 0.3)
    context.move_to(0.8, 0.3)
    context.line_to(0.2, 0.7)
    context.stroke()
    
    # Círculo cinza claro
    context.set_source_rgb(0.9, 0.9, 0.9)
    context.arc(0.5, 0.5, 0.3, 0, 2 * 3.14159)
    context.stroke()
    
    surface_png.write_to_png('cgpi1.png')
    print('✓ Imagem PNG criada: cgpi1.png')


# PASSO 2: DESENHAR CÍRCULO EM FORMATO MATRICIAL

def passo2():
    """
    Cria uma imagem matricial e desenha um círculo usando algoritmo de rasterização.
    """
    print('\n--- PASSO 2: Desenhando círculo matricial ---')
    
    # Cria imagem matricial 201x201 pixels em branco (255 = branco)
    f = np.ones((201, 201), dtype=np.uint8) * 255
    
    # Desenha círculo cinza claro (g=230) com centro (100,100) e raio 60
    desenhaCirculo(f, (100, 100), 60, 230)
    print('✓ Círculo desenhado')
    
    # Salva a imagem em PNG
    img = Image.fromarray(f, mode='L')
    img.save('cgpi2.png')
    print('✓ Imagem salva: cgpi2.png')

# PASSO 3: CONVERTER IMAGEM VETORIAL PARA MATRICIAL

def passo3():
    """
    Converte a imagem vetorial para formato matricial desenhando retas e círculo.
    """
    print('\n--- PASSO 3: Convertendo imagem vetorial para matricial ---')
    
    # Cria imagem matricial 201x201 pixels em branco
    f = np.ones((201, 201), dtype=np.uint8) * 255
    
    # Converte coordenadas vetoriais (0-1) para matriciais (0-200)
    # Primeira reta PRETA: (0.2,0.3) até (0.8,0.7)
    p1 = (round(0.2 * 201), round(0.3 * 201))  # (40, 60)
    q1 = (round(0.8 * 201), round(0.7 * 201))  # (161, 141)
    desenhaReta(f, p1, q1, 0)  # 0 = preto
    print('✓ Primeira reta desenhada (preta)')
    
    # Segunda reta CINZA ESCURO: (0.8,0.3) até (0.2,0.7)
    p2 = (round(0.8 * 201), round(0.3 * 201))  # (161, 60)
    q2 = (round(0.2 * 201), round(0.7 * 201))  # (40, 141)
    desenhaReta(f, p2, q2, 77)  # 77 ≈ cinza escuro
    print('✓ Segunda reta desenhada (cinza escuro)')
    
    # Círculo CINZA CLARO: centro (0.5,0.5) e raio 0.3
    centro = (round(0.5 * 201), round(0.5 * 201))  # (100, 100)
    raio = round(0.3 * 201)  # 60
    desenhaCirculo(f, centro, raio, 230)  # 230 = cinza claro
    print('✓ Círculo desenhado (cinza claro)')
    
    # Salva a imagem em PNG
    img = Image.fromarray(f, mode='L')
    img.save('cgpi3.png')
    print('✓ Imagem salva: cgpi3.png')

# EXECUÇÃO PRINCIPAL

if __name__ == '__main__':
    # Executa os três passos
    passo1()
    passo2()
    passo3()
    
    print('\n' + '=' * 50)
    print('Arquivos gerados:')
    print('  - cgpi1.svg (imagem vetorial)')
    print('  - cgpi1.png (imagem vetorial em PNG)')
    print('  - cgpi2.png (círculo matricial)')
    print('  - cgpi3.png (conversão vetorial para matricial)')
    print('=' * 50)