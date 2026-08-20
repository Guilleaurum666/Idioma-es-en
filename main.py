import random
from deep_translator import GoogleTranslator
import scipy.io.wavfile as wav
import sounddevice as sd
import speech_recognition as sr

words = {
    "facil": ["gato", "perro", "manzana", "leche", "sol"],
    "medio": ["banano", "escuela", "amigo", "ventana", "amarillo"],
    "dificil": [
        "tecnologia",
        "universidad",
        "informacion",
        "pronunciacion",
        "imaginacion",
    ],
}

punt = 0
error = 0
fallos = 0

while True:
    wor = (
        input("Ingrese la dificultad (facil, medio, dificil) o 'salir': ")
        .strip()
        .lower()
    )

    if wor == "salir":
        print("\n¡Gracias por jugar!")
        print(f"La puntuación final es de: {punt}")
        print(f"Fallos totales: {fallos}")
        if error >= 3:
            print(
                f"Errores de audio/red: {error}\nIntenta mejorar el audio o la conexión."
            )
        else:
            print(f"Errores totales de audio: {error}\n")
        break

    if wor not in words:
        print("Dificultad no válida. Intente de nuevo.\n")
        continue

    print(f"\nDificultad seleccionada: {wor.upper()}")
    palabra_espanol = random.choice(words[wor])

    try:
        palabra_ingles = (
            GoogleTranslator(source="es", target="en")
            .translate(palabra_espanol)
            .lower()
        )
    except Exception:
        print("Error de conexión al traducir. Inténtalo de nuevo.")
        continue

    print(f"Traduce y pronuncia en inglés la palabra: '{palabra_espanol}'")

    duration = 5
    sample_rate = 44100

    print("Habla ahora...")
    recor = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=1,
        dtype="int16",
    )
    sd.wait()
    wav.write("output.wav", sample_rate, recor)

    print("Grabación completa, reconociendo...")
    recognizer_instance = sr.Recognizer()

    with sr.AudioFile("output.wav") as source:
        audio = recognizer_instance.record(source)

    try:
        text = recognizer_instance.recognize_google(
            audio, language="en-US"
        ).lower()
        print("Dijiste (en inglés):", text)

        if text == palabra_ingles:
            print("¡Excelente pronunciación!")
            punt += 1
        else:
            print(
                f"No coincide: Tu pronunciación fue '{text}', se esperaba '{palabra_ingles}'."
            )
            fallos += 1

    except sr.UnknownValueError:
        print("No se pudo reconocer el habla. Intenta hablar más claro.")
        error += 1
    except sr.RequestError as e:
        print(f"Error del servicio de reconocimiento: {e}")
        error += 1

    if fallos == 3:
        print("\n¡Has fallado tres veces! Fin del juego.")
        break

    print(f"La puntuación actual es de: {punt}\n")