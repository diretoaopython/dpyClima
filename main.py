from datetime import datetime
import flet as ft
import dpyFuncoes

def main(page: ft.Page):
    def atualizarClima(e):
        ###########################################################
        # Obter o clima atual e visualizar no container central
        ###########################################################
        cidade, pais = pesqLocal.value.split(',')

        ## Clima atual
        dadosClima = dpyFuncoes.obterClimaPorNome(dpyFuncoes.apiKey, cidade=cidade, pais=pais)

        cntCentralLinha1.controls[0].value = dadosClima['name']
        cntCentralLinha2.controls[0].src =  f"https://openweathermap.org/img/wn/{dadosClima['weather'][0]['icon']}.png"
        cntCentralLinha3.controls[0].value = f"{int(dadosClima['main']['temp'])} °"
        cntCentralLinha4.controls[0].value = f"{dadosClima['main']['humidity']} %"

        ## Previsão do tempo
        # 1. Vamos obter os dados da previsão através da função obterPrevisaoPorNome
        dadosPrevisao = dpyFuncoes.obterPrevisaoPorNome(dpyFuncoes.apiKey, cidade=cidade, pais=pais)

        # 2. Atribuir os valores padrão ao dicionário que irá receber os dados do container inferior
        # tempMaxDia = {"2024-11-23": ("Seg", "10n", 28), "2024-11-24": ("Ter", "10d", 32),}
        from collections import defaultdict
        tempMaxDia = defaultdict(lambda: ("", "", float('-inf')))

        # 3. Buscar e tratar os dados que serão visualizados no container inferior
        previsoes = dadosPrevisao['list']
        for previsao in previsoes:
            # Armazenar dia e dia da semana
            data = datetime.fromtimestamp(previsao['dt'])
            dias = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom']
            diaTmp = dias[data.weekday()]
            dia = data.strftime('%Y/%m/%d')

            # Tupla de elementos
            # Ícone
            iconTmp = previsao['weather'][0]['icon']

            # Temperatura
            tempTmp = int(previsao['main']['temp'])

            if iconTmp.endswith('d'):
                if tempTmp > tempMaxDia[dia][2]:
                    tempMaxDia[dia] = (diaTmp, iconTmp, tempTmp)

        # 4. Exibir os dados no container inferior

        idxColuna = 0
        for item in tempMaxDia:
            if idxColuna <= 4:
                cntInferiorLinha1.controls[idxColuna].value = tempMaxDia[item][0]
                cntInferiorLinha2.controls[idxColuna].src = f"https://openweathermap.org/img/wn/{tempMaxDia[item][1]}.png"
                cntInferiorLinha3.controls[idxColuna].value = f"{tempMaxDia[item][2]} °"

                idxColuna += 1

        page.update()

    def obterLocalUsuario(e):
        listaInfIp = dpyFuncoes.obterCoordPorIpUsuario()

        # [latitude,longitude,cidade,regiao,pais]
        cidade = listaInfIp[2]
        pais = listaInfIp[4]
        pesqLocal.value = f"{cidade}, {pais}"
        pesqLocal.update()

        atualizarClima(e)


    page.bgcolor = ft.colors.BLACK
    page.title = "Clima"
    page.window.height = 720
    page.window.width = 350

    #######################################################################
    cntPrincipal = ft.Container(
        bgcolor="#3F6CB7",
        border_radius=35,
        height=page.window.height * 0.90,
        padding=10,
        width=page.window.width * 0.90,
        content= ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            height=page.window.height * 0.90,
            width=page.window.width * 0.90,
        )
    )
    #######################################################################
    # Container Superior
    #######################################################################
    cntSuperior = ft.Container(
        #bgcolor="white",
        height=100,
        width=cntPrincipal.width * 0.95,
        content=ft.Row(
        )
    )

    # Container Superior - Texto para pesquisar o local
    pesqLocal = ft.TextField(
        bgcolor="white",
        border_color="white",
        border_radius=10,
        width=cntSuperior.width * 0.80,
        hint_text="Informe a cidade e País",
        hint_style=ft.TextStyle(
            size=12,
            color=ft.colors.BLUE_GREY,
        ),
        text_align=ft.TextAlign.CENTER,
        text_style=ft.TextStyle(
            size=14,
            color=ft.colors.BLACK,
        ),
        value = "Goiânia, BR"

    )
    cntSuperior.content.controls.append(pesqLocal)

    # Container Superior - Botão para executar a pesquisa
    btnPesquisar = ft.IconButton(
        icon=ft.icons.SEARCH,
        on_click=atualizarClima,
    )
    cntSuperior.content.controls.append(btnPesquisar)

    #######################################################################
    # Container Central
    #######################################################################
    cntCentral = ft.Container(
        height=200,
        content=ft.Column(
        ),
    )

    cntCentralLinha1 = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Text(
                "Goiânia",
                font_family="Segaon Medium",
                color="white",
                size=38,
                weight=ft.FontWeight.BOLD
            ),
        ],
    )
    cntCentral.content.controls.append(cntCentralLinha1)

    cntCentralLinha2 = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Image(
                src="http://openweathermap.org/img/wn/02d.png",
                width=50,
                height=50,
            )
        ],
    )
    cntCentral.content.controls.append(cntCentralLinha2)

    cntCentralLinha3 = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Text(
                "38°",
                font_family="Segaon Medium",
                color="white",
                size=28,
            )
        ],
    )
    cntCentral.content.controls.append(cntCentralLinha3)

    cntCentralLinha4 = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Text(
                "75%",
                font_family="Segaon Medium",
                color="white",
            )
        ],
    )
    cntCentral.content.controls.append(cntCentralLinha4)

    #######################################################################
    # Container Inferior
    #######################################################################
    cntInferior = ft.Container(
        height=150,
        content=ft.Column(
        ),
    )

    cntInferiorLinha1 = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        controls=[
            ft.Text(
                f"D{i}",
                color="white",
            ) for i in range(1,6)
        ],
    )
    cntInferior.content.controls.append(cntInferiorLinha1)

    cntInferiorLinha2 = ft.Row(
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Image(
                src=f"http://openweathermap.org/img/wn/0{i}d.png",
                width=50,
                height=50,
            ) for i in range(1,6)
        ],
    )
    cntInferior.content.controls.append(cntInferiorLinha2)

    cntInferiorLinha3 = ft.Row(
        alignment=ft.MainAxisAlignment.SPACE_AROUND,
        controls=[
            ft.Text(
                f"T{i}",
                color="white",
            ) for i in range(1,6)
        ],
    )
    cntInferior.content.controls.append(cntInferiorLinha3)

    #######################################################################
    #######################################################################
    cntPrincipal.content.controls.append(cntSuperior)
    cntPrincipal.content.controls.append(cntCentral)
    cntPrincipal.content.controls.append(cntInferior)

    page.add(cntPrincipal)

    obterLocalUsuario(None)


ft.app(target=main)
