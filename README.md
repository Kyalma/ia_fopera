Notice pour entrainer et utiliser le réseau neuronal.

Par défaut, une sauvegarde des poids est fournie avec l'archive (dans ./data/player_select.h5)
Le programme peut être utilisé immédiatement. (Installer tout de même les requirements)

Pour entrainer le réseau neuronal (à partir de zéro):
$> pip install -r requirements.txt
$> for i in {1..100} ; do python fantome_opera_serveur.py && python super_parser.py ; done
$> python build_training_dataset.py
$> python train_neural_network.py

Temps d'exécution de l'entrainement sur cpu i7-9700K + 16GB Ram: 3,477s
