from django.shortcuts import render, get_object_or_404
from .forms import FormServico
from django.http import HttpResponse, FileResponse
from .models import Servico, ServicoAdicional
from io import BytesIO
from fpdf import FPDF

def novo_servico(request):
    if request.method == "GET":
        form = FormServico()
        return render(request, 'novo_servico.html', {'form': form})
    elif request.method == "POST":
        form = FormServico(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'principal.html', {'form': form})
        else:
            return render(request, 'novo_servico.html', {'form': form})
        
def listar_servico(request):
    if request.method == "GET":
        servicos = Servico.objects.all()
        return render(request, 'listar_servico.html', {'servicos': servicos})
    
def servico(request, identificador):
    servico = get_object_or_404(Servico, identificador=identificador)
    return render(request, 'servico.html', {'servico': servico})

def gerar_os(request, identificador):
    servico = get_object_or_404(Servico, identificador=identificador)

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('Arial', 'B', 12)

    pdf.set_fill_color(200, 220, 255)
    pdf.cell(0, 10, 'NOTA FISCAL', 0, 1, 'C', 1)

    pdf.cell(0, 10, f'Cliente: {servico.cliente.nome}', 0, 1, 'L')
    pdf.cell(0, 10, f'Data de Início: {servico.data_inicio}', 0, 1, 'L')
    pdf.cell(0, 10, f'Data de Entrega: {servico.data_entrega}', 0, 1, 'L')
    pdf.cell(0, 10, f'Protocolo: {servico.protocole}', 0, 1, 'L')

    pdf.ln(10)  

    pdf.set_fill_color(200, 220, 255)
    pdf.cell(35, 10, 'Descrição', 1, 0, 'C', 1)
    pdf.cell(25, 10, 'Quantidade', 1, 0, 'C', 1)
    pdf.cell(30, 10, 'Preço Unitário', 1, 0, 'C', 1)
    pdf.cell(30, 10, 'Total', 1, 1, 'C', 1)

    subtotal = 0
    for manutencao in servico.categoria_manutencao.all():
        pdf.cell(35, 10, manutencao.get_titulo_display(), 1)
        pdf.cell(25, 10, '1', 1)
        pdf.cell(30, 10, f'R$ {manutencao.preco:.2f}', 1)
        pdf.cell(30, 10, f'R$ {manutencao.preco:.2f}', 1, 1)
        subtotal += float(manutencao.preco)


    for servico_adicional in servico.servicos_adicionais.all():
        pdf.cell(35, 10, servico_adicional.titulo, 1)
        pdf.cell(25, 10, '1', 1)
        pdf.cell(30, 10, f'R$ {servico_adicional.preco:.2f}', 1)
        pdf.cell(30, 10, f'R$ {servico_adicional.preco:.2f}', 1, 1)
        subtotal += float(servico_adicional.preco)

    
    pdf.cell(90, 10, '', 0)  
    pdf.cell(30, 10, 'Subtotal:', 1, 0, 'C', 1)
    pdf.cell(30, 10, f'R$ {subtotal:.2f}', 1, 1, 'C')

    pdf.ln(10)  

    pdf.cell(0, 10, 'Obrigado por escolher nossos serviços!', 0, 1, 'C')

    pdf_content = pdf.output(dest='S').encode('latin1')
    pdf_bytes = BytesIO(pdf_content)

    return FileResponse(pdf_bytes, as_attachment=True, filename=f"nota_fiscal_{servico.protocole}.pdf")

def servico_adicional(request):
    identificador_servico = request.POST.get('identificador_servico')
    titulo = request.POST.get('titulo')
    descricao = request.POST.get('descricao')
    preco = request.POST.get('preco')

    servico_adicional = ServicoAdicional(titulo=titulo,descricao=descricao, preco=preco)
    
    servico_adicional.save()

    servico = Servico.objects.get(identificador=identificador_servico)
    servico.servicos_adicionais.add(servico_adicional)
    servico.save()
    return render(request,'principal.html')
def principal(request):
    
    return render(request, 'principal.html')