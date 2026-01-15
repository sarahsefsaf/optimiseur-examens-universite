
INSERT INTO departements(id , nom) VALUES 
(9,'informatique'),(10,'Mathemathique'),(11,'phisique'),(12,'chemie'),(13,'biologie'),(14,'Langues Étrangères'),(15,'Droit'); 

-- LICENCE 1
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Algorithmique & Programmation Impérative', 9, 'L1', 30),
('Mathématiques pour l''Informatique', 9, 'L1', 30),
('Architecture des Ordinateurs', 9, 'L1', 30),
('Systèmes d''Exploitation (Bases)', 9, 'L1', 30),
('Logique Mathématique', 9, 'L1', 30),
('Projet Informatique', 9, 'L1', 30);

-- LICENCE 2
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Structures de Données & Complexité', 9, 'L2', 30),
('Programmation Orientée Objet', 9, 'L2', 30),
('Bases de Données', 9, 'L2', 30),
('Réseaux Informatiques', 9, 'L2', 30),
('Méthodes Numériques', 9, 'L2', 30),
('Projet Développement Web', 9, 'L2', 30);

-- LICENCE 3
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Conception Logicielle (UML)', 9, 'L3', 30),
('Programmation Avancée', 9, 'L3', 30),
('Sécurité Informatique', 9, 'L3', 30),
('Intelligence Artificielle (Introduction)', 9, 'L3', 30),
('Projet d''Application', 9, 'L3', 30),
('Stage Professionnel', 9, 'L3', 30);

-- MASTER 1
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Algorithmique Avancée', 9, 'M1', 30),
('Systèmes Distribués', 9, 'M1', 30),
('Machine Learning', 9, 'M1', 30),
('Ingénierie du Logiciel', 9, 'M1', 30),
('Base de Données Avancées', 9, 'M1', 30),
('Sécurité des Réseaux', 9, 'M1', 30),
('Administration Système', 9, 'M1', 30),
('Recherche Opérationnelle', 9, 'M1', 30),
('Méthodologie de Recherche', 9, 'M1', 30);

-- MASTER 2
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Big Data & Analytics', 9, 'M2', 30),
('Cloud Computing', 9, 'M2', 30),
('Cybersécurité Avancée', 9, 'M2', 30),
('Développement Mobile', 9, 'M2', 30),
('Architecture Logicielle', 9, 'M2', 30),
('Gestion de Projet TI', 9, 'M2', 30),
('Veille Technologique', 9, 'M2', 30),
('Intelligence Artificielle Appliquée', 9, 'M2', 30),
('Mémoire de Master', 9, 'M2', 30);

-- LICENCE 1
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Algèbre Linéaire', 10, 'L1', 30),
('Analyse Réelle', 10, 'L1', 30),
('Mathématiques Discrètes', 10, 'L1', 30),
('Probabilités Élémentaires', 10, 'L1', 30),
('Calcul Différentiel', 10, 'L1', 30),
('Initiation à la Programmation', 10, 'L1', 30);

-- LICENCE 2
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Algèbre Avancée', 10, 'L2', 30),
('Analyse Complexe', 10, 'L2', 30),
('Statistiques Inférentielles', 10, 'L2', 30),
('Équations Différentielles', 10, 'L2', 30),
('Topologie', 10, 'L2', 30),
('Logique Formelle', 10, 'L2', 30);

-- LICENCE 3
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Algèbre Moderne', 10, 'L3', 30),
('Analyse Fonctionnelle', 10, 'L3', 30),
('Probabilités Avancées', 10, 'L3', 30),
('Géométrie Différentielle', 10, 'L3', 30),
('Optimisation', 10, 'L3', 30),
('Projet Mathématique', 10, 'L3', 30);

-- MASTER 1
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Théorie des Nombres', 10, 'M1', 30),
('Analyse Harmonique', 10, 'M1', 30),
('Processus Stochastiques', 10, 'M1', 30),
('Calcul Scientifique', 10, 'M1', 30),
('Algèbre Commutative', 10, 'M1', 30),
('Équations aux Dérivées Partielles', 10, 'M1', 30),
('Recherche Opérationnelle', 10, 'M1', 30),
('Modélisation Mathématique', 10, 'M1', 30),
('Séminaire de Recherche', 10, 'M1', 30);

-- MASTER 2
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Théorie des Catégories', 10, 'M2', 30),
('Analyse Numérique Avancée', 10, 'M2', 30),
('Statistique Mathématique', 10, 'M2', 30),
('Systèmes Dynamiques', 10, 'M2', 30),
('Mathématiques Financières', 10, 'M2', 30),
('Cryptographie', 10, 'M2', 30),
('Bio-Mathématiques', 10, 'M2', 30),
('Travaux Dirigés de Recherche', 10, 'M2', 30),
('Mémoire de Master', 10, 'M2', 30);


-- LICENCE 1
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Mécanique du Point', 11, 'L1', 30),
('Électricité & Magnétisme', 11, 'L1', 30),
('Thermodynamique', 11, 'L1', 30),
('Outils Mathématiques pour Physique', 11, 'L1', 30),
('Introduction à l''Optique', 11, 'L1', 30),
('TP de Physique Générale', 11, 'L1', 30);

-- LICENCE 2
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Mécanique Analytique', 11, 'L2', 30),
('Physique Quantique (Introduction)', 11, 'L2', 30),
('Physique Statistique', 11, 'L2', 30),
('Ondes & Vibrations', 11, 'L2', 30),
('Électromagnétisme', 11, 'L2', 30),
('TP de Physique Avancée', 11, 'L2', 30);

-- LICENCE 3
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Mécanique Quantique', 11, 'L3', 30),
('Relativité Restreinte', 11, 'L3', 30),
('Physique du Solide', 11, 'L3', 30),
('Physique Nucléaire', 11, 'L3', 30),
('Instrumentation & Mesures', 11, 'L3', 30),
('Projet Expérimental', 11, 'L3', 30);

-- MASTER 1
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Mécanique Quantique Avancée', 11, 'M1', 30),
('Physique des Particules', 11, 'M1', 30),
('Astrophysique', 11, 'M1', 30),
('Physique des Matériaux', 11, 'M1', 30),
('Thermodynamique Avancée', 11, 'M1', 30),
('Électrodynamique', 11, 'M1', 30),
('Méthodes Numériques en Physique', 11, 'M1', 30),
('TP Spécialisés', 11, 'M1', 30),
('Séminaire de Physique', 11, 'M1', 30);

-- MASTER 2
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Théorie Quantique des Champs', 11, 'M2', 30),
('Physique des Plasmas', 11, 'M2', 30),
('Cosmologie', 11, 'M2', 30),
('Nanophysique', 11, 'M2', 30),
('Optique Quantique', 11, 'M2', 30),
('Supraconductivité', 11, 'M2', 30),
('Physique Médicale', 11, 'M2', 30),
('Techniques Expérimentales', 11, 'M2', 30),
('Mémoire de Recherche', 11, 'M2', 30);


-- LICENCE 1
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Chimie Générale', 12, 'L1', 30),
('Chimie Organique 1', 12, 'L1', 30),
('Atomistique & Liaisons', 12, 'L1', 30),
('Chimie des Solutions', 12, 'L1', 30),
('Mathématiques pour Chimistes', 12, 'L1', 30),
('TP Chimie Générale', 12, 'L1', 30);

-- LICENCE 2
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Chimie Organique 2', 12, 'L2', 30),
('Chimie Minérale', 12, 'L2', 30),
('Cinétique Chimique', 12, 'L2', 30),
('Thermodynamique Chimique', 12, 'L2', 30),
('Spectroscopie', 12, 'L2', 30),
('TP Chimie Organique', 12, 'L2', 30);

-- LICENCE 3
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Chimie Organique Avancée', 12, 'L3', 30),
('Chimie des Polymères', 12, 'L3', 30),
('Chimie Analytique', 12, 'L3', 30),
('Chimie Quantique', 12, 'L3', 30),
('Chimie Industrielle', 12, 'L3', 30),
('Projet de Synthèse', 12, 'L3', 30);

-- MASTER 1
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Chimie Théorique', 12, 'M1', 30),
('Chimie des Matériaux', 12, 'M1', 30),
('Catalyse', 12, 'M1', 30),
('Chimie Verte', 12, 'M1', 30),
('Chimie Supramoléculaire', 12, 'M1', 30),
('Chimie des Solides', 12, 'M1', 30),
('Techniques Avancées d''Analyse', 12, 'M1', 30),
('TP Recherche', 12, 'M1', 30),
('Séminaire Chimie', 12, 'M1', 30);

-- MASTER 2
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Chimie Médicinale', 12, 'M2', 30),
('Nanomatériaux', 12, 'M2', 30),
('Chimie Computationnelle', 12, 'M2', 30),
('Électrochimie Avancée', 12, 'M2', 30),
('Chimie Environnementale', 12, 'M2', 30),
('Chimie des Procédés', 12, 'M2', 30),
('Chimie Bioorganique', 12, 'M2', 30),
('Stage Industriel/Recherche', 12, 'M2', 30),
('Mémoire de Master', 12, 'M2', 30);




-- LICENCE 1
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Biologie Cellulaire', 13, 'L1', 30),
('Biochimie Structurale', 13, 'L1', 30),
('Génétique Mendélienne', 13, 'L1', 30),
('Physiologie Végétale', 13, 'L1', 30),
('Zoologie', 13, 'L1', 30),
('TP Biologie Générale', 13, 'L1', 30);

-- LICENCE 2
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Biologie Moléculaire', 13, 'L2', 30),
('Microbiologie', 13, 'L2', 30),
('Physiologie Animale', 13, 'L2', 30),
('Écologie', 13, 'L2', 30),
('Bioinformatique (Introduction)', 13, 'L2', 30),
('TP Biologie Moléculaire', 13, 'L2', 30);

-- LICENCE 3
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Génétique des Populations', 13, 'L3', 30),
('Immunologie', 13, 'L3', 30),
('Biologie du Développement', 13, 'L3', 30),
('Biologie Évolutive', 13, 'L3', 30),
('Biochimie Métabolique', 13, 'L3', 30),
('Projet de Recherche', 13, 'L3', 30);

-- MASTER 1
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Génétique Avancée', 13, 'M1', 30),
('Biologie des Systèmes', 13, 'M1', 30),
('Neurosciences', 13, 'M1', 30),
('Biotechnologies', 13, 'M1', 30),
('Biochimie Structurale Avancée', 13, 'M1', 30),
('Écologie Quantitative', 13, 'M1', 30),
('Biologie Cellulaire Avancée', 13, 'M1', 30),
('Méthodes en Biologie', 13, 'M1', 30),
('Séminaire Scientifique', 13, 'M1', 30);

-- MASTER 2
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Biologie du Cancer', 13, 'M2', 30),
('Génomique & Protéomique', 13, 'M2', 30),
('Biologie Synthétique', 13, 'M2', 30),
('Éco-toxicologie', 13, 'M2', 30),
('Biologie Computationnelle', 13, 'M2', 30),
('Pharmacologie', 13, 'M2', 30),
('Biologie Végétale Avancée', 13, 'M2', 30),
('Stage de Recherche', 13, 'M2', 30),
('Mémoire de Master', 13, 'M2', 30);



-- LICENCE 1
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Anglais Général Niveau 1', 14, 'L1', 30),
('Phonétique & Prononciation', 14, 'L1', 30),
('Grammaire Fondamentale', 14, 'L1', 30),
('Civilisation Anglophone', 14, 'L1', 30),
('Espagnol/Allemand Débutant', 14, 'L1', 30),
('Expression Écrite', 14, 'L1', 30);

-- LICENCE 2
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Anglais Général Niveau 2', 14, 'L2', 30),
('Linguistique Générale', 14, 'L2', 30),
('Littérature Anglaise 1', 14, 'L2', 30),
('Traduction (Version/Thème)', 14, 'L2', 30),
('Langue des Affaires', 14, 'L2', 30),
('Communication Orale', 14, 'L2', 30);

-- LICENCE 3
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Anglais Avancé', 14, 'L3', 30),
('Linguistique Appliquée', 14, 'L3', 30),
('Littérature Comparée', 14, 'L3', 30),
('Traduction Spécialisée', 14, 'L3', 30),
('Interprétation de Liaison', 14, 'L3', 30),
('Projet Culturel', 14, 'L3', 30);

-- MASTER 1
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Linguistique Théorique', 14, 'M1', 30),
('Didactique des Langues', 14, 'M1', 30),
('Traduction Audiovisuelle', 14, 'M1', 30),
('Sociolinguistique', 14, 'M1', 30),
('Littérature Postcoloniale', 14, 'M1', 30),
('Anglais Scientifique', 14, 'M1', 30),
('Gestion de Projets Interculturels', 14, 'M1', 30),
('Langue 3 (Chinois/Arabe)', 14, 'M1', 30),
('Séminaire de Recherche', 14, 'M1', 30);

-- MASTER 2
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Traduction Professionnelle', 14, 'M2', 30),
('Enseignement des Langues', 14, 'M2', 30),
('Communication Interculturelle', 14, 'M2', 30),
('Édition Multilingue', 14, 'M2', 30),
('Linguistique de Corpus', 14, 'M2', 30),
('Traduction Assistée par Ordinateur', 14, 'M2', 30),
('Médiation Linguistique', 14, 'M2', 30),
('Stage Professionnel', 14, 'M2', 30),
('Mémoire de Recherche', 14, 'M2', 30);



-- LICENCE 1
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Introduction au Droit', 15, 'L1', 30),
('Droit Constitutionnel', 15, 'L1', 30),
('Droit Civil (Personnes/Famille)', 15, 'L1', 30),
('Histoire du Droit', 15, 'L1', 30),
('Institutions Administratives', 15, 'L1', 30),
('Méthodologie Juridique', 15, 'L1', 30);

-- LICENCE 2
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Droit des Obligations', 15, 'L2', 30),
('Droit Pénal Général', 15, 'L2', 30),
('Droit Administratif', 15, 'L2', 30),
('Droit Commercial', 15, 'L2', 30),
('Finances Publiques', 15, 'L2', 30),
('Droit International Public', 15, 'L2', 30);

-- LICENCE 3
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Droit des Contrats', 15, 'L3', 30),
('Procédure Civile', 15, 'L3', 30),
('Droit Fiscal', 15, 'L3', 30),
('Droit Social', 15, 'L3', 30),
('Droit de la Propriété', 15, 'L3', 30),
('Projet Juridique', 15, 'L3', 30);

-- MASTER 1
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Droit des Affaires', 15, 'M1', 30),
('Droit International Privé', 15, 'M1', 30),
('Contentieux Administratif', 15, 'M1', 30),
('Droit Bancaire', 15, 'M1', 30),
('Droit de l''Environnement', 15, 'M1', 30),
('Droit des Technologies', 15, 'M1', 30),
('Droit Européen', 15, 'M1', 30),
('Rédaction d''Actes', 15, 'M1', 30),
('Séminaire de Droit', 15, 'M1', 30);

-- MASTER 2
INSERT INTO modules (nom, departement_id, niveau, nb_heures) VALUES
('Droit des Sociétés Avancé', 15, 'M2', 30),
('Arbitrage International', 15, 'M2', 30),
('Droit de la Concurrence', 15, 'M2', 30),
('Droit des Marchés Financiers', 15, 'M2', 30),
('Droit Humanitaire', 15, 'M2', 30),
('Propriété Intellectuelle', 15, 'M2', 30),
('Éthique & Déontologie', 15, 'M2', 30),
('Stage Juridique', 15, 'M2', 30),
('Mémoire de Master', 15, 'M2', 30);