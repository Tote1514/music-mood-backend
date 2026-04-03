from services.mood_services import MoodGenerator

import pytest

@pytest.fixture
def mood_generator():
    return MoodGenerator()

def test_process_text_coloquial_phrases(mood_generator):
    text_inputs = [
        "Hoje estou me sentindo muito foda",
        "Fui mal na prova e estou bolado com isso",
        "Hoje estou de boa e só queria relaxar",
        "Estou meio pra baixo hoje porque meu crush não me respondeu",
        "Estou puto com o trânsito hoje. Queria quebrar tudo",
        "Chamei a minha crush pra sair e ela topou!",
    ]

    moods = mood_generator.process_texts(text_inputs)

    assert isinstance(moods, list)
    assert len(moods) == len(text_inputs)

    expected_moods_for_texts = [
        "animado",
        "pesado",
        "calmo",
        "triste",
        "pesado",
        "romantico",
    ]

    print("\n=== Resultados do modelo ===\n")

    for text, mood, expected_mood in zip(text_inputs, moods, expected_moods_for_texts):
        print(f"Frase: {text}")
        print(f"Saída: {mood}")
        print(f"Esperada: {expected_mood}\n")


@pytest.mark.parametrize("text, expected_mood", [
    ("Hoje estou me sentindo muito foda", "animado"),
    ("Fui mal na prova e estou bolado com isso", "pesado"),
    ("Hoje estou de boa e só queria relaxar", "calmo"),
    ("Estou meio pra baixo hoje porque meu crush não me respondeu", "triste"),
    ("Estou puto com o trânsito hoje. Queria quebrar tudo", "pesado"),
    ("Chamei a minha crush pra sair e ela topou!", "romantico"),
])
def test_process_coloquial_text_various_inputs(mood_generator, text, expected_mood):
    mood = mood_generator.process_texts([text])[0]

    assert mood["dominant_mood"] == expected_mood, f"Expected {expected_mood} but got {mood['dominant_mood']} for text: {text}"


@pytest.mark.parametrize("text, expected_mood", [
    ("Vou trabalhar agora de manhã", "calmo"),
    ("Estou apaixonado de verdade", "romantico"),
    ("Hoje foi um dia incrível, deu tudo certo", "animado"),
    ("Só queria ficar sozinho hoje", "triste"),
    ("Só quero ouvir música e ficar de boa", "calmo"),
    ("Estou puto com o trânsito hoje. Queria quebrar tudo", "pesado"),
])
def test_process_normal_text_various_inputs(mood_generator, text, expected_mood):
    mood = mood_generator.process_texts([text])[0]

    print("\n" + "="*50)
    print(f"Texto: {text}")
    print(f"Dominant mood: {mood['dominant_mood']}")

    print("Moods detectados:")
    for m in mood.get("moods", []):
        print(f" - {m['label']}: {m['score']:.2f}")

    assert mood["dominant_mood"] == expected_mood, (
        f"\nTexto: {text}"
        f"\nEsperado: {expected_mood}"
        f"\nRecebido: {mood['dominant_mood']}"
        f"\nMoods: {mood.get('moods', [])}"
    )

@pytest.mark.exploratory
def test_ambiguous_phrases(mood_generator):
    texts = [
        "Tô feliz, mas ao mesmo tempo preocupado com amanhã",
        "Sei lá",
        "Tô animado, mas cansado pra caramba",
        "Não estou triste, só não estou bem",
        "Tô de boa, mas meio estranho",
        "Nada de especial aconteceu",
        "Hoje sai com uma garota que eu gosto, mas ela não me respondeu depois",
        "A garota que eu gosto me chamou pra sair, mas eu tô meio desanimado hoje",
        "A garota que eu gosto me bloqueou nas redes sociais"
    ]

    results = mood_generator.process_texts(texts)

    for text, result in zip(texts, results):
        print("\n" + "="*50)
        print(f"Texto: {text}")
        print(f"Dominante: {result['dominant_mood']}")
        print(f"Moods: {result['moods']}")


@pytest.mark.exploratory
def test_input_cases(mood_generator):
    texts = [
        "Quero músicas pra relaxar",
        "Toca algo animado aí",
        "Quero algo pra ficar de boa",
        "Me indica músicas pra treinar",
        "Queria algo animado, mas não muito",
        "Algo mais leve hoje",
        "Terminei com minha namorada, queria ouvir música",
        "Briguei com um amigo, tô mal",
        "Tô estressado com o trabalho",
        "Tô feliz, mas cansado"
    ]

    results = mood_generator.process_texts(texts)

    for text, result in zip(texts, results):
        print("\n" + "="*50)
        print(f"Texto: {text}")
        print(f"Dominante: {result['dominant_mood']}")
        print(f"Moods: {result['moods']}")
