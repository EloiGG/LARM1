# **UV LARM**

## Groupe Cyan : Eloi GUIHARD GOUJON & Gabriel HARIVEL

### [Challenge 2](https://ceri-num.gitbook.io/uv-larm/challenge/challenge-2)

L'objectif de ce second challenge est de cartographier un environnement, détecter des bouteilles de soda, et placer un marqueur sur la carte, aux emplacements correspondant.

La stratégie utilisée pour ce faire est la suivante :
- Tant qu'il le peut, le robot avance
- Lorsqu'un obstacle est dans son champ de vision, il s'arrête linéairement
- Il se met à tourner sur lui-même, dans la direction opposée à l'obstacle, pendant une durée aléatoire
- Lorsqu'il a fini de tourner, si l'obstacle n'est plus dans son champ de vision, il se remet à avancer

Ainsi le robot changera de direction à chaque obstacle et "ricochera" sur celui-ci de façon aléatoire, lui permettant selon les lois de probabilités d'explorer toute la pièce sur une durée infinie.

Cette stratégie a été appliquée grâce à un seul noeud appelé __ricochet2.py__ se situant dans le package __grp-cyan__
