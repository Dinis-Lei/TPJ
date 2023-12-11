# TPJ Space Arcade

Dinis Lei 98452  
Bernardo Leandro 98652

## Game concept

Space arcade is a game where you have to control a spaceship and destroy enemy ships, trying to dodge bullets and asteroids and kill enemies to get the highest score. 

## Patterns 

|Pattern|Location|
|---|---|
|Service Locator| service_locator.py|
|Observer| observer.py|
|Command| signals.py|
|Prototype| actor.py, enemy.py|
|Component| spriteloader.py|
|Flyweight| spriteloader.py|
|Singleton| service_locator.py|
|State machine| spawner_manager|


### Service Locator

The [service locator](service_locator.py) pattern was used as an abstraction to access the observer and sound manager objects.

### Observer and Command

The [observer]() is used to establish the comunication between all objects, it does the communication of the player input, it signals when each phase of the main gameloop begins and any interaction between two objects is mediated by it (except for collision). It combines with the command pattern ([signals]()) to make so that events are more organized.

### Prototype

Prototype was used so that similar objects can share the same implementation, for example, the class [actor]() serves as a base for any game entity. It is also used when the spawner manager needs to spawn an enemy but it doesnt need to know its type

### Component

To decouple the logic of an entity and its graphical representation, the graphics of each object are separated.

### Flyweight

Because there are multiple copies of the same entity in the screen we use the flyweight so that they all share the same image resource.

### Singleton

We use the singleton pattern to garantee that every entity uses the same service locator, observer and sound manager. The service locator is the one that garantees the creation of the singletons.

### State Machine

To make the spawning of enemies less uniform and more random, the [spawner_manager]() alternates between 3 states:

- Easy
- Medium
- Hard

Each state uses a different pool of enemies and powerups and only when the pool is empty does the spawner change its state.
The states change based on the following probability table:

|Current state| Next State| Probability (%)|
|---|---|---|
|Easy| Easy| 30|
|Easy| Medium| 60|
|Easy| Hard| 10|
|Medium|Easy|50|
|Medium|Medium|25|
|Medium|Hard|25|
|Hard|Easy|20|
|Hard|Medium|60|
|Hard|Hard|20|

## Gameloop

As stated before the observer signals each phase of the game loop, this is done by calling a signals distincts for each phase. The phases are the following:

- **Player input**, this phase the signal processed varies on the input given by the player

- **Move**, this phase updates the location of every entity

- **Check collision**, checks if there are collisions occuring

- **Update**, updates the states of each entity (if they need to be deleted)

- **Display**, calls the display of each entity 

- **Spawn**, signals the spawner manager to spawn entities
