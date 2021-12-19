import numpy as np

class Croyance :
    
    def __init__(self, nb_avis, univers) :

        self.__nb_avis = nb_avis # Equivalent d'inspecteur
        self.__univers = univers # Univers du problème
        
        # Calcul
        self.__masses = self.__init_masses() # Init les masses

    def list_evenement (self) :
        """
        Imprime à l'écran tout les evenement
        """
        for even in self.__univers :
            print (even)

    def __init_masses (self):
        """
        initialise le dictionnaire qui regroupe les masses

        return : le dictionnaire des 
        """

        temp_masse = []

        for avis in range(0, self.__nb_avis) :

            temp = dict()

            for univer in self.__univers :
                # Initialise à 0 toute les possibiltés
                temp[univer] = [0.0, 0.0, 0.0]

            temp_masse.append(temp)

        return temp_masse

    
    def set_masses (self, num_avis, evenement, valeur) :
        """
        Init un evenement selon un avis avec la valeur donné en argument
        """
        self.__masses[num_avis][evenement][0] = valeur



    
    def croyance (self) :
        """
        Calcul la fonction de croyance
        """
        for masse in self.__masses :
            for evenement in self.__univers :
                croy = 0
                for key, value  in masse.items():
                    if all(item in list(evenement) for item in list(key)):
                        croy = croy + value[0]

                masse[evenement][1] = croy

    def plausabilite (self) :
        """
        Calcul la fonction de plausabilité
        """
        for masse in self.__masses:  
            for evenement in self.__univers:
                croy = 0
                for key, value in masse.items():
                    if any(item in list(evenement) for item in list(key)):
                        croy = croy + value[0]
                        
                masse[evenement][2] = croy


    def _inter(self,chaine1, chaine2):
        """
        """

        intersection = ""

        for c in chaine1:
            if c in chaine2 and not c in intersection:
                intersection += c

        return intersection
    
    def _denominateur(self,masse_1, masse_2):
        """
        Denominateur
        """

        inter_vide = []

        for ev1 in self.__univers:
            for ev2 in self.__univers:
                if self._inter(ev1,ev2) == '':
                    inter_vide.append((ev1, ev2))
        temp_mass_a = []
        temp_mass_b = []
        
        for i in inter_vide :

            temp_mass_a.append(masse_1[i[0]][0])
            temp_mass_b.append(masse_2[i[1]][0])

        temp_mass_a = np.array(temp_mass_a)
        temp_mass_b = np.array(temp_mass_b)

        return 1 - np.sum(temp_mass_a*temp_mass_b, axis = 0)

    def _numerateur(self,masse_a, masse_b, evenement):
        """
        Numerateur
        """

        inter = []

        for ev1 in self.__univers:
            for ev2 in self.__univers:
                if self._inter(ev1,ev2) == evenement:
                    inter.append((ev1,ev2))
        temp_mass_a = []
        temp_mass_b = []

        for i in inter:
            temp_mass_a.append(masse_a[i[0]][0])
            temp_mass_b.append(masse_b[i[1]][0])

        temp_mass_a = np.array(temp_mass_a)
        temp_mass_b = np.array(temp_mass_b)

        return np.sum(temp_mass_a*temp_mass_b, axis = 0)


    def dempster_shafer (self, num_masse_1, num_masse_2) :
        """
        calcul dempster shafer
        """

        dempster = dict()
        denominateur = self._denominateur(self.__masses[num_masse_1], self.__masses[num_masse_2])

        if denominateur == 0:
            print("Dénominateur nul")
            return 0
        
        for evenement in self.__univers:
                dempster[evenement] = [self._numerateur(self.__masses[num_masse_1],self.__masses[num_masse_2],evenement)/denominateur] 

        
        return dempster

    def get_masses (self) :
        return self.__masses
