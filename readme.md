# **UV LARM**

## Groupe Cyan : Eloi GUIHARD GOUJON & Gabriel HARIVEL

### [Challenge 2](https://ceri-num.gitbook.io/uv-larm/challenge/challenge-2)

L'objectif de ce second challenge est de cartographier un environnement, détecter des bouteilles de soda, et placer un marqueur sur la carte, aux emplacements correspondant.

#### __Vision__
La stratégie utilisée pour détecter les bouteilles est la suivante :
- Chaques images reçues du topic ``/camera/color/image_raw`` sont transformées en cv_image.
- On applique ensuite une __cascade de Haar__ grâce à la bibliothèque opencv qui nous permet d'avoir la liste des bouteilles et leur emplacement dans l'image. La cascade ne recherche pas la bouteille mais le logo "Nuka Cola" de celles-ci.
- L'algorithme repère beaucoup de faux positifs, en particulier les objets noirs. On applique ensuite un __filtre hsv__ sur le rouge dans les portions de l'image où une bouteille a été détectée. L'objectif est d'enlever les objets noirs, qui n'ont donc pas le logo rouge.
- Pour pouvoir visualiser cela, le programme retourne l'image avec les bouteilles encadrées en vert et les faux positifs encadrés en rouge.
Tout cela se fait dans le noeud _detection_node.py_

#### __Cartographie__
Pour la cartographie, on utilise le noeud gmapping qui découvre directement son environnement sur le topic ``/map``

#### __Marqueurs__
Pour placer les marqueurs dans rviz, on utilise les trois noeuds: *detection_node.py*, *changement_repere.py* et *marker.py*. La méthode est la suivante :
- Le noeud *detection_node.py* récupère les profondeurs des bouteilles dans le topic ``/camera/aligned_depth_to_color/image_raw``. Grâce à ces profondeurs, on retrouve la position des bouteilles dans la frame ``base_footprint``. Ces coordonnées sont envoyées dans le topic ``/BottleRelativeCoords``.
- Le noeud changement *changement_repere.py* récupère les coordonnées dans le repère du robot et les passe dans le repère du laboratoire, c'est à dire la frame ``map``. Ensuite il
- Le noeud *marker.py* crée des __Marker__ pour chaque bouteilles détectées et les publie dans le topic ``/bottle``.

Eloi ayant raté deux semaines de cours à cause du covid, nous n'avons pas eu le temps de faire des tests avec un robot à la place du rosbag.
