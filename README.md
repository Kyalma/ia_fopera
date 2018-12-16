Notice pour entrainer et utiliser le réseau neuronal.

Par défaut, une sauvegarde des poids est fournie avec l'archive (dans ./data/player_select.h5)
(Installer tout de même les requirements)

Pour entrainer le réseau neuronal à partir de zéro:
$> pip install -r requirements.txt
$> for i in {1..100} ; do python fantome_opera_serveur.py && python super_parser.py ; done
$> python build_training_dataset.py