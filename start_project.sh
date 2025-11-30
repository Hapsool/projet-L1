#!/bin/bash

set -e  # Arrête le script si une commande échoue

echo "=== Initialisation du projet ==="

# Se placer dans le dossier du script (racine du projet)
cd "$(dirname "$0")"

# Récupérer l'adresse IP locale du Raspberry Pi
IP=$(hostname -I | awk '{print $1}')

echo "Adresse IP locale détectée : $IP"
echo "Ton site web sera disponible sur : http://$IP:8000"

echo "=== Création / mise à jour de la base de données ==="
if python3 -m setup_database; then
    echo "✅ Base de données prête."
else
    echo "❌ Erreur lors du setup de la base de données."
    exit 1
fi

echo "=== Lancement du programme Raspberry Pi ==="
if python3 -m raspberry.run_pi; then
    echo "✅ Script Raspberry terminé."
else
    echo "❌ Erreur lors de l'exécution du Raspberry Pi script."
    exit 1
fi

echo "=== Projet lancé avec succès ! ==="
