## Implementar el juego de Piedra, Papel, y Tijera

- El juego puede de tener dos modos:
    - Solo: humano vs maquina. El juego recibe el objeto seleccionado por el jugador (humano) y lo compara contra un objeto que la maquina selecciona para determinar al vencedor. La maquina puede tener dos niveles de dificultad, modo fácil (siempre saca piedra), y modo normal (elige aleatoriamente algún objeto)
    - Multijugador: humano vs humano. El juego recibe el objeto seleccionado por dos jugadores y determina al vencedor.
- Los datos de entrada serán los objetos seleccionados (piedra, papel, o tijera) por el(los) jugador(es).
- Reglas del juego:
    - Papel vence Piedra
    - Piedra vence Tijera
    - Tijera vence Papel
- Asumir que los datos siempre serán correctos. No hay necesidad de validaciones.


Ejemplo:
```
$ ./piedra_papel_tijera --modo=multijugador
Jugador1: piedra
Jugador2: papel
Vencedor: Jugador1

$ ./piedra_papel_tijera --modo=solo --dificultad=facil
Jugador1: papel
Computador: piedra
Vencedor: Jugador1
```
