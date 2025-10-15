# Analyse fonctionnelle — SmartLight Web (Raspberry Pi)

## 1. Objectif
Système d’éclairage intelligent : allumer/éteindre automatiquement selon **présence** et **luminosité**, avec **contrôle manuel** via Web.

## 2. Périmètre
- Raspberry Pi (serveur Flask).
- Capteurs : Grove Light (lux), PIR (présence).
- Actionneur : LED RGB ou relais.
- Base : SQLite.
- Front : HTML/CSS/JS (responsive).

## 3. Utilisateurs & besoins
- Occupant : veut une lumière adaptée sans manipulations complexes.
- Évaluateur : veut voir l’état, l’historique et tester facilement.

## 4. Exigences fonctionnelles
- Lecture capteurs toutes les 1–5 s.
- Mode AUTO (seuil lux + présence) / MANUEL (boutons).
- Journalisation mesures + actions (SQLite).
- Historique et export CSV.

## 5. Données
Tables :
- **mesures(id, timestamp, lux, presence)**
- **actions(id, timestamp, mode, led_state, seuil)**

## 6. Règles de gestion (AUTO)
- Si `presence = 1` **et** `lux < seuil` ⇒ `LED = ON`.
- Sinon ⇒ `LED = OFF`.
- Anti-flash : hystérésis/temporisation (ex. 5 s).

## 7. Contraintes (cours)
- ≥ 1 capteur + ≥ 1 actionneur.
- Site Web + base de données.
- Interaction via site web et/ou actionneur.

## 8. Architecture
- Flask : `/api/state`, `/api/on`, `/api/off`, `/api/mode`, `/api/seuil`.
- Thread capteurs + thread décision AUTO + driver LED.
- SQLite (DAO simple).

## 9. IHM
- Grands boutons, états lisibles, couleurs cohérentes.
- Feedback immédiat après action.
- Compatible mobile (touch, contraste).

## 10. Tests
- Capteurs (plage de valeurs), actionneur (PWM/ON/OFF).
- UI (tâches : allumer, changer seuil, basculer AUTO).
- Temps de réaction bout-à-bout.

## 11. Risques
- Bruit capteurs → lissage (EMA) & hystérésis.
- Pannes → *fail safe* OFF.
- Relais 220V → boîtier, relais certifié.

## 12. Roadmap
S1: câblage & drivers — S2: API & UI — S3: DB & historique — S4: AUTO & tests — S5: polish & dossier IHM.

*Généré le 2025-10-15 12:19*
