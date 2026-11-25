sorteios = []
proximo_id_sorteio = 1

participantes = []
proximo_id_participante = 1


def ler_inteiro(mensagem):
    try:
        valor = int(input(mensagem))
    except ValueError:
        raise ValueError("Digite um numero inteiro valido.")

    if valor <= 0:
        raise ValueError("Digite um numero maior que zero.")

    return valor


def validar_texto(valor, campo):
    if not isinstance(valor, str) or valor.strip() == "":
        raise ValueError(f"{campo} e obrigatorio.")
    return valor.strip()


def buscar_sorteio(id_sorteio):
    for sorteio in sorteios:
        if sorteio["id"] == id_sorteio:
            return sorteio
    return None


def buscar_sorteio_por_premio(premio):
    for sorteio in sorteios:
        if sorteio["premio"].lower() == premio.lower():
            return sorteio
    return None


def buscar_participante(id_participante):
    for participante in participantes:
        if participante["id"] == id_participante:
            return participante
    return None


def buscar_participante_por_nome(id_sorteio, nome):
    for participante in participantes:
        if participante["sorteio_id"] == id_sorteio and participante["nome"].lower() == nome.lower():
            return participante
    return None


def participantes_por_sorteio(id_sorteio):
    return [participante for participante in participantes if participante["sorteio_id"] == id_sorteio]


def inserir_sorteio(premio):
    global proximo_id_sorteio

    erros = []
    premio = premio.strip()

    if premio == "":
        erros.append("O nome do premio e obrigatorio.")
    elif buscar_sorteio_por_premio(premio) is not None:
        erros.append("Ja existe um sorteio com esse premio.")

    if erros:
        raise ValueError("\n".join(erros))

    sorteio = {"id": proximo_id_sorteio, "premio": premio, "vencedor_id": None}
    sorteios.append(sorteio)
    proximo_id_sorteio += 1
    return sorteio


def alterar_sorteio(id_sorteio, premio):
    sorteio = buscar_sorteio(id_sorteio)
    erros = []
    premio = premio.strip()

    if sorteio is None:
        erros.append("Sorteio nao encontrado.")
    if premio == "":
        erros.append("O nome do premio e obrigatorio.")
    else:
        outro = buscar_sorteio_por_premio(premio)
        if outro is not None and outro["id"] != id_sorteio:
            erros.append("Ja existe outro sorteio com esse premio.")

    if erros:
        raise ValueError("\n".join(erros))

    sorteio["premio"] = premio
    return True


def remover_sorteio(id_sorteio):
    sorteio = buscar_sorteio(id_sorteio)

    if sorteio is None:
        raise ValueError("Sorteio nao encontrado.")
    if participantes_por_sorteio(id_sorteio):
        raise ValueError("Nao e possivel remover um sorteio que possui participantes.")

    sorteios.remove(sorteio)
    return True


def inserir_participante(nome, id_sorteio):
    global proximo_id_participante

    sorteio = buscar_sorteio(id_sorteio)
    erros = []
    nome = nome.strip()

    if sorteio is None:
        erros.append("Sorteio nao encontrado.")
    if nome == "":
        erros.append("O nome do participante e obrigatorio.")
    elif buscar_participante_por_nome(id_sorteio, nome) is not None:
        erros.append("Esse participante ja esta cadastrado no sorteio.")

    if erros:
        raise ValueError("\n".join(erros))

    participante = {
        "id": proximo_id_participante,
        "nome": nome,
        "sorteio_id": id_sorteio
    }
    participantes.append(participante)
    proximo_id_participante += 1
    return participante


def alterar_participante(id_participante, nome):
    participante = buscar_participante(id_participante)
    erros = []
    nome = nome.strip()

    if participante is None:
        erros.append("Participante nao encontrado.")
    if nome == "":
        erros.append("O nome do participante e obrigatorio.")
    elif participante is not None:
        outro = buscar_participante_por_nome(participante["sorteio_id"], nome)
        if outro is not None and outro["id"] != id_participante:
            erros.append("Ja existe um participante com esse nome nesse sorteio.")

    if erros:
        raise ValueError("\n".join(erros))

    participante["nome"] = nome
    return True


def remover_participante(id_participante):
    participante = buscar_participante(id_participante)

    if participante is None:
        raise ValueError("Participante nao encontrado.")

    for sorteio in sorteios:
        if sorteio["vencedor_id"] == id_participante:
            sorteio["vencedor_id"] = None

    participantes.remove(participante)
    return True


def definir_vencedor(id_sorteio, id_participante):
    sorteio = buscar_sorteio(id_sorteio)
    participante = buscar_participante(id_participante)
    erros = []

    if sorteio is None:
        erros.append("Sorteio nao encontrado.")
    if participante is None:
        erros.append("Participante nao encontrado.")
    elif participante["sorteio_id"] != id_sorteio:
        erros.append("O participante nao pertence a esse sorteio.")

    if erros:
        raise ValueError("\n".join(erros))

    sorteio["vencedor_id"] = id_participante
    return True


def consultar_vencedor(id_sorteio):
    sorteio = buscar_sorteio(id_sorteio)

    if sorteio is None or sorteio["vencedor_id"] is None:
        return None

    return buscar_participante(sorteio["vencedor_id"])


def exibir_sorteio(sorteio):
    print(f"ID: {sorteio['id']}")
    print(f"Premio: {sorteio['premio']}")
    vencedor = consultar_vencedor(sorteio["id"])
    print(f"Vencedor: {vencedor['nome'] if vencedor else 'Ainda nao definido'}")
    print("-" * 30)


def exibir_participante(participante):
    sorteio = buscar_sorteio(participante["sorteio_id"])
    print(f"ID: {participante['id']}")
    print(f"Nome: {participante['nome']}")
    print(f"Sorteio: {sorteio['premio'] if sorteio else 'Nao encontrado'}")
    print("-" * 30)


def menu_sorteios():
    while True:
        print("\n===== SORTEIOS =====")
        print("1 - Cadastrar sorteio")
        print("2 - Listar sorteios")
        print("3 - Consultar sorteio")
        print("4 - Alterar sorteio")
        print("5 - Remover sorteio")
        print("0 - Voltar")

        try:
            opcao = input("Escolha uma opcao: ")

            if opcao == "1":
                sorteio = inserir_sorteio(input("Digite o nome do premio: "))
                print(f"Sorteio cadastrado com ID {sorteio['id']}!")

            elif opcao == "2":
                if not sorteios:
                    print("Nenhum sorteio cadastrado.")
                else:
                    for sorteio in sorteios:
                        exibir_sorteio(sorteio)

            elif opcao == "3":
                sorteio = buscar_sorteio(ler_inteiro("Digite o ID do sorteio: "))
                if sorteio is None:
                    print("Sorteio nao encontrado.")
                else:
                    exibir_sorteio(sorteio)

            elif opcao == "4":
                id_sorteio = ler_inteiro("Digite o ID do sorteio: ")
                premio = input("Digite o novo premio: ")
                alterar_sorteio(id_sorteio, premio)
                print("Sorteio alterado com sucesso!")

            elif opcao == "5":
                remover_sorteio(ler_inteiro("Digite o ID do sorteio: "))
                print("Sorteio removido com sucesso!")

            elif opcao == "0":
                break
            else:
                print("Opcao invalida.")

        except ValueError as erro:
            print(f"Erro: {erro}")


def menu_participantes():
    while True:
        print("\n===== PARTICIPANTES =====")
        print("1 - Cadastrar participante")
        print("2 - Listar participantes de um sorteio")
        print("3 - Consultar participante por ID")
        print("4 - Alterar participante")
        print("5 - Remover participante")
        print("0 - Voltar")

        try:
            opcao = input("Escolha uma opcao: ")

            if opcao == "1":
                premio = validar_texto(input("Digite o nome do premio: "), "O nome do premio")
                sorteio = buscar_sorteio_por_premio(premio)
                if sorteio is None:
                    raise ValueError("Sorteio nao encontrado.")
                participante = inserir_participante(
                    input("Digite o nome do participante: "), sorteio["id"]
                )
                print(f"Participante cadastrado com ID {participante['id']}!")

            elif opcao == "2":
                premio = validar_texto(input("Digite o nome do premio: "), "O nome do premio")
                sorteio = buscar_sorteio_por_premio(premio)
                if sorteio is None:
                    raise ValueError("Sorteio nao encontrado.")
                lista = participantes_por_sorteio(sorteio["id"])
                print(f"\nParticipantes do sorteio {sorteio['premio']}:")
                if not lista:
                    print("Nenhum participante cadastrado.")
                else:
                    for participante in lista:
                        exibir_participante(participante)

            elif opcao == "3":
                participante = buscar_participante(ler_inteiro("Digite o ID do participante: "))
                if participante is None:
                    print("Participante nao encontrado.")
                else:
                    exibir_participante(participante)

            elif opcao == "4":
                id_participante = ler_inteiro("Digite o ID do participante: ")
                alterar_participante(id_participante, input("Digite o novo nome: "))
                print("Participante alterado com sucesso!")

            elif opcao == "5":
                remover_participante(ler_inteiro("Digite o ID do participante: "))
                print("Participante removido com sucesso!")

            elif opcao == "0":
                break
            else:
                print("Opcao invalida.")

        except ValueError as erro:
            print(f"Erro: {erro}")


def menu_resultados():
    while True:
        print("\n===== RESULTADOS =====")
        print("1 - Informar vencedor")
        print("2 - Consultar vencedor")
        print("0 - Voltar")

        try:
            opcao = input("Escolha uma opcao: ")

            if opcao == "1":
                premio = validar_texto(input("Digite o nome do premio: "), "O nome do premio")
                sorteio = buscar_sorteio_por_premio(premio)
                if sorteio is None:
                    raise ValueError("Sorteio nao encontrado.")
                nome = validar_texto(input("Digite o nome do participante vencedor: "), "O nome do participante")
                participante = buscar_participante_por_nome(sorteio["id"], nome)
                if participante is None:
                    raise ValueError("Participante nao cadastrado nesse sorteio.")
                definir_vencedor(sorteio["id"], participante["id"])
                print("Vencedor registrado com sucesso!")

            elif opcao == "2":
                premio = validar_texto(input("Digite o nome do premio: "), "O nome do premio")
                sorteio = buscar_sorteio_por_premio(premio)
                if sorteio is None:
                    raise ValueError("Sorteio nao encontrado.")
                vencedor = consultar_vencedor(sorteio["id"])
                print(f"Premio: {sorteio['premio']}")
                print(f"Vencedor: {vencedor['nome'] if vencedor else 'Ainda nao definido'}")

            elif opcao == "0":
                break
            else:
                print("Opcao invalida.")

        except ValueError as erro:
            print(f"Erro: {erro}")


def menu_principal():
    while True:
        print("\n===== GESTOR DE SORTEIOS =====")
        print("1 - Sorteios")
        print("2 - Participantes")
        print("3 - Resultados")
        print("0 - Sair")

        try:
            opcao = input("Escolha uma opcao: ")

            if opcao == "1":
                menu_sorteios()
            elif opcao == "2":
                menu_participantes()
            elif opcao == "3":
                menu_resultados()
            elif opcao == "0":
                print("Programa encerrado!")
                break
            else:
                print("Opcao invalida.")

        except ValueError as erro:
            print(f"Erro: {erro}")


menu_principal()
